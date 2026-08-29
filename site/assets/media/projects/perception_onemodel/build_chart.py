# -*- coding: utf-8 -*-
"""
Multi-task Static Perception · Training-set Iteration (Mar – Dec 2025)
Homologous (co-annotated) vs. heterogeneous (task-specific) composition.
A faint "homologous frontier" polyline traces the nested core:
    LB/RE/RM/CL 4.36M  ⊃  +GoalPoint 3.36M  ⊃  +GRE 1.10M
Output: static_datasets_iteration.gif
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import to_rgb
from matplotlib.transforms import blended_transform_factory
from matplotlib.animation import FuncAnimation, PillowWriter
from datetime import date, timedelta

# ============================== style ==============================
plt.rcParams["font.family"] = "DejaVu Sans"      # swap to a CJK font to show Chinese
BG, TEXT, MUTED, FAINT, ACCENT = "#060708", "#EEF2F8", "#6B7689", "#39414F", "#5B8CFF"

TASKS = ["LaneBoundary", "RoadEdge", "RoadMarker", "Centerline", "GoalPoint", "GRE", "Freespace"]
DISPLAY = {
    "LaneBoundary": "Lane Boundary", "RoadEdge": "Road Edge", "RoadMarker": "Road Marker",
    "Centerline": "Centerline", "GoalPoint": "Goal Point", "GRE": "GRE", "Freespace": "Freespace",
}
COLOR = {                                        # spread across the hue wheel, high contrast on black
    "LaneBoundary": "#5B8CFF", "RoadEdge": "#34D399", "RoadMarker": "#22D3EE",
    "Centerline": "#A78BFA", "GoalPoint": "#FB7185", "GRE": "#FB923C", "Freespace": "#FBBF24",
}

# ============================== data model ==============================
# Final HOMOLOGOUS (co-annotated) frames — the nested core you described
HOMO = {
    "LaneBoundary": 4_360_000, "RoadEdge": 4_360_000, "RoadMarker": 4_360_000,
    "Centerline":   4_360_000, "GoalPoint": 3_360_000, "GRE": 1_100_000, "Freespace": 0,
}
# Final HETEROGENEOUS (task-specific) frames
HET = {
    "LaneBoundary": 520_000, "RoadEdge": 400_000, "RoadMarker": 480_000,
    "Centerline":   660_000, "GoalPoint": 440_000, "GRE": 1_020_000, "Freespace": 1_560_000,
}                                                # GRE total = 1.10M + 1.02M = 2.12M  ✓ (200多万)
INTRO = {                                        # cycle at which each task enters the loop
    "LaneBoundary": 0, "RoadEdge": 0, "RoadMarker": 0, "Centerline": 0,
    "Freespace": 4, "GoalPoint": 8, "GRE": 14,
}
BASE_FRAC = 0.22                                 # baseline tasks already hold this fraction at cycle 0

N_CYCLES = 20
START, END = date(2025, 3, 1), date(2025, 12, 31)
SPAN = (END - START).days

# ============================== helpers ==============================
def lighten(c, a=0.5):
    r = to_rgb(c); return tuple(x + (1 - x) * a for x in r)

def fmt(v):
    v = max(v, 0)
    if v >= 1e6: return f"{v/1e6:.2f}M"
    if v >= 1e3: return f"{v/1e3:.0f}K"
    return str(int(round(v)))

def fmt_tick(v):
    return f"{v/1e6:g}M" if v >= 1e6 else f"{v/1e3:g}K"

def nice_step(xmax, n=6):
    raw = xmax / n; mag = 10 ** np.floor(np.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if m * mag >= raw: return m * mag
    return 10 * mag

def ease(t):                                     # smoothstep (frame easing)
    t = min(max(t, 0.0), 1.0); return t * t * (3 - 2 * t)

def ease_out(p, k=1.8):                           # saturating growth
    p = np.clip(p, 0, 1); return 1 - (1 - p) ** k

def hard_frac(c, task):                           # hard-case share grows as the set matures
    f = 0.06 + 0.18 * (c / N_CYCLES)
    if task == "GRE":          f *= 1.5
    elif task == "GoalPoint":  f *= 1.10
    return min(f, 0.5)

# ---- build cumulative curves (programmatic, diminishing returns) ----
def build(task):
    s, H, E = INTRO[task], HOMO[task], HET[task]
    homo = np.zeros(N_CYCLES + 1); het = np.zeros(N_CYCLES + 1)
    if s == 0:                                    # baseline task: starts at BASE_FRAC, grows to 1
        for c in range(N_CYCLES + 1):
            f = BASE_FRAC + (1 - BASE_FRAC) * ease_out(c / N_CYCLES)
            homo[c], het[c] = H * f, E * f
    else:                                         # introduced later: first batch lands at cycle s
        for c in range(s, N_CYCLES + 1):
            f = ease_out((c - s + 1) / (N_CYCLES - s + 1))
            homo[c], het[c] = H * f, E * f
    return homo, het

HOMO_CUM, HET_CUM = {}, {}
for t in TASKS:
    HOMO_CUM[t], HET_CUM[t] = build(t)
TOT_CUM  = {t: HOMO_CUM[t] + HET_CUM[t] for t in TASKS}
HARD_CUM = {t: np.array([TOT_CUM[t][c] * hard_frac(c, t) for c in range(N_CYCLES + 1)]) for t in TASKS}

INC = {}
for t in TASKS:
    a = np.zeros(N_CYCLES + 1); a[1:] = np.diff(TOT_CUM[t]); INC[t] = a
DTOT  = np.array([0.0] + [sum(INC[t][c] for t in TASKS) for c in range(1, N_CYCLES + 1)])
DHARD = np.array([0.0] + [sum(HARD_CUM[t][c] - HARD_CUM[t][c - 1] for t in TASKS) for c in range(1, N_CYCLES + 1)])

XMAX = max(TOT_CUM[t][-1] for t in TASKS) * 1.16
STEP = nice_step(XMAX)
Y_TOP, HH = 6.6, 0.30

# ============================== frame schedule ==============================
T_INIT, T_TRANS, T_HOLD, T_OUT = 8, 5, 3, 14
schedule = [(0, 0, 1.0, "hold", 0)] * T_INIT
for k in range(1, N_CYCLES + 1):
    schedule += [(k - 1, k, (f + 1) / T_TRANS, "trans", k) for f in range(T_TRANS)]
    schedule += [(k, k, 1.0, "hold", k)] * T_HOLD
schedule += [(N_CYCLES, N_CYCLES, 1.0, "hold", N_CYCLES)] * T_OUT
N_FRAMES = len(schedule)

def caption(b):
    if b == 0:
        bl = sum(TOT_CUM[t][0] for t in TASKS)
        nb = sum(TOT_CUM[t][0] > 1 for t in TASKS)
        return f"Baseline established      ·      {nb} base tasks      ·      {bl/1e6:.2f}M frames"
    s = f"Cycle {b:02d}/{N_CYCLES}      +{fmt(DTOT[b])} frames      ·      hard cases  +{fmt(DHARD[b])}"
    nt_ = [DISPLAY[t] for t in TASKS if INTRO[t] == b]
    if nt_:
        s += "        ●  new task:  " + ", ".join(nt_)
    return s

# ============================== canvas ==============================
fig = plt.figure(figsize=(10, 5.8), facecolor=BG, dpi=100)

ov = fig.add_axes([0, 0, 1, 1]); ov.set_xlim(0, 1); ov.set_ylim(0, 1); ov.axis("off")
# soft radial glow (premium depth on near-black)
def make_glow(n=220, cx=0.5, cy=0.80, rad=0.52, power=2.2):
    yy, xx = np.mgrid[0:n, 0:n].astype(float)
    xn, yn = xx / (n - 1), 1 - yy / (n - 1)
    g = np.clip(1 - np.sqrt((xn - cx) ** 2 + (yn - cy) ** 2) / rad, 0, 1) ** power
    img = np.zeros((n, n, 4)); img[..., :3] = to_rgb(ACCENT); img[..., 3] = g * 0.10
    return img
ov.imshow(make_glow(), extent=[0, 1, 0, 1], origin="upper", zorder=-5, aspect="auto", interpolation="bilinear")
ov.add_patch(Rectangle((0.05, 0.892), 0.005, 0.05, color=ACCENT))           # title accent bar
ov.plot([0.05, 0.95], [0.873, 0.873], color=FAINT, lw=0.8, alpha=0.55)      # header divider

ax = fig.add_axes([0.205, 0.205, 0.73, 0.43]); ax.set_facecolor("none")
prog = fig.add_axes([0.205, 0.145, 0.73, 0.0075]); prog.set_xlim(0, 1); prog.set_ylim(0, 1); prog.axis("off")
prog.add_patch(Rectangle((0, 0), 1, 1, color=TEXT, alpha=0.07))
prog_fill = prog.add_patch(Rectangle((0, 0), 0.0, 1, color=ACCENT))

# static text
fig.text(0.078, 0.928, "MULTI-TASK  STATIC  PERCEPTION", color=TEXT, fontsize=14.5, fontweight="bold")
fig.text(0.078, 0.898, "Training-set iteration   ·   Mar – Dec 2025   ·   20 cycles", color=MUTED, fontsize=8.5)
fig.text(0.50, 0.842, "TOTAL   ANNOTATION   FRAMES", color=MUTED, fontsize=9, ha="center")
fig.text(0.205, 0.658, "Bars:  solid = homologous (co-annotated)    ·    faded = task-specific (heterogeneous)",
         color=MUTED, fontsize=7.5, ha="left")
fig.text(0.205, 0.118, "Mar 2025", color=MUTED, fontsize=7.5, ha="left")
fig.text(0.935, 0.118, "Dec 2025", color=MUTED, fontsize=7.5, ha="right")

# dynamic text
tx_date  = fig.text(0.945, 0.928, "", color=TEXT,   fontsize=11.5, ha="right", fontweight="bold")
tx_cycle = fig.text(0.945, 0.898, "", color=ACCENT, fontsize=8.5,  ha="right", fontweight="bold")
tx_total = fig.text(0.50, 0.775, "", color=TEXT, fontsize=33, ha="center", va="center", fontweight="bold")
tx_homo  = fig.text(0.31, 0.708, "", color="#C2CBDA", fontsize=9, ha="center")
tx_het   = fig.text(0.50, 0.708, "", color="#7A8493", fontsize=9, ha="center")
tx_hard  = fig.text(0.69, 0.708, "", color="#A2873F", fontsize=9, ha="center")
tx_cap   = fig.text(0.57, 0.050, "", color="#9AA4B4", fontsize=9, ha="center")

# ============================== per frame ==============================
def update(i):
    a, b, t, kind, k = schedule[i]
    e   = ease(t) if kind == "trans" else 1.0
    pos = a + (b - a) * e

    homo = {x: HOMO_CUM[x][a] + (HOMO_CUM[x][b] - HOMO_CUM[x][a]) * e for x in TASKS}
    het  = {x: HET_CUM[x][a]  + (HET_CUM[x][b]  - HET_CUM[x][a])  * e for x in TASKS}
    hard = {x: HARD_CUM[x][a] + (HARD_CUM[x][b] - HARD_CUM[x][a]) * e for x in TASKS}
    tot  = {x: homo[x] + het[x] for x in TASKS}
    Th, Te, Td = sum(homo.values()), sum(het.values()), sum(hard.values())
    Tt = Th + Te

    ax.clear(); ax.set_facecolor("none")
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(0, XMAX); ax.set_ylim(-0.95, 7.35)

    ax.plot([0, 0], [0.15, 7.05], color=TEXT, alpha=0.14, lw=1, zorder=0)
    for gx in np.arange(STEP, XMAX, STEP):
        ax.plot([gx, gx], [0.15, 7.05], color=TEXT, alpha=0.045, lw=1, zorder=0)
        ax.text(gx, -0.55, fmt_tick(gx), ha="center", va="top", color=MUTED, fontsize=7, alpha=0.6)

    nt = blended_transform_factory(ax.transAxes, ax.transData)
    pulse = 0.5 + 0.4 * np.sin(i * 0.45)
    contour = []
    for s, x in enumerate(TASKS):
        v = tot[x]
        if v <= 1: continue
        y, c = Y_TOP - s, COLOR[x]
        fa = e if (kind == "trans" and b == INTRO[x]) else 1.0
        hv, ev, dv = homo[x], het[x], hard[x]
        ax.add_patch(Rectangle((0, y - HH - 0.07), v, 2 * HH + 0.14, color=c, alpha=0.05 * fa, lw=0, zorder=1))     # halo
        if hv > 1:                                                                                                  # homologous (solid)
            ax.add_patch(Rectangle((0, y - HH), hv, 2 * HH, color=c, alpha=0.92 * fa, lw=0, zorder=2))
        if ev > 1:                                                                                                  # heterogeneous (faded)
            ax.add_patch(Rectangle((hv, y - HH), ev, 2 * HH, color=c, alpha=0.32 * fa, lw=0, zorder=2))
            ax.plot([hv, v], [y + HH, y + HH], color=c, alpha=0.55 * fa, lw=0.8, zorder=3)
            ax.plot([hv, v], [y - HH, y - HH], color=c, alpha=0.55 * fa, lw=0.8, zorder=3)
        if dv > 1:                                                                                                  # hard-case strip
            ax.add_patch(Rectangle((0, y - HH - 0.135), dv, 0.06, color=lighten(c, 0.30), alpha=0.85 * fa, lw=0, zorder=3))
        ew = 0.006 * XMAX                                                                                           # pulsing frontier
        ax.add_patch(Rectangle((max(v - ew, 0), y - HH), min(ew, v), 2 * HH, color="#FFFFFF", alpha=0.42 * pulse * fa, lw=0, zorder=4))
        ax.text(-0.015, y, DISPLAY[x], transform=nt, ha="right", va="center", color=lighten(c, 0.40), fontsize=8.5, alpha=fa, zorder=5)
        ax.text(v + 0.012 * XMAX, y, fmt(v), ha="left", va="center", color=lighten(c, 0.55), fontsize=9, fontweight="bold", alpha=fa, zorder=5)
        if kind == "hold" and k >= 1 and INC[x][k] > 1:
            ax.text(v + 0.012 * XMAX, y + 0.36, "+" + fmt(INC[x][k]), ha="left", va="center", color=lighten(c, 0.6), fontsize=7, alpha=0.85, zorder=5)
        contour.append((hv, y))

    if len(contour) >= 2:                                                                                           # homologous frontier (nesting)
        cxs, cys = [p[0] for p in contour], [p[1] for p in contour]
        ax.plot(cxs, cys, color="#9AA6BC", alpha=0.32, lw=1.1, zorder=3, solid_capstyle="round")
        ax.scatter(cxs, cys, s=9, color="#B7C0D2", alpha=0.45, zorder=4, edgecolors="none")

    d = START + timedelta(days=int(round(SPAN * pos / N_CYCLES)))
    tx_date.set_text(d.strftime("%b %d, %Y"))
    tx_cycle.set_text("BASELINE" if b == 0 else f"CYCLE {b:02d} / {N_CYCLES}")
    tx_total.set_text(f"{Tt/1e6:.2f}M")
    tx_homo.set_text(f"\u25A0  homologous   {Th/1e6:.2f}M")
    tx_het.set_text(f"\u25A1  heterogeneous   {Te/1e6:.2f}M")
    tx_hard.set_text(f"\u2581  hard cases   {Td/1e6:.2f}M")
    tx_cap.set_text(caption(b))
    prog_fill.set_width(max(pos / N_CYCLES, 1e-4))
    return []

# ============================== output ==============================
if __name__ == "__main__":
    out = "/workspace/jca3code/jiangchaokang/assets/media/projects/perception_onemodel/static_datasets_iteration.gif"
    FuncAnimation(fig, update, frames=N_FRAMES, blit=False).save(
        out, writer=PillowWriter(fps=18), savefig_kwargs={"facecolor": BG})
    print(f"saved -> {out}  ({N_FRAMES} frames)")
    print(f"start {sum(TOT_CUM[t][0] for t in TASKS)/1e6:.2f}M  ->  final {sum(TOT_CUM[t][-1] for t in TASKS)/1e6:.2f}M"
          f"  (homo {sum(HOMO[t] for t in TASKS)/1e6:.2f}M / het {sum(HET[t] for t in TASKS)/1e6:.2f}M)")