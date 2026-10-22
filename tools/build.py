"""Builds every page of the Choi Dong Jin site (cdj.kr).  Run:  python3 tools/build.py

Edit the content here (works in WORKS, texts, contact), run it, then commit the generated HTML.
Text comes in pairs: t("English", "한국어").  Pressing L on the site switches language.
"""
import os, time
VER = time.strftime("%Y%m%d%H%M")
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- contact & links ----
EMAIL = "hello@cdj.kr"
BRAND = "Choi Dong Jin"
KO_SITE = "https://kindaofficial.xyz"   # the studio site
SITE_URL = "https://cdj.kr/"   # the site's address (share links: og:url, og:image)
ONE_LINE = "Choi Dong Jin is a Seoul-based furniture brand that connects people and space through light."
ONE_LINE_KO = "Choi Dong Jin은 빛으로 사람과 공간, 가구를 잇는 서울의 가구 브랜드입니다."
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%2300ff00'/%3E%3C/svg%3E"


def t(en, ko, tag="span", cls=""):
    """The same text in both languages; CSS shows the one that matches <html data-lang>."""
    c = f" {cls}" if cls else ""
    return f'<{tag} class="en{c}">{en}</{tag}><{tag} class="ko{c}" lang="ko">{ko}</{tag}>'


def head(r, title, desc, body_cls="", extra="", url=None):
    """url: the page's path under SITE_URL (for og:url); None leaves og:url out."""
    bc = f' class="{body_cls}"' if body_cls else ""
    og_url = f'<meta property="og:url" content="{SITE_URL}{url}">\n' if url is not None else ""
    return f'''<!doctype html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{extra}<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE_URL}{OG}">
{og_url}<link rel="icon" href="{FAVICON}">
<script>try{{var l=sessionStorage.getItem("site-lang");if(l){{document.documentElement.setAttribute("data-lang",l);document.documentElement.lang=l}}}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/site.css?v={VER}">
</head>
<body{bc}>
'''


def masthead(r, cur):
    items = [("object/", "Object", "오브젝트"),
             ("studio/", "Studio", "스튜디오"), ("records/", "Records", "기록")]
    AC = ' aria-current="page"'
    nav = "".join(f'<a href="{r}{h}"{AC if en == cur else ""}>{t(en, ko)}</a>' for h, en, ko in items)
    return f'''<header class="masthead">
  <a class="logo" href="{r or './'}" aria-label="{BRAND}, home">{BRAND}</a>
  <nav class="nav" aria-label="Main">{nav}</nav>
</header>
<main>
'''


def footer(r):
    return f'''</main>
<footer class="footer">
  <span class="copy">© {BRAND}, <span data-year>2026</span></span>
  <ul>
    <li><a href="{r}studio/">{t("About", "소개")}</a></li>
    <li><a href="mailto:{EMAIL}">{t("Contact", "문의")}</a></li>
    <li><a href="{KO_SITE}" target="_blank" rel="noopener">Kinda Official ↗</a></li>
  </ul>
  <div class="signup">
    <!-- To connect a newsletter service, set the form's action/method to its signup endpoint
         (e.g. Buttondown: action="https://buttondown.com/api/emails/embed-subscribe/USERNAME" method="post"). -->
    <form>
      <input name="email" type="email" placeholder="Newsletter — email" data-ph-en="Newsletter — email" data-ph-ko="뉴스레터 — 이메일" aria-label="Email for newsletter" required autocomplete="email">
      <button type="submit">{t("Subscribe", "구독")}</button>
    </form>
    <p class="result" role="status">{t("Thank you.", "감사합니다.")}</p>
  </div>
</footer>
<div class="lang-toast" aria-live="polite"></div>
<script src="{r}assets/js/site.js?v={VER}"></script>
</body>
</html>
'''


def write(path, html):
    p = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(html)


def facts(rows):
    """rows: (label_en, label_ko, value_en, value_ko); a value_ko of None reuses the English value."""
    out = []
    for a, ak, b, bk in rows:
        val = b if bk is None else t(b, bk)
        out.append(f"<tr><th>{t(a, ak)}</th><td>{val}</td></tr>")
    return '<table class="facts">' + "".join(out) + "</table>"


# ================= WORKS DATA (newest first) — add a new work here =================
# Each work lives in object/<slug>/ with its videos and a poster.jpg (the still shown before a video plays).
WORKS = [
    dict(slug="warmwelcome", title="Warm Welcome", year="2026",
         poster="poster.jpg", videos=["warmwelcome.mp4"],
         alt="Warm Welcome: a tall light-box coat stand by a wall; a coat hung on it becomes a dark silhouette against warm light."),
    dict(slug="yellowbox", title="Yellow Box", year="2026",
         poster="poster.jpg", videos=["yellowbox1.mp4", "yellowbox2.mp4"],
         alt="Yellow Box: a cube seat that glows warm yellow while someone sits on it."),
]
W = {w["slug"]: w for w in WORKS}
OG = "object/warmwelcome/poster.jpg"


def grid(r, works):
    return '<section class="grid">\n' + "".join(
        f'''  <a class="item" href="{w['slug']}/" data-video="{w['slug']}/{w['videos'][0]}">
    <div class="thumb"><img src="{w['slug']}/{w['poster']}" alt="{w['alt']}" loading="lazy"></div>
    <div class="cap">{w['title']}, {w['year']}</div>
  </a>
''' for w in works) + "</section>\n"


def video(src, poster, label, eager=False):
    return (f'<video src="{src}" autoplay muted loop playsinline preload="{"auto" if eager else "metadata"}" '
            f'poster="{poster}" aria-label="{label}"></video>')


# ================= HOME: one work fills the screen =================
r = ""
w = W["warmwelcome"]
write("index.html",
    head(r, BRAND, ONE_LINE, body_cls="home", url="")
    + masthead(r, "")
    + f'''<a class="cover" href="object/{w['slug']}/">
  {video(f"object/{w['slug']}/{w['videos'][0]}", f"object/{w['slug']}/{w['poster']}", w['alt'], eager=True)}
  <span class="cap">{w['title']}, {w['year']}</span>
</a>
'''
    + footer(r))

# ================= OBJECT: every work =================
r = "../"
write("object/index.html",
    head(r, f"Object — {BRAND}", f"Furniture by {BRAND}.", url="object/")
    + masthead(r, "Object")
    + f'<p class="intro">{BRAND} Object</p>\n'
    + grid(r, WORKS) + footer(r))


# ================= WORK PAGE (same order for every work) =================
def detail(w, body, rows=(), noindex=False):
    """body: (en_html, ko_html) · rows: facts() rows added before Exhibitions/Enquiries"""
    r = "../../"
    first, more = w["videos"][0], w["videos"][1:]
    all_rows = list(rows) + [
        ("Exhibitions", "전시", "First public showing to be announced.", "첫 공개 일정은 추후 안내합니다."),
        ("Enquiries", "문의", f'<a href="mailto:{EMAIL}?subject={w["title"]}">{EMAIL}</a>', None)]
    extra_videos = "".join(f'<section class="hero more">{video(v, w["poster"], w["alt"])}</section>\n' for v in more)
    desc = w["alt"]
    return (head(r, f"{w['title']}, {w['year']} — {BRAND}", desc,
                 extra='<meta name="robots" content="noindex">\n' if noindex else "",
                 url=f"object/{w['slug']}/")
        + masthead(r, "Object")
        + f'''<section class="hero">
  {video(first, w["poster"], w["alt"], eager=True)}
</section>

<section class="text">
  <div><h1>{w['title']}, {w['year']}</h1><div class="muted">{BRAND}</div></div>
  <div class="body">
    <div class="en">{body[0]}</div>
    <div class="ko" lang="ko">{body[1]}</div>
  </div>
</section>
{extra_videos}
<section class="text">
  <h2 class="muted">{t("Details", "정보")}</h2>
  <div class="body">{facts(all_rows)}</div>
</section>
'''
        + footer(r))


write("object/warmwelcome/index.html", detail(W["warmwelcome"],
    body=('''<p class="lead">A coat stand for the entrance.</p>
    <p>You come home and hang up the bag and coat you carried all day. You leave the social self you wore outside on the hook, and step into your own space.</p>
    <p>Standing at an adult’s height, it stops being a place to hang clothes and becomes a door into your own room. The coat left hanging becomes a silhouette: the shape of your body, standing in light.</p>''',
          '''<p class="lead">현관을 위한 코트걸이.</p>
    <p>집에 돌아와 하루 종일 들고 다닌 가방과 코트를 겁니다. 밖에서 입고 있던 사회적인 나를 고리에 걸어두고, 나만의 공간으로 들어섭니다.</p>
    <p>어른의 키만큼 서 있는 이것은 옷을 거는 곳이 아니라 내 방으로 들어가는 문이 됩니다. 걸어둔 코트는 실루엣이 됩니다. 빛 속에 서 있는 내 몸의 모양.</p>''')))

write("object/yellowbox/index.html", detail(W["yellowbox"],
    body=('''<p class="lead">It does not switch off when you get up.</p>
    <p>It stays on for exactly as long as you sat, then slowly fades. Sit for ten minutes, and ten minutes remain.</p>
    <p>What completes a room, in the end, is the person who was in it. Even after they leave, the room stays complete for a while. This afterglow is not a delay but a trace, exactly as long as someone stayed.</p>
    <p>In architecture, the chair defines the smallest relationship between body and space. This chair records it.</p>''',
          '''<p class="lead">일어나도 꺼지지 않습니다.</p>
    <p>앉아 있던 시간만큼 정확히 켜져 있다가, 천천히 사라집니다. 10분을 앉았다면 10분이 남습니다.</p>
    <p>결국 방을 완성하는 것은 그 안에 있던 사람입니다. 그 사람이 떠난 뒤에도 방은 한동안 완성된 채로 남습니다. 이 잔광은 지연이 아니라 흔적, 누군가 머문 시간만큼의 흔적입니다.</p>
    <p>건축에서 의자는 몸과 공간 사이의 가장 작은 관계를 정합니다. 이 의자는 그 관계를 기록합니다.</p>''')))

# The template page lives inside a work folder's sibling and borrows Warm Welcome's media as a stand-in.
tpl = detail(dict(slug="_template", title="Title", year="2027", poster="../warmwelcome/poster.jpg",
                  videos=["../warmwelcome/warmwelcome.mp4"], alt="Describe the piece"),
    body=('<p class="lead">One sentence on what the piece is.</p>\n    <p>Then what it does, and why.</p>',
          '<p class="lead">작품이 무엇인지 한 문장.</p>\n    <p>무엇을 하는지, 왜 그런지.</p>'),
    rows=[("Material", "재료", "…", "…"), ("Dimensions", "크기", "…", "…"), ("Edition", "에디션", "…", "…")],
    noindex=True)
tpl = tpl.replace("<title>", '<!-- TEMPLATE: put the videos and a poster.jpg in object/<slug>/, add the work to WORKS in tools/build.py,\n     write a detail() call for it, then run: python3 tools/build.py -->\n<title>', 1)
write("object/_template/index.html", tpl)

# ================= STUDIO =================
r = "../"
write("studio/index.html",
    head(r, f"Studio — {BRAND}", ONE_LINE, url="studio/")
    + masthead(r, "Studio")
    + f'''<section class="text">
  <h1>{t("Studio", "스튜디오")}</h1>
  <div class="body">
    {t(ONE_LINE, ONE_LINE_KO, "p", "lead")}
    <div class="en">
    <p>Choi Dong Jin is made in Seoul by art director Jin Choi, who leads the design, and WooChan Kim, who runs business and operations. The two also run the studio <a href="{KO_SITE}" target="_blank" rel="noopener">Kinda Official</a>.</p>
    <p>A room can be designed to look finished: correct, complete, official. Choi Dong Jin is interested in what makes it someone’s, the person who comes home, sits down and leaves a trace. The furniture notices that person and answers in light, so that a space begins to recognise the people inside it.</p>
    </div>
    <div class="ko" lang="ko">
    <p>Choi Dong Jin은 디자인을 이끄는 아트디렉터 최동진과 사업과 운영을 맡은 김우찬이 서울에서 만듭니다. 두 사람은 스튜디오 <a href="{KO_SITE}" target="_blank" rel="noopener">Kinda Official</a>도 함께 운영합니다.</p>
    <p>공간은 반듯하고 완성된, ‘공식적인’ 모습으로 설계될 수 있습니다. Choi Dong Jin은 그 공간을 누군가의 것으로 만드는 것, 집에 돌아오고, 앉고, 흔적을 남기는 사람에게 관심을 둡니다. 가구는 그 사람을 알아채고 빛으로 답해, 공간이 그 안의 사람을 알아보게 만듭니다.</p>
    </div>
  </div>
</section>

<section class="text">
  <h2 class="muted">{t("Contact", "연락처")}</h2>
  <div class="body">{facts([("General", "일반 문의", f'<a href="mailto:{EMAIL}">{EMAIL}</a>', None),
                            ("Collaborations", "협업", "Festivals, museums, galleries, collectors, brands and spaces", "페스티벌, 미술관, 갤러리, 컬렉터, 브랜드, 공간")])}</div>
</section>
'''
    + footer(r))

# ================= RECORDS =================
write("records/index.html",
    head(r, f"Records — {BRAND}", f"Exhibitions and press for {BRAND}.", url="records/")
    + masthead(r, "Records")
    + f'''<section class="text">
  <h1>{t("Exhibitions", "전시")}</h1>
  <div class="body muted">{t("None yet.", "아직 없습니다.")}</div>
</section>
<section class="text">
  <h1>{t("Press", "언론")}</h1>
  <div class="body">{t("None yet.", "아직 없습니다.", "p", "muted")}<p>{t("Press enquiries", "취재 문의")}: <a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
</section>
'''
    + footer(r))

# ================= 404 (root-absolute: served at any path) =================
r = "/"
write("404.html",
    head(r, f"Not found — {BRAND}", "This page does not exist.")
    + masthead(r, "")
    + f'<section class="void">{t("This page does not exist.", "요청하신 페이지가 없습니다.", "h1")}<a href="/">{t("Back to home", "홈으로")}</a></section>\n'
    + footer(r))
print("ok")
