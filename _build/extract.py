# -*- coding: utf-8 -*-
"""Extract every piece of text from the plusxtech.com pages we crawled.

Input : _build/source-pages.json  (url -> {bread, html, text})
Output: _build/content.json
"""
import json, os, re, sys
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "source-pages.json"), encoding="utf-8"))
B = "https://www.plusxtech.com"


# ---------------------------------------------------------------- helpers
def txt(el):
    if el is None:
        return ""
    for br in el.find_all("br"):
        br.replace_with("\n")
    s = el.get_text("")
    s = s.replace("\u00a0", " ").replace("\u3000", " ")
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{2,}", "\n", s)
    return s.strip()


def paras(el):
    out = []
    if el is None:
        return out
    for p in el.find_all("p"):
        if p.find("p") is not None:      # skip wrappers around real paragraphs
            continue
        t = txt(p)
        if t and t not in out:
            out.append(t)
    if not out:
        t = txt(el)
        if t:
            out.append(t)
    return out


ALLOWED = {"strong", "b", "em", "i", "br", "sup", "sub", "a"}


def inline_html(el):
    out = []

    def walk(node):
        for ch in node.children:
            if getattr(ch, "name", None):
                if ch.name in ("script", "style", "img", "iframe", "video", "source"):
                    continue
                if ch.name == "br":
                    out.append("<br>")
                elif ch.name in ALLOWED:
                    attrs = ""
                    if ch.name == "a" and ch.get("href"):
                        attrs = ' href="%s" target="_blank" rel="noopener"' % ch["href"]
                    out.append("<%s%s>" % (ch.name, attrs))
                    walk(ch)
                    out.append("</%s>" % ch.name)
                else:
                    walk(ch)
            else:
                out.append(str(ch))

    walk(el)
    s = "".join(out)
    s = re.sub(r"<strong>\s*</strong>", "", s)
    s = re.sub(r"<em>\s*</em>", "", s)
    s = re.sub(r"<a[^>]*>\s*</a>", "", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"(<br>\s*)+$", "", s)
    s = re.sub(r"^\s*(<br>\s*)+", "", s)
    return s.strip()


def strip_tags(s):
    return BeautifulSoup(s or "", "html.parser").get_text("", strip=True)


def blocks(el):
    """Heading / paragraph / list-item blocks, de-duplicated and ordered."""
    out, seen = [], set()
    if el is None:
        return out
    for node in el.find_all(["h1", "h2", "h3", "h4", "p", "li", "blockquote"]):
        if node.name == "li" and node.find("p") is not None:
            # take the inner paragraphs instead of the whole li
            continue
        if node.name == "p" and node.find_parent("li") is not None:
            continue
        t = txt(node)
        if not t:
            continue
        h = inline_html(node) if node.name in ("p", "li", "blockquote") else ""
        if node.name in ("h1", "h2", "h3", "h4"):
            typ = "h2" if node.name in ("h1", "h2") else node.name
            val = t
        elif node.name == "li":
            typ, val = "li", h or t
        else:
            typ, val = "p", h or t
        key = (typ, val)
        if key in seen:
            continue
        seen.add(key)
        out.append({"t": typ, "x": val})
    return out


def app_data(url, slug, name):
    s = BeautifulSoup(data[url]["html"], "html.parser")
    lead = s.select_one(".application-blurb")
    title = txt(lead.select_one("h2")) if lead else ""
    lead_paras = paras(lead) if lead else []
    if lead_paras and title and lead_paras[0] == title:
        lead_paras = lead_paras[1:]
    sections = []
    for inner in s.select(".application01-inner"):
        h3 = txt(inner.select_one("h3"))
        ps = [p for p in paras(inner) if p != h3]
        sections.append({"title": h3, "paras": ps})
    tags = [txt(x) for x in s.select(".application01-right li div")]
    tags = [t for t in tags if t]
    related = [txt(x) for x in s.select(".application02 .application02-view p")]
    related = [t for t in related if t]
    fam = ""
    a3 = s.select_one(".application03")
    if a3:
        ps = [txt(x) for x in a3.select(".application02-view p") if txt(x)]
        fam = ps[0] if ps else ""
    family_label = txt(a3.select_one(".application-title")) if a3 else ""
    return {
        "slug": slug, "name": name, "title": title, "lead": lead_paras,
        "sections": sections, "tags": tags, "related": related,
        "family": fam, "family_label": family_label, "source": url,
    }


def product_data(url, slug, cat):
    s = BeautifulSoup(data[url]["html"], "html.parser")
    c = s.select_one(".ETFT-content")
    name = txt(c.select_one("h3")) if c else ""
    intro = paras(c) if c else []
    intro = [x for x in intro if x != name]
    feats = []
    for mi in s.select(".materials-item"):
        n = txt(mi.select_one(".materials1 .materials-content"))
        d = txt(mi.select_one(".materials2 .materials-content"))
        if n or d:
            feats.append({"name": n, "desc": d})
    colors = [txt(x) for x in s.select(".color-view p") if txt(x)]
    series = []
    for sv in s.select(".series-view"):
        ds = txt(sv.select_one(".series-content"))
        nm = ""
        for p in sv.find_all("p", recursive=False):
            if "downLoad" not in (p.get("class") or []):
                nm = txt(p)
        a = sv.select_one("a.downLoad")
        pdf = a["href"] if a and a.get("href") else ""
        if ds or nm:
            series.append({"name": nm, "desc": ds, "pdf": pdf})
    return {"slug": slug, "name": name, "cat": cat, "intro": intro,
            "features": feats, "colors": colors, "series": series, "source": url}


# ---------------------------------------------------------------- home
hs = BeautifulSoup(data[B + "/"]["html"], "html.parser")
desc = [txt(x) for x in hs.select(".index01 .application-content")]
apps = []
for i, a in enumerate(hs.select(".index01 .application-index a")):
    apps.append({
        "label": txt(a.select_one("p")),
        "href": a.get("href", ""),
        "desc": desc[i] if i < len(desc) else "",
    })
home_产品页 = []
for sl in hs.select(".index02 .produtc > .swiper-wrapper > .swiper-slide"):
    box = sl.select_one(".product-left-box")
    if not box:
        continue
    home_产品页.append({
        "name": txt(box.select_one("h3")),
        "intro": txt(box.select_one("p")),
        "href": box.get("href", ""),
        "features": [txt(x) for x in sl.select(".product-right li p")],
    })
home_news = []
for it in hs.select(".index06 .news-info .swiper-slide"):
    a = it.find("a")
    home_news.append({
        "title": txt(it.select_one(".news-title")),
        "date": txt(it.select_one(".news-date")),
        "href": a.get("href", "") if a else "",
    })
home_news = home_news[:3]
service_note = ("\"在微笑中服务，在规范中创新\"是正宇的服务宗旨和目标。我们为用户提供内容丰富、"
                "及时响应的全方位服务支持。您可以拨打正宇的服务热线，或给我们发送邮件，"
                "专业的售后团队就会为您提供系统化的服务。")


# ---------------------------------------------------------------- about
as_ = BeautifulSoup(data[B + "/about/"]["html"], "html.parser")
about_stats = []
for li in as_.select(".NumList .item"):
    num = txt(li.select_one(".num"))
    label = txt(li.select_one("p"))
    m = re.match(r"^(\d+)\s*(.*)$", num)
    about_stats.append({"value": m.group(1) if m else num,
                        "suffix": (m.group(2) if m else "").strip(),
                        "label": label})
about_intro = []
for p in as_.select(".AboutInfo .Info p"):
    t = txt(p)
    if t:
        about_intro.append(t)
about_history = []
for li in as_.select(".HistoryInfo .slider .item"):
    year = txt(li.select_one(".year"))
    d = txt(li.select_one(".desc"))
    if year and d:
        about_history.append({"year": year, "desc": d})
about_values = []
for box in as_.select(".CultureInfo .application-box"):
    about_values.append({
        "num": txt(box.select_one(".application-index")),
        "title": txt(box.select_one(".application-title")),
        "desc": txt(box.select_one(".dot2")),
    })
about_video = txt(as_.select_one(".AboutInfo .Video p"))


# ---------------------------------------------------------------- quality / methods / faq / video / talent
qs = BeautifulSoup(data[B + "/quality/index"]["html"], "html.parser")
quality = []
for sec in qs.select(".quality > div"):
    quality.append({
        "title": txt(sec.select_one(".quality-title")),
        "items": [txt(x) for x in sec.select(".quality-txt") if txt(x)],
    })

ms = BeautifulSoup(data[B + "/method/list"]["html"], "html.parser")
methods = [{"name": txt(b.select_one(".process-title")),
            "desc": txt(b.select_one(".process-content"))}
           for b in ms.select(".process-box")]

fs = BeautifulSoup(data[B + "/fqa/list"]["html"], "html.parser")
faq = []
for li in fs.select(".FaqList .item"):
    q = txt(li.select_one(".ti"))
    if q.startswith("Q"):
        q = q[1:].strip()
    a = txt(li.select_one(".desc"))
    a = re.sub(r"^A\s*[：:]\s*", "", a)
    if q and a:
        faq.append({"q": q, "a": a})

vs = BeautifulSoup(data[B + "/video/list"]["html"], "html.parser")
video = []
for sec in vs.select(".quality > div"):
    video.append({"title": txt(sec.select_one(".quality-title")),
                  "items": [txt(x) for x in sec.select(".quality-txt") if txt(x)]})

ts = BeautifulSoup(data[B + "/talentconcept/"]["html"], "html.parser")
talent_reasons = []
for li in ts.select(".talent01 .talent-view li"):
    talent_reasons.append({"title": txt(li.select_one("h3")), "desc": txt(li.select_one("p"))})
talent_recruit = [{"title": txt(a.select_one("h3")), "href": a.get("href", "")}
                  for a in ts.select(".talent-recruit")]
talent_life = []
for li in ts.select(".talent02 .slider .item"):
    d = txt(li.select_one(".desc"))
    if d and d not in talent_life:
        talent_life.append(d)

# ---------------------------------------------------------------- privacy
ps = BeautifulSoup(data[B + "/col112/"]["html"], "html.parser")
raw = txt(ps.select_one(".lt_area"))
lines = [l.strip() for l in raw.split("\n") if l.strip()]

# ---------------------------------------------------------------- news
news_items = {}
for u in [B + "/news/list", B + "/news/list_1", B + "/news/list_2"]:
    if u not in data:
        continue
    s = BeautifulSoup(data[u]["html"], "html.parser")
    for it in s.select(".News_list .item"):
        a = it.find("a")
        if not a:
            continue
        href = a.get("href", "")
        news_items[href] = {
            "title": txt(it.select_one(".tit")),
            "excerpt": txt(it.select_one(".dec")),
            "date": txt(it.select_one(".date span")),
            "href": href,
        }

news = []
for href, item in news_items.items():
    rec = dict(item)
    if href.startswith("/news/"):
        url = B + href
        rec["external"] = False
        rec["slug"] = href.rsplit("/", 1)[-1]
        if url in data:
            s = BeautifulSoup(data[url]["html"], "html.parser")
            rec["title"] = txt(s.select_one(".lt_title")) or rec["title"]
            t = txt(s.select_one(".lt_share .time"))
            rec["date"] = re.sub(r"^发布时间：", "", t) or rec["date"]
            rec["body"] = blocks(s.select_one(".lt_area"))
        else:
            rec["body"] = []
    else:
        rec["external"] = True
        rec["slug"] = ""
        rec["body"] = []
    news.append(rec)

# ---------------------------------------------------------------- jobs (live API, cached)
jobs = []
try:
    import requests
    H = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json",
         "Referer": B + "/joinus/list"}
    r = requests.post(
        B + "/ajax/list_page?siteId=1&columnId=45&subId=0&pageNumber=0&pageSize=100",
        json={}, headers=H, timeout=30)
    for j in r.json()["info"]["list"]:
        finfo = j.get("finfo") or {}
        jobs.append({
            "title": j.get("TITLE", ""),
            "type": finfo.get("ZPLX", ""),
            "category": finfo.get("ZWLX", ""),
            "location": finfo.get("GZDD", ""),
            "date": (j.get("PUBLISHDATE") or "")[:10],
            "duties": blocks(BeautifulSoup(j.get("CONTENT") or "", "html.parser")),
            "requirements": blocks(BeautifulSoup(j.get("RZZG") or "", "html.parser")),
            "email": j.get("EMAIL", ""),
        })
except Exception as e:  # pragma: no cover
    print("job fetch failed:", e, file=sys.stderr)
    if os.path.exists(os.path.join(HERE, "jobs.json")):
        jobs = json.load(open(os.path.join(HERE, "jobs.json"), encoding="utf-8"))

job_filters = {}
js = BeautifulSoup(data[B + "/joinus/list"]["html"], "html.parser")
for sel in js.select(".JobSearch select"):
    opts = [txt(o) for o in sel.find_all("option")]
    job_filters[opts[0]] = opts[1:]

content = {
    "site": {
        "phone": "400-1020-490",
        "email": "marketing@plusxtech.com",
        "website": "www.plusxtech.com",
        "address": "中国湖北省咸宁市赤壁市中伙铺镇长山社区光谷纵四路西侧1号1号楼、2号楼、3号楼",
        "copyright": "Copyright © 2023  正宇新材料（湖北）有限公司版权所有",
        "icp": "鄂ICP备2023027748号",
    },
    "home": {"应用行业页": apps, "产品页": home_产品页, "news": home_news,
             "service_note": service_note},
    "about": {"title": "关于正宇", "stats": about_stats, "intro": about_intro,
              "history": about_history, "values": about_values, "video": about_video},
    "quality": quality,
    "产品页": [
        product_data(B + "/product/PSUfilm", "psu", "原膜"),
        product_data(B + "/product/PTFEfilm", "ptfe", "原膜"),
        product_data(B + "/product/PFAfilm", "pfa", "原膜"),
        product_data(B + "/product/FEPfilm", "fep", "原膜"),
        product_data(B + "/product/ETFEfilm", "etfe", "原膜"),
        product_data(B + "/product/PVDFfilm", "光伏df", "原膜"),
        product_data(B + "/product/PEEKFilm", "peek", "原膜"),
        product_data(B + "/col121/ECTAPE", "ec", "胶带"),
        product_data(B + "/col121/ETFEtape", "etfe-tape", "胶带"),
        product_data(B + "/col121/PTFEtape", "ptfe-tape", "胶带"),
        product_data(B + "/col121/PSAtape", "psa-tape", "胶带"),
        product_data(B + "/col125/FPfilm", "fp", "复合膜"),
        product_data(B + "/col125/EPfilm", "ep", "复合膜"),
    ],
    "应用行业页": [
        app_data(B + "/application/3", "航空", "航空"),
        app_data(B + "/application/7", "光伏", "光伏"),
        app_data(B + "/application/45", "半导体", "半导体"),
        app_data(B + "/application/5", "电子", "电子"),
        app_data(B + "/application/2", "医药", "医药"),
        app_data(B + "/application/106", "化工", "化工"),
        app_data(B + "/application/6", "建材", "建材"),
        app_data(B + "/application/4", "农业", "农业"),
        app_data(B + "/application/1", "家装", "家装"),
        app_data(B + "/application/105", "交通", "交通"),
    ],
    "methods": methods,
    "faq": faq,
    "news": news,
    "talent": {"reasons": talent_reasons, "recruit": talent_recruit, "life": talent_life},
    "video": video,
    "jobs": jobs,
    "job_filters": job_filters,
    "privacy": {"title": "隐私政策", "raw": lines},
}

out = os.path.join(HERE, "content.json")
json.dump(content, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(jobs, open(os.path.join(HERE, "jobs.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("home apps", len(apps), "home 产品页", len(home_产品页))
print("about stats", about_stats, "history", len(about_history), "values", len(about_values))
print("quality", quality)
print("methods", len(methods), "faq", len(faq), "video", video)
print("talent", len(talent_reasons), len(talent_life))
print("privacy lines", len(lines))
for p in content["产品页"]:
    print("product", p["slug"], p["name"], len(p["intro"]), len(p["features"]),
          len(p["colors"]), len(p["series"]))
for a in content["应用行业页"]:
    print("app", a["slug"], a["name"], len(a["lead"]), len(a["sections"]), len(a["tags"]))
print("news", len(news), "with body", sum(1 for n in news if n["body"]))
print("jobs", len(jobs))
print("written", out)
