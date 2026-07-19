# Malay Vocal Personas — Prompt Snippets for Music AI

Use these as vocal description fragments inside the `--prompt` argument for `mmx music generate` or Suno style tags. Mix and match with genre/instrument/mood elements.

---

## Male Ballad Vocalists

### Zamani (ex-Slam)
```
powerful male vocalist with rich warm vibrato and melismatic delivery,
emotional intensity building from intimate whisper to soaring belt,
1990s Malaysian pop ballad vocal style
```
Signature: emotional climaxes, long sustained notes on chorus, vulnerability in verses.
Key songs: Gerimis Mengundang, Kembali Terjalin, Kau Ilhamku.
BPM range: 68-85 (verse) → 80-95 (chorus).

### M. Nasir
```
husky male baritone with poetic delivery, slight rasp, folk-rock
inflection, storytelling vocal style, Malaysian art-pop sensibility
```
Signature: literary lyrics, theatrical delivery, folk-rock crossover.
BPM range: 80-110.

### Awie (Wings)
```
raw powerful male rock vocalist, high-energy belting, raspy edge,
Malaysian rock kapak vocal style
```
Signature: explosive energy, rock ballad to hard rock range.
BPM range: 90-130.

### Hafiz Suip
```
smooth contemporary male pop vocalist, clear tone, controlled vibrato,
modern Malaysian pop ballad style
```
Signature: clean production, radio-friendly, emotional but polished.
BPM range: 70-90.

## Female Ballad Vocalists

### Siti Nurhaliza
```
soaring female soprano with crystalline clarity, melismatic ornamentation,
powerful controlled vibrato, Malaysian pop-dangdut crossover elegance
```
Signature: vocal acrobatics, sustained high notes, graceful ornamentation.
BPM range: 70-100.

### Ella (Rock Queen)
```
powerful female rock vocalist, raw emotional edge, raspy belting,
Malaysian rock queen vocal style
```
Signature: rock ballad power, emotional rawness, genre-crossing.
BPM range: 85-120.

### Dayang Nurfaizah
```
soulful female R&B vocalist, rich lower register, smooth runs,
contemporary Malaysian soul-pop style
```
Signature: groove-oriented, R&B runs, emotional depth.
BPM range: 75-100.

## Genre-Specific Prompt Templates

### 90s Malay Rock Ballad (Zamani/Awie style)
```
Malay emotional rock ballad, powerful male vocalist with raspy vibrato
and soaring belt, electric guitar power chords, piano, string orchestra,
drums building from soft to explosive, 1990s Malaysian rock ballad era,
heartfelt romantic longing, slow tempo 72 BPM building to 95 BPM on
chorus, warm analog production, no electronic instruments, acoustic
organic verses with electric chorus
```

### Contemporary Malay Pop (Hafiz/Siti style)
```
contemporary Malaysian pop ballad, smooth polished male/female vocalist
with clear controlled vibrato, piano-driven, subtle strings, light
electronic pads, modern clean production, romantic and uplifting,
75 BPM, radio-friendly arrangement
```

### Malay Folk-Pop Fusion (M. Nasir style)
```
Malaysian folk-pop, husky male baritone with poetic storytelling delivery,
acoustic guitar, traditional percussion (gendang, rebab), modern
arrangement with folk roots, nostalgic and contemplative, 90 BPM,
warm organic production
```

---

## Prompt Engineering Notes

- **Don't name the artist directly** in the prompt — describe the vocal STYLE instead. "Like Zamani" may produce worse results than describing his vocal characteristics.
- **BPM controls energy** — Malay ballads typically start slow (68-75 BPM) and build on chorus (85-95 BPM). Single BPM works too but less dynamic.
- **Strings are mandatory** for Malay ballads — "lush string orchestra" or "string arrangement" should always appear.
- **No electronic instruments** for 90s style. Allow subtle synths for contemporary style.
- **"Warm analog production"** helps push away from default pop-EDM sound.

---

*Source: Zamani-style "Kembali Merindu" generation session, 2026-07-13. Successful output: 2:54, 256kbps, emotional ballad with piano+strings arrangement.*
