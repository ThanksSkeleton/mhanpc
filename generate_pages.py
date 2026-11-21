"""Generate the static pages Discord reads before JavaScript runs."""

import json
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
BASE_URL = "https://thanksskeleton.github.io/mhanpc/"
STUDENTS = json.loads((ROOT / "students.json").read_text())


def page(student, url, relative_base):
    title = f"{student['hero']} | MHA NPCs"
    description = (
        f"{student['real']} · {student['playbook']}\n"
        f"Power: {student['power']}\n"
        f"{student['worst']} → {student['best']}"
    )
    image = BASE_URL + "portraits/" + quote(student["portrait"])
    attr = lambda value: escape(value, quote=True)
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
  <meta property="og:image" content="{attr(image)}">
  <meta property="og:image:alt" content="{attr(student['hero'] + ' portrait')}">
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
        <img id="portrait" height="300" alt="">
        <h1 id="hero"></h1>
        <p>Power: <span id="power"></span></p>
        <p>Name: <span id="real-name"></span></p>
        <p><i id="playbook"></i></p>
        <p><span id="worst" style="color: red"></span> ===&gt; <span id="best" style="color: blue"></span></p>
      </td>
    </tr>
  </table>

  <script src="students.js"></script>
  <script src="app.js"></script>
</body>
</html>
'''


(ROOT / "students.js").write_text("window.students = " + json.dumps(STUDENTS, ensure_ascii=False) + ";\n")
(ROOT / "index.html").write_text(page(STUDENTS[0], BASE_URL, "./"))
directory = ROOT / "students"
directory.mkdir(exist_ok=True)
for student in STUDENTS:
    url = BASE_URL + "students/" + student["slug"] + ".html"
    (directory / (student["slug"] + ".html")).write_text(page(student, url, "../"))
