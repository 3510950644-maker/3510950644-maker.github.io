# -*- coding: utf-8 -*-
"""Static checks for the bilingual site: links, ids, media, tag balance, toggle."""
import glob, os, re
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
files = sorted(glob.glob("*.html")) + sorted(glob.glob(os.path.join("en", "*.html")))
docs, ids = {}, {}
for f in files:
    s = BeautifulSoup(open(f, encoding="utf-8").read(), "html.parser")
    docs[f] = s
    key = f.replace("\\", "/")
    ids[key] = [x.get("id") for x in s.find_all(id=True)]

broken = []
for f, s in docs.items():
    base_dir = os.path.dirname(f)
    for a in s.find_all("a", href=True):
        h = a["href"].strip()
        if h.startswith(("http://", "https://", "mailto:", "tel:", "javascript:")):
            continue
        path, _, frag = h.partition("#")
        target = os.path.normpath(os.path.join(base_dir, path)) if path else f
        target = target.replace("\\", "/")
        if path and not os.path.exists(target):
            broken.append((f, h, "missing file"))
        elif frag:
            tids = ids.get(target.replace("\\", "/"), [])
            if frag not in tids:
                broken.append((f, h, "missing anchor"))

dup = {f: {i for i in ids[f.replace(chr(92), '/')] if ids[f.replace(chr(92), '/')].count(i) > 1} for f in files}
media = {f: len(docs[f].find_all("iframe")) for f in files}
media = {f: n for f, n in media.items() if n}
视频 = {f: len(docs[f].find_all("video")) for f in files}
视频 = {f: n for f, n in 视频.items() if n}

missing_图片 = []
for f, s in docs.items():
    base = os.path.dirname(f)
    for img in s.find_all("img", src=True):
        src = img["src"].strip()
        if src.startswith(("http://", "https://", "data:")):
            continue
        target = os.path.normpath(os.path.join(base, src)).replace("\\", "/")
        if not os.path.exists(target):
            missing_图片.append((f, src))
    for el in s.select("[style*=background-image]"):
        for src in re.findall(r"url\(['\"]?([^'\")]+)", el.get("style", "")):
            if src.startswith(("http://", "https://", "data:")):
                continue
            target = os.path.normpath(os.path.join(base, src)).replace("\\", "/")
            if not os.path.exists(target):
                missing_图片.append((f, src))

# language toggle pairing
toggle_bad = []
for f in files:
    a = docs[f].select_one(".lang-toggle")
    if not a:
        toggle_bad.append((f, "no toggle"))
        continue
    h = a["href"]
    target = os.path.normpath(os.path.join(os.path.dirname(f), h)).replace("\\", "/")
    if not os.path.exists(target):
        toggle_bad.append((f, h))

# structural tag balance
void = {"br", "img", "input", "meta", "link", "hr", "source", "area", "base", "col",
        "embed", "param", "track", "wbr"}
issues = []
for f in files:
    s = open(f, encoding="utf-8").read()
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<(script|style)\b.*?</\1>", "", s, flags=re.S | re.I)
    stack = []
    for m in re.finditer(r"<(/?)([a-zA-Z][a-zA-Z0-9-]*)\b([^>]*)>", s):
        closing, name, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if name in void or attrs.rstrip().endswith("/"):
            continue
        if not closing:
            stack.append(name)
        elif stack and stack[-1] == name:
            stack.pop()
        elif name in stack:
            while stack and stack[-1] != name:
                stack.pop()
            stack.pop()
        else:
            issues.append((f, name, "stray close"))
    if stack:
        issues.append((f, stack[-1], "unclosed"))

print("html pages:", len(files), "(zh %d / en %d)" % (len(glob.glob("*.html")), len(glob.glob("en/*.html"))))
print("broken internal links:", len(broken))
for b in broken[:12]:
    print("  ", b)
print("pages with duplicate ids:", {k: v for k, v in dup.items() if v})
print("pages with iframe:", media)
print("pages with video:", 视频)
print("missing image files:", len(missing_图片))
for m in missing_图片[:12]:
    print("  ", m)
print("language toggle problems:", toggle_bad)
print("tag balance issues:", len(issues))
for x in issues[:12]:
    print("  ", x)
