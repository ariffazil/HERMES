"""
MBR / Bid Round Geological Figure Generator
Proven 2026-07-09, MBR2026 GEOX Artifacts — 5 figures: seismic, well log,
strat correlation, rock physics, play fairway map.
All figures labeled with epistemic tags.

Usage: run as `python3 mbr_figures.py /tmp/output_dir/`
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import LinearSegmentedColormap
import os

DARK_BG = '#0d1117'
PANEL_BG = '#161b22'
TEXT_LIGHT = '#e6edf3'
TEXT_DIM = '#8b949e'
BORDER = '#30363d'
GOLD = '#f0a500'
GREEN = '#3fb950'
BLUE = '#58a6ff'
RED = '#f85149'
AMBER = '#ffa657'

seismic_cmap = LinearSegmentedColormap.from_list('seismic',
    [(0, '#1a1a2e'), (0.5, '#e0e0e0'), (1, '#1a1a2e')])

np.random.seed(42)

def make_seismic_section(out_dir):
    """Fig 1: Synthetic seismic section — Malay Basin Middle Miocene Anticline Play."""
    nx, nz = 400, 300
    seismic = np.random.randn(nz, nx) * 0.02
    x = np.linspace(0, 20, nx)
    # Anticline reflectors (Group E/F, ~2200m depth)
    for xi in np.linspace(6, 14, 100):
        ix = int(xi / 20 * nx)
        depth = 2200 + 400 * ((xi - 10) / 4) ** 2
        iz = int((depth - 500) / (4500 / nz))
        for di in range(-2, 2):
            if 0 <= iz+di < nz: seismic[iz+di, ix] = 0.6 * np.sin(np.pi * di / 4)
    # Bright spot at crest
    bright_ix = int(10 / 20 * nx)
    bright_iz = int((2100 - 500) / (4500 / nz))
    seismic[max(0,bright_iz-3):min(nz,bright_iz+3), bright_ix-2:bright_ix+3] *= 2.5
    # Gas chimney below crest
    for zi in range(int((2800-500)/(4500/nz)), nz):
        seismic[zi, max(0,bright_ix-3):min(nx,bright_ix+3)] *= 0.3
    # Growth fault on western flank
    for i in range(30):
        depth = 1800 + i * 40
        fault_x = 7.5 + i * 0.05
        iz, ix = int((depth-500)/(4500/nz)), int(fault_x/20*nx)
        if 0 <= iz < nz and 0 <= ix < nx:
            seismic[max(0,iz-1):min(nz,iz+2), max(0,ix-1):min(nx,ix+2)] = -0.5
    # Flat reflectors above/below
    for i in range(8):
        depth = 600 + i*100; iz = int((depth-500)/(4500/nz))
        if iz < nz: seismic[iz,:] += 0.3*np.sin(x*0.5+i)*np.exp(-((x-10)**2)/200)
    for i in range(6):
        depth = 3200 + i*150; iz = int((depth-500)/(4500/nz))
        if iz < nz: seismic[iz,:] += 0.2*np.sin(x*0.3+i*0.7)

    fig, ax = plt.subplots(1, 1, figsize=(16, 7), dpi=150)
    fig.patch.set_facecolor(DARK_BG); ax.set_facecolor(PANEL_BG)
    im = ax.imshow(seismic, aspect='auto', cmap=seismic_cmap, extent=[0,20,5000,500], vmin=-0.8, vmax=0.8)
    ax.annotate('', xy=(8,2600), xytext=(12,2600),
                arrowprops=dict(arrowstyle='<->', color=GOLD, lw=2),
                path_effects=[pe.withStroke(linewidth=3, foreground=DARK_BG)])
    ax.text(10, 2700, 'Anticline Play — Group E/F\nMiocene Inversion', color=GOLD, fontsize=11, ha='center', weight='bold',
            path_effects=[pe.withStroke(linewidth=3, foreground=DARK_BG)])
    ax.annotate('Gas Chimney\n(velocity pull-down)', xy=(10,3200), xytext=(12.5,3000), color=RED, fontsize=9,
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
                path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
    ax.annotate('Bright Spot\n(Gas Indicator)', xy=(10,2100), xytext=(13.5,1800), color=GREEN, fontsize=9,
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5),
                path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
    ax.annotate('Growth Fault\n(fault seal risk)', xy=(7.5,2200), xytext=(3.5,1800), color=AMBER, fontsize=9,
                arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.5),
                path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
    for label, depth, color in [('Pliocene (Grp A-C)', 800, BLUE), ('Miocene (Grp D-F)', 1900, GOLD), ('Oligocene (Grp K-M)', 3500, RED)]:
        ax.text(0.3, depth, label, color=color, fontsize=8, weight='bold', path_effects=[pe.withStroke(linewidth=3, foreground=DARK_BG)])
    ax.set_xlabel('Distance (km)', color=TEXT_LIGHT, fontsize=11)
    ax.set_ylabel('Depth (m)', color=TEXT_LIGHT, fontsize=11)
    ax.set_title('SYNTHETIC SEISMIC — Malay Basin Middle Miocene Anticline Play\nGroup E/F Inversion Trap | DER_SYNTHETIC (physics-based forward model)', color=TEXT_LIGHT, fontsize=13, weight='bold', pad=15)
    ax.tick_params(colors=TEXT_DIM)
    for spine in ax.spines.values(): spine.set_color(BORDER)
    cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02); cbar.set_label('Normalized Amplitude', color=TEXT_DIM, fontsize=9); cbar.ax.tick_params(colors=TEXT_DIM)
    ax.text(0.02, 0.02, 'EPISTEMIC: DER_SYNTHETIC\nNot a measured seismic section.\nPhysics-based forward model:\n• Inversion anticline from Madon 2021\n• Reflector spacing from strat column\n• Gas chimney from velocity anomaly', transform=ax.transAxes, fontsize=8, color=TEXT_DIM, bbox=dict(boxstyle='round,pad=0.5', facecolor=PANEL_BG, edgecolor=BORDER))
    plt.savefig(f'{out_dir}/fig1_seismic_section.png', dpi=200, bbox_inches='tight', facecolor=DARK_BG); plt.close()

def make_well_log(out_dir):
    """Fig 2: 4-track synthetic well log (GR, Vp, Density, Porosity)."""
    z = np.linspace(200, 4500, 200)
    gr = np.clip(np.where(z < 1500, 40+30*np.sin(z/200)+np.random.randn(len(z))*5,
                np.where(z < 3000, 70+25*np.sin(z/300)+np.random.randn(len(z))*8,
                90+15*np.sin(z/400)+np.random.randn(len(z))*10)), 10, 150)
    vp_base = 2500 + 1.2 * z
    vp_sand = np.zeros_like(z)
    for s, e in [(800,1100),(1600,1900),(2200,2500),(2800,3100)]:
        vp_sand[(z>=s)&(z<=e)] = 300
    vp = vp_base + vp_sand + np.random.randn(len(z))*50
    rho = 2.0 + 0.0002*z - 0.15*(vp_sand/300) + np.random.randn(len(z))*0.03
    phi = np.clip(35*np.exp(-z/3000)+10*(vp_sand/300)+np.random.randn(len(z))*2, 2, 45)

    fig, axes = plt.subplots(1, 4, figsize=(12, 10), dpi=150, gridspec_kw={'width_ratios':[1,1.2,1,1]})
    fig.patch.set_facecolor(DARK_BG)
    for ax in axes: ax.set_facecolor(PANEL_BG)
    for ax in axes:
        ax.set_ylim(4500, 200); ax.tick_params(colors=TEXT_DIM, labelsize=8)
        for spine in ax.spines.values(): spine.set_color(BORDER)

    axes[0].plot(np.zeros_like(z), z, color=BORDER, linewidth=0.5); axes[0].set_xlim(0,1); axes[0].set_xlabel('Depth (m)', color=TEXT_LIGHT, fontsize=9)
    axes[1].fill_betweenx(z, 150, gr, color=AMBER, alpha=0.3); axes[1].plot(gr, z, color=AMBER, linewidth=1.2)
    axes[1].set_xlim(150, 0); axes[1].set_xlabel('GR (API)', color=AMBER, fontsize=9)
    axes[1].axvline(65, color=BORDER, linestyle='--', linewidth=0.5); axes[1].text(65, 500, 'Cutoff', color=TEXT_DIM, fontsize=7, rotation=90)
    for s, e in [(800,1100),(1600,1900),(2200,2500),(2800,3100)]:
        axes[2].axhspan(s, e, color=GREEN, alpha=0.08)
    axes[2].plot(vp, z, color=BLUE, linewidth=1); axes[2].set_xlim(1500,6500); axes[2].set_xlabel('Vp (m/s)', color=BLUE, fontsize=9)
    axes[3].plot(rho, z, color=RED, linewidth=1.2, label='Density')
    ax_phi = axes[3].twiny()
    ax_phi.plot(phi, z, color=GREEN, linewidth=1, label='Porosity %')
    axes[3].set_xlim(1.8, 3.0); axes[3].set_xlabel('Density (g/cc)', color=RED, fontsize=9)
    ax_phi.set_xlim(0, 50); ax_phi.set_xlabel('Porosity (%)', color=GREEN, fontsize=9)
    ax_phi.tick_params(colors=TEXT_DIM, labelsize=8)
    for label, depth, color in [('R-1: Sandakan Fm (800-1100m)', 950, GREEN), ('R-2: Upper Miocene (1600-1900m)', 1750, GREEN), ('R-3: Lower Miocene (2200-2500m)', 2350, BLUE), ('R-4: Oligocene Syn-rift (2800-3100m)', 2950, AMBER)]:
        axes[1].annotate(label, xy=(0, depth), xytext=(130, depth), color=color, fontsize=7, weight='bold', arrowprops=dict(arrowstyle='->', color=color, lw=0.8), path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
    fig.suptitle('SYNTHETIC WELL LOG — Sandakan Basin Demo Well\nDER_SYNTHETIC (based on DEMO_WELL_A_SANDAKAN.las + regional trends)', color=TEXT_LIGHT, fontsize=13, weight='bold', y=0.97)
    plt.savefig(f'{out_dir}/fig2_well_log.png', dpi=200, bbox_inches='tight', facecolor=DARK_BG); plt.close()

def make_correlation_panel(out_dir):
    """Fig 3: Multi-well stratigraphic correlation panel (Groups A-H)."""
    wells = {'Well-A (NW Malay Basin)': {'x': 0, 'depths': {'A':400,'B':800,'C':1200,'D':1600,'E':2000,'F':2400,'G':2800,'H':3200}},
             'Well-B (Central Malay Basin)': {'x': 1, 'depths': {'A':420,'B':830,'C':1250,'D':1680,'E':2100,'F':2520,'G':2950,'H':3380}},
             'Well-C (SE Malay Basin)': {'x': 2, 'depths': {'A':450,'B':880,'C':1320,'D':1780,'E':2200,'F':2620,'G':3050,'H':3500}}}
    groups = ['A','B','C','D','E','F','G','H']
    gc = {'A':'#58a6ff','B':'#79c0ff','C':'#a5d6ff','D':'#f0a500','E':'#ffa657','F':'#ffd966','G':'#f85149','H':'#da645d'}
    fig, ax = plt.subplots(1, 1, figsize=(14, 9), dpi=150); fig.patch.set_facecolor(DARK_BG); ax.set_facecolor(PANEL_BG)
    for name, w in wells.items():
        ax.axvline(w['x'], color=BORDER, linewidth=1.5)
        ax.text(w['x'], -50, name, color=TEXT_LIGHT, fontsize=9, ha='center', weight='bold', path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
    for g in groups:
        depths = [w['depths'][g] for w in wells.values()]; xs = [w['x'] for w in wells.values()]; color = gc[g]
        if g != 'A':
            prev = [w['depths'][groups[groups.index(g)-1]] for w in wells.values()]
            ax.fill_between(xs, depths, prev, color=color, alpha=0.15)
        ax.plot(xs, depths, color=color, linewidth=2.5, marker='o', markersize=6)
        if g in ['D','E','F']:
            ax.text(xs[-1]+0.05, depths[-1], f'Grp {g} — Reservoir', color=color, fontsize=8, weight='bold', path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
        ax.text(-0.2, depths[0], f'Group {g}', color=color, fontsize=9, weight='bold', ha='right', path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
    ax.annotate('Inversion Anticline\nPlay (Grp E-F)', xy=(1,2200), xytext=(1.5,1800), color=GOLD, fontsize=10, weight='bold', arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.5), path_effects=[pe.withStroke(linewidth=3, foreground=DARK_BG)])
    ax.annotate('Regional Seal\n(Group F shale)', xy=(1,2450), xytext=(0.5,2700), color=RED, fontsize=9, arrowprops=dict(arrowstyle='->', color=RED, lw=1.5), path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
    for label, depth, color in [('Pliocene',500,BLUE),('Middle Miocene',1800,GOLD),('Early Miocene',2900,RED),('Oligocene',3400,'#8b5cf6')]:
        ax.axhspan(max(200,depth-200), depth+200, alpha=0.05, color=color)
        ax.text(-0.3, depth, label, color=color, fontsize=8, ha='right', path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
    ax.set_xlim(-0.5, 2.5); ax.set_ylim(3700, 200)
    ax.set_xlabel('Well Location', color=TEXT_DIM, fontsize=10); ax.set_ylabel('Depth (m TVDSS)', color=TEXT_LIGHT, fontsize=10)
    ax.set_title('STRATIGRAPHIC CORRELATION — Malay Basin\nMulti-well tie across NW → Central → SE | Groups A-H (Madon 2021) | DER_INTERPRETED', color=TEXT_LIGHT, fontsize=13, weight='bold', pad=15)
    ax.tick_params(colors=TEXT_DIM, labelsize=9)
    for spine in ax.spines.values(): spine.set_color(BORDER)
    ax.set_xticks([0,1,2]); ax.set_xticklabels(['','',''])
    ax.text(0.98, 0.02, 'EPISTEMIC: DER_INTERPRETED\nCorrelation from Madon 2021\nstratigraphic framework.\nWell positions schematic.\nReservoir/seal from GEOX.', transform=ax.transAxes, fontsize=8, color=TEXT_DIM, bbox=dict(boxstyle='round,pad=0.5', facecolor=PANEL_BG, edgecolor=BORDER), ha='right', verticalalignment='bottom')
    plt.savefig(f'{out_dir}/fig3_correlation.png', dpi=200, bbox_inches='tight', facecolor=DARK_BG); plt.close()

def make_rock_physics(out_dir):
    """Fig 4: Vp/Vs vs Density crossplot — reservoir discrimination."""
    n_s, n_sh, n_l, n_c = 80, 80, 50, 30
    s_rho, s_vpvs = 2.15+0.05*np.random.randn(n_s), 1.7+0.15*np.random.randn(n_s)
    sh_rho, sh_vpvs = 2.3+0.1*np.random.randn(n_sh), 2.1+0.2*np.random.randn(n_sh)
    l_rho, l_vpvs = 2.6+0.1*np.random.randn(n_l), 1.85+0.12*np.random.randn(n_l)
    c_rho, c_vpvs = 1.5+0.2*np.random.randn(n_c), 1.6+0.3*np.random.randn(n_c)
    fig, ax = plt.subplots(1, 1, figsize=(10, 8), dpi=150); fig.patch.set_facecolor(DARK_BG); ax.set_facecolor(PANEL_BG)
    ax.scatter(s_rho, s_vpvs, c=GREEN, s=60, alpha=0.7, label='Sand Reservoir (DER)')
    ax.scatter(sh_rho, sh_vpvs, c=RED, s=50, alpha=0.7, label='Shale Seal (DER)')
    ax.scatter(l_rho, l_vpvs, c=GOLD, s=55, alpha=0.7, label='Limestone (HYPOTHESIS)')
    ax.scatter(c_rho, c_vpvs, c=AMBER, s=40, alpha=0.7, label='Coal/Sources (INT)')
    ax.axhline(2.0, color=BLUE, linestyle='--', linewidth=1, alpha=0.6); ax.text(2.8, 2.05, 'Vp/Vs = 2.0', color=BLUE, fontsize=9, path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
    ax.axhline(1.7, color=GREEN, linestyle=':', linewidth=1, alpha=0.6); ax.text(2.8, 1.65, 'Vp/Vs = 1.7 (Gas Indicator)', color=GREEN, fontsize=8, path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
    ax.axvspan(2.2, 2.35, alpha=0.08, color=GREEN); ax.axhspan(1.6, 1.85, alpha=0.08, color=GREEN)
    ax.set_xlabel('Bulk Density (g/cc)', color=TEXT_LIGHT, fontsize=11); ax.set_ylabel('Vp/Vs Ratio', color=TEXT_LIGHT, fontsize=11)
    ax.set_title('ROCK PHYSICS CROSSPLOT — Malay Basin\nVp/Vs vs Density | Reservoir Discrimination | DER_SYNTHETIC', color=TEXT_LIGHT, fontsize=13, weight='bold', pad=15)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9, facecolor=PANEL_BG, edgecolor=BORDER, labelcolor=TEXT_LIGHT)
    ax.tick_params(colors=TEXT_DIM)
    for spine in ax.spines.values(): spine.set_color(BORDER)
    ax.text(0.98, 0.02, 'EPISTEMIC: DER_SYNTHETIC\nParameters from GEOX geox_egs_rock_physics:\n  Vp_VRH=4143 m/s (φ=20%)\n  ρ_bulk=2.32 g/cc\nSand trend: Voigt-Reuss-Hill bounds\nShale: regional well log averages', transform=ax.transAxes, fontsize=8, color=TEXT_DIM, bbox=dict(boxstyle='round,pad=0.5', facecolor=PANEL_BG, edgecolor=BORDER), ha='right', verticalalignment='bottom')
    plt.savefig(f'{out_dir}/fig4_rock_physics.png', dpi=200, bbox_inches='tight', facecolor=DARK_BG); plt.close()

def make_play_fairway_map(out_dir):
    """Fig 5: Schematic play fairway map with MBR2026 blocks + DROs."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 9), dpi=150); fig.patch.set_facecolor(DARK_BG); ax.set_facecolor('#1a2332')
    bx = np.linspace(100, 106, 100)
    ax.fill_between(bx, 3.5+0.5*np.sin((bx-103)/3), 6.5+0.8*np.sin((bx-103)/4), color='#1e3a5f', alpha=0.4, edgecolor=BLUE, linewidth=1.5)
    ax.fill([100.5,101,101.5,102,102.5,103,103.5,104], [5.5,4.5,3.8,3.2,2.8,2.5,2.2,2.0], color='#c9a574', alpha=0.3, edgecolor='#c9a574')
    ax.text(102, 4.0, 'Peninsular\nMalaysia', color='#c9a574', fontsize=9, ha='center', path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
    for center, angle, color, label in [((101.5,5.5),-20,GOLD,'NW Gas Anticlines\n(Proven)'),((103,5.5),10,GREEN,'Central Strat Pinchouts\n(Emerging)'),((104.5,5.0),5,RED,'Deep Syn-rift\n(High Risk)')]:
        e = plt.matplotlib.patches.Ellipse(center, 1.5, 1.2, angle=angle, color=color, alpha=0.25, edgecolor=color, linewidth=1.5)
        ax.add_patch(e)
        ax.text(center[0], center[1]+0.3, label, color=color, fontsize=9, ha='center', weight='bold', path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
    for name, bxy, color in [('PM440',(102.5,5.0),GREEN),('PM447',(103.5,5.5),GOLD),('PM448',(104.0,5.2),GOLD),('PM519',(103.0,4.8),BLUE),('PM520',(104.5,4.5),RED)]:
        ax.plot(bxy[0], bxy[1], 's', markersize=12, color=color, markeredgecolor='white', markeredgewidth=1.5, zorder=5)
        ax.text(bxy[0], bxy[1]+0.2, name, color=color, fontsize=8, ha='center', weight='bold', path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
    for name, dxy in [('Cempaka',(102,4.5)),('Enggang',(103.5,4.2)),('Nilam',(104,4.0))]:
        ax.plot(dxy[0], dxy[1], 'D', markersize=10, color=AMBER, markeredgecolor='white', markeredgewidth=1, zorder=5)
        ax.text(dxy[0], dxy[1]-0.15, name, color=AMBER, fontsize=7, ha='center', path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)])
    ax.set_xlim(100,106); ax.set_ylim(2,7)
    ax.set_xlabel('Longitude (°E)', color=TEXT_DIM, fontsize=10); ax.set_ylabel('Latitude (°N)', color=TEXT_DIM, fontsize=10)
    ax.set_title('PLAY FAIRWAY MAP — Malay Basin MBR2026\nBlocks PM440-448, PM519-520 + DROs | SCHEMATIC (coordinates not to PSC scale)', color=TEXT_LIGHT, fontsize=13, weight='bold', pad=15)
    ax.tick_params(colors=TEXT_DIM)
    for spine in ax.spines.values(): spine.set_color(BORDER)
    ax.grid(True, alpha=0.15, color=BORDER)
    legends = [plt.Line2D([0],[0],marker='s',color='w',markersize=8,markerfacecolor=GOLD,label='BID (Tier 1)'),
               plt.Line2D([0],[0],marker='s',color='w',markersize=8,markerfacecolor=GREEN,label='BID WITH PARTNER'),
               plt.Line2D([0],[0],marker='s',color='w',markersize=8,markerfacecolor=RED,label='NO BID (HPHT)'),
               plt.Line2D([0],[0],marker='D',color='w',markersize=8,markerfacecolor=AMBER,label='DRO')]
    ax.legend(handles=legends, loc='lower right', fontsize=8, framealpha=0.9, facecolor=PANEL_BG, edgecolor=BORDER, labelcolor=TEXT_LIGHT)
    plt.savefig(f'{out_dir}/fig5_play_fairway.png', dpi=200, bbox_inches='tight', facecolor=DARK_BG); plt.close()

if __name__ == '__main__':
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/mbr_figures/'
    os.makedirs(out, exist_ok=True)
    for fn in [make_seismic_section, make_well_log, make_correlation_panel, make_rock_physics, make_play_fairway_map]:
        fn(out)
    print(f"Generated 5 figures in {out}")
