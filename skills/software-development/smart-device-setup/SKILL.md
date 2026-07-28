---
name: smart-device-setup
title: Smart Device & Wearable Setup
description: Help users provision, configure, and troubleshoot smart devices (wearables, bands, watches, eSIM, connected appliances). Mixes local telco knowledge with step-by-step guidance.
---

# Smart Device & Wearable Setup

Help users set up smart devices — bands, watches, eSIM wearables, and connected appliances. This skill covers the class-level workflow; session-specific detail goes in `references/`.

## When to Use

User asks any of:
- "How to set up X device" (band, watch, eSIM, smart appliance)
- "How to activate eSIM / get number for wearable"
- "How to evaluate fitness/health data from device"
- "Which telco supports X device in Malaysia"

Do NOT use for: one-off Google queries about device specs (just search). Use for multi-step provisioning requiring local knowledge (telco compatibility, regional firmware quirks, BM-language-friendly explanations).

## Workflow

### 1. Identify the Device

From what the user says or sends:
- Product name + model variant (Pro/NFC/LTE/eSIM)
- Global vs China version (important: China firmware often no English)
- Image of box/device → look for model number on box label

### 2. Research Phase (parallel)

| What | Why |
|---|---|
| Official specs page (mi.com) | Features, sensors, eSIM support |
| Official manual | Setup steps, pairing guide |
| Telco compatibility (if eSIM) | Which MY telcos support the device for eSIM/wearable plans |
| Local support pages | Malaysia-specific setup quirks |

### 3. Structure the Answer

| For whom | Format |
|---|---|
| **Coder / tech person** (Arif) | Direct, short tables, BM-English mix |
| **Non-coder** (Aliff, Izzu) | Simple BM, no jargon, step-by-step |
| **Third-person** (Syed, via Arif) | Even simpler, funny/practical tone |

### 4. eSIM / Telco Guidance (Malaysia-specific)

When the device has eSIM and the user asks about getting a number:

| Telco | Wearable eSIM Support | Notes |
|---|---|---|
| **Spark (CelcomDigi digital)** | ❌ Phone-only eSIM | Need separate GadgetSIM or WatchSIM |
| **CelcomDigi GadgetSIM** | ✅ RM15/mth | For tablets, wearables, bands |
| **CelcomDigi WatchSIM** | ✅ RM20/mth | One-number-two-devices (Apple Watch mainly) |
| **Maxis** | ✅ Selected watches | Check device compatibility |
| **U Mobile** | ✅ eSIM for phones, limited wearables | |
| **Yes** | ✅ eSIM | |

**Key question flow:**
1. Does user already have a telco plan? → Which one?
2. Is the plan a phone plan or wearable plan? → Phone plans often don't work on bands.
3. Where to find the number? → In telco app (Spark, MyCelcomDigi, MyMaxis) under Account/Profile.
4. If activating eSIM for band specifically → Need QR from telco → Scan in band Settings > eSIM.

### 5. Step-by-Step Setup Pattern

For every device, use this consistent structure:

```
## [Device Name] Setup

### Step 1: Install App
- [App name], where to download

### Step 2: Pair / Connect
- Bluetooth pairing process
- App permissions needed

### Step 3: Initial Config
- Language, profile, permissions
- Key settings to turn ON/OFF

### Step 4: Feature Setup
- eSIM (if applicable)
- Health tracking (HR, sleep, GPS)
- Notifications

### Step 5: Verify
- Confirm sync working
- Test key feature
```

### 6. Fitness Data Evaluation

When asked to evaluate someone's fitness data from a wearable:

| Metric | What to Look For | Target (general) |
|---|---|---|
| Resting HR | Trend over days/week | 50-80 bpm |
| Sleep score | Deep/REM/Light ratio | >75/100 |
| Steps | Daily consistency | 8k-10k/day |
| Workout frequency | Per week | 3-5x |
| HRV | Recovery signal | Higher = better recovery |

Avoid: overinterpreting single data points. Compare trends, not snapshots.

## Pitfalls

- **China firmware**: Samsung/Mi bands from China often locked to Chinese UI. Cannot change to English. Manage expectations early.
- **eSIM ≠ Wearable eSIM**: Spark/Yoodo phone eSIM ≠ wearable eSIM. Check plan type before promising it works on the band.
- **Samsung SmartThings sticker**: The code on the sticker (e.g. W013B8944DGBF0) is the device/serial ID, NOT the model number. The real model number is a longer format like WD13BB944DGBFQ. Check the product box or larger label.
- **Non-coder communication**: For Arif's friends (Aliff, Syed, Izzu), explain as "macam cerita kedai kopi" — plain BM, no jargon, short paragraphs, one point at a time.

## Related Skills

- `federation-git-zen` — for git-based workflows (different class)
- `hermes-agent` — for Hermes Agent configuration
