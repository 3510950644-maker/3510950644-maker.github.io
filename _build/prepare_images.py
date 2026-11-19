# -*- coding: utf-8 -*-
"""Prepare optimized web 图片 from /图片 and write _build/images.json."""
import json, os
from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "images")
OUT = os.path.join(ROOT, "assets", "图片")

PRODUCTS = {
    "psu": "PSU.png",
    "ptfe": "PTFE.jpg",
    "pfa": "PFA.png",
    "fep": "FEP.png",
    "etfe": "ETFE.png",
    "光伏df": "PVDF.png",
    "peek": "PEEK.png",
    "ec": "EC.png",
    "etfe-tape": "ETFE胶带.jpg",
    "ptfe-tape": "PTFE胶带.png",
    "psa-tape": "压敏胶带.png",
    "fp": "FP复合膜.jpg",
    "ep": "EP复合膜.jpg",
}

APPS = {
    "航空": [
        ("ec-long-wave-tape.jpg", "ec-tape", "EC 长效透波胶带", "EC Long-acting Wave-transparent Tape"),
        ("etfe-mr-release-series.jpg", "etfe-mr", "ETFE MR 系列（离型级）", "ETFE MR Series (Release Grade)"),
        ("ETFE Tape.jpg", "etfe-tape", "ETFE Tape", "ETFE Tape"),
        ("fep-mr-series.jpg", "fep-mr", "FEP MR 系列", "FEP MR Series"),
        ("peek-series.png", "peek", "PEEK 系列", "PEEK Series"),
        ("pfa-series.jpg", "pfa", "PFA 系列", "PFA Series"),
        ("PTFE MR.jpg", "ptfe-mr", "PTFE MR", "PTFE MR"),
        ("PTFE tape.png", "ptfe-tape", "PTFE tape", "PTFE Tape"),
    ],
    "光伏": [
        ("etfe-hp-series.jpg", "etfe-hp", "ETFE HP 系列（超纯级）", "ETFE HP Series (Ultra-pure)"),
        ("etfe-mr-series.png", "etfe-mr", "ETFE MR 系列（离型级）", "ETFE MR Series (Release Grade)"),
        ("fep-hp-series.jpg", "fep-hp", "FEP HP 系列", "FEP HP Series"),
        ("peek-series.png", "peek", "PEEK 系列", "PEEK Series"),
        ("pfa-series.jpg", "pfa", "PFA 系列", "PFA Series"),
    ],
    "半导体": [
        ("ep-composite.jpg", "ep-composite", "EP 复合膜", "EP Composite Film"),
        ("etfe-mr-composite.jpg", "etfe-mr-composite", "ETFE MR 复合膜", "ETFE MR Composite Film"),
        ("fep-mr-series.jpg", "fep-mr", "FEP MR 系列", "FEP MR Series"),
        ("fp-composite.jpg", "fp-composite", "FP 复合膜", "FP Composite Film"),
        ("pfa-mr-series.jpg", "pfa-mr", "PFA MR 系列", "PFA MR Series"),
    ],
    "电子": [
        ("ep-composite.jpg", "ep-composite", "EP 复合膜", "EP Composite Film"),
        ("etfe-mr-series.jpg", "etfe-mr", "ETFE MR 系列", "ETFE MR Series"),
        ("fep-mr-series.jpg", "fep-mr", "FEP MR 系列", "FEP MR Series"),
        ("fp-composite.jpg", "fp-composite", "FP 复合膜", "FP Composite Film"),
        ("pfa-mr-series.jpg", "pfa-mr", "PFA MR 系列", "PFA MR Series"),
    ],
    "医药": [
        ("etfe-hp-series.jpg", "etfe-hp", "ETFE HP 系列（超纯级）", "ETFE HP Series (Ultra-pure)"),
        ("fep-mr-mold-series.png", "fep-mr-mold", "FEP MR 模具离型系列", "FEP MR Mold Release Series"),
        ("peek-series.png", "peek", "PEEK 系列", "PEEK Series"),
        ("pfa-series.jpg", "pfa", "PFA 系列", "PFA Series"),
    ],
    "化工": [
        ("peek-series.png", "peek", "PEEK 系列", "PEEK Series"),
        ("pfa-series.jpg", "pfa", "PFA 系列", "PFA Series"),
    ],
    "建材": [
        ("AG.jpg", "ag", "ETFE AG 系列（建筑型）", "ETFE AG Series (Architectural)"),
        ("fep-mr-mold-series.png", "fep-mr-mold", "FEP MR 模具离型系列", "FEP MR Mold Release Series"),
        ("peek-series.png", "peek", "PEEK 系列", "PEEK Series"),
        ("pfa-series.jpg", "pfa", "PFA 系列", "PFA Series"),
    ],
    "农业": [
        ("AG.jpg", "ag", "ETFE AG 系列（建筑型）", "ETFE AG Series (Architectural)"),
        ("fep-mr-mold-series.png", "fep-mr-mold", "FEP MR 模具离型系列", "FEP MR Mold Release Series"),
        ("peek-series.png", "peek", "PEEK 系列", "PEEK Series"),
        ("pfa-series.jpg", "pfa", "PFA 系列", "PFA Series"),
    ],
}

INDUSTRIES = {
    "航空": "aviation.jpg",
    "光伏": "光伏.jpg",
    "半导体": "semi.jpg",
    "电子": "电子.jpg",
    "医药": "医药.jpg",
    "化工": "化工.png",
    "建材": "建材.png",
    "农业": "agri.jpg",
    "家装": "家装.jpg",
    "交通": "交通.png",
}

METHODS = {
    "喷砂/化学磨砂/涂层哑光": ("spraying.jpg", "sandblast"),
    "蚀刻": ("etching.jpg", "etch"),
    "印染": ("printing.jpg", "dye"),
    "涂层": ("coating.jpg", "coating"),
    "电镀/喷溅": ("plating.jpg", "plating"),
    "电晕处理": ("corona.jpg", "corona"),
    "开槽": ("slitting.jpg", "slitting"),
    "切割/冲压": ("cutting.jpg", "cutting"),
    "压花": ("embossing.jpg", "emboss"),
    "压成型": ("thermoforming.jpg", "thermoform"),
    "层压": ("laminating.jpg", "laminate"),
    "退火": ("annealing.jpg", "anneal"),
}


def resize(im, max_w):
    if im.width > max_w:
        h = int(im.height * max_w / im.width)
        im = im.resize((max_w, h), Image.LANCZOS)
    return im


def save_webp(src, dst, max_w):
    im = Image.open(src)
    im.load()
    im = resize(im, max_w)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA" if "A" in im.mode else "RGB")
    im.save(dst, "WEBP", quality=84, method=6)


def save_jpg(src, dst, max_w):
    im = Image.open(src)
    im.load()
    im = resize(im, max_w).convert("RGB")
    im.save(dst, "JPEG", quality=86, optimize=True)


def trim_white(src, dst, max_w):
    im = Image.open(src).convert("RGB")
    mask = im.convert("L").point(lambda p: 255 if p < 246 else 0)
    box = mask.getbbox()
    if box:
        pad = 24
        box = (max(0, box[0] - pad), max(0, box[1] - pad),
               min(im.width, box[2] + pad), min(im.height, box[3] + pad))
        im = im.crop(box)
    im = resize(im, max_w)
    im.save(dst, "WEBP", quality=86, method=6)


manifest = {"products": {}, "applications": {}, "methods": {}, "banners": {}, "industries": {}}

for slug, name in PRODUCTS.items():
    d = os.path.join(OUT, "products")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, slug + ".webp")
    save_webp(os.path.join(SRC, "products", name), p, 1200)
    manifest["products"][slug] = "assets/images/products/" + slug + ".webp"

for slug, items in APPS.items():
    d = os.path.join(OUT, "applications", slug)
    os.makedirs(d, exist_ok=True)
    manifest["applications"][slug] = []
    for filename, key, zh, en in items:
        p = os.path.join(d, key + ".webp")
        save_webp(os.path.join(SRC, "applications", {"航空": "航空", "光伏": "光伏",
                                                  "半导体": "半导体", "电子": "电子",
                                                  "医药": "医药", "化工": "化工",
                                                  "建材": "建材", "农业": "农业"}[slug], filename),
                  p, 900)
        manifest["applications"][slug].append({
            "path": "assets/images/applications/%s/%s.webp" % (slug, key),
            "zh": zh, "en": en,
        })

for name, (filename, key) in METHODS.items():
    d = os.path.join(OUT, "methods")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, key + ".webp")
    trim_white(os.path.join(SRC, "film-knowledge", filename), p, 900)
    manifest["methods"][name] = "assets/images/methods/" + key + ".webp"

for slug, name in INDUSTRIES.items():
    d = os.path.join(OUT, "industries")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, slug + ".webp")
    save_webp(os.path.join(HERE, "appimg_src", name), p, 1200)
    manifest["industries"][slug] = "assets/images/industries/" + slug + ".webp"

os.makedirs(os.path.join(OUT, "banners"), exist_ok=True)
save_jpg(os.path.join(SRC, "company-image.jpg"), os.path.join(OUT, "banners", "company.jpg"), 1920)
save_jpg(os.path.join(SRC, "产品页-overview.jpg"), os.path.join(OUT, "banners", "产品页.jpg"), 1920)
save_jpg(os.path.join(HERE, "about-bg-source.jpg"), os.path.join(OUT, "banners", "about.jpg"), 1920)
manifest["banners"] = {"company": "assets/images/banners/company.jpg",
                       "products": "assets/images/banners/products.jpg",
                       "about": "assets/images/banners/about.jpg"}

json.dump(manifest, open(os.path.join(HERE, "images.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

total = 0
for dp, dn, fn in os.walk(OUT):
    for f in fn:
        total += os.path.getsize(os.path.join(dp, f))
print("图片 written:", sum(len(fn) for _, _, fn in os.walk(OUT)), "size %.1f MB" % (total / 1024 / 1024))
print("manifest: _build/images.json")
