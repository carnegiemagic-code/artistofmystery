#!/usr/bin/env python3
"""Builds artistofmystery.com: Dean Carnegie's paintings, as a gallery wall.

Rebuilt Oct 2026 from the old iWeb site (still on the hacked GoDaddy hosting). Only the paintings,
their titles and Dean's own gallery notes came across. Its own look on purpose (not the kids' sites).

Run:  python3 build.py   (copies images from ../artistofmystery-src/img and writes the pages)
Edit the words in INTRO / GALLERIES below. Edit painting titles in PAINTINGS.
House rules: no em dashes, no prices.
"""
import html
import json
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "artistofmystery-src")
SITE = "https://artistofmystery.com/"
EMAIL = "info@carnegiemagic.com"

# Old title from the iWeb feed -> (clean title, size, note). Duplicates across the old albums are listed once.
PAINTINGS = {
    "magic": [
        ("MagicArt-hhpaint4.jpg", "Houdini, Purple", "24 x 30", ""),
        ("MagicArt-IMG_0382.jpg", "Houdini in Chains", "16 x 20", ""),
        ("MagicArt-houdinistainedglass.jpg", "Houdini, Stained Glass", "16 x 20", ""),
        ("MagicArt-houdini-copy.jpg", "Houdini, Red", "22 x 28", ""),
        ("MagicArt-IMG_0950.jpg", "Houdini, Green", "", "Private collection"),
        ("MagicArt-youngharry.jpg", "Young Houdini", "", "Private collection"),
        ("MagicArt-dantesm.jpg", "Dante", "", "Private collection"),
        ("MagicArt-IMG_0949.jpg", "Dante, No Cigar!", "11 x 14", ""),
        ("MagicArt-cardinismall.jpg", "Cardini", "", "Private collection"),
        ("MagicArt-c1.jpg", "Cardini", "", "Private collection"),
        ("MagicArt-photochungsm.jpg", "Chung Ling Soo", "16 x 20", ""),
        ("MagicArt-thurston.jpg", "Thurston, Colors", "16 x 20", "Private collection"),
        ("MagicArt-Thurston2.jpg", "Thurston", "", "Private collection"),
        ("MagicArt-blackst.jpg", "Blackstone, Profile", "16 x 20", ""),
        ("MagicArt-b1.jpg", "Blackstone Sr.", "", "Not for sale"),
        ("MagicArt-herrmanndevil.jpg", "Herrmann and the Devil", "16 x 20", ""),
        ("MagicArt-kellarhat.jpg", "Harry Kellar", "", "Not for sale"),
        ("MagicArt-rh.jpg", "Robert-Houdin", "22 x 28", ""),
        ("MagicArt-devant.jpg", "David Devant", "16 x 20", ""),
        ("MagicArt-germpnt.jpg", "Karl Germain", "", ""),
        ("MagicArt-fumanchusmall.jpg", "Fu Manchu", "22 x 28", ""),
        ("MagicArt-legrand.jpg", "Marco the Magi", "", "Private collection"),
        ("MagicArt-lgd.jpg", "Le Grand David", "", "Private collection"),
        ("MagicArt-sly.jpg", "Slydini", "22 x 28", ""),
        ("MagicArt-rich.jpg", "Richiardi", "16 x 20", ""),
        ("MagicArt-henning.jpg", "Doug Henning", "22 x 28", ""),
        ("MagicArt-000_0191.jpg", "Henning, Caricature", "16 x 20", "Private collection"),
        ("MagicArt-000_0190.jpg", "Henning, Planets", "", "Private collection"),
        ("MagicArt-Copperfield.jpg", "Copperfield", "22 x 28", "Private collection"),
        ("MagicArt-davec2.jpg", "Copperfield", "", "Not for sale"),
        ("MagicArt-photo1.jpg", "Lance Burton", "", "Private collection"),
        ("MagicArt-lanceb.jpg", "Lance Burton, Blue", "", ""),
        ("MagicArt-pt.jpg", "Penn & Teller", "", "Private collection"),
        ("MagicArt-c-angel.jpg", "Criss Angel", "16 x 20", ""),
        ("NewArt-photo.jpg", "Cesareo Pelaez, Linking Rings", "", "Not for sale"),
        ("MagicArt-ballv.jpg", "Ball Vase", "11 x 14", "Private collection"),
        ("MagicArt-IMG_1098.jpg", "Matisse Vase", "11 x 14", "Private collection"),
        ("MagicArt-IMG_1099.jpg", "Matisse Split Vase", "11 x 14", ""),
        ("MagicArt-dachula.jpg", "Carnegie", "", "Not for sale"),
    ],
    "hats": [
        ("Hats-houdinihat1.jpg", "Houdini", "", "Not for sale"),
        ("Hats-IMG_0013.jpg", "Kellar", "", "Not for sale"),
        ("Hats-blackstonesmall.jpg", "Harry Blackstone Sr.", "", "Not for sale"),
        ("Hats-hermannsmall.jpg", "Alexander Herrmann", "", "Not for sale"),
        ("Hats-IMG_0006.jpg", "Harry Anderson", "", "Not for sale"),
    ],
    "beyond": [
        ("art2-poe.jpg", "Edgar Allan Poe", "", ""),
        ("art2-elvis2.jpg", "Elvis", "", "Private collection"),
        ("art2-lisa5_edited2.jpg", "Ukraine Girl", "", "Private collection"),
        ("art2-dla.jpg", "Lovely", "", "Private collection"),
        ("art2-boxers.jpg", "Boxers", "", "Private collection"),
        ("art2-IMG_0081-1.jpg", "Starstruck", "", "Private collection"),
        ("art2-bucket.jpg", "Buckethead", "", "Private collection"),
        ("art2-flowersforyou.jpg", "Flowers", "", "Private collection"),
        ("art2-IMG_0178_2.jpg", "Winter", "", "Private collection"),
        ("art2-abstractdac.jpg", "Abstract", "", ""),
        ("art2-beforeafter.jpg", "Fishbowl", "", ""),
        ("NewArt-IMG_1030a.jpg", "Butterfly", "", ""),
    ],
}

GALLERIES = [
    ("magic", "The Art of Magic",
     "Dean's paintings of the great magicians, in styles that run from abstract caricature to something closer "
     "to impressionism. The Cardini has appeared on the covers of three different magazines, and the Dante on two "
     "more and inside a third. The David Devant and Harry Blackstone Sr. both appear in the book <em>The Art of "
     "Deception</em>. Cesareo Pelaez performing the Linking Rings is done in a Cubist style, and the Lance Burton "
     "is Dean's take on an early publicity photo."),
    ("hats", "The Magic Hats",
     "A series of magicians in their hats, and every hat is different: Houdini, Kellar, Blackstone, Herrmann and "
     "Harry Anderson. None of the hat paintings are for sale."),
    ("beyond", "Beyond Magic",
     "Now and then Dean paints something that has nothing to do with magic. The oldest piece here is the Boxers, "
     "painted when he was in high school. The Ukraine Girl is the first in a series."),
]


def esc(s):
    return html.escape(s, quote=True)


def card(i, item, gallery):
    src, title, size, note = item
    label = " &middot; ".join(x for x in [esc(size) + " in." if size else "", esc(note)] if x)
    return (f'<figure class="work"><button class="frame" data-i="{i}" aria-label="View {esc(title)} larger">'
            f'<img src="img/{src}" alt="{esc(title)}, painting by Dean Carnegie" loading="lazy"></button>'
            f'<figcaption><span class="t">{esc(title)}</span>'
            + (f'<span class="m">{label}</span>' if label else "") + "</figcaption></figure>")


def build():
    os.makedirs(os.path.join(HERE, "img"), exist_ok=True)
    order, sections = [], []
    for key, name, text in GALLERIES:
        cards = []
        for item in PAINTINGS[key]:
            src = item[0]
            shutil.copy2(os.path.join(SRC, "img", src), os.path.join(HERE, "img", src))
            cards.append(card(len(order), item, key))
            order.append({"src": "img/" + src, "title": item[1], "meta": " · ".join(x for x in [item[2] + " in." if item[2] else "", item[3]] if x)})
        sections.append(f'<section class="gallery" id="{key}"><div class="wrap"><h2>{name}</h2>'
                        f'<p class="note">{text}</p><div class="wall">{"".join(cards)}</div></div></section>')
    shutil.copy2(os.path.join(SRC, "img", "MagicArt-hhpaint4.jpg"), os.path.join(HERE, "img", "share.jpg"))
    count = len(order)
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dean Carnegie | Paintings of Magic and Magicians</title>
<meta name="description" content="Original paintings by Dean Carnegie, the Artist of Mystery: Houdini, Cardini, Dante, Thurston, Kellar and the great magicians, in acrylic, watercolor and pen and ink.">
<link rel="canonical" href="{SITE}">
<meta property="og:title" content="Dean Carnegie | Paintings of Magic and Magicians">
<meta property="og:description" content="Original paintings of the great magicians by Dean Carnegie, the Artist of Mystery.">
<meta property="og:image" content="{SITE}img/share.jpg">
<meta property="og:url" content="{SITE}">
<meta property="og:type" content="website">
<link rel="icon" href="img/share.jpg">
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@type": "Person", "name": "Dean Carnegie",
             "alternateName": "The Artist of Mystery", "jobTitle": "Painter and magician",
             "url": SITE, "sameAs": ["https://carnegiemagic.com/", "https://art.carnegiemagic.com/",
                                     "https://themagicdetective.com/", "https://en.wikipedia.org/wiki/Dean_Carnegie"]})}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="top">
  <div class="wrap bar">
    <a class="mark" href="./">Dean Carnegie<span>The Artist of Mystery</span></a>
    <nav aria-label="Galleries"><a href="#magic">The Art of Magic</a><a href="#hats">Magic Hats</a><a href="#beyond">Beyond Magic</a><a href="#about">About</a></nav>
  </div>
</header>
<main>
<section class="hero">
  <div class="wrap hero-row">
    <div>
      <p class="eyebrow">Paintings</p>
      <h1>Magic and the magicians, in paint</h1>
      <p class="lede">Dean Carnegie is a magician, painter, author and magic historian. His paintings
      usually focus on the world of magic and the people who made it, with the occasional
      detour somewhere else entirely. Around a hundred paintings so far, most of them magicians.
      Here are {count} of them.</p>
    </div>
    <img class="hero-img" src="img/MagicArt-hhpaint4.jpg" alt="Houdini, Purple, painting by Dean Carnegie">
  </div>
</section>
{"".join(sections)}
<section class="about" id="about">
  <div class="wrap about-grid">
    <div>
      <h2>About the work</h2>
      <p>Most of the paintings are acrylic. There are also watercolors and some pen and ink drawings.
      Every piece is an original, not a copy and not a print. Dean's magic paintings have appeared on
      magazine covers, including <em>Elan</em> and <em>MAGIC</em>, and inside books on the history of magic.</p>
      <p>Some paintings are available, and Dean takes the occasional commission. To ask about a piece,
      email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div>
    <div class="links">
      <h3>More from Dean Carnegie</h3>
      <a href="https://art.carnegiemagic.com/">The Houdini paintings</a>
      <a href="https://carnegiemagic.com/">Carnegie, illusionist</a>
      <a href="https://themagicdetective.com/">The Magic Detective</a>
    </div>
  </div>
</section>
</main>
<footer class="foot"><div class="wrap">&copy; DAC Productions. All paintings and images &copy; Dean Carnegie. No reproduction without permission.</div></footer>

<div class="lightbox" hidden>
  <button class="lb-close" aria-label="Close">&times;</button>
  <button class="lb-prev" aria-label="Previous painting">&#8249;</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-next" aria-label="Next painting">&#8250;</button>
</div>
<script>
const works = {json.dumps(order)};
const lb = document.querySelector('.lightbox'), lbImg = lb.querySelector('img'), lbCap = lb.querySelector('figcaption');
let cur = 0;
function show(i) {{
  cur = (i + works.length) % works.length;
  const w = works[cur];
  lbImg.src = w.src; lbImg.alt = w.title;
  lbCap.innerHTML = '<span class="t"></span><span class="m"></span>';
  lbCap.querySelector('.t').textContent = w.title;
  lbCap.querySelector('.m').textContent = w.meta;
  lb.hidden = false; document.body.style.overflow = 'hidden';
}}
function close() {{ lb.hidden = true; document.body.style.overflow = ''; }}
document.querySelectorAll('.frame').forEach(b => b.addEventListener('click', () => show(+b.dataset.i)));
lb.querySelector('.lb-close').onclick = close;
lb.querySelector('.lb-prev').onclick = () => show(cur - 1);
lb.querySelector('.lb-next').onclick = () => show(cur + 1);
lb.addEventListener('click', e => {{ if (e.target === lb) close(); }});
document.addEventListener('keydown', e => {{
  if (lb.hidden) return;
  if (e.key === 'Escape') close();
  if (e.key === 'ArrowLeft') show(cur - 1);
  if (e.key === 'ArrowRight') show(cur + 1);
}});
</script>
</body>
</html>
"""
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)

    # old iWeb addresses -> the matching gallery on the new page
    old = {"ArtistofMystery/Welcome.html": "", "ArtistofMystery/Paintings/Paintings.html": "",
           "ArtistofMystery/Paintings/Pages/MagicArt.html": "#magic", "ArtistofMystery/Paintings/Pages/NewArt.html": "#magic",
           "ArtistofMystery/Paintings/Pages/Hats.html": "#hats", "ArtistofMystery/Paintings/Pages/art2.html": "#beyond"}
    for path, anchor in old.items():
        dest = os.path.join(HERE, path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        target = SITE + anchor
        with open(dest, "w") as f:
            f.write(f'<!doctype html><meta charset="utf-8"><title>Dean Carnegie Paintings</title>'
                    f'<link rel="canonical" href="{SITE}"><meta name="robots" content="noindex">'
                    f'<meta http-equiv="refresh" content="0; url={target}"><a href="{target}">Continue</a>')
    with open(os.path.join(HERE, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                f'<url><loc>{SITE}</loc></url></urlset>\n')
    with open(os.path.join(HERE, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
    print(f"built: {count} paintings")


if __name__ == "__main__":
    build()
