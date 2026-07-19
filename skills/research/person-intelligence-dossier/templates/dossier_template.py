"""Build a Person Intelligence Dossier — v1 template (proven 2026-07-08).

Replicates the Freddy Bakon dossier structure. Modify the 7 dataclasses below
for a new subject and re-run.

Stack: matplotlib 3.11+ (figures) + weasyprint 68.1 (PDF).

Usage:
    python3 dossier_template.py <name> <out_dir>

Output:
    <out_dir>/<slug>_profile.html
    <out_dir>/<slug>_profile.pdf
    <out_dir>/.receipt.json
    <out_dir>/figures/fig1_career_timeline.png
    <out_dir>/figures/fig2_field_geography.png
    <out_dir>/figures/fig3_capability_matrix.png
"""
from __future__ import annotations
import sys, os, json, datetime, hashlib, subprocess
from pathlib import Path

# ==== DATA MODEL — edit these for each subject ================================

SUBJECT = {
    "full_name": "Replaceable Subject",
    "subtitle": "Role · Discipline · Specialism",
    "employer": "Employer Co. Sdn. Bhd.",
    "location": "City, Country",
    "education": "B.Eng. Discipline — University",
    "years_employer": 0,
    "years_industry": 0,
    "concurrent_roles": 0,
    "linguistic_heritage": "Heritage sentence.",       # Iban/Malay/etc
    "languages": "English, Malay",
    "abstract": "One paragraph that summarises who they are.",
    "keywords": "kw1 · kw2 · kw3",
    "honest_gaps": ["Family layer not attempted.", "Anticipated assignments flagged SPEC."],
    "sources": [
        ("LinkedIn (URL slug)", "employment + IPM stack"),
        ("OnePetro DOI", "paper authorship"),
    ],
    "milestones": [
        # (date, description, color, x)
        ("YYYY-MM", "Role at A\n2018–2020", "#666666", 0.0),
        ("YYYY-MM", "Role at B\n2020–present", "#3d6e4f", 1.2),
    ],
    "fields": [
        # (name, lon, lat, note, color)
        ("Field 1", 103.5, 4.5, "Year · 5 wells", "#b8860b"),
    ],
    "frontier_name": "Frontier X",            # the upcoming thing
    "frontier_color": "#a83a3a",
    "role_table_rows": [
        ("Period", "Role", "Field", "Highlights"),
        ("YYYY", "Eng", "Field", "Description"),
    ],
    "papers": [
        ("DOI", "Title", "Date", "Co-authors"),
    ],
    "conversation_starters": [
        ("Domain question", "What it tests"),
    ],
}


# ==== FIGURE GENERATION ========================================================

def make_figures(out_dir: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patheffects as pe
    import numpy as np

    WHITE, INK, GOLD, SAR, SAB = "#ffffff", "#0d1117", "#b8860b", "#3d6e4f", "#1f3a5f"
    SUR = SUBJECT["frontier_color"]
    plt.rcParams.update({"figure.facecolor": WHITE, "axes.facecolor": WHITE,
                         "text.color": INK, "font.family": "DejaVu Serif",
                         "font.size": 10})

    # ---- FIG 1: Career timeline ----
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.axhline(y=0, xmin=0.04, xmax=0.96, color=INK, linewidth=2.5, zorder=1)
    for i, (date, desc, color, x) in enumerate(SUBJECT["milestones"]):
        y = 1.6 if i % 2 == 0 else -1.6
        ax.plot(x, 0, "o", markersize=14, color=color, markeredgecolor=INK, markeredgewidth=1.4, zorder=3)
        ax.plot(x, 0, "o", markersize=6, color=WHITE, zorder=4)
        ax.plot([x, x], [0, y * 0.55], color=color, linewidth=1.2, alpha=0.7, zorder=2)
        ax.text(x, y * 0.62, date, ha="center", va="center", fontsize=8.5, fontweight="bold",
                color=color, bbox=dict(boxstyle="round,pad=0.32", fc="white", ec=color, lw=1.1))
        lines = desc.split("\n"); box_h = 0.42 + 0.18 * len(lines)
        ax.add_patch(plt.FancyBboxPatch((x - 0.92, y * 0.95 - box_h / 2), 1.84, box_h,
                                        boxstyle="round,pad=0.04,rounding_size=0.08",
                                        lw=1.0, ec=color, fc=color, alpha=0.10, zorder=2))
        txt = ax.text(x, y * 0.95, desc, ha="center", va="center", fontsize=8.2, linespacing=1.4)
        txt.set_path_effects([pe.withStroke(linewidth=2.4, foreground="white")])
    ax.set_xlim(-0.6, max(8.4, len(SUBJECT["milestones"]) * 1.3 + 1))
    ax.set_ylim(-3.4, 3.4); ax.axis("off")
    ax.text(0.05, 0.97, f'{SUBJECT["full_name"]} — Career Spine',
            transform=ax.transAxes, fontsize=15, fontweight="bold")
    ax.text(0.05, 0.93, f'{SUBJECT["years_industry"]}+ years operating · {SUBJECT["years_employer"]} years {SUBJECT["employer"]}',
            transform=ax.transAxes, fontsize=9.5, color="#4a5568", style="italic")
    plt.tight_layout()
    plt.savefig(out_dir / "figures/fig1_career_timeline.png", dpi=200, bbox_inches="tight")
    plt.close()

    # ---- FIG 2: Field geography (schematic) ----
    fig, ax = plt.subplots(figsize=(12, 7))
    # Borneo + Peninsular Malaysia polygons (replace with subject's region)
    ax.set_xlim(98, 130); ax.set_ylim(-0.5, 8.5); ax.grid(True, alpha=0.3, ls=":")
    ax.set_xlabel("Longitude (°E)"); ax.set_ylabel("Latitude (°N)")
    for name, lon, lat, note, color in SUBJECT["fields"]:
        ax.plot(lon, lat, "o", markersize=11, color=color, markeredgecolor=INK, markeredgewidth=1.0, zorder=4)
        ax.annotate(name, (lon, lat), xytext=(lon + 0.7, lat + 0.3), fontsize=8.5, fontweight="bold",
                    color=color,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color, lw=0.9, alpha=0.92),
                    arrowprops=dict(arrowstyle="-", color=color, lw=0.6, alpha=0.7))
        ax.text(lon, lat - 0.55, note, fontsize=7.2, ha="center", style="italic")
    ax.text(0.01, 1.04, "Operating Footprint — schematic; coordinates relative positioning only.",
            transform=ax.transAxes, fontsize=12.5, fontweight="bold")
    plt.tight_layout()
    plt.savefig(out_dir / "figures/fig2_field_geography.png", dpi=200, bbox_inches="tight")
    plt.close()

    # ---- FIG 3: Capability matrix (built-in template) ----
    fig, ax = plt.subplots(figsize=(12, 6))
    caps = [
        ("Capability 1", 5), ("Capability 2", 5), ("Capability 3", 5),
        ("Capability 4", 4), ("Capability 5", 4),
        ("Frontier 1", 1), ("Frontier 2", 1),
    ]
    labels, values = zip(*caps)
    bar_colors = [SAR if v == 5 else GOLD if v == 4 else SUR for v in values]
    ax.barh(range(len(labels)), values, color=bar_colors, edgecolor=INK, linewidth=0.8, height=0.7)
    for i, v in enumerate(values):
        ax.text(v + 0.08, i, f"{v}/5", va="center", fontsize=8.5, fontweight="bold")
    ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels, fontsize=9.5)
    ax.invert_yaxis(); ax.set_xlim(0, 5.6); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.text(0.01, 1.05, "Technical Capability Profile — specialisation vs frontier",
            transform=ax.transAxes, fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(out_dir / "figures/fig3_capability_matrix.png", dpi=200, bbox_inches="tight")
    plt.close()
    print("Figures OK")


# ==== HTML MANUSCRIPT ==========================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{full_name} — Professional Profile</title>
<style>
@page {{ size: A4; margin: 1.8cm 1.6cm 2.0cm 1.6cm;
  @top-center {{ content: "{full_name} — Professional Profile"; font-family: "DejaVu Serif", serif; font-size: 9pt; color: #6a737d; }}
  @bottom-left {{ content: "Prepared {date} · arifOS federation"; font-family: "DejaVu Serif", serif; font-size: 8pt; color: #8b949e; }}
  @bottom-right {{ content: "Page " counter(page) " / " counter(pages); font-family: "DejaVu Serif", serif; font-size: 8pt; color: #8b949e; }} }}
body {{ font-family: "DejaVu Serif", serif; color: #0d1117; line-height: 1.5; font-size: 10.5pt; }}
.cover {{ text-align: center; margin-top: 2.5cm; page-break-after: always; }}
.cover h1 {{ font-size: 26pt; color: #b8860b; font-weight: bold; }}
.cover .subtitle {{ font-size: 13pt; color: #1f3a5f; font-style: italic; margin-bottom: 1.2cm; }}
.cover .meta {{ font-size: 10pt; color: #4a5568; margin-bottom: 0.2cm; }}
.cover .abstract-box {{ border: 1.4pt solid #b8860b; background: #fff8e7; padding: 0.5cm 0.6cm; margin: 1.5cm 1.8cm 1cm 1.8cm; text-align: left; }}
.cover .keywords {{ font-size: 9pt; color: #4a5568; margin-top: 0.5cm; }}
h1 {{ font-size: 16pt; color: #1f3a5f; border-bottom: 2pt solid #b8860b; padding-bottom: 0.2cm; margin-top: 0.6cm; }}
h2 {{ font-size: 12.5pt; color: #b8860b; margin-top: 0.6cm; }}
img.figure {{ display: block; max-width: 100%; margin: 0.4cm auto 0.6cm auto; }}
.caption {{ font-size: 9pt; color: #4a5568; font-style: italic; text-align: center; margin-bottom: 0.4cm; }}
table.profile {{ border-collapse: collapse; width: 100%; margin: 0.3cm 0; font-size: 10pt; }}
table.profile th {{ background: #1f3a5f; color: white; padding: 0.18cm 0.25cm; text-align: left; border: 0.5pt solid #1f3a5f; }}
table.profile td {{ padding: 0.16cm 0.25cm; border: 0.5pt solid #c0c0c0; vertical-align: top; }}
table.profile tr:nth-child(even) td {{ background: #f5f1e6; }}
.epistemic {{ display: inline-block; font-size: 8.5pt; padding: 1px 6px; border-radius: 3px; font-weight: bold; margin-right: 4px; }}
.epistemic.OBS {{ background: #d4edda; color: #155724; }}
.epistemic.DER {{ background: #cfe2ff; color: #084298; }}
.epistemic.INT {{ background: #fff3cd; color: #856404; }}
.epistemic.SPEC {{ background: #f8d7da; color: #721c24; }}
.callout {{ border-left: 3pt solid #b8860b; background: #fff8e7; padding: 0.3cm 0.5cm; margin: 0.4cm 0; font-size: 10pt; }}
ul {{ margin: 0.2cm 0 0.4cm 0; padding-left: 0.6cm; }}
.footer-motto {{ text-align: center; font-size: 9pt; color: #8b949e; font-style: italic; margin-top: 1cm; }}
</style></head><body>

<div class="cover">
  <h1>{full_name}</h1>
  <div class="subtitle">{subtitle}</div>
  <div class="meta"><strong>{employer}</strong></div>
  <div class="meta">{location}</div>
  <div class="meta">{education}</div>
  <div class="meta" style="margin-top: 0.5cm;"><strong>{years_employer} years</strong> at employer · <strong>{years_industry}+ years</strong> operating · <strong>{concurrent_roles} concurrent</strong> role lineages</div>
  <div class="abstract-box"><strong>Profile summary.</strong> {abstract}</div>
  <div class="keywords"><strong>Keywords:</strong> {keywords}</div>
</div>

<h1>1 · Identity &amp; Lineage</h1>
<p><strong>Full name:</strong> {full_name}<br><strong>Heritage:</strong> {linguistic_heritage}<br><strong>Tertiary education:</strong> {education}<br><strong>Languages:</strong> {languages}</p>

<h1>2 · Career Spine</h1>
<img class="figure" src="figures/fig1_career_timeline.png">
<div class="caption">Figure 1 — Career lineage. Concurrent roles called out explicitly.</div>

<h1>3 · Operating Footprint</h1>
<img class="figure" src="figures/fig2_field_geography.png">
<div class="caption">Figure 2 — Schematic; coordinates indicate relative positioning, not navigational accuracy.</div>

<h1>4 · Technical Capability Profile</h1>
<img class="figure" src="figures/fig3_capability_matrix.png">
<div class="caption">Figure 3 — Self-assessed proficiency. <span class="epistemic OBS">OBS</span> capabilities reflect documented expertise; <span class="epistemic SPEC">SPEC</span> marks the frontier.</div>

<h1>5 · Technical Contributions</h1>
<table class="profile">
<thead><tr>{paper_header}</tr></thead>
<tbody>{paper_rows}</tbody>
</table>

<h1>6 · Sources &amp; Provenance</h1>
<ul>{source_list}</ul>
<div class="callout"><strong>Honest gap:</strong> {honest_gaps_text}</div>

<div class="footer-motto">DITEMPA BUKAN DIBERI · Forged, not given.<br>Profile prepared {date} · arifOS federation</div>

</body></html>
"""


def build_html(out_dir: Path) -> Path:
    paper_header = "".join(f"<th>{c}</th>" for c in SUBJECT["papers"][0])
    paper_rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
                          for r in SUBJECT["papers"][1:])
    source_list = "".join(f"<li><strong>{n}</strong> — {why}</li>" for n, why in SUBJECT["sources"])
    gaps = " · ".join(SUBJECT["honest_gaps"])
    date = datetime.date.today().isoformat()

    html = HTML_TEMPLATE.format(
        full_name=SUBJECT["full_name"], subtitle=SUBJECT["subtitle"],
        employer=SUBJECT["employer"], location=SUBJECT["location"],
        education=SUBJECT["education"], years_employer=SUBJECT["years_employer"],
        years_industry=SUBJECT["years_industry"], concurrent_roles=SUBJECT["concurrent_roles"],
        linguistic_heritage=SUBJECT["linguistic_heritage"], languages=SUBJECT["languages"],
        abstract=SUBJECT["abstract"], keywords=SUBJECT["keywords"],
        paper_header=paper_header, paper_rows=paper_rows,
        source_list=source_list, honest_gaps_text=gaps, date=date,
    )
    out_html = out_dir / "manuscript.html"
    out_html.write_text(html, encoding="utf-8")
    return out_html


def build_pdf(out_dir: Path, html_path: Path):
    pdf_path = out_dir / f'{SUBJECT["full_name"].replace(" ", "_")}_Profile.pdf'
    subprocess.run(["weasyprint", str(html_path), str(pdf_path)],
                   capture_output=True, check=True)
    return pdf_path


def build_receipt(out_dir: Path, pdf_path: Path):
    h = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    receipt = {
        "artifact_id": out_dir.name,
        "filename": pdf_path.name,
        "sha256": h,
        "byte_length": pdf_path.stat().st_size,
        "prepared_for": SUBJECT["full_name"],
        "prepared_by": "arifOS federation",
        "prepared_at": datetime.datetime.now().astimezone().isoformat(),
        "honest_gaps": SUBJECT["honest_gaps"],
    }
    (out_dir / ".receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    return h


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 dossier_template.py <name_slug> <out_dir>")
        sys.exit(1)
    name_slug, out_dir = sys.argv[1], Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "figures").mkdir(exist_ok=True)
    make_figures(out_dir)
    html_path = build_html(out_dir)
    pdf_path = build_pdf(out_dir, html_path)
    h = build_receipt(out_dir, pdf_path)
    print(f"Done. PDF: {pdf_path}, sha256: {h}")


if __name__ == "__main__":
    main()
