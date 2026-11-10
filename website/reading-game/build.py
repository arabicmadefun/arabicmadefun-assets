"""Build rg.js from game.html + parts.json (pictures). Run: python3 build.py"""
import json, pathlib, re
here = pathlib.Path(__file__).parent
src = (here / "game.html").read_text()
parts = json.loads((here / "parts.json").read_text())
for k, v in parts.items():
    src = src.replace("{{" + k + "}}", v)
assert "{{" not in src, "unfilled placeholder"
m = re.search(r"<script>(.*)</script>", src, re.S)
markup, js = src[:m.start()], m.group(1)
markup = re.sub(r">\s+<", "><", markup)
out = ("/* Arabic Made Fun: Sami & Mya reading game for /pages/arabic-reading-game. Built from game.html by build.py. */\n"
       "(function(){var mt=document.getElementById('amf-rg-mount');if(!mt)return;mt.innerHTML=" + json.dumps(markup, ensure_ascii=False) + ";\n" + js + "\n})();\n")
(here / "rg.js").write_text(out)
print("rg.js", len(out), "chars")
