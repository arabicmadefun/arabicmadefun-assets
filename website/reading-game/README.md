# Sami & Mya reading game

`rg.js` draws the whole game (styles, pictures, logic) into `<div id="amf-rg-mount">`
on the Shopify page `/pages/arabic-reading-game`. The page body only holds that div and a
`<script>` loading this file from jsDelivr, pinned to a commit.

To change the game: edit `rg.js`, commit, then point the page's script tag at the new commit hash.

Source: `game.html` (page markup, styles and script, with {{PLACEHOLDERS}} for pictures) and
`parts.json` (the pictures). Run `python3 build.py` to rebuild `rg.js`.

Flow: age + optional child name → letters → words → sentence (each card has Pass; a child who
reads fewer than 2 letters or 2 words skips the harder rounds) → tracing (with Pass) →
"checking" moment → lead step (parent name, email, optional WhatsApp; skippable) → result +
in-page trial booking → confirmation.

Data:
- Lead step: Klaviyo profile (reading_level, reading_scores, child_age, child_name, whatsapp,
  rg_utm_*) + subscription to its own list RCTUtB "Reading Test leads (Sami & Mya game)"
  (custom_source "Reading game"). No flow on that list yet.
- Booking: same as the Arabic Club form: Klaviyo profile with the club fields (trial_class,
  child_name, child_age, whatsapp, arabic_at_home, parent_time_zone, club_booked_at,
  club_source "Reading game booking", club_utm_source/medium, club_utm_campaign=reading_test,
  club_utm_content=game_<level>) + subscription to X9QTYr, then the store contact form
  (so the owner gets the usual email) which returns to the page with ?contact_posted=true.
- Trial dates live in the DATES list in game.html; values must match the club page's options.

Events (Hotjar + Shopify custom events): rg_start, rg_pass, rg_finished, rg_lead_view,
rg_lead_submit, rg_lead_skip, rg_result, rg_book_submit, rg_booked, rg_whatsapp, rg_share.
Meta custom events: ReadingGameLead, ReadingGameTrialBooked.

Audio: recorded clips go in `audio/<key>.mp3` (keys: l_ba l_ta l_mim l_sin w_bab w_qitt w_bayt s_cat)
and the key is added to AUDIO_KEYS in game.html. Clips play first; the phone's Arabic voice is the
fallback (iPhone mutes it in silent mode, so a tip appears under the speaker).
Lead step fields: parent first name, email, child's first language. WhatsApp is asked at booking
with a country-code picker (guessed from the time zone, any country).
