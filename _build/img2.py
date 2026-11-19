p="_build/build.py"
s=open(p,encoding="utf-8").read()

s=s.replace('''    hero_html = """<section class="hero">''','''    hero_img = IMAGES.get("banners", {}).get("产品页", "")
    hero_style = ' style="--hero-img:url(\\'%s\\')"' % img_url(hero_img) if hero_img else ""
    hero_html = """<section class="hero hero-photo"%s>''' % "{HERO_STYLE}")
# Oops placeholder; handle below
s=s.replace('''    hero_html = """<section class="hero hero-photo"%s>''' % "{HERO_STYLE}"),''','''XX''')
open(p,"w",encoding="utf-8").write(s)
print("partial")
