# -*- coding: utf-8 -*-
"""Extract the English content from plusxtech.cn into _build/content-en.json."""
import json, os, re, sys
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "en_pages.json"), encoding="utf-8"))
B = "https://www.plusxtech.cn"


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
        if p.find("p") is not None:
            continue
        t = txt(p)
        if t and t not in out:
            out.append(t)
    if not out:
        t = txt(el)
        if t:
            out.append(t)
    return out


def inline_html(el):
    allowed = {"strong", "b", "em", "i", "br", "sup", "sub", "a"}
    out = []

    def walk(node):
        for ch in node.children:
            if getattr(ch, "name", None):
                if ch.name in ("script", "style", "img", "iframe", "video", "source"):
                    continue
                if ch.name == "br":
                    out.append("<br>")
                elif ch.name in allowed:
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


def e_plain(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def blocks(el):
    out, seen = [], set()
    if el is None:
        return out
    for node in el.find_all(["h1", "h2", "h3", "h4", "p", "li", "blockquote"]):
        if node.name == "li" and node.find("p") is not None:
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


def product(url, slug):
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
    return {"slug": slug, "name": name, "intro": intro,
            "features": feats, "colors": colors, "series": series, "source": url}


def app(url, slug):
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
    return {"slug": slug, "name": "", "title": title, "lead": lead_paras,
            "sections": sections, "tags": tags, "related": related,
            "family": fam, "source": url}


# ---------------------------------------------------------------- home
hs = BeautifulSoup(data[B + "/"]["html"], "html.parser")
home_apps = []
for a in hs.select(".index01 .application.swiper a"):
    home_apps.append({"label": txt(a.select_one("p")), "href": a.get("href", ""), "desc": ""})
home_产品页 = []
for sl in hs.select(".index02 .produtc > .swiper-wrapper > .swiper-slide"):
    box = sl.select_one(".product-left > a") or sl.select_one(".product-left-box")
    if not box:
        continue
    home_产品页.append({
        "name": txt(box.select_one("h3")),
        "intro": txt(box.select_one("p")),
        "href": box.get("href", ""),
        "features": [txt(x) for x in sl.select(".product-right li p")],
    })
service_note = ("\"Serving in a smile, innovating in the standard\" is the service purpose and goal of "
                "Plusxtech. We provide users with rich content, timely response and full service support. "
                "You can call Plusxtech service hotline, or send us an email, and the professional "
                "after-sales team will provide you with a systematic service.")

# ---------------------------------------------------------------- about
as_ = BeautifulSoup(data[B + "/col67/"]["html"], "html.parser")
about_stats = []
for li in as_.select(".NumList .item"):
    num = txt(li.select_one(".num"))
    label = txt(li.select_one("p"))
    m = re.match(r"^(\d+)\s*(.*)$", num)
    about_stats.append({"value": m.group(1) if m else num,
                        "suffix": (m.group(2) if m else "").strip(),
                        "label": label})
about_intro = [x for x in (txt(p) for p in as_.select(".AboutInfo .Info p")) if x]
about_history = []
for li in as_.select(".HistoryInfo .slider .item"):
    year = txt(li.select_one(".year"))
    d = txt(li.select_one(".desc"))
    if year and d and (year, d) not in [(h["year"], h["desc"]) for h in about_history]:
        about_history.append({"year": year, "desc": d})
about_values = []
for box in as_.select(".CultureInfo .application-box"):
    about_values.append({
        "num": txt(box.select_one(".application-index")),
        "title": txt(box.select_one(".application-title")),
        "desc": txt(box.select_one(".dot2")),
    })

# ---------------------------------------------------------------- 产品页
产品页 = [
    product(B + "/product/PTFEfilm", "ptfe"),
    product(B + "/product/PFAfilm", "pfa"),
    product(B + "/product/FEPfilm", "fep"),
    product(B + "/product/ETFEfilm", "etfe"),
    product(B + "/product/PVDFfilm", "光伏df"),
    product(B + "/product/PEEKfilm", "peek"),
    product(B + "/tape/ECtape", "ec"),
    product(B + "/tape/ETFEtape", "etfe-tape"),
    product(B + "/tape/PTFEtape", "ptfe-tape"),
    product(B + "/tape/PSAtape", "psa-tape"),
    product(B + "/col122/EPcompositefilm", "ep"),
]

# PSU and FP have no English page on plusxtech.cn – translate the Chinese copy.
产品页.insert(0, {
    "slug": "psu", "name": "PSU Film",
    "intro": ["PSU film is a high-performance film made from PSU polysulfone resin through a "
              "high-temperature extrusion casting process. It combines many advantages of "
              "polysulfone-based high-performance thermoplastic films, such as excellent heat "
              "resistance, outstanding mechanical strength, good 化工 resistance, prominent "
              "dielectric properties, high transparency and dimensional stability. PSU film can be "
              "thermoformed, compounded with a variety of substrates and used as a high-performance "
              "laminating adhesive, and can be adapted for sterilization through downstream "
              "processing, meeting demanding requirements across multiple fields."],
    "features": [], "colors": [], "series": [], "source": "translated",
})
产品页.append({
    "slug": "fp", "name": "FP Composite Film",
    "intro": ["FEP-FP is a composite material made of FEP fluoroplastic (fluorinated ethylene "
              "propylene copolymer) resin cast film and PET resin (polyethylene terephthalate). FEP "
              "film combines many advantages of fluoropolymer films, such as excellent heat "
              "resistance, 化工 resistance, non-stick properties and dielectric performance."],
    "features": [
        {"name": "Pure base material formula",
         "desc": "Contains no plasticizers, additives or other extra materials; the material is pure."},
        {"name": "Strong 化工 resistance",
         "desc": "The material has excellent 化工 inertness and solvent resistance, and can "
                 "withstand most 化工s."},
        {"name": "Low-friction non-stick surface",
         "desc": "Excellent non-stick properties, low surface friction coefficient, good release and "
                 "anti-sticking performance."},
        {"name": "Wide temperature range",
         "desc": "Stable for long-term use from -70℃ to 180℃, with short-term resistance up to 230℃, "
                 "and stable performance under high and low temperature conditions."},
    ],
    "colors": [], "series": [], "source": "translated",
})
CAT = {"psu": "Film", "ptfe": "Film", "pfa": "Film", "fep": "Film", "etfe": "Film",
       "光伏df": "Film", "peek": "Film", "ec": "Tape", "etfe-tape": "Tape",
       "ptfe-tape": "Tape", "psa-tape": "Tape", "fp": "Composite", "ep": "Composite"}
for p in 产品页:
    p["cat"] = CAT[p["slug"]]

# ---------------------------------------------------------------- 应用行业页
APP_DEF = [
    ("航空", "Aviation", "/col82/80"),
    ("光伏", "Photovoltaic", "/col82/79"),
    ("半导体", "Semiconductor", "/col82/78"),
    ("电子", "Electronics", "/col82/76"),
    ("医药", "Medical", "/col82/77"),
    ("化工", "Chemical", "/col82/107"),
    ("建材", "Construction", "/col82/75"),
    ("农业", "Agriculture", "/col82/74"),
    ("家装", "Home Improvement", "/col82/73"),
    ("交通", "Traffic", "/col82/108"),
]
应用行业页 = []
for slug, name, path in APP_DEF:
    a = app(B + path, slug)
    a["name"] = name
    应用行业页.append(a)

# fill home application descriptions from the application pages
home_map = {"Automobile": "交通", "Aviation": "航空", "Photovoltaic": "光伏",
            "Semiconductor": "半导体", "Electronics": "电子",
            "Medicine": "医药", "Architecture": "建材", "Agriculture": "农业",
            "Home decoration": "家装"}
for a in home_apps:
    slug = home_map.get(a["label"], "")
    rec = next((x for x in 应用行业页 if x["slug"] == slug), None)
    if rec and rec["lead"]:
        a["desc"] = rec["lead"][0]
    else:
        a["desc"] = ""

# ---------------------------------------------------------------- methods / faq / video
ms = BeautifulSoup(data[B + "/col87/list"]["html"], "html.parser")
methods = [{"name": txt(b.select_one(".process-title")),
            "desc": txt(b.select_one(".process-content"))}
           for b in ms.select(".process-box")]

fs = BeautifulSoup(data[B + "/col91/list"]["html"], "html.parser")
faq = []
for li in fs.select(".FaqList .item"):
    q = txt(li.select_one(".ti"))
    if q.startswith("Q"):
        q = q[1:].strip()
    a = txt(li.select_one(".desc"))
    a = re.sub(r"^A\s*[：:]\s*", "", a)
    if q and a:
        faq.append({"q": q, "a": a})

vs = BeautifulSoup(data[B + "/col92/list"]["html"], "html.parser")
video = []
for sec in vs.select(".quality > div"):
    title = txt(sec.select_one(".quality-title"))
    items = [txt(x) for x in sec.select(".quality-txt") if txt(x)]
    if title or items:
        video.append({"title": title, "items": items})

# ---------------------------------------------------------------- privacy
ps = BeautifulSoup(data[B + "/col113/"]["html"], "html.parser")
area = ps.select_one(".lt_area")
privacy_blocks = []
if area:
    for p in area.find_all("p", recursive=False):
        t = txt(p)
        if not t:
            continue
        for line in t.split("\n"):
            line = line.strip()
            if not line:
                continue
            if re.match(r"^Article\s+\d+", line):
                privacy_blocks.append({"t": "h2", "x": line})
            else:
                privacy_blocks.append({"t": "p", "x": e_plain(line)})

content = {
    "site": {
        "phone": "400-1020-490",
        "email": "marketing@plusxtech.com",
        "website": "www.plusxtech.com",
        "address": "Building 1、2、3, No 1, West Side of Guanggu Zongsi Road, Changshan Community, "
                   "Zhonghuopu Town, Chibi City, Xianning City, Hubei Province, China",
        "copyright": "Copyright © 2023  PLUSXTECH CO., LTD",
        "icp": "鄂ICP备2023027748号",
    },
    "home": {"应用行业页": home_apps, "产品页": home_产品页,
             "service_note": service_note},
    "about": {"title": "About us", "stats": about_stats, "intro": about_intro,
              "history": about_history, "values": about_values},
    "产品页": 产品页,
    "应用行业页": 应用行业页,
    "methods": methods,
    "faq": faq,
    "video": video,
    "privacy": {"title": "Privacy Policy", "blocks": privacy_blocks},
}

json.dump(content, open(os.path.join(HERE, "content-en.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("home apps", len(home_apps), "home 产品页", len(home_产品页))
print("about", about_stats, len(about_intro), len(about_history), len(about_values))
print("产品页", len(产品页), [(p["slug"], len(p["intro"]), len(p["features"]), len(p["series"])) for p in 产品页])
print("应用行业页", len(应用行业页), [(a["slug"], len(a["sections"])) for a in 应用行业页])
print("methods", len(methods), "faq", len(faq), "video", [(v["title"], len(v["items"])) for v in video])
print("privacy blocks", len(privacy_blocks))
print("service", service_note[:80])
