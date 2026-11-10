# Sami & Mya reading game

`rg.js` draws the whole game (styles, pictures, logic) into `<div id="amf-rg-mount">`
on the Shopify page `/pages/arabic-reading-game`. The page body only holds that div and a
`<script>` loading this file from jsDelivr, pinned to a commit.

To change the game: edit `rg.js`, commit, then point the page's script tag at the new commit hash.

Tracking: the "Book a free trial class" buttons go to `/pages/arabic-club#amf-book` with
`utm_campaign=reading_test`, `utm_source`/`utm_medium` copied from the game page's own URL
(default `reading_game`/`site`), and `utm_content` = `intro_link` or `result_<level>`.
Hotjar events: rg_start, rg_result, rg_club_click, rg_whatsapp, rg_share.
