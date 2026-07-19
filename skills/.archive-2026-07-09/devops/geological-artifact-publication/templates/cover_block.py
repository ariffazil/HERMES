#!/usr/bin/env python3
"""
Starter template: 2D cross-section + 3D block + timeline in one figure.
Proven 2026-07-03 (Kinabalu Two-Oceanics, 3549×3408 PNG).
Edit the geometry functions for your own cross-section.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.patheffects as pe

# === Edit these for your topic ===
W, D = 400, 80   # horizontal extent, depth (km)
xs = np.linspace(0, W, 401)

def topo(x):
    # Composite Gaussian peaks — replace with your topography
    return (0.6 * np.exp(-((x-90)/18)**2)
          + 1.5 * np.exp(-((x-130)/15)**2)
          + 4.095 * np.exp(-((x-220)/10)**2)  # <-- main peak (Kinabalu)
          + 0.3 * np.exp(-((x-260)/22)**2))

def moho(x):
    return 24 + 8*np.exp(-((x-130)/40)**2) - 2*np.exp(-((x-260)/40)**2)

def oph_top(x):
    return 5 + 0.5*np.exp(-((x-130)/30)**2)

# === Build figure ===
fig = plt.figure(figsize=(20, 13), dpi=180, facecolor='#fbfaf6')
gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.0], height_ratios=[1.0, 0.55],
                      hspace=0.08, wspace=0.05)
ax = fig.add_subplot(gs[0, :])
# ... (paint cross-section here) ...
# === Save ===
plt.savefig('/root/your_block.png', dpi=180, bbox_inches='tight', facecolor='#fbfaf6')
print("Saved /root/your_block.png")
