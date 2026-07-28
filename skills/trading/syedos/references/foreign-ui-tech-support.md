# Foreign-Language Appliance / UI Tech Support (for Syed & non-English speakers)

When Syed (or any user) asks for help with an appliance or device that has a **Chinese/foreign-language UI**, follow this pattern.

## Signal
- User sends photo(s) of an appliance display showing non-English text
- User says "cari manual" / "tak faham bahasa" / "step by step"
- User wants to change language or find the English manual

## Pipeline

### 1. Identify the Model
The SmartThings sticker often has the real model code embedded:
- Look for codes like `WD13B8944DGBF0` → likely `WD13BB944DGBFQ` (Samsung Malaysia)
- The sticker label codes may be OCR/font variations (e.g. `B8944` = `BB944`, `F0` = `FQ`)
- Check Samsung MY support: `https://www.samsung.com/my/support/model/<MODEL>/`
- Search alternative models: drop the last few chars and search

### 2. Find the English Manual
- **Manualslib** is the most reliable source — search by model or series name
- Samsung Malaysia support page (`samsung.com/my`) usually has English docs
- If the page is JS-rendered, use manualslib as fallback
- The manual may cover a whole series (e.g. "WD BB Series") that includes the specific model

### 3. DO NOT Over-Explain — Go Straight to Steps
When user says "now tell me step by step" — **stop explaining the process and give the steps immediately**. This is the correction signal.

**Style rule:**
```
Bad: "First you need to find the Settings menu which is called 设置 in Chinese etc etc"
Good: "1. Tekan & tahan ⚙️ 3 saat. 2. Cari 语言. 3. Pilih English."
```

### 4. Provide Chinese → English Mapping
When giving navigation steps, include both:
- The Chinese characters as they appear on screen
- The English meaning
- A visual indicator (icon description) if applicable

Example format:
```
| Cari ni... | Maksud |
|---|---|
| 语言 | Language ← pilih ni |
| 设置 | Settings |
| 水质硬度 | Water Hardness |
```

### 5. Identify "Language" Menu Entry
In Chinese appliance firmwares, the language setting may be called:
- **语言** (yǔ yán) — most common
- **语言设置** (yǔ yán shè zhì) — less common
- **English / 英语** (yīng yǔ) — the option to select

### 6. Handle Firmware Lock
Many China-market appliances (Samsung, Haier, Midea) have **locked firmware** with no English option:
- Samsung China models often lack language toggle
- Fallback: use the **SmartThings app** (English) to control the machine
- Fallback: provide the English manual PDF as reference for matching icons/functions
- Offer to translate any screen on WhatsApp
### 7. Samsung Washing Machine — Language Change (proven 2026-07-27)

When Syed asks to change Samsung washing machine language to BM:

**Two methods:**

| Method | Steps |
|--------|-------|
| **Official** | Tekan & tahan **"Additional Function"** 3 saat → Pusing dial ke **"Factory Reset"** → Tekan OK |
| **Alternate** | Tekan & tahan **"Delay End" + "Pre Wash"** serentak 3 saat (langsung masuk menu bahasa) |

**CRITICAL — BM NOT AVAILABLE.** Samsung models for Middle East/Asia market hanya ada: English, Arabic, Turkish, French. Tiada Bahasa Melayu atau Indonesia. Jangan janji boleh tukar BM sebelum semak dulu. Ini limitasi firmware, bukan pengguna salah setting.

Jika abang nak BM — model pasaran Malaysia/Indonesia mesti guna code berbeza:
- Cari model number pada SmartThings sticker
- Bandingkan dengan senarai model Samsung Malaysia Support
- Kalau code berakhir `GU-R` (middle east) → takde BM
- Kalau code berakhir `MS` → mungkin ada BM

**Jika takde pilihan BM:**
- Cadang guna **SmartThings App** (semua English/BM)
- Atau tawarkan diri: "Nak saya terjemah screen, WhatsApp je" — abang hantar gambar, saya guide guna ikon/bentuk, bukan text.

**Alert: "Child Lock not supported" (童锁不支持)** — ini maksudnya model ni takde fungsi child lock. BUKAN rosak. Jangan suruh hantar servis.

### 8. Manual Delivery

When found, provide:
- Direct link to the manual
- Brief summary of what's inside (safety, cycles, troubleshooting)
- One-line offer: "Nak saya terjemah mana-mana screen, WhatsApp je"
