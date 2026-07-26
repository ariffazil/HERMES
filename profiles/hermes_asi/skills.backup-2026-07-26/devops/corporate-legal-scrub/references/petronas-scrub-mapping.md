# PETRONAS Scrub — Reference Mapping (2026-07-14)

## Anonymization Mapping Used

| Original | Replacement | Context |
|----------|-------------|---------|
| PETRONAS | NOC-A / NOC / Malaysian NOC | Formal references |
| PETRONAS_MPM | NOC_A_MPM | Test operator strings |
| PETRONAS | NOC_A | Test operator names |
| TriCipta | NOC-AI-Partner | Subsidiary/AI arm |
| petronas_proprietary | noc_proprietary | Code field names |
| Petronas field calibration | NOC field calibration | Technical claims |
| "PETRONAS canonical name" | "NOC canonical name" | Comments |
| "PETRONAS dataset ref" | "Malaysian NOC dataset ref" | Schema descriptions |
| "PETRONAS Sabah Basin v3" | "NOC-A Sabah Basin v3" | Data source IDs |
| "PETRONAS Upstream" | "NOC-A Upstream" | Source author |
| "verbatim PETRONAS naming" | "verbatim NOC naming" | URI scheme docs |
| "PETRONAS" (in atlas data) | "Malaysian NOC" | Atlas fiscal regime |
| Petronas/field companions | NOC/field companions | Benchmark notes |
| "not Petronas" | "not NOC-proprietary" | Benchmark disclaimers |

## Files Modified (27 total)

### Nuked (16 files — `docs/petronas/`)
Full directory removed. Contents archived to `/root/.private/petronas-memory/`.

### Anonymized (11 files)
- `contracts/schemas/earth_layer_registry.py` — 5 replacements
- `src/geox_mcp/resources/__init__.py` — 1 replacement
- `src/geox_mcp/uri_schemes.py` — 1 replacement
- `src/geox_mcp/tools/geox_atlas.py` — 1 replacement
- `src/geox_core/benchmarks/geox_001_well_seismic_truth.py` — 7 replacements
- `src/geox_core/benchmarks/geox_001_orthogonal_route.py` — 1 replacement
- `tests/test_bid_round_screener.py` — 6 replacements
- `GENESIS/011_COMPETITIVE_LAYER_MAP.md` — 7 replacements (including TriCipta)
- `GENESIS/014_PETREL_DSG_DELTA.md` — 1 replacement

## Commit
```
5d9647aa chore(legal): remove all PETRONAS references — nuke docs/petronas/, anonymize source/tests/genesis/contracts
27 files changed, 34 insertions(+), 1706 deletions(-)
```

## Private Archive
`/root/.private/petronas-memory/` — 18 files, chmod 600, with README.md index.
