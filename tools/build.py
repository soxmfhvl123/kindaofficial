"""Builds every page of kindaofficial.xyz.  Run:  python3 tools/build.py

Edit the content here (works in WORKS, texts, contact), run it, then commit the generated HTML.
Text comes in pairs: t("English", "한국어").  Pressing L on the site switches language.
"""
import os, time
VER = time.strftime("%Y%m%d%H%M")
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- contact & links ----
EMAIL = "hello@kindaofficial.com"   # placeholder — replace with the real address
INSTA = "kindaofficial_official"
LIVE = "https://soxmfhvl123.github.io/dataism/"
FC = "https://fakechurch.xyz"
ONE_LINE = "Kinda Official is a Seoul-based duo turning data into light and space, to show where people stand among machines."
ONE_LINE_KO = "Kinda Official은 데이터를 빛과 공간으로 바꿔, 기술 속 사람의 자리를 보여주는 서울의 2인 스튜디오입니다."
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%2300ff00'/%3E%3C/svg%3E"
IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 3.3.1 4.8 1.7 4.9 4.9.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 3.2-1.7 4.8-4.9 4.9-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-3.3-.1-4.8-1.7-4.9-4.9C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8C2.4 3.9 3.9 2.4 7.2 2.3 8.4 2.2 8.8 2.2 12 2.2zM12 0C8.7 0 8.3 0 7.1.1 2.7.3.3 2.7.1 7.1 0 8.3 0 8.7 0 12s0 3.7.1 4.9c.2 4.4 2.6 6.8 7 7 1.2.1 1.6.1 4.9.1s3.7 0 4.9-.1c4.4-.2 6.8-2.6 7-7 .1-1.2.1-1.6.1-4.9s0-3.7-.1-4.9c-.2-4.4-2.6-6.8-7-7C15.7 0 15.3 0 12 0zm0 5.8a6.2 6.2 0 1 0 0 12.4 6.2 6.2 0 0 0 0-12.4zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.8a1.4 1.4 0 1 0 0 2.9 1.4 1.4 0 0 0 0-2.9z"/></svg>'


def t(en, ko, tag="span", cls=""):
    """The same text in both languages; CSS shows the one that matches <html data-lang>."""
    c = f" {cls}" if cls else ""
    return f'<{tag} class="en{c}">{en}</{tag}><{tag} class="ko{c}" lang="ko">{ko}</{tag}>'


def head(r, title, desc, body_cls="", extra=""):
    bc = f' class="{body_cls}"' if body_cls else ""
    return f'''<!doctype html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{extra}<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{r}assets/img/dataism-render.jpg">
<link rel="icon" href="{FAVICON}">
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
  <a class="logo" href="{r or './'}" aria-label="Kinda Official, home"><i>kinda</i> Official</a>
  <nav class="nav" aria-label="Main">{nav}</nav>
  <div class="social"><a href="https://instagram.com/{INSTA}" target="_blank" rel="noopener" aria-label="Instagram">{IG}</a></div>
</header>
<main>
'''


def footer(r):
    return f'''</main>
<footer class="footer">
  <span class="copy">© Kinda Official, <span data-year>2026</span></span>
  <ul>
    <li><a href="{r}studio/">{t("About", "소개")}</a></li>
    <li><a href="mailto:{EMAIL}">{t("Contact", "문의")}</a></li>
    <li><a href="https://instagram.com/{INSTA}" target="_blank" rel="noopener">Instagram</a></li>
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


DATAISM_ALT = "Dataism: a cross-shaped LED installation glowing in a dark room, its panels filled with live text and numbers."

# ================= WORKS DATA (newest first) — add a new work here =================
# video: optional path to a short muted clip; it plays when the thumbnail is hovered.
WORKS = [
    dict(slug="dataism", title="Dataism", year="2026", part=("FAKE CHURCH", "FAKE CHURCH"),
         img="dataism-render.jpg", alt=DATAISM_ALT, video=""),
]
W = {w["slug"]: w for w in WORKS}


def grid(r, works, base):
    return '<section class="grid">\n' + "".join(
        f'''  <a class="item" href="{base}{w['slug']}/"{f' data-video="{w["video"]}"' if w.get("video") else ""}>
    <div class="thumb"><img src="{r}assets/img/{w['img']}" alt="{w['alt']}" loading="lazy"></div>
    <div class="cap">{w['title']}, {w['year']}</div>
  </a>
''' for w in works) + "</section>\n"


# ================= HOME: one work fills the screen =================
r = ""
write("index.html",
    head(r, "Kinda Official", ONE_LINE, body_cls="home")
    + masthead(r, "")
    + f'''<a class="cover" href="object/dataism/">
  <video src="assets/video/dataism.mp4" autoplay muted loop playsinline preload="auto" poster="assets/img/dataism-render.jpg" aria-label="{DATAISM_ALT}"></video>
  <span class="cap">Dataism, 2026</span>
</a>
'''
    + footer(r))

# ================= OBJECT: every work =================
r = "../"
write("object/index.html",
    head(r, "Object — Kinda Official", "Kinda Official Object.")
    + masthead(r, "Object")
    + '<p class="intro">Kinda Official Object</p>\n'
    + grid(r, WORKS, "") + footer(r))


# ================= WORK PAGE (same order for every work) =================
def detail(w, lead, body, rows, photos=(), extra="", links=(), credits=()):
    """lead: (en, ko) · body: (en_html, ko_html) · rows/credits: facts() rows · links: (name_en, name_ko, url)"""
    r = "../../"
    imgs = ""
    if photos:
        imgs = '<section class="images">' + "".join(f'<img src="../../assets/img/{s}" alt="{a}" loading="lazy">' for s, a in photos) + "</section>\n"
    all_rows = list(rows) + [
        ("Exhibitions", "전시", "First public showing to be announced.", "첫 공개 일정은 추후 안내합니다."),
        ("Enquiries", "문의", f'<a href="mailto:{EMAIL}?subject={w["title"]}">{EMAIL}</a>', None)]
    all_rows += list(credits)
    if links:
        en = " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{n} ↗</a>' for n, _, u in links)
        ko = " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{k} ↗</a>' for _, k, u in links)
        all_rows.append(("Links", "링크", en, ko))
    return (head(r, f"{w['title']}, {w['year']} — Kinda Official", f"{w['title']}, {w['year']}. {lead[0]}")
        + masthead(r, "Object")
        + f'''<section class="hero">
  <!-- Documentation video, 1–2 min: swap the <img> for <video controls> or a Vimeo <iframe> when filmed. -->
  <img src="../../assets/img/{w['img']}" alt="{w['alt']}" fetchpriority="high">
</section>

<section class="text">
  <div><h1>{w['title']}, {w['year']}</h1><div class="muted">{t(*w['part'])}</div></div>
  <div class="body">
    {t(lead[0], lead[1], "p", "lead")}
    <div class="en">{body[0]}</div>
    <div class="ko" lang="ko">{body[1]}</div>
  </div>
</section>
{extra}{imgs}
<section class="text">
  <h2 class="muted">{t("Details", "정보")}</h2>
  <div class="body">{facts(all_rows)}</div>
</section>
'''
        + footer(r))


write("object/dataism/index.html", detail(W["dataism"],
    lead=("An installation that receives AI activity from around the world in real time and inscribes it on a cross of LEDs.",
          "전 세계의 AI 활동을 실시간으로 받아 십자가 모양 LED에 새기는 설치 작품."),
    body=('''<p>It starts from an observation: more and more of our judgment is handed to machines, and the line between what we decide and what is decided for us grows faint. Dataism makes that handover visible as worship.</p>
    <p>Twelve live feeds run across sixteen LED panels: which AI services are up or down, how many commits were written with AI in the last minute, which models were released today, what people are saying about them. Nothing is pre-recorded. It is the altar of <a href="https://fakechurch.xyz" target="_blank" rel="noopener">FAKE CHURCH</a>.</p>''',
          '''<p>이 작업은 하나의 관찰에서 시작합니다. 우리는 점점 더 많은 판단을 기계에 맡기고, 내가 정한 것과 나를 대신해 정해진 것의 경계는 흐려집니다. Dataism은 그 넘겨줌을 예배의 모습으로 드러냅니다.</p>
    <p>16장의 LED 패널 위로 실시간 데이터 12종이 흐릅니다. 어떤 AI 서비스가 켜지고 꺼졌는지, 지난 1분 동안 AI와 함께 쓴 커밋이 몇 개인지, 오늘 어떤 모델이 공개됐는지, 사람들이 그것에 대해 무엇을 말하는지. 미리 녹화된 것은 없습니다. <a href="https://fakechurch.xyz" target="_blank" rel="noopener">FAKE CHURCH</a>의 제단입니다.</p>'''),
    rows=[
        ("Medium", "매체", "LED panels, computer, custom software, live data", "LED 패널, 컴퓨터, 자체 제작 소프트웨어, 실시간 데이터"),
        ("Form", "형태", "Cross, 6 × 12 units", "십자가, 6 × 12 단위"),
        ("Display", "디스플레이", "16 LED panels, 172 × 86 px each · 516 × 1032 px total", "LED 패널 16장, 장당 172 × 86 px · 전체 516 × 1032 px"),
        ("Dimensions", "크기", "To be confirmed with the physical piece", "실물 제작 후 확정"),
        ("Data", "데이터", '''12 public live feeds<ul>
      <li>AI service status: OpenAI, Claude, GitHub, Cursor, Cloudflare</li>
      <li>GitHub commits co-authored with Claude and Copilot</li>
      <li>Hugging Face new and trending models</li>
      <li>Hacker News · OpenRouter · Bluesky · Wikipedia edits</li>
      <li>UK grid carbon intensity</li>
    </ul>''', '''공개 실시간 데이터 12종<ul>
      <li>AI 서비스 상태: OpenAI, Claude, GitHub, Cursor, Cloudflare</li>
      <li>Claude, Copilot과 함께 쓴 GitHub 커밋</li>
      <li>Hugging Face 신규·인기 모델</li>
      <li>Hacker News · OpenRouter · Bluesky · 위키백과 편집</li>
      <li>영국 전력망 탄소 집약도</li>
    </ul>'''),
        ("Installation", "설치", "Mains power, network connection. Leans against or mounts on a wall.", "상시 전원, 인터넷 연결. 벽에 기대거나 벽에 부착."),
        ("Operation", "운영", "Runs continuously, no operator", "상시 가동, 운영 인력 불필요"),
    ],
    credits=[("Credits", "크레딧", "Concept, design, code: Kinda Official", "콘셉트, 디자인, 코드: Kinda Official")],
    links=[("Dataism live", "Dataism 라이브", LIVE), ("fakechurch.xyz", "fakechurch.xyz", FC)],
    extra=f'''
<div class="live">
  <iframe src="{LIVE}" title="Dataism live feed" loading="lazy"></iframe>
  <button type="button" data-interact>{t("Interact", "조작하기")}</button>
</div>
<p class="live-cap">{t("Live — the software that runs on the cross, running in your browser now.", "라이브 — 십자가에서 돌아가는 소프트웨어가 지금 이 브라우저에서 돌아가고 있습니다.")}</p>
'''))

tpl = detail(dict(slug="_template", title="Title", year="2027", part=("Project name or Kinda Official Object", "프로젝트명 또는 Kinda Official Object"),
                  img="dataism-render.jpg", alt="Describe the image"),
    lead=("One or two sentences on what the work is.", "작품이 무엇인지 한두 문장."),
    body=("<p>The observation it starts from, then how it works.</p>", "<p>출발한 관찰, 그리고 작동 방식.</p>"),
    rows=[("Material", "재료", "…", "…"), ("Dimensions", "크기", "…", "…"),
          ("Data / sensors", "데이터·센서", "…", "…"), ("Power &amp; installation", "전원·설치", "…", "…")])
tpl = tpl.replace("<title>", '<meta name="robots" content="noindex">\n<!-- TEMPLATE: add the work to WORKS in tools/build.py and write a detail() call for it, then run the script.\n     Object pieces: add dimensions, weight and edition size to Details. -->\n<title>', 1)
write("object/_template/index.html", tpl)

# ================= STUDIO =================
r = "../"
write("studio/index.html",
    head(r, "Studio — Kinda Official", ONE_LINE)
    + masthead(r, "Studio")
    + f'''<section class="text">
  <h1>{t("Studio", "스튜디오")}</h1>
  <div class="body">
    {t(ONE_LINE, ONE_LINE_KO, "p", "lead")}
    <div class="en">
    <p>Kinda Official was founded in Seoul by art director Jin Choi, who leads the creative work, and WooChan Kim, who runs business and operations.</p>
    <p>The name holds the question behind every work. More and more, the official answers come from machines, down to what we choose. Kinda Official looks at what those answers leave out: the place where people still stand.</p>
    </div>
    <div class="ko" lang="ko">
    <p>Kinda Official은 작업 전체를 이끄는 아트디렉터 최동진과 사업과 운영을 맡은 김우찬이 서울에서 시작한 2인 스튜디오입니다.</p>
    <p>이름에는 모든 작업의 질문이 담겨 있습니다. 오늘날 공식적인 답은 점점 기계가 정합니다. 우리가 무엇을 고를지까지도요. Kinda Official은 그 답이 미처 닿지 않는 곳, 여전히 사람이 서 있는 자리를 들여다봅니다.</p>
    </div>
  </div>
</section>

<section class="text">
  <h2 class="muted">{t("Contact", "연락처")}</h2>
  <div class="body">{facts([("General", "일반 문의", f'<a href="mailto:{EMAIL}">{EMAIL}</a>', None),
                            ("Instagram", "Instagram", f'<a href="https://instagram.com/{INSTA}" target="_blank" rel="noopener">@{INSTA}</a>', None),
                            ("Collaborations", "협업", "Festivals, museums, galleries, collectors, brands and spaces", "페스티벌, 미술관, 갤러리, 컬렉터, 브랜드, 공간")])}</div>
</section>
'''
    + footer(r))

# ================= RECORDS =================
write("records/index.html",
    head(r, "Records — Kinda Official", "Exhibitions and press for Kinda Official.")
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
    head(r, "Not found — Kinda Official", "This page does not exist.")
    + masthead(r, "")
    + f'<section class="void">{t("This page does not officially exist.", "요청하신 페이지는 공식적으로 존재하지 않습니다.", "h1")}<a href="/">{t("Back to home", "홈으로")}</a></section>\n'
    + footer(r))
print("ok")
