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

v7 (Nov 23, Marya's feedback): age is a dropdown 4–12; progress bar shows labelled steps
(Letters · Words · Sentence · Tracing · Result, hidden on the start screen); no speech bubbles on the
game screens; smaller letter, picture and speaker button so each step fits one phone screen; tracing
board 10:7 with the letter sized from its real bounds (no empty space under it). Tracing goes letter by
letter (ب ت م س): a letter passes at ~85% coverage and moves on by itself (no Finish button); going off
the letter shows "Oops! Let's try again" and the board clears itself; Pass skips one letter; after the
last letter the game moves on to the result. reading_scores now include "Traced x/4".

v8 (Nov 23, Marya's feedback): two new steps built from the AMF workbooks. "Joined letters" (from Letter
Shapes + Split & Join): ـبـ and ـجـ (which letter?), جَمَل (which letters?), و + ل + د (which word?).
"Vocabulary" (from the picture flashcards): sun, book, moon, pencil, car → choose the Arabic word.
Tap answers (3 shuffled options + "I don't know"); wrong answers show the right one. Order: Letters →
Joined → Words → Sentence → Vocab → Tracing → Result (children who read fewer than 2 letters go straight
to tracing; fewer than 2 words skips the sentence). Level: Words group now also needs 2/4 joined letters.
Vocabulary is reported, not used for the level. Tracing is stricter: ~95% of the letter AND every piece
(body, each dot) 80% covered before "Bravo" ("Almost! Don't forget the dot."). The instruction line above
the board is one fixed line so the board never moves while tracing.

v9 (Nov 23): "Story" step for strong readers (same two texts as the French game), only after the sentence
is read: a vowelled story, then one without vowels, each with an Arabic question and 3 answers.
New levels: Readers group (1/2 stories) and Confident readers group (2/2). Result: the Sentence box shows
"Story x/2" when the stories were played. reading_scores add "Story x/2".
