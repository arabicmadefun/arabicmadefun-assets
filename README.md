# Arabic Made Fun: listing images

Public product images for the Arabic Made Fun Shopify store, one folder per SKU.
Shopify copies these into Content > Files; the store uses the cdn.shopify.com copies.
Printable PDFs are never stored here.

## Pinterest pins

`pins/` holds the Pinterest pin images (1000 × 1500) and `pins/pinterest-bulk-upload.csv`.
They are made from `pinmaker/pins.csv` by `pinmaker/make_pins.py` using `pinmaker/template.html`.

**To add or change a pin:** edit a row in `pinmaker/pins.csv` on GitHub and commit.
The "Make Pinterest pins" action re-makes the images and the CSV within a few minutes.
Then download `pins/pinterest-bulk-upload.csv` and upload it in Pinterest (Create → Bulk create Pins).

Columns in `pins.csv`:
- `style`: product, bundle, ramadan or sampler (sets the button color)
- `headline`, `subline`, `cta`: the words on the pin
- `images`: one image path from this repo, or up to 3 separated by `|` for a bundle collage
- `link`: the Etsy listing or store page, without tracking tags (they are added for you).
  Leave it empty until the product is live; that pin is then left out of the upload CSV.
- `title`, `description`, `keywords`, `board`, `publish_date`: what Pinterest shows and when

Image URLs in the CSV point to
`https://raw.githubusercontent.com/arabicmadefun/arabicmadefun-assets/main/pins/`.
To use another host (GitHub Pages, Vercel), set the repo variable `PIN_BASE_URL`
or run `python3 pinmaker/make_pins.py --base <url>`.
