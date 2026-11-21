"""Generate the static pages Discord reads before JavaScript runs."""

import json
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
BASE_URL = "https://thanksskeleton.github.io/mhanpc/"
STUDENTS = json.loads((ROOT / "students.json").read_text())


def page(student, url, relative_base, gm=False, gallery=False):
    title = "Masks MHA NPC Gallery" if gallery else f"{student['hero']} | MHA NPCs"
    description = (
        "Browse the Masks MHA NPC Gallery."
        if gallery else f"{student['real']} · {student['playbook']}\nPower: {student['power']}"
    )
    if gm and not gallery:
        description += f"\n{student['worst']} → {student['best']}"
    image = BASE_URL + "portraits/" + quote(student["portrait"])
    attr = lambda value: escape(value, quote=True)
    quotes = (
        '<p><span id="worst" style="color: red"></span> ===&gt; '
        '<span id="best" style="color: blue"></span></p>'
        if gm else ""
    )
    image_tags = "" if gallery else (
        f'  <meta property="og:image" content="{attr(image)}">\n'
        f'  <meta property="og:image:alt" content="{attr(student["hero"] + " portrait")}">\n'
    )
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <base href="{relative_base}">
  <title>{escape(title)}</title>
  <meta name="description" content="{attr(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{attr(url)}">
  <meta property="og:title" content="{attr(title)}">
  <meta property="og:description" content="{attr(description)}">
{image_tags.rstrip()}
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="data:,">
</head>
<body>
  <table width="100%">
    <tr>
      <td width="35%" valign="top">
        <form id="students"></form>
      </td>
      <td valign="top">
        <img id="portrait" height="600" alt="">
        <h1 id="hero"></h1>
        <p>Power: <span id="power"></span></p>
        <p>Name: <span id="real-name"></span></p>
        <p><i id="playbook"></i></p>
{('        ' + quotes) if quotes else ''}
      </td>
    </tr>
  </table>

  <script src="{'gm/' if gm else ''}students.js"></script>
  <script src="app.js"></script>
</body>
</html>
'''


(ROOT / "students.js").write_text(
    "window.students = " + json.dumps(
        [{key: value for key, value in student.items() if key not in ("worst", "best")}
         for student in STUDENTS], ensure_ascii=False
    ) + ";\n"
)
(ROOT / "index.html").write_text(page(STUDENTS[0], BASE_URL, "./", gallery=True))
directory = ROOT / "students"
directory.mkdir(exist_ok=True)
for student in STUDENTS:
    url = BASE_URL + "students/" + student["slug"] + ".html"
    (directory / (student["slug"] + ".html")).write_text(page(student, url, "../"))

spacer = ROOT / "X1"
spacer.mkdir(exist_ok=True)
(spacer / "index.html").write_text(page(STUDENTS[0], BASE_URL + "X1/", "../", gallery=True))
spacer_students = spacer / "students"
spacer_students.mkdir(exist_ok=True)
for student in STUDENTS:
    url = BASE_URL + "X1/students/" + student["slug"] + ".html"
    (spacer_students / (student["slug"] + ".html")).write_text(page(student, url, "../../"))

gm_directory = ROOT / "gm"
gm_directory.mkdir(exist_ok=True)
(gm_directory / "students.js").write_text(
    "window.students = " + json.dumps(STUDENTS, ensure_ascii=False) + ";\n"
)
(gm_directory / "index.html").write_text(page(STUDENTS[0], BASE_URL + "gm/", "../", gm=True))
gm_students = gm_directory / "students"
gm_students.mkdir(exist_ok=True)
for student in STUDENTS:
    url = BASE_URL + "gm/students/" + student["slug"] + ".html"
    (gm_students / (student["slug"] + ".html")).write_text(page(student, url, "../../", gm=True))
