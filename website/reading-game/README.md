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
- v6 (Nov 23): no trial booking. The result screen asks which weekly times suit (TIMES list in game.html,
  UAE time, multi-select) and saves them to Klaviyo preferred_class_times (+ X9QTYr, club_source
  "Reading game weekly times"). The confirmation screen shows the full price (AED 290, $79 for US time zones)
  and a "Book the seat" button (FOUNDING checkout link). Events: rg_pay_click; Meta ReadingGameTimesSent, ReadingGamePayClick.

Events (Hotjar + Shopify custom events): rg_start, rg_pass, rg_finished, rg_lead_view,
rg_lead_submit, rg_lead_skip, rg_result, rg_book_submit, rg_booked, rg_whatsapp, rg_share.
Meta custom events: ReadingGameLead, ReadingGameTrialBooked.

Audio: recorded clips go in `audio/<key>.mp3` (keys: l_ba l_ta l_mim l_sin w_bab w_qitt w_bayt s_cat p_ahsant p_labas; owner's voice, recorded Nov 10, split from one memo, loudness-normalized to -16 LUFS)
and the key is added to AUDIO_KEYS in game.html. Clips play first; the phone's Arabic voice is the
fallback (iPhone mutes it in silent mode, so a tip appears under the speaker).
Lead step fields: parent first name, email, child's first language. WhatsApp is asked at booking
with a country-code picker (guessed from the time zone, any country).

Hosting (Nov 10): jsDelivr refuses files from this repo at random because the repo is over its 50 MB
limit (product videos). So the live page loads everything from Shopify Files instead:
- clips: cdn.shopify.com/.../files/amf-rg-<key>.mp3 (copies of audio/*.mp3)
- script: a versioned copy of rg.js uploaded to Shopify Files (amf-reading-game-vN.js (current v5)); bump N on every change
  and update the script tag in the page body.
