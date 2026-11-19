# -*- coding: utf-8 -*-
"""Verify that every retained source line appears in the matching language site."""
import json, os, re, glob
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
B_CN = "https://www.plusxtech.com"
B_EN = "https://www.plusxtech.cn"

CN_KEEP = [
    "/", "/about/", "/product/list", "/application", "/application/3", "/application/7",
    "/application/45", "/application/5", "/application/2", "/application/106",
    "/application/6", "/application/4", "/application/1", "/application/105",
    "/method/list", "/fqa/list", "/col112/",
    "/product/PSUfilm", "/product/PTFEfilm", "/product/PFAfilm", "/product/FEPfilm",
    "/product/ETFEfilm", "/product/PVDFfilm", "/product/PEEKFilm",
    "/col121/ECTAPE", "/col121/ETFEtape", "/col121/PTFEtape", "/col121/PSAtape",
    "/col125/FPfilm", "/col125/EPfilm", "/col121/list", "/col125/list",
    "/product/49", "/?guide=1",
]
EN_KEEP = [
    "/", "/col67/", "/product/list", "/col82", "/col82/80", "/col82/79", "/col82/78",
    "/col82/76", "/col82/77", "/col82/107", "/col82/75", "/col82/74", "/col82/73",
    "/col82/108", "/col87/list", "/col91/list", "/col113/",
    "/product/PTFEfilm", "/product/PFAfilm", "/product/FEPfilm", "/product/ETFEfilm",
    "/product/PVDFfilm", "/product/PEEKfilm", "/tape/ECtape", "/tape/ETFEtape",
    "/tape/PTFEtape", "/tape/PSAtape", "/tape/list", "/col122/list",
    "/col122/EPcompositefilm",
]


def norm(s):
    return re.sub(r"\s+", "", s or "")


def corpus(files):
    out = []
    for f in files:
        s = BeautifulSoup(open(f, encoding="utf-8").read(), "html.parser")
        for t in s(["script", "style"]):
            t.decompose()
        main = s.find("main") or s
        out.append(norm(main.get_text("")))
    return "".join(out)


SKIP = {
    "×", "<", ">", "Q", "A", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
    "11", "12", "观看视频", "Watch video", "Join us", "提交", "submit", "显示更多", "收起更多",
    "了解更多>", "More >", "浏览数量：", "[上一篇]", "[下一篇]", "返回列表", "slide↓",
    "正宇宣传片", "COMPANY INTRODUCTION VIDEO", "产品系列", "Product series",
    "加入我们", "新闻动态", "pack up",
}
SKIP_PARTS = ("[上一篇]", "[下一篇]", "返回列表", "浏览数量", "了解更多", "More >",
              "Watch video", "Join us")
SKIP_PREFIX = ("VitaFlon®半导体高温离型膜：", "VitaFlon® 高温离型膜｜", "让光伏",
               "Technology Empowering Agriculture", "Why has the VitaFlon", "PLUSXTECH 亮相")


def check(lang, pages, keep, base):
    files = (glob.glob(os.path.join(ROOT, "*.html")) if lang == "zh"
             else glob.glob(os.path.join(ROOT, "en", "*.html")))
    text = corpus(files)
    missing = []
    for path in keep:
        url = base + path
        if url not in pages:
            print("  [warn] source page not crawled:", url)
            continue
        for line in (pages[url].get("text") or "").split("\n"):
            t = line.strip()
            n = norm(t)
            if len(n) < 4 or t in SKIP or any(p in t for p in SKIP_PARTS):
                continue
            if t.endswith("...") or t.endswith("…"):
                continue
            if any(t.startswith(x) for x in SKIP_PREFIX):
                continue
            if re.match(r"^\d{2}-\d{2}$", t):
                continue
            t2 = re.sub(r"^A\s*[：:]\s*", "", t)
            t2 = re.sub(r"^Q\s*[：:]?\s*", "", t2)
            if norm(t2) not in text:
                missing.append((url, t))
    print("[%s] pages: %d  missing lines: %d" % (lang, len(files), len(missing)))
    seen = set()
    for url, t in missing:
        if (url, t) in seen:
            continue
        seen.add((url, t))
        print("  -", url, "|", t[:150])
    return missing


cn = json.load(open(os.path.join(HERE, "source-pages.json"), encoding="utf-8"))
en = json.load(open(os.path.join(HERE, "en_pages.json"), encoding="utf-8"))
m1 = check("zh", cn, CN_KEEP, B_CN)
m2 = check("en", en, EN_KEEP, B_EN)
