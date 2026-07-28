---
name: appliance-manual-research
description: Find manuals and documentation for Asian-market home appliances — Samsung, LG, Haier, Midea brands where the UI is Chinese-only and model stickers use SmartThings/factory codes instead of standard retail model numbers. Covers sticker decoding, manual databases, and regional support sites.
---

# Appliance Manual Research

Find user manuals for Asian-market home appliances where:
- The UI/display is **Chinese-only** (中文)
- The sticker shows **SmartThings** branding with QR + alphanumeric code
- The code on the sticker is a **factory/serial code**, not the retail model number
- Regional variants exist (China/CN, Malaysia/MY, Pakistan/PK)

## Trigger conditions

The user sends photos of:
- A SmartThings sticker on an appliance
- A control panel with Chinese text
- An appliance they can't identify the model of
- A request: "cari manual" / "find manual" / "nak manual" / "manual for my X"

## Workflow

### Step 1: Read the sticker code

The SmartThings sticker typically shows:
```
[SmartThings logo] | [QR code]
                    W013B8944DGBF0 01
                    0ASV5NAL300104W
```

**Key insight:** The code on a SmartThings sticker is NOT the retail model number. It's a factory/SmartThings registration code. Decode it:

1. Check if a leading `W` should be `WD` (washer dryer prefix for Samsung)
   - `W013B...` → likely `WD13B...`
2. Samsung washer dryer model formats:
   - `WD` = Washer Dryer
   - Number = capacity in kg (e.g. `13` = 13kg)
   - Remainder = series/spec variant
3. The `F0` / `FQ` suffix = color/market variant code

### Step 2: Search with multiple codes

```
WD13B8944DGBF0    ← sticker code
WD13BB944DGBSC    ← China variant
WD13BB944DGBFQ    ← Malaysia variant
```

Try these searches:
- `samsung.com.cn/support/model/<CODE>/` — Samsung China support
- `samsung.com/my/support/model/<CODE>/` — Samsung Malaysia support
- `manualslib.com` search
- `manua.ls` search
- Direct web search: `"<CODE>" Samsung manual English`

### Step 3: Samsung regional support sites

| Region | URL pattern | Language |
|--------|------------|----------|
| **China** | `samsung.com.cn/support/model/<CODE>/` | Chinese |
| **Malaysia** | `samsung.com.my/support/model/<CODE>/` | English/BM |
| **Pakistan** | `samsung.com.pk/support/model/<CODE>/` | English |
| **Global** | `samsung.com/us/support/downloads/` | English |

**NOTE:** Samsung support pages use **JavaScript** to render the "Manuals & Downloads" section. Extracting via `smart_fetch` or `web_extract` will show template variables like `{{file.description}}`. Workaround:
- Use **manualslib.com** which pre-processes the Samsung manuals
- Search for the model series (e.g. "WD BB Series") which covers many variants

### Step 4: Manualslib technique

- URL: `manualslib.com/manual/<ID>/Samsung-<Series>.html`
- The manual contains English *plus* a second language (often Indonesian or Malay)
- English is typically the first ~70 pages
- Search term: `site:manualslib.com <brand> <series> manual`

### Step 5: Handle Chinese-only UI

When the user asks "mana nak tukar bahasa" (where to change language):

1. Settings access: hold Settings button (⚙️) for 3 seconds
2. Language option depends on firmware region:
   - **Malaysia/MY models** — usually have English option
   - **China/CN models** — often **Chinese-only** firmware
3. If language cannot be changed:
   - Provide the manual as reference
   - Offer to translate specific screen text
   - Map Chinese cycle names to English equivalents

### Step 6: Common Samsung cycle translations

| Chinese | Pinyin | English |
|---------|--------|---------|
| 棉质节能洗 | Mián zhì jiēnéng xǐ | Cotton Eco Wash |
| 超节能洗 | Chāo jiēnéng xǐ | Super Energy-Saving Wash |
| 洗涤+烘干 | Xǐdí + hōnggān | Wash + Dry |
| 烘干 | Hōnggān | Drying only |
| 化纤 | Huàxiān | Synthetic |
| 羊毛 | Yáng máo | Wool |
| 低温洗 | Dīwēn xǐ | Low Temp Wash |
| 强力洗 | Qiánglì xǐ | Heavy/Powerful Wash |
| 蒸汽除菌 | Zhēngqì chújūn | Steam Sterilization |
| 减少微纤维 | Jiǎnshǎo wēixiānwéi | Reduce Microfiber |
| 静音洗 | Jìngyīn xǐ | Silent Wash |
| 轻柔 | Qīngróu | Gentle |
| 衬衫 | Chènshān | Shirts |
| 排水/脱水 | Páishuǐ/tuōshuǐ | Drain/Spin |
| 漂洗+脱水 | Piǎo xǐ + tuō shuǐ | Rinse + Spin |
| 15 分钟快洗 | 15 fēnzhōng kuài xǐ | 15-min Quick Wash |
| 超快速 | Chāo kuàisù | Super Speed |
| AI 洗涤 | AI xǐdí | AI Wash |
| 筒清洁+ | Tǒng qīngjié+ | Drum Clean+ |
| 寝具 | Qǐn jù | Bedding |
| 加烘干 | Jiā hōnggān | Add drying |

## Pitfalls

- **Do NOT assume the sticker code IS the model number.** SmartThings stickers use factory codes. The retail model is usually similar but not identical.
- Samsung China models often end in `SC` or `/SC` suffix. Malaysia models end in `FQ`. They are the same hardware with different firmware.
- Samsung support pages are JavaScript-heavy. `web_extract` and `smart_fetch` (HTTP mode) fail to render the download links. Use manualslib or browser mode instead.
- Not all Samsung washer dryers have a language switch. China-market firmware is often locked to Chinese.
