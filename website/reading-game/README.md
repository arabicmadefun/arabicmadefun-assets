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

## French version (Nov 13, 2026)
`game-fr.html` -> `rg-fr.js` (build.py builds both). Live page: /pages/jeu-de-lecture-arabe (short link /test-lecture),
script in Shopify Files as `amf-reading-game-fr-vN.js` (current v4).
Differences from English: French text, age chips 4-5 / 6-7 / 8-9 / 10-11 / 12+, a 4th round "Texte"
(2 short texts with a 3-choice comprehension question: 1st with vowels, 2nd without; shown only if the sentence was read),
two extra levels (reader = "Groupe Lecteurs", advanced = "Groupe Lecteurs confirmés").
No trial booking: the result screen is a waitlist for a francophone group (preferred slot, Arabic at home, number of
interested kids, WhatsApp). Lead + waitlist go to Klaviyo list VD67XE (fr_waitlist, fr_preferred_slot,
fr_interested_kids, reading_game_lang=fr) and the store contact form. Never subscribes to X9QTYr (trial bookings).
Texts have no recorded clips (t_1, t_2): Pass falls back to the phone voice.
FR v2 (Nov 13): no sound at all (MUTE=true: no clips, no phone voice, no tones), no speaker button and no pictures;
cards answer with "J'ai trouvé !" (known) or "Je ne sais pas" (tried, not known) and go straight to the next card.
FR v3 (Nov 13): tracing moved to the start (warm-up before letters); waitlist slots in Morocco time; new last round
"Devine !" (5 "Comment dit-on… ?" flashcards: soleil, livre, fête, école, papillon; 3 Arabic choices each), shown to any
child who read 2+ words; score "Vocabulaire x/5" (Klaviyo reading_vocab), does not change the level.
FR v4 (Nov 13): tracing = 4 letters in a row (ب ت م س) with a progress row and "Lettre x sur 4". A letter passes only when
85% is covered AND every separate piece (body, each dot) is at least 60% covered (pieces found with 5 px cells,
4-neighbour). Success or "Je ne sais pas, lettre suivante" both show a short "Bravo ! / Pas grave ! Lettre suivante"
card, then the next letter. Score "Tracé x/4" (Klaviyo reading_trace). Waitlist: Friday afternoon slot added; optional
parent note (Klaviyo fr_parent_note, contact[Note]).
