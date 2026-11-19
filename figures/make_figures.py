"""Draw the two README figures of certified-dark-core from the float-map data the repository ships.

Usage:  python figures/make_figures.py [--png]        (run from the repository root)
Needs Python 3.11 and matplotlib 3.11. Writes figures/band-map.svg and figures/krein-collision.svg.
(scorecard.svg at the repository root is drawn by tools/make_scorecard.py.)

EVERYTHING PLOTTED HERE IS FLOAT (double-precision B-spline Galerkin, checked only by changing the resolution).
Nothing in these two figures is certified. The data:
  data/band-map/MAP.json      coarse sweep (sigma0 = 0.30 .. 5.00, step 0.05, L = 0..6): coarse_table[*].maxre
                              fine sweep   (sigma0 = 1.30 .. 2.40, step 0.01, L = 0..14): fine_table[*].maxre
                              refined edges: edges.lo1.bracket, edges.hi1.bracket
  data/band-map/sw_f1.json,   fine sweep, full records: per sigma0 and L, the internal modes w with their Krein
  data/band-map/sw_f2.json    signs ("low": [w, sign]) and the growing eigenvalues ("unst": [Re, Im])
  data/band-map/edge_lo1.json, edge_hi1.json   the +-1e-4 and +-0.002 offsets around each refined edge
The published band of arXiv:2402.07998 (1.55 to 2.07, Fig. 8 caption) is drawn for comparison.
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BG, BORDER, GRID, AXC, TXT, ACC = "#1c2026", "#2f353d", "#22272e", "#9aa4ae", "#e8edf2", "#39ff14"
C_L0, C_L2, C_L3, C_L4 = "#3987e5", "#d95926", "#9085e9", "#c98500"   # validated categorical order (dark surface)
W_IN = 12.5
PNG = "--png" in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "figures")

plt.rcParams.update({
    "svg.fonttype": "none", "svg.hashsalt": "moki-julio",
    "font.family": "sans-serif", "font.sans-serif": ["Segoe UI", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 15, "axes.labelsize": 16, "xtick.labelsize": 14, "ytick.labelsize": 14,
    "axes.facecolor": BG, "figure.facecolor": "none", "savefig.facecolor": "none",
    "axes.edgecolor": AXC, "axes.labelcolor": TXT, "xtick.color": AXC, "ytick.color": AXC,
    "text.color": TXT, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 1.0,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
    "legend.fontsize": 13, "lines.linewidth": 2.0, "axes.axisbelow": True,
})


def new_fig(h_in):
    fig = plt.figure(figsize=(W_IN, h_in))
    fig.patches.append(FancyBboxPatch((0.004, 0.006), 0.992, 0.988, boxstyle="round,pad=0,rounding_size=0.015",
                                      transform=fig.transFigure, facecolor=BG, edgecolor=BORDER, linewidth=1.5,
                                      zorder=-10))
    return fig


def title(fig, main, sub):
    h = fig.get_figheight()
    fig.text(0.035, 1 - 0.40 / h, main, fontsize=20, fontweight="bold", color=TXT, va="top")
    fig.text(0.035, 1 - 0.84 / h, sub, fontsize=14, color=AXC, va="top")


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": None})
    with open(path, encoding="utf-8") as fh:
        svg = fh.read().replace("font-family: 'Segoe UI';", "font-family: 'Segoe UI', 'Helvetica', 'Arial', sans-serif;")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)
    if PNG:
        prev = os.path.join(ROOT, "_preview")
        os.makedirs(prev, exist_ok=True)
        fig.savefig(os.path.join(prev, name.replace(".svg", ".png")), format="png", dpi=110)
    plt.close(fig)


def load(rel):
    return json.load(open(os.path.join(ROOT, rel), encoding="utf-8"))


def float_tag(ax):
    ax.text(0.99, 0.97, "FLOAT MAP - not certified", transform=ax.transAxes, ha="right", va="top", fontsize=12,
            color=ACC, fontweight="bold")


def fig_band():
    M = load("data/band-map/MAP.json")
    lo = M["edges"]["lo1"]["bracket"]
    hi = M["edges"]["hi1"]["bracket"]
    s_lo, s_hi = sum(lo) / 2, sum(hi) / 2
    fig = new_fig(6.4)
    title(fig, "Where the one-shell core is stable (float map)",
          "Largest growth rate max Re(lambda) per angular sector L against the central amplitude sigma0. "
          "Zero = no growing mode.")
    axA = fig.add_axes([0.075, 0.13, 0.40, 0.66])
    axB = fig.add_axes([0.565, 0.13, 0.40, 0.66])
    # coarse: L = 0, 2, 3, 4 (L = 1, 5, 6 never unstable on the grid)
    rows = M["coarse_table"]
    xs = [r["sig0"] for r in rows]
    for L, c in (("0", C_L0), ("2", C_L2), ("3", C_L3), ("4", C_L4)):
        ys = [r["maxre"][L] if r["n_unst"][L] else 0.0 for r in rows]
        axA.plot(xs, ys, color=c, lw=2)
        pos, ha = {"0": ((0.75, 0.10), "center"), "2": ((4.95, 0.50), "right"), "3": ((3.30, 1.05), "right"),
                   "4": ((4.32, 0.90), "left")}[L]
        axA.text(pos[0], pos[1], "L = %s" % L, ha=ha, fontsize=13, color=TXT)
    axA.axvspan(s_lo, s_hi, color=ACC, alpha=0.12, lw=0)
    axA.set_xlabel("sigma0 (coarse sweep, step 0.05)")
    axA.set_ylabel("max Re(lambda)")
    axA.set_xlim(0.3, 5.0)
    axA.set_ylim(0, None)
    axA.text(0.02, 0.88, "L = 1, 5, 6: never unstable", transform=axA.transAxes, va="top", fontsize=12, color=AXC)
    float_tag(axA)
    # fine: L = 0 and L = 2 (every other L up to 14 stays at rounding level)
    rows = M["fine_table"]
    xs = [r["sig0"] for r in rows]
    for L, c in (("0", C_L0), ("2", C_L2)):
        ys = [r["maxre"][L] if r["n_unst"][L] else 0.0 for r in rows]
        axB.plot(xs, ys, color=c, lw=2, marker="o", ms=3.0)
    axB.axvspan(s_lo, s_hi, color=ACC, alpha=0.15, lw=0)
    for x in (1.55, 2.07):
        axB.axvline(x, color=AXC, lw=1.2, ls="--")
    axB.text(1.55, 0.195, " 1.55", fontsize=12, color=AXC)
    axB.text(2.07, 0.195, " 2.07", fontsize=12, color=AXC)
    axB.text(1.80, 0.17, "published band\n(dashed, 2402.07998)", ha="center", fontsize=12, color=AXC)
    axB.text((s_lo + s_hi) / 2, 0.09, "float band\n[%.4f, %.4f]" % (s_lo, s_hi), ha="center", fontsize=13,
             color=ACC, fontweight="bold")
    axB.text(1.33, 0.065, "L = 0", fontsize=13, color=TXT)
    axB.text(2.25, 0.12, "L = 2", fontsize=13, color=TXT)
    axB.set_xlabel("sigma0 (fine sweep, step 0.01, L = 0..14)")
    axB.set_xlim(1.3, 2.4)
    axB.set_ylim(0, 0.22)
    float_tag(axB)
    save(fig, "band-map.svg")


# The sw_f1 rows at sigma0 = 1.43 and 1.79 carry a bogus background (E = -0.034 and -0.105: the tail started on a grid
# sample at the node; data/band-map/MAP.md, "Engine", change 2). MAP.json was rebuilt from recomputed points; the raw
# sweep rows were not, so they are skipped here.
BAD_SW = (1.43, 1.79)


def krein_rows(L):
    out = []
    for f in ("data/band-map/sw_f1.json", "data/band-map/sw_f2.json"):
        for r in load(f):
            if any(abs(r["sig0"] - b) < 1e-9 for b in BAD_SW):
                continue
            d = r["L"][L]
            low = d["low"]
            neg = [w for w, s in low if s < 0]
            rec = {"s": r["sig0"], "neg": None, "pos": None, "re": None, "im": None}
            if neg:
                wn = neg[0]
                rec["neg"] = wn
                above = [w for w, s in low if s > 0 and w > wn]
                rec["pos"] = min(above) if above else None
            if d["unst"]:
                rec["re"], rec["im"] = d["unst"][0]
            out.append(rec)
    return sorted(out, key=lambda x: x["s"])


def fig_krein():
    M = load("data/band-map/MAP.json")
    fig = new_fig(7.6)
    title(fig, "How each edge breaks: two oscillations meet (float)",
          "Krein collision: a negative-energy mode and a positive-energy mode merge and leave the axis as a growing pair.")
    panels = [("0", "lower edge, L = 0", (1.30, 2.40), M["edges"]["lo1"]["bracket"]),
              ("2", "upper edge, L = 2", (1.30, 2.40), M["edges"]["hi1"]["bracket"])]
    for k, (L, name, xl, br) in enumerate(panels):
        x0 = 0.075 + k * 0.49
        axT = fig.add_axes([x0, 0.36, 0.40, 0.40])
        axR = fig.add_axes([x0, 0.10, 0.40, 0.18], sharex=axT)
        rows = krein_rows(L)
        s = [r["s"] for r in rows]
        axT.plot(s, [r["neg"] for r in rows], color=C_L2, lw=2, marker="o", ms=3)
        axT.plot(s, [r["pos"] for r in rows], color=C_L0, lw=2, marker="o", ms=3)
        axT.plot(s, [r["im"] for r in rows], color=C_L3, lw=2.6)
        axR.plot(s, [r["re"] if r["re"] is not None else 0.0 for r in rows], color=C_L3, lw=2.6)
        e = sum(br) / 2
        for ax in (axT, axR):
            ax.axvline(e, color=ACC, lw=1.2, ls="--")
        axT.set_title(name, fontsize=15, color=TXT, loc="left")
        axT.set_ylabel("frequency w = Im(lambda)")
        axR.set_ylabel("Re(lambda)")
        axR.set_xlabel("sigma0")
        axT.tick_params(labelbottom=False)
        axT.set_xlim(*xl)
        float_tag(axT)
        axT.text(e, axT.get_ylim()[1] * 0.02 + axT.get_ylim()[0] * 0.98, " edge %.7f" % e, fontsize=12, color=ACC)
    # direct labels (identity is never colour alone)
    fig.text(0.035, 0.835, "orange: negative-Krein mode   blue: its positive-Krein partner   violet: the merged growing "
             "pair (Im above, Re below)", fontsize=13, color=TXT)
    save(fig, "krein-collision.svg")


if __name__ == "__main__":
    fig_band()
    fig_krein()
    print("figures written: band-map.svg, krein-collision.svg")
