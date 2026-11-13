"""Build the reading game scripts. Run: python3 build.py
game.html    -> rg.js     (English, /pages/arabic-reading-game)
game-fr.html -> rg-fr.js  (French + Texte level, /pages/jeu-de-lecture-arabe)
Pictures come from parts.json ({{PLACEHOLDERS}})."""
import json, pathlib, re
here = pathlib.Path(__file__).parent
parts = json.loads((here / "parts.json").read_text())
# French class picture: same drawing, French labels
parts["CLASS_SVG_FR"] = (parts["CLASS_SVG"]
    .replace("Arabic Made Fun Club · Week 1", "Arabic Made Fun · Groupe FR")
    .replace(">Teacher<", ">Prof<"))

def build(src_name, out_name, page):
    src = (here / src_name).read_text()
    for k, v in parts.items():
        src = src.replace("{{" + k + "}}", v)
    assert "{{" not in src, "unfilled placeholder in " + src_name
    m = re.search(r"<script>(.*)</script>", src, re.S)
    markup, js = src[:m.start()], m.group(1)
    markup = re.sub(r">\s+<", "><", markup)
    out = ("/* Arabic Made Fun: Sami & Mya reading game for " + page + ". Built from " + src_name + " by build.py. */\n"
           "(function(){var mt=document.getElementById('amf-rg-mount');if(!mt)return;mt.innerHTML=" + json.dumps(markup, ensure_ascii=False) + ";\n" + js + "\n})();\n")
    (here / out_name).write_text(out)
    print(out_name, len(out), "chars")

build("game.html", "rg.js", "/pages/arabic-reading-game")
build("game-fr.html", "rg-fr.js", "/pages/jeu-de-lecture-arabe")
