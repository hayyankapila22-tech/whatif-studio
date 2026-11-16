# EPISODE PROMPT: "How does a blackhead form?" (HOW DOES IT WORK? special)

> Paste this whole document back into the WHAT IF chat. It sits on top of the **Master Production Prompt (v2)**. Everything in the master prompt applies (caption engine, motion language, audio chain, -14 LUFS, safe zones, quality checklist) **except** where this file says otherwise.

---

## 0. WHAT THIS EPISODE IS

- **Format:** a new "HOW DOES IT WORK?" explainer. It answers a question viewers have actually wondered about, at the same premium quality as the What-ifs.
- **Jeremy:** **not in this episode.** The scale references are a fingertip, a grain of salt and a human hair. Leave room for a Jeremy cameo later in variant S1-J if we want to test it.
- **Topic:** How blackheads form, why they're black, and what actually gets rid of them.
- **Topic score:** curiosity 5 · visual potential 5 · sourceable facts 4 = **14/15**. Build it.
- **Template:** body explainer (cross-section + "well, not exactly" myth-bust + what to do).
- **Tone:** curious, friendly, slightly conspiratorial. Never gross, never shaming. **No real pus, no real squeezing footage, no close-up photos of real skin.** Everything is clean, designed 3D/2.5D illustration.
- **Safety:** educational only. Include the footnote *"Not medical advice. See a GP or dermatologist if spots are painful or not improving."* No prescription doses. Products are named by **ingredient** only, never by brand.

---

## 1. LOOK & FEEL (preset S1, adapted: "SKIN LAB")

| Element | Direction |
|---|---|
| **Studio sequence** | `DARK` for "how it forms" (the problem), then a diagonal wipe to `WHITE` for "what to do" (the fix), then a short return to `DARK` for the final twist + loop. |
| **Hero object** | A **3D skin "cake slice"**: a rectangular block of skin cut open like a patent drawing. Top surface is matte skin (`#D7A47E` with subtle pore texture). The cut face shows stacked layers: thin translucent epidermis, pink-beige dermis (`#E0C5B1`), and a soft fat layer (`#F2E6CF`). One **follicle tube** runs down through it with a **sebaceous gland** (lobed, pale yellow, subsurface glow) at the bottom. Soft area light, contact shadow on the studio floor, f/2.8 depth of field on close-ups. |
| **Materials** | Skin: subsurface scattering, matte. Sebum: glossy pale-yellow gel (the *only* glossy thing). Dead skin cells: thin translucent off-white flakes. Oxidised plug: dark brown-black, slightly matte. |
| **Skin tone** | The control uses `#D7A47E`. **Every variant rotates the skin tone** (light / medium / deep) so the channel never shows only one skin type. |
| **Accents** (keyword colour = object colour) | **Sun Yellow `#FFD23F`** = oil / sebum / the plug · **Signal Mint `#3EE6A8`** = fixes / healthy / normal · **Alarm Red `#FF3B30`** = squeezing / inflammation only. Off-white objects (skin cells) use a **neutral white selection box**. |
| **Captions** | `C1` build mode with the colour-matched Figma selection box (exact master-prompt engine). |
| **Footnotes** | "Magnified illustration", "Simplified", "Not to scale", "Not medical advice…" |
| **HUD** | Top-left, below the captions: `PORE STATUS: CLEAR → CLOGGED → OPEN → OXIDISED → CLEARING`. It is a mono pill whose colour follows the state. |
| **Idle motion** | Gland gently "breathes" (±1 % scale), tiny sebum droplets drift upward, dust specks float, slow 2–4 % push-ins. No frame is ever still. |

**Music mood:** curious, 80–90 BPM, soft plucks plus a warm pad. Sub-bass hit on the plug forming and on the squeeze. Low riser into the twist.

---

## 2. HOOK OPTIONS

| Code | Hook line | Opening visual |
|---|---|---|
| **H4 Wrong-belief (control)** | "That black dot on your nose? It isn't dirt." | Macro of a skin surface, dark studio. One dark dot gets a Figma selection box, and the camera dives straight into it. |
| H1 Question | "How does a blackhead actually form?" | The skin block rises into frame and rotates to show its cut face. |
| H2 Shock stat | "Your face has up to nine hundred oil glands in every square centimetre." | A fingertip-sized square on the skin lights up, and 900 tiny yellow dots pop in a grid. |
| H3 POV | "You lean into the mirror… and there it is." | A mirror-frame inset with a soft magnifying circle sliding across the nose. |

---

## 3. FULL SCRIPT (control: `H4-S1-C1-P2-E1-L60`)

Markup follows master prompt §3: `*keyword*`, `||` phrase break, `//` cliffhanger pause (+250 ms), `{SFX:x}`, `{CHAPTER}`.
**Spoken word count: 154 → about 60 s at 155 wpm.**

```
That black dot on your *nose*? || It isn't *dirt*. //
Every pore is a tiny *tube* || with an *oil* gland inside.
Your face has up to *900* of them || in every square *centimetre*.
It pumps out *sebum* || to keep skin *soft*.
Its lining sheds *dead skin cells*.
Normally, || they slide out *together*. //
But sometimes, || the cells get *sticky*.
They clump with the oil || and form a *plug*. {SFX:hit}
Sealed over? || That's a *whitehead*.
But if the top stays *open*... //
air reaches the plug, || and it *darkens*. || Like a sliced *apple*.
That's a *blackhead*. {SFX:pop}
{CHAPTER}
So... || should you *squeeze* it? //
Well, || *not exactly*. {SFX:hit}
Squeezing can tear the pore wall || and push the plug *deeper*.
*Salicylic acid* || dissolves the plug instead.
A *retinoid* || stops cells sticking.
Then give it *six to eight weeks*. //
And one last *twist*.
Many grey dots on your nose || aren't blackheads at all. //
They're *sebaceous filaments*. || Totally *normal*.
So that black dot on your nose…
```

**TTS input notes** (write numbers in words for voice 1):
- "900" → "nine hundred"
- "six to eight weeks" stays as words
- "sebaceous" → `seh-BAY-shus`
- "salicylic" → `sal-ih-SIL-ik`
- "retinoid" → `RET-ih-noyd`
- Add all three to `pronunciations.json`.

**Loop:** the last line, "So that black dot on your nose…", runs straight into the first: "That black dot on your nose? It isn't dirt." The final frame matches frame 1, with a macro of the skin surface and a single dot.

---

## 4. BEAT-BY-BEAT VISUALS

| # | t (≈) | VO | Visual | Labels / HUD / SFX |
|---|---|---|---|---|
| 1 | 0–2.5 s | That black dot on your *nose*? \|\| It isn't *dirt*. | DARK studio. Macro skin surface fills the frame. One dot gets a **white Figma selection box** drawn around it. On "dirt", a grey `DIRT?` pill pops in, gets a red strike-through and falls away. | HUD `PORE STATUS: ?` · pop SFX · tick on strike |
| 2 | 2.5–5.5 s | Every pore is a tiny *tube* \|\| with an *oil* gland inside. | **Push-through:** the camera dives into the dot, and the surface splits open (top slides up 30 %) to reveal the **skin cake-slice** cross-section. The follicle tube glows faintly. The sebaceous gland at the bottom lights up yellow. | Pills: `PORE` (white), `OIL GLAND` (yellow) with leader lines · footnote *Magnified illustration* |
| 3 | 5.5–9 s | Your face has up to *900* of them \|\| in every square *centimetre*. | Pull back to the top surface. A **1 cm² square** (ruler edges, tick marks) lights up next to a fingertip for scale. 900 tiny yellow dots pop in a grid inside it, in a wave. | Big counter `0 → 900` + small `PER cm²` (easeOutExpo, tick + ding) · footnote *Forehead & T-zone: 400–900 per cm² (DermNet)* |
| 4 | 9–12 s | It pumps out *sebum* \|\| to keep skin *soft*. | Back in the cross-section. Glossy yellow sebum droplets rise up the tube and spread on the surface as a thin sheen. The surface highlight softens. | Pill `SEBUM` (yellow) |
| 5 | 12–15 s | Its lining sheds *dead skin cells*. | Off-white translucent flakes peel from the tube wall and drift upward. | Pill `DEAD SKIN CELLS` (white) |
| 6 | 15–18 s | Normally, \|\| they slide out *together*. // | Flakes and oil flow smoothly out of the pore opening (satisfying, clean). | HUD `CLEAR` (mint) · Pill `NORMAL` (mint) |
| 7 | 18–21 s | But sometimes, \|\| the cells get *sticky*. | Flow slows. Flakes start clumping. The camera drifts closer with a 4 % push. | HUD flickers `CLEAR → ?` |
| 8 | 21–24 s | They clump with the oil \|\| and form a *plug*. | Flakes + sebum compress into a dense yellow **plug** filling the tube. **Impact moment:** 2-frame flash, 8 px shake, sub hit. The tube visibly bulges a little. | HUD `CLOGGED` (yellow) · Pill `PLUG` · `{SFX:hit}` |
| 9 | 24–27 s | Sealed over? \|\| That's a *whitehead*. | **Split screen** (thin divider): LEFT tube gets a thin skin "lid" growing over it, with a pale bump. | Pill `WHITEHEAD` (white) · `CLOSED` small mono tag |
| 10 | 27–29 s | But if the top stays *open*... // | RIGHT tube: the opening stays wide. Tiny air particles (white specks labelled `O₂`) drift toward it. | Pill `OPEN` · riser starts |
| 11 | 29–33 s | air reaches the plug, \|\| and it *darkens*. \|\| Like a sliced *apple*. | The plug's exposed top shifts yellow → amber → dark brown-black. A rounded **magnify inset** shows an apple slice browning in a matched timelapse (morph: apple flesh colour → plug colour). | HUD `OXIDISED` (dark) · footnote *Oxidation of melanin & oils, not dirt* |
| 12 | 33–35 s | That's a *blackhead*. | Camera pulls back to the surface: the dark dot from frame 1 is back, now "explained". A ruler slides in: `≈ 1–3 mm`. | Pill `BLACKHEAD` (dark w/ white text) · pop |
| — | ~35 s | {CHAPTER} | **Diagonal wipe** (mint slab → paper-white slab, 300 ms, whoosh + paper swipe) → WHITE studio. | — |
| 13 | 35–37 s | So... \|\| should you *squeeze* it? // | WHITE studio. Clean skin block on a white floor. Two stylised fingertips (matte, no nails detail) hover either side of the pore. | Pill `SQUEEZE?` (red outline) |
| 14 | 37–38.5 s | Well, \|\| *not exactly*. | The fingertips press. **Impact:** red wash 0.4 s, shake, sub hit. | `{SFX:hit}` |
| 15 | 38.5–42 s | Squeezing can tear the pore wall \|\| and push the plug *deeper*. | Cross-section: the tube wall cracks (thin red fracture line) and the plug is shoved down. A soft red inflammation glow blooms around it (stylised, not gory). | Pill `INFLAMMATION` (red) · footnote *Can lead to marks or scarring* |
| 16 | 42–45.5 s | *Salicylic acid* \|\| dissolves the plug instead. | Rewind-whoosh: the crack un-cracks. Mint droplets (labelled `BHA`) sink into the pore. Because it's oil-soluble, they travel *down* the tube and the plug breaks into small pieces that float out. | Pill `SALICYLIC ACID` (mint) · HUD `CLEARING` (mint) |
| 17 | 45.5–48.5 s | A *retinoid* \|\| stops cells sticking. | New flakes along the tube wall shed smoothly instead of clumping (a mint shimmer passes over the tube lining). | Pill `RETINOID` (mint) · footnote *Some retinoids need a prescription. Ask a pharmacist.* |
| 18 | 48.5–51 s | Then give it *six to eight weeks*. // | A minimalist calendar strip flips week 1 → 8. The pore visibly clears week by week. | Counter `WEEK 1 → 8` (tick per week) · footnote *AAD guidance* |
| — | ~51 s | — | **Wipe back to DARK.** | whoosh |
| 19 | 51–53 s | And one last *twist*. | DARK studio. Macro nose surface again, now with an even grid of many small grey dots. | riser |
| 20 | 53–55.5 s | Many grey dots on your nose \|\| aren't blackheads at all. // | Two tubes side by side. LEFT: blackhead (dark raised plug). RIGHT: **sebaceous filament**, a thin, pale, flat column lining the pore, smooth with the surface. | Pills `BLACKHEAD` vs `FILAMENT` |
| 21 | 55.5–58 s | They're *sebaceous filaments*. \|\| Totally *normal*. | A mint ✓ pops on the filament. It "breathes" gently: it's meant to be there. | Pill `✓ NORMAL` (mint) · footnote *Not medical advice. See a GP or dermatologist if spots are painful or not improving.* |
| 22 | 58–60 s | So that black dot on your nose… | Camera pushes back to the single-dot macro. The final frame **matches frame 1** for the loop. | Source line: *Sources: AAD · DermNet · Cleveland Clinic* |

**Jeremy-free scale ladder:** human hair (~0.07 mm) → pore opening → blackhead 1–3 mm → grain of salt → fingertip (the 1 cm² square). Show at least the blackhead vs. grain of salt vs. fingertip in beat 12.

---

## 5. JSON SPEC

```json
{
  "id": "howitworks_blackheads_v1",
  "format": "regular",
  "series_tag": "HOW DOES IT WORK?",
  "title_on_screen": "HOW do blackheads form?",
  "jeremy": false,
  "studio_sequence": ["DARK", "WHITE", "DARK"],
  "accents": ["Sun Yellow", "Signal Mint"],
  "danger": "Alarm Red",
  "skin_tone": "#D7A47E",
  "caption_mode": "build",
  "transition_style": "mixed",
  "music_mood": "curious",
  "target_seconds": 60,
  "hud": {
    "label": "PORE STATUS",
    "states": [[0, "?"], [15, "CLEAR"], [21, "CLOGGED"], [29, "OXIDISED"], [42, "CLEARING"]]
  },
  "beats": [
    {"t_hint": "0-2.5s", "beat": "HOOK", "vo": "That black dot on your *nose*? || It isn't *dirt*. //",
     "visual": "DARK studio macro skin surface; Figma box on one dot; DIRT? pill struck through and dropped",
     "labels": ["DIRT? (grey, struck)"], "counter": null, "sfx": ["pop", "tick"],
     "footnote": null, "camera": "slow push-in 3%", "jeremy": null},
    {"t_hint": "2.5-5.5s", "beat": "SETUP", "vo": "Every pore is a tiny *tube* || with an *oil* gland inside.",
     "visual": "push-through into the dot; surface splits open to the skin cake-slice cross-section; gland glows yellow",
     "labels": ["PORE (white)", "OIL GLAND (yellow)"], "counter": null, "sfx": ["whoosh", "pop", "pop"],
     "footnote": "Magnified illustration", "camera": "dive + settle", "jeremy": null},
    {"t_hint": "5.5-9s", "beat": "ESCALATION 1", "vo": "Your face has up to *900* of them || in every square *centimetre*.",
     "visual": "1 cm square beside a fingertip; 900 yellow dots wave in",
     "labels": [], "counter": {"from": 0, "to": 900, "unit": "PER cm²"}, "sfx": ["tick x10", "ding"],
     "footnote": "Forehead & T-zone: 400–900 per cm² (DermNet)", "camera": "pull back", "jeremy": null},
    {"t_hint": "9-18s", "beat": "MECHANISM", "vo": "It pumps out *sebum* || to keep skin *soft*. Its lining sheds *dead skin cells*. Normally, || they slide out *together*. //",
     "visual": "sebum droplets rise; flakes peel; both flow out cleanly",
     "labels": ["SEBUM (yellow)", "DEAD SKIN CELLS (white)", "NORMAL (mint)"], "counter": null, "sfx": ["pop x3"],
     "footnote": null, "camera": "slow drift", "jeremy": null},
    {"t_hint": "18-24s", "beat": "TURN 1", "vo": "But sometimes, || the cells get *sticky*. They clump with the oil || and form a *plug*. {SFX:hit}",
     "visual": "flakes clump, compress into yellow plug; tube bulges",
     "labels": ["PLUG (yellow)"], "counter": null, "sfx": ["hit"],
     "footnote": "Simplified", "camera": "push 4% then 8px shake", "jeremy": null},
    {"t_hint": "24-35s", "beat": "ESCALATION 2", "vo": "Sealed over? || That's a *whitehead*. But if the top stays *open*... // air reaches the plug, || and it *darkens*. || Like a sliced *apple*. That's a *blackhead*.",
     "visual": "split screen whitehead vs open pore; O2 specks; plug top yellow to black; apple inset morph; ruler 1-3 mm vs grain of salt",
     "labels": ["WHITEHEAD", "OPEN", "BLACKHEAD"], "counter": null, "sfx": ["riser", "pop"],
     "footnote": "Oxidation of melanin & oils, not dirt", "camera": "split, then pull back", "jeremy": null},
    {"t_hint": "35-42s", "beat": "WELL, NOT EXACTLY", "vo": "{CHAPTER} So... || should you *squeeze* it? // Well, || *not exactly*. {SFX:hit} Squeezing can tear the pore wall || and push the plug *deeper*.",
     "visual": "mint/paper wipe to WHITE; stylised fingertips press; red wash; wall cracks, plug pushed down, soft red glow",
     "labels": ["SQUEEZE? (red outline)", "INFLAMMATION (red)"], "counter": null, "sfx": ["whoosh", "paper", "hit"],
     "footnote": "Can lead to marks or scarring", "camera": "shake 8 frames", "jeremy": null},
    {"t_hint": "42-51s", "beat": "FIX", "vo": "*Salicylic acid* || dissolves the plug instead. A *retinoid* || stops cells sticking. Then give it *six to eight weeks*. //",
     "visual": "rewind crack; mint BHA droplets travel down, plug breaks up; lining sheds smoothly; calendar week 1-8, pore clears",
     "labels": ["SALICYLIC ACID (mint)", "RETINOID (mint)"], "counter": {"from": 1, "to": 8, "unit": "WEEKS"}, "sfx": ["pop", "pop", "tick x8"],
     "footnote": "Some retinoids need a prescription. Ask a pharmacist. · AAD guidance", "camera": "slow push", "jeremy": null},
    {"t_hint": "51-58s", "beat": "PEAK / TWIST", "vo": "And one last *twist*. Many grey dots on your nose || aren't blackheads at all. // They're *sebaceous filaments*. || Totally *normal*.",
     "visual": "wipe to DARK; grid of grey dots; blackhead vs filament tubes; mint tick on filament",
     "labels": ["BLACKHEAD", "FILAMENT", "✓ NORMAL (mint)"], "counter": null, "sfx": ["whoosh", "riser", "pop"],
     "footnote": "Not medical advice. See a GP or dermatologist if spots are painful or not improving.", "camera": "side-by-side push", "jeremy": null},
    {"t_hint": "58-60s", "beat": "PAYOFF + LOOP", "vo": "So that black dot on your nose…",
     "visual": "push back to single-dot macro; final frame matches frame 1",
     "labels": [], "counter": null, "sfx": [],
     "footnote": "Sources: AAD · DermNet · Cleveland Clinic", "camera": "match frame 1", "jeremy": null}
  ],
  "sources": ["American Academy of Dermatology (types of acne, 6–8 weeks)", "DermNet NZ (sebum, 400–900 glands/cm²)", "Cleveland Clinic / MedicineNet (oxidation, 1–3 mm)", "Sebaceous filament explainers (dermatologist-reviewed)"],
  "comment_question": "Blackheads or filaments: check your nose and tell me which you've got.",
  "loop_check": "'So that black dot on your nose…' flows into 'That black dot on your nose? It isn't dirt.'"
}
```

---

## 6. VARIANT PLAN (control + 3 challengers)

File names follow `{topic}_{variantcode}.mp4`.

| File | Changes | Re-voice? |
|---|---|---|
| `blackheads_H4-S1-C1-P2-E1-L60.mp4` | **Control.** Skin tone medium. | — |
| `blackheads_H2-S1-C1-P2-E1-L60.mp4` | Hook → shock stat ("…nine hundred oil glands in every square centimetre"). Skin tone deep. | Yes (first line only) |
| `blackheads_H4-S2-C3-P2-E1-L60.mp4` | Style → **Flat Explainer** (warm vector, colour-bar wipes, full-sentence rise-in captions). Skin tone light. | No |
| `blackheads_H4-S1-C1-P2-E2-L60.mp4` | Ending → comment question + animated follow beat ("Blackheads or filaments? Check your nose and tell me."). | Yes (last line only) |

---

## 7. SOURCES FOR EVERY NUMBER / CLAIM

| Claim on screen | Source |
|---|---|
| Black colour = oxidation, not dirt | American Academy of Dermatology ("the black dots aren't dirt"); Cleveland Clinic; MedicineNet |
| Pore = follicle opening with an oil gland; sebum + dead cells form the plug | AAD; DermNet NZ |
| Up to 400–900 oil glands per cm² (forehead / T-zone) | DermNet NZ "Sebum"; Sci. Reports 2018 (sebaceous gland density) |
| Blackheads usually 1–3 mm | MedicineNet (dermatology-reviewed) |
| Whitehead = closed pore, blackhead = open pore | AAD "Types of breakouts" |
| Squeezing can rupture the follicle and push debris deeper → inflammation / scarring | Dermatology guidance (AAD; hospital dermatology articles) |
| Salicylic acid and retinoids (adapalene) are standard treatments | AAD acne guideline; Cleveland Clinic |
| Give treatment 6–8 weeks | AAD ("give treatment six to eight weeks to work") |
| Sebaceous filaments are a normal pore lining, not blackheads | Dermatologist-reviewed explainers (L'Oréal/AAD-cited; Mayo/NHS-cited) |

> Note for the build: adapalene is over-the-counter in the US but **prescription-only in the UK**. That's why the footnote says "some retinoids need a prescription" and the script never tells viewers to buy a specific one.

---

## 8. EPISODE-SPECIFIC CHECKLIST (on top of master §7)

- [ ] Hook dot + selection box visible in frame 1. Dive starts within 1 s.
- [ ] Nothing graphic: no real skin photos, no pus, no blood. Squeeze is stylised and short (≤ 1.5 s).
- [ ] Every treatment is named by ingredient, not brand. The "not medical advice" footnote is on screen ≥ 2 s.
- [ ] Skin tone rotated per variant (light / medium / deep).
- [ ] At least 3 numbers: 900 per cm², 1–3 mm, 6–8 weeks. Each has a scale reference (fingertip square, grain of salt, calendar).
- [ ] Cliffhanger breaks at "It isn't dirt //", "slide out together //", "stays open… //", "squeeze it? //", "weeks //", "at all //".
- [ ] Chapter switch DARK → WHITE at the squeeze question. Final frame matches frame 1.
- [ ] Captions match VO word for word ("900" on screen ↔ "nine hundred" spoken).

---

## 9. BUILD INSTRUCTIONS FOR THE CHAT

1. Confirm the script word count and runtime. Then generate the VO with **voice 1** (or the best available stand-in if voice 1 can't be reached, and say so). Use per-sentence calls and the master-prompt settings.
2. Get word timings (TTS alignment or WhisperX). All label pops, counters and impacts snap to keyword starts ±2 frames.
3. Render in the cloud at 1080×1920, 30 fps. The cross-section beats may use 60 fps if motion is heavy.
4. Before the full render, show me 4 stills: **hook (beat 1), plug forming (beat 8), squeeze turn (beat 14), filament twist (beat 21)**.
5. Then render the control, mix to -14 LUFS / -1 dBTP, and send it. Render the 3 challengers after I approve the control.
