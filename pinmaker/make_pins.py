#!/usr/bin/env python3
"""Make Pinterest pin images and the Pinterest bulk-upload CSV from pinmaker/pins.csv.

  python3 pinmaker/make_pins.py                 # all pins
  python3 pinmaker/make_pins.py --only p01,s01  # just these pins
  python3 pinmaker/make_pins.py --csv-only      # rebuild the CSV, keep images

Output:
  pins/amf-pin-<id>.jpg           1000x1500 images
  pins/pinterest-bulk-upload.csv  ready for Pinterest > Create > Bulk create
  (publish_date in pins.csv is US Eastern time; the CSV gets UTC, as Pinterest expects.
   Set PIN_TZ, e.g. PIN_TZ=Asia/Dubai, to use another time zone.)
Pins with an empty `link` (product not live yet) get an image but are left
out of the CSV, and are listed at the end of the run.
"""
import argparse, csv, html, os, sys, tempfile
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from urllib.parse import urlencode

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "pinmaker")
OUT = os.path.join(ROOT, "pins")
DEFAULT_BASE = "https://raw.githubusercontent.com/arabicmadefun/arabicmadefun-assets/main/pins/"
CAMPAIGN = "pins_nov26"
# publish_date in pins.csv is local time here; Pinterest wants UTC
LOCAL_TZ = ZoneInfo(os.environ.get("PIN_TZ") or "America/New_York")


def to_utc(local):
    dt = datetime.strptime(local, "%Y-%m-%dT%H:%M").replace(tzinfo=LOCAL_TZ)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def page_html(row, template):
    imgs = [p.strip() for p in row["images"].split("|") if p.strip()]
    for p in imgs:
        if not os.path.exists(os.path.join(ROOT, p)):
            sys.exit(f"{row['id']}: image not found: {p}")
    tags = "".join(f'<img src="{html.escape(os.path.join(ROOT, p))}">' for p in imgs)
    fill = {
        "style": row["style"],
        "headline": html.escape(row["headline"]),
        "subline": html.escape(row["subline"]),
        "cta": html.escape(row["cta"]),
        "images": tags,
        "cardclass": "multi" if len(imgs) > 1 else "",
    }
    out = template
    for k, v in fill.items():
        out = out.replace("{{" + k + "}}", v)
    return out


def render(rows):
    from playwright.sync_api import sync_playwright
    template = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1000, "height": 1500})
        for row in rows:
            # written next to template.html so fonts/ resolves
            with tempfile.NamedTemporaryFile("w", suffix=".html", dir=HERE, delete=False, encoding="utf-8") as f:
                f.write(page_html(row, template))
                tmp = f.name
            try:
                page.goto("file://" + tmp)
                page.evaluate("document.fonts.ready")
                page.wait_for_load_state("networkidle")
                dest = os.path.join(OUT, f"amf-pin-{row['id']}.jpg")
                page.screenshot(path=dest, type="jpeg", quality=88)
                print("made", os.path.relpath(dest, ROOT))
            finally:
                os.remove(tmp)
        browser.close()


def tracked(link, pin_id):
    q = urlencode({"utm_source": "pinterest", "utm_medium": "organic",
                   "utm_campaign": CAMPAIGN, "utm_content": pin_id})
    return link + ("&" if "?" in link else "?") + q


def write_csv(rows, base):
    base = base.rstrip("/") + "/"
    dest = os.path.join(OUT, "pinterest-bulk-upload.csv")
    waiting = []
    with open(dest, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Title", "Media URL", "Pinterest board", "Thumbnail", "Description",
                    "Link", "Publish date", "Keywords"])
        for r in rows:
            if not r["link"].strip():
                waiting.append(r)
                continue
            w.writerow([r["title"], f"{base}amf-pin-{r['id']}.jpg", r["board"], "",
                        r["description"], tracked(r["link"].strip(), r["id"]),
                        to_utc(r["publish_date"]), r["keywords"]])
    print(f"\nwrote {os.path.relpath(dest, ROOT)}: {len(rows) - len(waiting)} pins")
    if waiting:
        print("not in the CSV yet (no link, product not live):")
        for r in waiting:
            print(f"  {r['id']}  {r['publish_date']}  {r['sku']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated pin ids to render")
    ap.add_argument("--csv-only", action="store_true", help="skip images, rebuild the CSV")
    ap.add_argument("--base", default=os.environ.get("PIN_BASE_URL") or DEFAULT_BASE,
                    help="public URL of the pins/ folder")
    a = ap.parse_args()
    rows = list(csv.DictReader(open(os.path.join(HERE, "pins.csv"), encoding="utf-8")))
    rows.sort(key=lambda r: (r["publish_date"], r["id"]))
    if not a.csv_only:
        pick = set(a.only.split(",")) if a.only else None
        render([r for r in rows if pick is None or r["id"] in pick])
    write_csv(rows, a.base)


if __name__ == "__main__":
    main()
