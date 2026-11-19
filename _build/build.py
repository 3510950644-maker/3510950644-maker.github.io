# -*- coding: utf-8 -*-
"""Bilingual static site builder (Chinese + English)."""
import json, os, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EN_DIR = os.path.join(ROOT, "en")

DATA = {
    "zh": json.load(open(os.path.join(HERE, "content.json"), encoding="utf-8")),
    "en": json.load(open(os.path.join(HERE, "content-en.json"), encoding="utf-8")),
}

IMAGES = {"产品页": {}, "应用行业页": {}, "methods": {}, "banners": {}}
_img_file = os.path.join(HERE, "images.json")
if os.path.exists(_img_file):
    IMAGES = json.load(open(_img_file, encoding="utf-8"))

PRODUCT_META = {
    "psu":       ("PSU",       "product-psu.html",       "#dde3ea", "#8fa0b5"),
    "ptfe":      ("PTFE",      "product-ptfe.html",      "#efece5", "#b9b3a6"),
    "pfa":       ("PFA",       "product-pfa.html",       "#d9efe9", "#4f9c8b"),
    "fep":       ("FEP",       "product-fep.html",       "#dde8f4", "#5b80ad"),
    "etfe":      ("ETFE",      "product-etfe.html",      "#e2f1f5", "#5fa6b8"),
    "光伏df":      ("PVDF",      "product-pvdf.html",      "#e9e2f2", "#7d6aa3"),
    "peek":      ("PEEK",      "product-peek.html",      "#f3e8d6", "#b08a52"),
    "ec":        ("EC",        "product-ec.html",        "#e2e6e3", "#6d7f74"),
    "etfe-tape": ("ETFE TAPE", "product-etfe-tape.html", "#e0f1f2", "#5aa3a6"),
    "ptfe-tape": ("PTFE TAPE", "product-ptfe-tape.html", "#efeade", "#a79a7c"),
    "psa-tape":  ("PSA TAPE",  "product-psa-tape.html",  "#e6e6e4", "#8b8d8a"),
    "fp":        ("FP",        "product-fp.html",        "#e0ecdf", "#6c9a6a"),
    "ep":        ("EP",        "product-ep.html",        "#e2e5f0", "#6b78a8"),
}
FILMS = ["psu", "ptfe", "pfa", "fep", "etfe", "光伏df", "peek"]
TAPES = ["ec", "etfe-tape", "ptfe-tape", "psa-tape"]
COMPS = ["fp", "ep"]
PRODUCT_ORDER = FILMS + TAPES + COMPS

APP_META = [
    ("航空",     "航空",   "Aerospace",        "application-aerospace.html",     "#172a48", "#2f5f7a"),
    ("光伏",            "光伏",   "Photovoltaics",    "application-pv.html",            "#1b3a4b", "#3c7d8c"),
    ("半导体", "半导体", "Semiconductor",    "application-semiconductor.html", "#1a2436", "#4b6484"),
    ("电子",   "电子",   "Electronics",      "application-electronics.html",   "#1d2b3a", "#4f7285"),
    ("医药",       "医药",   "Medical industry", "application-medical.html",       "#1f3a3f", "#4f8a86"),
    ("化工",      "化工",   "Chemical industry","application-chemical.html",      "#24313a", "#607d84"),
    ("建材",      "建材",   "Construction",     "application-building.html",      "#26313d", "#71808f"),
    ("农业",   "农业",   "Agriculture",      "application-agriculture.html",   "#26382c", "#6f9070"),
    ("家装",      "家装",   "Home decoration",  "application-interior.html",      "#2b2622", "#8a7a6a"),
    ("交通",     "交通",   "Traffic",          "application-transport.html",     "#22272d", "#6b7784"),
]
HOME_APP_SLUGS = {
    "zh": ["交通", "航空", "光伏", "半导体", "医药",
           "电子", "建材", "家装", "农业"],
    "en": ["交通", "航空", "光伏", "半导体", "电子",
           "医药", "建材", "农业", "家装"],
}
HOME_PROD_SLUGS = ["ptfe", "pfa", "fep", "etfe", "光伏df", "peek", "psa-tape"]

CAT_LABELS = {
    "zh": {"film": "原膜", "tape": "胶带", "comp": "复合膜"},
    "en": {"film": "Film", "tape": "Tape", "comp": "Composite"},
}


def cat_key(slug):
    if slug in FILMS:
        return "film"
    if slug in TAPES:
        return "tape"
    return "comp"


def 产品页_of(lang):
    return {p["slug"]: p for p in DATA[lang]["产品页"]}


def apps_of(lang):
    return {a["slug"]: a for a in DATA[lang]["应用行业页"]}


TXT = {
    "zh": {
        "brand": "正宇新材",
        "brand_company": "正宇新材料（湖北）有限公司",
        "topbar": "正宇新材 · 特种高分子薄膜材料",
        "nav": [
            ("home", "首页", "index.html", []),
            ("about", "关于我们", "about.html", []),
            ("产品页", "产品中心", "product-center.html", []),
            ("应用行业页", "应用领域", "applications.html", []),
            ("knowledge", "薄膜知识", "knowledge.html", []),
        ],
        "lang_label": "EN",
        "footer": {
            "about": "关于我们", "产品页": "产品中心", "应用行业页": "应用领域",
            "knowledge": "薄膜知识", "phone": "服务热线", "email": "邮箱",
            "website": "网址", "privacy": "隐私政策", "contact": "联系我们",
        },
        "home": {
            "eyebrow": "PLUSXTECH · 正宇新材料（湖北）有限公司",
            "title": "创新可靠的<br><em>材料供应商</em>",
            "cta1": "探索产品", "cta2": "了解正宇",
            "swatches": ["高透 · 耐候 · 自清洁", "耐化学 · 宽温 · 易加工", "低摩擦 · 绝缘 · 耐热"],
            "apps_kicker": "APPLICATIONS / 应用领域", "apps_title": "应用场景", "apps_lead": "",
            "apps_all": "查看全部应用领域",
            "产品页_kicker": "PRODUCTS / 产品中心", "产品页_title": "产品中心",
            "产品页_lead": "原膜 · 胶带 · 复合膜",
            "产品页_all": "查看全部产品", "product_more": "查看详情",
            "about_kicker": "ABOUT / 关于正宇", "about_title": "关于正宇",
            "about_more": "了解更多",
            "service_kicker": "SERVICE / 服务承诺",
            "service_title": "在微笑中服务<br>在规范中创新",
            "service_phone": "服务热线", "service_email": "电子邮箱", "service_web": "官方网站",
            "desc": "正宇新材专注特种高分子薄膜材料的研发与制造，提供 ETFE、PTFE、PFA、FEP、PVDF、PEEK 等原膜、胶带与复合膜产品。",
        },
        "about": {
            "hero_kicker": "ABOUT / 关于我们", "hero_title": "关于正宇",
            "hero_lead": "正宇新材专注于特种高分子薄膜材料的研发",
            "profile": "PROFILE", "company": "正宇新材料（湖北）有限公司",
            "fact_est": "成立时间", "fact_lines": "生产线", "fact_series": "产品系列",
            "fact_addr": "公司地址",
            "video_label": "正宇宣传片", "video_close": "关闭",
            "history_kicker": "HISTORY / 发展历程", "history_title": "发展历程",
            "values_kicker": "VALUES / 核心价值观", "values_title": "核心价值观",
        },
        "产品页": {
            "hero_kicker": "PRODUCTS / 产品中心", "hero_title": "产品中心",
            "hero_lead": "原膜 · 胶带 · 复合膜",
            "film_kicker": "FILM / 原膜", "film_lead": "PSU、PTFE、PFA、FEP、ETFE、PVDF、PEEK 等特种高分子薄膜。",
            "tape_kicker": "TAPE / 胶带", "tape_lead": "长效疏水透波薄膜、ETFE 胶带、PTFE 胶带与压敏胶带。",
            "comp_kicker": "COMPOSITE / 复合膜", "comp_lead": "氟塑料薄膜与 PET 等基材复合而成的高功能材料。",
            "cta_title": "需要选型支持？", "cta_lead": "欢迎联系我们获取产品资料、样品与技术建议。",
            "phone": "服务热线", "email": "电子邮箱",
        },
        "product": {
            "crumb": "产品中心",
            "features_kicker": "PROPERTIES / 材料特性", "features_title": "材料特性",
            "colors_kicker": "COLORS / 颜色种类", "colors_title": "颜色种类",
            "series_kicker": "SERIES / 产品系列", "series_title": "产品系列",
            "more_kicker": "MORE / 同类产品", "more_title": "同类产品",
            "download": "下载产品资料 (PDF)",
            "cta_title": "获取 %s 样品与资料",
            "cta_lead": "欢迎致电或邮件联系我们，获取选型建议、样品与产品资料。",
        },
        "应用行业页": {
            "hero_kicker": "APPLICATIONS / 应用领域", "hero_title": "应用领域",
        },
        "app": {
            "hero_kicker": "APPLICATIONS / 应用领域",
            "aside_app": "应用方向", "aside_related": "相关产品",
            "related_kicker": "RELATED / 相关产品",
            "gallery_kicker": "SERIES / 产品系列", "gallery_title": "产品系列",
            "aside_family": "产品家族", "aside_contact": "联系正宇",
        },
        "knowledge": {
            "hero_kicker": "KNOWLEDGE / 薄膜知识", "hero_title": "薄膜知识",
            "methods_kicker": "PROCESSING / 薄膜加工方法", "methods_title": "薄膜加工方法",
            "tools_kicker": "FAQ / 薄膜知识", "tools_title": "问答",
            "tool1_title": "卷取直径/重量计算",
            "tool1_desc": "填写厚度、长度与芯体尺寸，计算薄膜卷的近似直径与重量。",
            "tool1_cta": "打开计算器",
            "tool2_title": "常见问题",
            "tool2_desc": "半导体、光伏、医药、农业等应用中的选型与工艺问题解答。",
            "tool2_cta": "浏览 %s 条问答",
            "tool3_title": "视频中心",
            "tool3_desc": "品牌视频与 ETFE 在各应用领域的介绍视频目录。",
            "tool3_cta": "查看视频目录",
            "tag_tool": "工具", "tag_faq": "问答", "tag_video": "视频",
        },
        "calc": {
            "hero_kicker": "TOOLS / 薄膜知识", "hero_title": "卷取直径/重量计算",
            "hero_lead": "填写以下信息，计算薄膜的近似直径与重量。",
            "title1": "卷取直径计算",
            "desc1": "填写以下信息。计算薄膜的近似直径。",
            "thickness": "厚度（微米）", "range500": "1 至 500",
            "length": "长度（米）", "range9999": "1 至 9999",
            "core": "芯体尺寸",
            "cores": [("3英寸（塑料芯）", 76.2), ("3 英寸（纸芯）", 76.2),
                      ("6 英寸（纸芯）", 152.4), ("6 英寸（塑料芯）", 152.4)],
            "button": "计算", "result1": "卷取直径", "mm": "毫米",
            "note1": "(注释 1) 此计算得出的值是近似值，实际值可能因卷绕条件等而有所不同。",
            "note2": "(注释 2) 计算厚度时，纸芯为 14 毫米，塑料芯材为 8 毫米。",
            "title2": "卷尺重量计算",
            "desc2": "薄膜的近似重量根据厚度和宽度计算得出。",
            "product": "产品名称",
            "产品页": [("VitaFlon™ETFE", 1.75), ("FlexFlon™ETFE", 1.75),
                         ("VitaFlon™FEP", 2.15), ("FlexFlon™FEP", 2.15),
                         ("VitaFlon™PFA", 2.15), ("FlexFlon™PFA", 2.15),
                         ("VitaFlon™PCTFE", 2.13), ("PEEK FILM", 1.30)],
            "width": "宽度（毫米）", "length_m": "长度（米）",
            "result2": "重量", "kg": "千克",
        },
        "faq": {
            "hero_kicker": "FAQ / 薄膜知识", "hero_title": "常见问题",
            "hero_lead": "以下问答整理自正宇新材官网，覆盖半导体、光伏、医药、农业等应用中的常见问题。",
            "search": "搜索问题关键词，例如：离型膜、透光率、耐温",
            "count": "共 %s 条问答", "empty": "没有找到匹配的问题，请尝试其他关键词。",
            "note": "",
        },
        "video": {
            "hero_kicker": "VIDEO / 薄膜知识", "hero_title": "视频中心",
            "hero_lead": "品牌视频与产品视频目录。",
            "note": "按“仅文本、不含视频”的要求，本页仅保留视频栏目与标题，视频文件未收录。",
            "intro_video": "正宇宣传片",
        },
        "privacy": {
            "hero_kicker": "PRIVACY / 隐私政策", "hero_title": "隐私政策",
            "hero_lead": "隐私声明",
        },
        "cats": CAT_LABELS["zh"],
        "site": DATA["zh"]["site"],
    },
    "en": {
        "brand": "PLUSXTECH",
        "brand_company": "PLUSXTECH CO., LTD",
        "topbar": "PLUSXTECH · Specialty Polymer Films",
        "nav": [
            ("home", "Home", "index.html", []),
            ("about", "About", "about.html", []),
            ("产品页", "Products", "product-center.html", []),
            ("应用行业页", "Applications", "applications.html", []),
            ("knowledge", "Knowledge", "knowledge.html", []),
        ],
        "lang_label": "中文",
        "footer": {
            "about": "About", "产品页": "Products", "应用行业页": "Applications",
            "knowledge": "Knowledge", "phone": "Service hotline", "email": "Email",
            "website": "Website", "privacy": "Privacy Policy", "contact": "Contact us",
        },
        "home": {
            "eyebrow": "PLUSXTECH · PLUSXTECH CO., LTD",
            "title": "Innovative &amp; Reliable<br><em>Materials Supplier</em>",
            "cta1": "Explore 产品页", "cta2": "About PLUSXTECH",
            "swatches": ["High transparency · Weather resistant · Self-cleaning",
                         "Chemical resistant · Wide temperature range · Easy to process",
                         "Low friction · Insulation · Heat resistant"],
            "apps_kicker": "APPLICATIONS", "apps_title": "Applications",
            "apps_lead": "With excellent properties, ETFE film material has been used in a wide range of 应用行业页 such as photovoltaic, architecture, 电子, 农业, aviation, medicine, car, home decoration and other industries.",
            "apps_all": "View all 应用行业页",
            "产品页_kicker": "PRODUCTS", "产品页_title": "Products",
            "产品页_lead": "Film · Tape · Composite",
            "产品页_all": "View all 产品页", "product_more": "View details",
            "about_kicker": "ABOUT / PLUSXTECH", "about_title": "About PLUSXTECH",
            "about_more": "Learn more",
            "service_kicker": "SERVICE",
            "service_title": "Serving in a smile<br>Innovating in the standard",
            "service_phone": "Service hotline", "service_email": "Email", "service_web": "Website",
            "desc": "PLUSXTECH specializes in specialty polymer films, offering ETFE, PTFE, PFA, FEP, PVDF and PEEK films, tapes and composite films.",
        },
        "about": {
            "hero_kicker": "ABOUT / ABOUT US", "hero_title": "About us",
            "hero_lead": "PLUSXTECH focuses on the special high-polymer film.",
            "profile": "PROFILE", "company": "PLUSXTECH CO., LTD",
            "fact_est": "Established", "fact_lines": "Production lines", "fact_series": "Product series",
            "fact_addr": "Address",
            "video_label": "COMPANY INTRODUCTION VIDEO", "video_close": "Close",
            "history_kicker": "HISTORY / DEVELOPMENT", "history_title": "Development history",
            "values_kicker": "VALUES / CORE VALUES", "values_title": "Core values",
        },
        "产品页": {
            "hero_kicker": "PRODUCTS", "hero_title": "Products",
            "hero_lead": "Film · Tape · Composite",
            "film_kicker": "FILM", "film_lead": "Specialty polymer films including PSU, PTFE, PFA, FEP, ETFE, PVDF and PEEK.",
            "tape_kicker": "TAPE", "tape_lead": "Long-acting hydrophobic wave-transparent film, ETFE tape, PTFE tape and pressure-sensitive tape.",
            "comp_kicker": "COMPOSITE", "comp_lead": "High-performance materials made by combining fluoroplastic film with PET and other substrates.",
            "cta_title": "Need help selecting a product?", "cta_lead": "Contact us for product data, samples and technical advice.",
            "phone": "Service hotline", "email": "Email",
        },
        "product": {
            "crumb": "Products",
            "features_kicker": "PROPERTIES / MATERIAL CHARACTERISTICS", "features_title": "Material characteristics",
            "colors_kicker": "COLORS", "colors_title": "Color category",
            "series_kicker": "SERIES", "series_title": "Product series",
            "more_kicker": "MORE / RELATED", "more_title": "Related 产品页",
            "download": "Download product data (PDF)",
            "cta_title": "Request samples and data for %s",
            "cta_lead": "Contact us by phone or email for selection advice, samples and product data.",
        },
        "应用行业页": {
            "hero_kicker": "APPLICATIONS", "hero_title": "Applications",
        },
        "app": {
            "hero_kicker": "APPLICATIONS",
            "aside_app": "Applications", "aside_related": "Related Products",
            "related_kicker": "RELATED PRODUCTS",
            "gallery_kicker": "PRODUCT SERIES", "gallery_title": "Product series",
            "aside_family": "Product Family", "aside_contact": "Contact PLUSXTECH",
        },
        "knowledge": {
            "hero_kicker": "KNOWLEDGE", "hero_title": "Knowledge",
            "methods_kicker": "PROCESSING / THIN FILM PROCESSING METHODS",
            "methods_title": "Thin film processing methods",
            "tools_kicker": "FAQ / KNOWLEDGE", "tools_title": "Questions",
            "tool1_title": "Coiling diameter/weight calculation",
            "tool1_desc": "Calculate the approximate diameter and weight of a film roll from thickness, length and core size.",
            "tool1_cta": "Open calculator",
            "tool2_title": "FAQ",
            "tool2_desc": "Answers on material selection and processing for 半导体, photovoltaic, 医药, agricultural and other 应用行业页.",
            "tool2_cta": "Browse %s questions",
            "tool3_title": "Videos",
            "tool3_desc": "Catalogue of brand 视频 and ETFE application 视频.",
            "tool3_cta": "View video catalogue",
            "tag_tool": "Tool", "tag_faq": "FAQ", "tag_video": "Video",
        },
        "calc": {
            "hero_kicker": "TOOLS / KNOWLEDGE", "hero_title": "Coiling diameter/weight calculation",
            "hero_lead": "Fill in the following information to calculate the approximate diameter and weight of a film roll.",
            "title1": "Calculation of coiling diameter",
            "desc1": "Fill in the following information. Calculate the approximate diameter of the thin film.",
            "thickness": "Thickness (microns)", "range500": "1 to 500",
            "length": "Length（M）", "range9999": "1 to 9999",
            "core": "core size",
            "cores": [("Three inches （plastic tube core）", 94.2),
                      ("Three inches（paper tube core）", 104.2),
                      ("Six inches (Paper tube core)", 180.4),
                      ("Six inches (Plastic tube core)", 168.4)],
            "button": "count", "result1": "Coiling diameter", "mm": "mm",
            "note1": "(Note 1) The calculated value is an approximate value, The actual value may vary depending on winding conditions, etc.",
            "note2": "(Note 2) When calculating the thickness, the paper core is 14mm and the plastic core is 8mm.",
            "title2": "Weight calculation",
            "desc2": "The approximate weight of the film is calculated based on its thickness and width.",
            "product": "product name",
            "产品页": [("VitaFlon™ETFE", 1.75), ("FlexFlon™ETFE", 1.75),
                         ("VitaFlon™FEP", 2.15), ("FlexFlon™FEP", 2.15),
                         ("VitaFlon™PFA", 2.15), ("FlexFlon™PFA", 2.15),
                         ("VitaFlon™PCTFE", 2.1), ("PEEK", 1.7)],
            "width": "Width (millimeter)", "length_m": "Length（meters)",
            "result2": "Weight", "kg": "kg",
        },
        "faq": {
            "hero_kicker": "FAQ", "hero_title": "FAQ",
            "hero_lead": "Questions and answers from the PLUSXTECH website.",
            "search": "Search questions, e.g. release film, light transmittance, temperature resistance",
            "count": "%s questions", "empty": "No matching questions. Try another keyword.",
            "note": "",
        },
        "video": {
            "hero_kicker": "VIDEO", "hero_title": "Videos",
            "hero_lead": "Brand 视频 and product 视频.",
            "note": "Per the text-only requirement, video files are not included; only section names and titles are listed.",
            "intro_video": "COMPANY INTRODUCTION VIDEO",
        },
        "privacy": {
            "hero_kicker": "PRIVACY POLICY", "hero_title": "Privacy Policy",
            "hero_lead": "Privacy Policy",
        },
        "cats": CAT_LABELS["en"],
        "site": DATA["en"]["site"],
    },
}


def e(s):
    return html.escape(str(s or ""), quote=True)


def meta_desc(text, n=150):
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    first = re.split(r"(?<=[。！？.!?])\s*", text, maxsplit=1)[0] if text else ""
    if len(first) > n:
        first = first[:n - 1].rstrip() + "…"
    return first


# per-language globals
LANG = "zh"
D = DATA["zh"]
T = TXT["zh"]
OUT = ROOT
ASSET = ""
PRODUCTS = {}
APPS = {}


def setup(lang):
    global LANG, D, T, OUT, ASSET, PRODUCTS, APPS
    LANG = lang
    D = DATA[lang]
    T = TXT[lang]
    OUT = ROOT if lang == "zh" else EN_DIR
    ASSET = "" if lang == "zh" else "../"
    PRODUCTS = 产品页_of(lang)
    APPS = apps_of(lang)


def brand():
    return T["brand"]


def lang_href(filename):
    return ("en/" + filename) if LANG == "zh" else ("../" + filename)


# ------------------------------------------------------------------ chrome
def header(active):
    items = []
    for key, label, href, _ in T["nav"]:
        drop = []
        if key == "产品页":
            drop = [(T["cats"]["film"], "product-center.html#film"),
                    (T["cats"]["tape"], "product-center.html#tape"),
                    (T["cats"]["comp"], "product-center.html#composite")]
        elif key == "应用行业页":
            drop = [((a[1] if LANG == "zh" else a[2]), a[3]) for a in APP_META]
        elif key == "knowledge":
            drop = ([("薄膜加工方法", "knowledge.html"), ("常见问题", "faq.html")] if LANG == "zh" else
                    [("Thin film processing methods", "knowledge.html"), ("FAQ", "faq.html")])
        cls = ' class="active"' if key == active else ""
        if drop:
            links = "".join('<a href="%s">%s</a>' % (h, e(l)) for l, h in drop)
            items.append('<li class="has-drop"><a href="%s"%s>%s</a><div class="drop">%s</div></li>'
                         % (href, cls, e(label), links))
        else:
            items.append('<li><a href="%s"%s>%s</a></li>' % (href, cls, e(label)))
    return """
<div class="topline"><div class="container top-inner">
  <span>%(topbar)s</span>
  <span><a href="tel:%(phone)s">%(phone)s</a> · <a href="mailto:%(email)s">%(email)s</a></span>
</div></div>
<header class="header">
  <div class="container nav-wrap">
    <a class="brand" href="index.html"><img class="brand-logo" src="%(logo_dark)s" alt="%(brand_alt)s"></a>
    <ul class="nav">%(items)s</ul>
    <a class="lang-toggle" href="%(lang_href)s" hreflang="%(hreflang)s" aria-label="%(lang_label)s"><span class="%(zh_cls)s">中</span><i>/</i><span class="%(en_cls)s">EN</span></a>
    <button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false">☰</button>
  </div>
</header>""" % {
        "topbar": e(T["topbar"]), "phone": T["site"]["phone"], "email": T["site"]["email"],
        "brand": e(T["brand"]), "items": "".join(items),
        "logo_dark": img_url("assets/images/brand/logo-dark.png"),
        "brand_alt": "PLUSXTECH 正宇新材",
        "lang_href": lang_href(PAGE_FILE), "hreflang": "en" if LANG == "zh" else "zh-CN",
        "lang_label": "Switch to English" if LANG == "zh" else "切换到中文",
        "zh_cls": "on" if LANG == "zh" else "", "en_cls": "on" if LANG == "en" else "",
    }


def footer():
    prod_links = ('<a href="product-center.html">%s</a>'
                  '<a href="product-center.html#film">%s</a>'
                  '<a href="product-center.html#tape">%s</a>'
                  '<a href="product-center.html#composite">%s</a>') % (
        e(T["footer"]["产品页"]), e(T["cats"]["film"]), e(T["cats"]["tape"]), e(T["cats"]["comp"]))
    app_links = "".join('<a href="%s">%s</a>' % (a[3], e(a[1] if LANG == "zh" else a[2]))
                        for a in APP_META)
    know_links = (
        '<a href="knowledge.html">%s</a><a href="faq.html">%s</a><a href="privacy.html">%s</a>'
    ) % (("薄膜加工方法", "常见问题", "隐私政策")
         if LANG == "zh" else
         ("Thin film processing methods", "FAQ", "Privacy Policy"))
    return """
<footer class="footer">
  <div class="container footer-top">
    <div class="footer-brand">
      <a class="brand light" href="index.html"><img class="brand-logo brand-logo-light" src="%(logo_white)s" alt="%(brand_alt)s"></a>
      <p>%(addr)s</p>
      <p class="footer-contact"><span>%(phone_label)s <a href="tel:%(phone)s">%(phone)s</a></span><span>%(email_label)s <a href="mailto:%(email)s">%(email)s</a></span><span>%(web_label)s <a href="https://www.plusxtech.com" target="_blank" rel="noopener">%(web)s</a></span></p>
    </div>
    <div class="footer-col"><h4>%(about)s</h4>
      <a href="about.html">%(about_name)s</a><a href="index.html#service">%(contact)s</a><a href="privacy.html">%(privacy)s</a>
    </div>
    <div class="footer-col"><h4>%(产品页)s</h4>%(prod_links)s</div>
    <div class="footer-col"><h4>%(apps)s</h4>%(app_links)s</div>
    <div class="footer-col"><h4>%(knowledge)s</h4>%(know_links)s</div>
  </div>
  <div class="container footer-bottom">
    <span>%(copyright)s</span>
    <span><a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener">%(icp)s</a> · <a href="privacy.html">%(privacy)s</a></span>
  </div>
</footer>""" % {
        "brand": e(T["brand"]), "addr": e(T["site"]["address"]),
        "logo_white": img_url("assets/images/brand/logo-white.png"),
        "brand_alt": "PLUSXTECH 正宇新材",
        "phone_label": e(T["footer"]["phone"]), "phone": T["site"]["phone"],
        "email_label": e(T["footer"]["email"]), "email": T["site"]["email"],
        "web_label": e(T["footer"]["website"]), "web": e(T["site"]["website"]),
        "about": e(T["footer"]["about"]), "about_name": e(T["about"]["hero_title"]),
        "产品页": e(T["footer"]["产品页"]), "prod_links": prod_links,
        "apps": e(T["footer"]["应用行业页"]), "app_links": app_links,
        "knowledge": e(T["footer"]["knowledge"]), "know_links": know_links,
        "copyright": e(T["site"]["copyright"]), "icp": e(T["site"]["icp"]),
        "privacy": e(T["footer"]["privacy"]),
        "contact": e(T["footer"]["contact"]),
    }


PAGE_FILE = "index.html"


def page(filename, title, desc, active, body, scripts=()):
    global PAGE_FILE
    PAGE_FILE = filename
    extra = "".join('<script src="%s%s"></script>' % (ASSET, s) for s in scripts)
    return """<!doctype html>
<html lang="%s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:type" content="website">
<link rel="stylesheet" href="%sstyles.css">
</head>
<body class="%s">
%s
<main>
%s
</main>
%s
<script src="%sscript.js"></script>
%s
</body>
</html>""" % ("zh-CN" if LANG == "zh" else "en", e(title), e(desc), e(title), e(desc),
              ASSET, "home" if active == "home" else "", header(active), body, footer(),
              ASSET, extra)


def hero(kicker, title, lead="", crumbs=None, meta="", cls="", style=""):
    c = ""
    if crumbs:
        parts = []
        for i, (label, href) in enumerate(crumbs):
            if i:
                parts.append('<span class="sep">/</span>')
            parts.append('<a href="%s">%s</a>' % (href, e(label)) if href else '<span>%s</span>' % e(label))
        c = '<nav class="crumb" aria-label="Breadcrumb">%s</nav>' % "".join(parts)
    lead_html = '<p class="page-lead">%s</p>' % e(lead) if lead else ""
    return """<section class="page-hero %s" style="%s">
  <div class="container">
    %s
    <div class="eyebrow">%s</div>
    <h1>%s</h1>
    %s
    %s
  </div>
</section>""" % (cls, style, c, e(kicker), e(title), lead_html, meta)


def section_head(kicker, title, lead="", link=None):
    l = ""
    if link:
        l = '<a class="arrow-link" href="%s">%s <span>↗</span></a>' % (link[1], e(link[0]))
    lead_html = '<p class="section-lead">%s</p>' % e(lead) if lead else ""
    return """<div class="section-head">
  <div><div class="kicker">%s</div><h2>%s</h2>%s</div>
  %s
</div>""" % (e(kicker), title, lead_html, l)


def mat_style(slug):
    _, _, c1, c2 = PRODUCT_META[slug]
    return 'style="--mat1:%s;--mat2:%s"' % (c1, c2)


def img_url(path):
    return (ASSET + path) if path else ""


def mat_visual(slug, code, name, cls=""):
    path = IMAGES.get("产品页", {}).get(slug)
    if path:
        return ('<div class="mat-visual %s has-img" style="background-image:url(\'%s\')">'
                '<b>%s</b><span>%s</span></div>') % (cls, img_url(path), e(code), e(name))
    return '<div class="mat-visual %s" %s><b>%s</b><span>%s</span></div>' % (
        cls, mat_style(slug), e(code), e(name))


def app_图片(slug):
    return IMAGES.get("应用行业页", {}).get(slug, [])


def product_name(slug):
    return PRODUCTS[slug]["name"]


# ------------------------------------------------------------------ home
def build_home():
    h = D["home"]
    about = D["about"]
    def stat_html(s):
        sup = "<sup>%s</sup>" % e(s["suffix"]) if s["suffix"] else ""
        return '<div><b>%s%s</b><span>%s</span></div>' % (e(s["value"]), sup, e(s["label"]))
    stats = "".join(stat_html(s) for s in about["stats"])
    hero_html = """<section class="hero hero-photo">
  <div class="hero-orb orb-a"></div><div class="hero-orb orb-b"></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <div class="eyebrow">%s</div>
      <h1>%s</h1>
      <p>%s</p>
      <div class="hero-actions">
        <a class="btn btn-light" href="product-center.html">%s <span>↗</span></a>
        <a class="text-link" href="about.html">%s <span>→</span></a>
      </div>
      <div class="hero-stats">%s</div>
    </div>
    <div class="hero-visual" aria-hidden="true">
      <div class="swatch swatch-1"><b>ETFE</b><span>%s</span></div>
      <div class="swatch swatch-2"><b>PFA</b><span>%s</span></div>
      <div class="swatch swatch-3"><b>PTFE</b><span>%s</span></div>
    </div>
  </div>
</section>""" % (e(T["home"]["eyebrow"]), T["home"]["title"], e(about["intro"][0]),
                e(T["home"]["cta1"]), e(T["home"]["cta2"]), stats,
                e(T["home"]["swatches"][0]), e(T["home"]["swatches"][1]), e(T["home"]["swatches"][2]))

    _hero_img = IMAGES.get("banners", {}).get("产品页", "")
    if _hero_img:
        hero_html = hero_html.replace('<section class="hero hero-photo">',
            '<section class="hero hero-photo" style="--hero-img:url(\'%s\')">' % img_url(_hero_img), 1)

    app_cards = []
    for i, a in enumerate(h["应用行业页"]):
        order = HOME_APP_SLUGS[LANG]
        slug = order[i] if i < len(order) else ""
        href = next((x[3] for x in APP_META if x[0] == slug), "applications.html")
        app_cards.append("""<a class="app-card" href="%s">
  <div class="app-card-top"><span class="app-index">%02d</span><span class="app-name">%s</span><span class="app-arrow">↗</span></div>
  <p>%s</p>
</a>""" % (href, i + 1, e(a["label"]), e(a["desc"])))

    prod_cards = []
    for i, slug in enumerate(HOME_PROD_SLUGS):
        if i >= len(h["产品页"]):
            break
        p = h["产品页"][i]
        meta = PRODUCT_META[slug]
        tags = "".join("<span>%s</span>" % e(f) for f in p["features"][:6])
        prod_cards.append("""<a class="product-card" href="%s">
  %s
  <div class="product-card-body">
    <h3>%s</h3>
    <p>%s</p>
    <div class="chips">%s</div>
  </div>
</a>""" % (meta[1], mat_visual(slug, meta[0], p["name"]), e(p["name"]), e(p["intro"]), tags))

    values = "".join("""<div class="value-card">
  <span class="value-num">%s</span><h3>%s</h3><p>%s</p>
</div>""" % (e(v["num"]), e(v["title"]), e(v["desc"])) for v in about["values"])

    body = hero_html + """
<section class="section" id="应用行业页">
  <div class="container">
    %s
    <div class="app-grid">%s</div>
    <div class="center-link"><a class="arrow-link" href="applications.html">%s <span>↗</span></a></div>
  </div>
</section>

<section class="section section-alt" id="产品页">
  <div class="container">
    %s
    <div class="product-grid">%s</div>
  </div>
</section>

<section class="section" id="about">
  <div class="container about-split">
    <div>
      <div class="kicker">%s</div>
      <h2>%s</h2>
      <div class="about-text"><p>%s</p><p>%s</p></div>
      <a class="arrow-link" href="about.html">%s <span>↗</span></a>
    </div>
    <div class="values">%s</div>
  </div>
</section>

<section class="section section-alt" id="service">
  <div class="container service-band">
    <div>
      <div class="kicker">%s</div>
      <h2>%s</h2>
      <p class="section-lead">%s</p>
    </div>
    <div class="service-contact">
      <a href="tel:%s"><span>%s</span><b>%s</b></a>
      <a href="mailto:%s"><span>%s</span><b>%s</b></a>
      <a href="https://www.plusxtech.com" target="_blank" rel="noopener"><span>%s</span><b>%s</b></a>
    </div>
  </div>
</section>
""" % (
        section_head(T["home"]["apps_kicker"], T["home"]["apps_title"], T["home"]["apps_lead"]),
        "".join(app_cards), e(T["home"]["apps_all"]),
        section_head(T["home"]["产品页_kicker"], T["home"]["产品页_title"], T["home"]["产品页_lead"],
                     (T["home"]["产品页_all"], "product-center.html")),
        "".join(prod_cards),
        e(T["home"]["about_kicker"]), e(T["home"]["about_title"]),
        e(about["intro"][0]), e(about["intro"][1] if len(about["intro"]) > 1 else ""),
        e(T["home"]["about_more"]), values,
        e(T["home"]["service_kicker"]), T["home"]["service_title"], e(h["service_note"]),
        T["site"]["phone"], e(T["home"]["service_phone"]), T["site"]["phone"],
        T["site"]["email"], e(T["home"]["service_email"]), T["site"]["email"],
        e(T["home"]["service_web"]), e(T["site"]["website"]),
    )
    title = ("正宇新材 | 创新可靠的材料供应商" if LANG == "zh"
             else "PLUSXTECH | Innovative & Reliable Materials Supplier")
    desc = T["home"]["desc"]
    return page("index.html", title, desc, "home", body)


# ------------------------------------------------------------------ about
def build_about():
    a = D["about"]
    def stat_html(s):
        sup = "<sup>%s</sup>" % e(s["suffix"]) if s["suffix"] else ""
        return '<div><b>%s%s</b><span>%s</span></div>' % (e(s["value"]), sup, e(s["label"]))
    stats = "".join(stat_html(s) for s in a["stats"])
    intro = "".join("<p>%s</p>" % e(p) for p in a["intro"])
    history = "".join("""<div class="timeline-item">
  <div class="timeline-year">%s</div><p>%s</p>
</div>""" % (e(x["year"]), e(x["desc"])) for x in a["history"])
    values = "".join("""<div class="value-card">
  <span class="value-num">%s</span><h3>%s</h3><p>%s</p>
</div>""" % (e(v["num"]), e(v["title"]), e(v["desc"])) for v in a["values"])
    est = a["stats"][0]["value"] if a["stats"] else ""
    lines = a["stats"][1]["value"] if len(a["stats"]) > 1 else ""
    series = a["stats"][2]["value"] if len(a["stats"]) > 2 else ""
    if LANG == "zh":
        fact_est, fact_lines, fact_series = "%s 年" % est, "%s 条生产线投产" % lines, "%s 大产品系列" % series
    else:
        fact_est, fact_lines, fact_series = est, "%s production lines" % lines, "%s product series" % series
    _about_bg = IMAGES.get("banners", {}).get("about", "")
    _poster = IMAGES.get("banners", {}).get("company", "")
    _video_src = "assets/video/company-en.mp4" if LANG == "en" else "assets/video/company.mp4"
    _company_banner = ('<figure class="company-banner"><img src="%s" alt="%s" loading="lazy"></figure>'
                       % (img_url(_poster), e("PLUSXTECH 工厂" if LANG == "zh" else "PLUSXTECH factory"))) if _poster else ""
    body = hero(T["about"]["hero_kicker"], T["about"]["hero_title"], "",
                [("首页" if LANG == "zh" else "Home", "index.html"),
                 (T["footer"]["about"], None), (T["about"]["hero_title"], None)]) + _company_banner + """
<section class="section about-stats"><div class="container">
  <div class="stats-row">%s</div>
</div></section>

<section class="about-video" style="--about-bg:url('%s')">
  <div class="about-video-shade"></div>
  <div class="container about-video-inner">
    <div class="about-video-copy">%s</div>
    <button class="about-video-play" type="button" data-video-open aria-label="%s">
      <span class="play-ring"><span>▶</span></span>
      <span class="play-label">%s</span>
    </button>
  </div>
</section>

<section class="section section-alt"><div class="container">
  %s
  <div class="timeline">%s</div>
</div></section>

<section class="section"><div class="container">
  %s
  <div class="value-grid">%s</div>
</div></section>

<div class="video-modal" id="video-modal" hidden>
  <div class="video-modal-backdrop" data-video-close></div>
  <div class="video-modal-panel">
    <button class="video-modal-close" type="button" data-video-close aria-label="%s">×</button>
    <video id="company-video" controls playsinline preload="none" poster="%s">
      <source src="%s" type="video/mp4">
    </video>
  </div>
</div>
""" % (stats, img_url(_about_bg), intro, e(T["about"]["video_label"]), e(T["about"]["video_label"]),
       section_head(T["about"]["history_kicker"], T["about"]["history_title"]), history,
       section_head(T["about"]["values_kicker"], T["about"]["values_title"]), values,
       e(T["about"]["video_close"]), img_url(_poster), img_url(_video_src))
    title = "关于正宇 | 正宇新材" if LANG == "zh" else "About us | PLUSXTECH"
    return page("about.html", title, meta_desc(a["intro"][0] if a["intro"] else title), "about", body)


# ------------------------------------------------------------------ 产品页
def product_card(p, show_more=False):
    slug = p["slug"]
    meta = PRODUCT_META[slug]
    tags = "".join("<span>%s</span>" % e(f["name"]) for f in p["features"][:6])
    more = '<span class="card-more">%s ↗</span>' % e(T["home"]["product_more"]) if show_more else ""
    return """<a class="product-card" href="%s">
  %s
  <div class="product-card-body">
    <h3>%s</h3><p>%s</p><div class="chips">%s</div>%s
  </div>
</a>""" % (meta[1], mat_visual(slug, meta[0], p["name"]), e(p["name"]),
           e(p["intro"][0] if p["intro"] else ""), tags, more)


def build_产品页():
    films = [PRODUCTS[s] for s in FILMS]
    tapes = [PRODUCTS[s] for s in TAPES]
    comps = [PRODUCTS[s] for s in COMPS]
    _hero_img = IMAGES.get("banners", {}).get("产品页", "")
    body = hero(T["产品页"]["hero_kicker"], T["产品页"]["hero_title"], T["产品页"]["hero_lead"],
                [("首页" if LANG == "zh" else "Home", "index.html"), (T["产品页"]["hero_title"], None)],
                cls="page-hero-photo" if _hero_img else "",
                style="--hero-img:url('%s')" % img_url(_hero_img) if _hero_img else "") + """
<section class="section" id="film"><div class="container">
  %s
  <div class="product-grid">%s</div>
</div></section>
<section class="section section-alt" id="tape"><div class="container">
  %s
  <div class="product-grid">%s</div>
</div></section>
<section class="section" id="composite"><div class="container">
  %s
  <div class="product-grid">%s</div>
</div></section>
<section class="section section-alt"><div class="container cta-band">
  <div><div class="kicker">CONTACT</div><h2>%s</h2><p class="section-lead">%s</p></div>
  <div class="cta-actions"><a class="btn btn-dark" href="tel:%s">%s <span>↗</span></a>
  <a class="text-link" href="mailto:%s">%s</a></div>
</div></section>
""" % (section_head(T["产品页"]["film_kicker"], T["cats"]["film"], T["产品页"]["film_lead"]),
       "".join(product_card(p, True) for p in films),
       section_head(T["产品页"]["tape_kicker"], T["cats"]["tape"], T["产品页"]["tape_lead"]),
       "".join(product_card(p, True) for p in tapes),
       section_head(T["产品页"]["comp_kicker"], T["cats"]["comp"], T["产品页"]["comp_lead"]),
       "".join(product_card(p, True) for p in comps),
       e(T["产品页"]["cta_title"]), e(T["产品页"]["cta_lead"]),
       T["site"]["phone"], T["site"]["phone"], T["site"]["email"], T["site"]["email"])
    title = "产品中心 | 正宇新材" if LANG == "zh" else "Products | PLUSXTECH"
    return page("product-center.html", title, T["产品页"]["hero_lead"], "产品页", body)


def build_product(slug):
    p = PRODUCTS[slug]
    meta = PRODUCT_META[slug]
    ck = cat_key(slug)
    cat = T["cats"][ck]
    feats = ""
    if p["features"]:
        cards = "".join("""<div class="feature-card">
  <span class="feature-num">%02d</span><h3>%s</h3><p>%s</p>
</div>""" % (i + 1, e(f["name"]), e(f["desc"])) for i, f in enumerate(p["features"]))
        feats = """<section class="section"><div class="container">
  %s
  <div class="feature-grid">%s</div>
</div></section>""" % (section_head(T["product"]["features_kicker"], T["product"]["features_title"]), cards)
    colors = ""
    if p["colors"]:
        colors = """<section class="section section-alt"><div class="container">
  <div class="kicker">%s</div><h2>%s</h2>
  <div class="color-row">%s</div>
</div></section>""" % (e(T["product"]["colors_kicker"]), e(T["product"]["colors_title"]),
                       "".join('<span class="color-chip">%s</span>' % e(c) for c in p["colors"]))
    series = ""
    if p["series"]:
        cards = []
        for s in p["series"]:
            dl = ('<a class="download" href="%s" target="_blank" rel="noopener">%s ↗</a>'
                  % (e(s["pdf"]), e(T["product"]["download"]))) if s["pdf"] else ""
            cards.append("""<article class="series-card"><h3>%s</h3><p>%s</p>%s</article>"""
                         % (e(s["name"]), e(s["desc"]), dl))
        series = """<section class="section"><div class="container">
  %s
  <div class="series-grid">%s</div>
</div></section>""" % (section_head(T["product"]["series_kicker"], T["product"]["series_title"]), "".join(cards))
    siblings = [s for s in PRODUCT_ORDER if cat_key(s) == ck and s != slug]
    sib = ""
    if siblings:
        links = "".join('<a href="%s">%s</a>' % (PRODUCT_META[s][1], e(PRODUCTS[s]["name"])) for s in siblings)
        sib = """<section class="section section-alt"><div class="container">
  <div class="kicker">%s</div><div class="link-row">%s</div>
</div></section>""" % (e(T["product"]["more_kicker"]), links)
    intro = "".join("<p>%s</p>" % e(x) for x in p["intro"])
    body = hero("%s / %s" % (cat, T["product"]["crumb"]), p["name"], "",
                [("首页" if LANG == "zh" else "Home", "index.html"),
                 (T["product"]["crumb"], "product-center.html"),
                 (cat, "product-center.html#%s" % {"film": "film", "tape": "tape", "comp": "composite"}[ck]),
                 (p["name"], None)]) + """
<section class="product-intro"><div class="container product-intro-grid">
  %s
  <div class="prose">%s</div>
</div></section>
%s%s%s%s
<section class="section section-dark"><div class="container cta-band">
  <div><div class="kicker">CONTACT</div><h2>%s</h2><p class="section-lead">%s</p></div>
  <div class="cta-actions"><a class="btn btn-light" href="tel:%s">%s <span>↗</span></a>
  <a class="text-link" href="mailto:%s">%s</a></div>
</div></section>
""" % (mat_visual(slug, meta[0], p["name"], "tall"), intro, feats, colors, series, sib,
       e(T["product"]["cta_title"] % p["name"]), e(T["product"]["cta_lead"]),
       T["site"]["phone"], T["site"]["phone"], T["site"]["email"], T["site"]["email"])
    title = "%s | %s" % (p["name"], "正宇新材" if LANG == "zh" else "PLUSXTECH")
    return page(meta[1], title, meta_desc(p["intro"][0] if p["intro"] else title), "产品页", body)


# ------------------------------------------------------------------ 应用行业页
def build_应用行业页():
    cards = []
    for i, (slug, zh, en, href, c1, c2) in enumerate(APP_META):
        a = APPS[slug]
        name = zh if LANG == "zh" else en
        lead_title = a["lead"][0] if a["lead"] else name
        _ind = IMAGES.get("industries", {}).get(slug)
        _media = ('<div class="app-card-media"><img src="%s" alt="%s" loading="lazy"></div>'
                  % (img_url(_ind), e(name))) if _ind else ""
        cards.append("""<a class="app-card tall" href="%s">
  %s
  <div class="app-card-body">
    <div class="app-card-top"><span class="app-index">%02d</span><h3 class="app-name">%s</h3><span class="app-arrow">↗</span></div>
    <p class="app-lead">%s</p>
  </div>
</a>""" % (href, _media, i + 1, e(name), e(lead_title)))
    body = hero(T["应用行业页"]["hero_kicker"], T["应用行业页"]["hero_title"], "",
                [("首页" if LANG == "zh" else "Home", "index.html"), (T["应用行业页"]["hero_title"], None)]) + """
<section class="section"><div class="container"><div class="app-grid wide">%s</div></div></section>
""" % "".join(cards)
    title = "应用领域 | 正宇新材" if LANG == "zh" else "Applications | PLUSXTECH"
    return page("applications.html", title, title, "应用行业页", body)


def build_application(slug):
    a = APPS[slug]
    meta = next(x for x in APP_META if x[0] == slug)
    name = meta[1] if LANG == "zh" else meta[2]
    tabs = "".join('<a href="%s"%s>%s</a>' % (x[3], ' class="active"' if x[0] == slug else "",
                                               e(x[1] if LANG == "zh" else x[2])) for x in APP_META)
    sections = "".join("""<article class="app-section">
  <span class="section-num">%02d</span>
  <div><h3>%s</h3>%s</div>
</article>""" % (i + 1, e(s["title"]),
                  "".join("<p>%s</p>" % e(x).replace("\n", "<br>") for x in s["paras"]))
                     for i, s in enumerate(a["sections"]))
    tags = "".join("<span>%s</span>" % e(t) for t in a["tags"])
    related = "".join("<span>%s</span>" % e(r) for r in a["related"])
    _gallery_imgs = app_图片(slug)
    gallery = ""
    if _gallery_imgs:
        figs = "".join('<figure class="related-card"><img src="%s" alt="%s" loading="lazy"><figcaption>%s</figcaption></figure>'
                       % (img_url(m["path"]), e(m["zh"] if LANG == "zh" else m["en"]),
                          e(m["zh"] if LANG == "zh" else m["en"])) for m in _gallery_imgs)
        gallery = ('<section class="section section-alt"><div class="container">%s'
                   '<div class="related-grid">%s</div></div></section>') % (
            section_head(T["app"]["gallery_kicker"], T["app"]["gallery_title"]), figs)
    lead_title = '<p class="app-title">%s</p>' % e(a["title"]) if a["title"] else ""
    body = hero(T["app"]["hero_kicker"], name, "",
                [("首页" if LANG == "zh" else "Home", "index.html"),
                 (T["应用行业页"]["hero_title"], "applications.html"), (name, None)]) + """
<section class="app-lead"><div class="container">
  %s
  <div class="prose lead-prose">%s</div>
  <div class="app-tabs">%s</div>
</div></section>
<section class="section"><div class="container app-body-grid">
  <div class="app-sections">%s</div>
  <aside class="app-aside">
    <div class="aside-block"><h3>%s</h3><div class="chips">%s</div></div>
    <div class="aside-block"><h3>%s</h3><div class="chips">%s</div></div>
    <div class="aside-block"><h3>%s</h3><p class="family">%s</p></div>
    <div class="aside-block contact-mini"><h3>%s</h3>
      <a href="tel:%s">%s</a><a href="mailto:%s">%s</a></div>
  </aside>
</div></section>
""" % (lead_title, "".join("<p>%s</p>" % e(x) for x in a["lead"]), tabs, sections,
       e(T["app"]["aside_app"]), tags, e(T["app"]["aside_related"]), related,
       e(T["app"]["aside_family"]), e(a["family"] or "Vitaflon™"),
       e(T["app"]["aside_contact"]), T["site"]["phone"], T["site"]["phone"],
       T["site"]["email"], T["site"]["email"]) + gallery
    title = ("%s应用 | 正宇新材" % name) if LANG == "zh" else ("%s | PLUSXTECH" % (a["title"] or (name + " 应用行业页")))
    desc = meta_desc(a["lead"][0] if a["lead"] else title)
    return page(meta[3], title, desc, "应用行业页", body)


# ------------------------------------------------------------------ knowledge
def build_knowledge():
    def _method_card(i, m):
        path = IMAGES.get("methods", {}).get(m["name"])
        media = ('<div class="method-media"><img src="%s" alt="%s" loading="lazy"></div>'
                 % (img_url(path), e(m["name"]))) if path else ""
        return """<div class="method-card">
  %s
  <span class="method-num">%02d</span><h3>%s</h3><p>%s</p>
</div>""" % (media, i + 1, e(m["name"]), e(m["desc"]))
    cards = "".join(_method_card(i, m) for i, m in enumerate(D["methods"]))
    k = T["knowledge"]
    body = hero(k["hero_kicker"], k["hero_title"], "",
                [("首页" if LANG == "zh" else "Home", "index.html"), (k["hero_title"], None)]) + """
<section class="section"><div class="container">
  %s
  <div class="method-grid">%s</div>
</div></section>
<section class="section section-alt"><div class="container">
  %s
  <div class="tool-grid">
    <a class="tool-card" href="faq.html"><span>%s</span><h3>%s</h3><p>%s</p><b>%s ↗</b></a>
  </div>
</div></section>
""" % (section_head(k["methods_kicker"], k["methods_title"]), cards,
       section_head(k["tools_kicker"], k["tools_title"]),
       e(k["tag_faq"]), e(k["tool2_title"]), e(k["tool2_desc"]), e(k["tool2_cta"] % len(D["faq"])))
    title = "薄膜知识 | 正宇新材" if LANG == "zh" else "Knowledge | PLUSXTECH"
    return page("knowledge.html", title, k["hero_title"], "knowledge", body)


def build_faq():
    items = "".join("""<details class="faq-item">
  <summary><span class="q">Q</span><span>%s</span></summary>
  <div class="faq-a"><span class="a">A</span><div>%s</div></div>
</details>""" % (e(x["q"]), e(x["a"]).replace("\n", "<br>")) for x in D["faq"])
    k = T["faq"]
    body = hero(k["hero_kicker"], k["hero_title"], k["hero_lead"],
                [("首页" if LANG == "zh" else "Home", "index.html"),
                 (T["knowledge"]["hero_title"], "knowledge.html"), (k["hero_title"], None)]) + """
<section class="section"><div class="container faq-wrap">
  <div class="faq-tools">
    <input id="faq-search" type="search" placeholder="%s" aria-label="%s">
    <span id="faq-count" data-total="%d">%s</span>
  </div>
  <div class="faq-list" id="faq-list">%s</div>
  <p class="empty-tip" id="faq-empty" hidden>%s</p>
</div></section>
""" % (e(k["search"]), e(k["search"]), len(D["faq"]), e(k["count"] % len(D["faq"])), items, e(k["empty"]))
    title = "常见问题 | 正宇新材" if LANG == "zh" else "FAQ | PLUSXTECH"
    return page("faq.html", title, k["hero_lead"], "knowledge", body, ("faq.js",))


# ------------------------------------------------------------------ privacy
def build_privacy():
    k = T["privacy"]
    if LANG == "zh":
        raw = D["privacy"]["raw"]
        sections = []
        rest = raw[4:]
        for i in range(0, len(rest) - 1, 2):
            sections.append((rest[i], rest[i + 1]))
        sec_html = "".join("""<section class="privacy-section"><h2>%s</h2><p>%s</p></section>"""
                           % (e(h), e(p)) for h, p in sections)
        body = hero(k["hero_kicker"], k["hero_title"], "",
                    [("首页", "index.html"), (k["hero_title"], None)]) + """
<section class="section"><div class="container article">
  <div class="privacy-lead">
    <p>%s</p><p>--------------</p><p>· 隐私安全</p><p>%s</p>
  </div>
  %s
</div></section>
""" % (e(raw[0].replace("隐私政策", "")), e(raw[3]), sec_html)
    else:
        blocks = []
        for b in D["privacy"]["blocks"]:
            if b["t"] == "h2":
                head, _, rest = b["x"].partition("\n")
                blocks.append("<h2>%s</h2>" % e(head))
                if rest.strip():
                    blocks.append("<p>%s</p>" % e(rest.strip()))
            else:
                blocks.append("<p>%s</p>" % b["x"])
        body = hero(k["hero_kicker"], k["hero_title"], "",
                    [("Home", "index.html"), (k["hero_title"], None)]) + """
<section class="section"><div class="container article privacy-en">
  %s
</div></section>
""" % "\n".join(blocks)
    title = "隐私政策 | 正宇新材" if LANG == "zh" else "Privacy Policy | PLUSXTECH"
    return page("privacy.html", title, k["hero_title"], "", body)


# ------------------------------------------------------------------ run
def write(filename, text):
    open(os.path.join(OUT, filename), "w", encoding="utf-8").write(text)


def build_all():
    os.makedirs(EN_DIR, exist_ok=True)

    # home
    write("index.html", build_home())
    write("about.html", build_about())
    write("product-center.html", build_产品页())
    for slug in PRODUCT_ORDER:
        write(PRODUCT_META[slug][1], build_product(slug))
    write("applications.html", build_应用行业页())
    for a in APP_META:
        write(a[3], build_application(a[0]))
    write("knowledge.html", build_knowledge())
    write("faq.html", build_faq())
    write("privacy.html", build_privacy())


def main():
    setup("zh")
    build_all()
    setup("en")
    build_all()
    print("Chinese pages: 30 ->", ROOT)
    print("English pages: 30 ->", EN_DIR)


if __name__ == "__main__":
    main()
