"""Regenerate the SkillCascade blog's SVG diagrams and Table 2 heatmap.

Run with Python 3 and matplotlib installed. The website has no Python dependency.
Source: https://arxiv.org/pdf/2609.30383v1, sections 1, 3–4 and Table 2.
"""

from pathlib import Path
from html import escape
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

OUT = Path(__file__).resolve().parents[1] / "assets/img/blog/skillcascade"
OUT.mkdir(parents=True, exist_ok=True)
INK, TEAL, MUTED, BG, RED = "#19383c", "#166a6f", "#53686c", "#fdfcfa", "#ad4a32"


def start(height, title, description):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}" role="img" aria-labelledby="title desc">',
        f"<title id=\"title\">{escape(title)}</title><desc id=\"desc\">{escape(description)}</desc>",
        f'<rect width="800" height="{height}" fill="{BG}"/>',
        f'<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,1 L8,5 L0,9" fill="none" stroke="{TEAL}" stroke-width="1.5"/></marker></defs>',
        '<g font-family="Arial, Helvetica, sans-serif">',
    ]


def text(x, y, value, size=25, color=INK, weight="400", anchor="start"):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'


def box(x, y, w, h, fill="#eff5f3", stroke="#c9dad6"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'


def arrow(y1, y2, x=400):
    return f'<path d="M{x},{y1} V{y2}" fill="none" stroke="{TEAL}" stroke-width="2.5" marker-end="url(#arrow)"/>'


svg = start(940, "How a warning disappears", "Illustrative prescription-review cascade from the paper introduction.")
svg += [
    text(50, 62, "How a warning disappears", 36, weight="700"),
    text(50, 106, "Locally plausible choices. A harmful joint outcome.", 24, MUTED),
]
steps = [
    (155, "01", "Extract the history", "A recently discontinued medication", "receives a weaker signal.", "#eff5f3"),
    (365, "02", "Evaluate interactions", "The associated interaction alert", "receives a lower priority.", "#f8f1df"),
    (575, "03", "Summarize the findings", "Low-priority alerts are omitted", "from the final report.", "#fae9e3"),
]
for y, n, title, line1, line2, fill in steps:
    svg += [box(50, y, 700, 145, fill),
            text(75, y+45, n, 24, TEAL, "700"),
            text(135, y+45, title, 29, weight="700"),
            text(135, y+88, line1, 26),
            text(135, y+121, line2, 26)]
for top, bottom in [(305, 357), (515, 567), (725, 786)]:
    svg.append(arrow(top, bottom))
svg += [box(50, 798, 700, 94, "#ad4a32", "#ad4a32"),
        text(400, 837, "The critical warning is missing.", 29, "#ffffff", "700", "middle"),
        text(400, 870, "The failure emerges across the handoffs.", 23, "#ffffff", anchor="middle"),
        text(50, 925, "Mechanism illustration · not a measured clinical outcome", 19, MUTED),
        "</g></svg>"]
(OUT / "warning-cascade.svg").write_text("\n".join(svg))

svg = start(1110, "From a scenario to an audited case", "Five SkillCascade agent roles, sandbox execution, and expert audit.")
svg += [text(45, 58, "From a scenario to an audited case", 34, weight="700"),
        text(45, 100, "Five agent roles + sandbox execution + expert audit", 23, MUTED)]
steps = [
    (130, "01  Scenario Discovery Agent", "Find a realistic task and a skill combination."),
    (260, "02  Attack Agent", "Propose coordinated skill modifications."),
    (390, "03  Scanner Agent", "Review each skill in an independent session."),
    (520, "04  Test Case Generator Agent", "Prepare task inputs and evaluation criteria."),
    (650, "Sandbox execution", "Run the target agent; capture output and trace."),
    (780, "05  Judge Agent", "Evaluate the outcome against the criteria."),
]
for y, title, detail in steps:
    execution = title == "Sandbox execution"
    svg += [box(45, y, 660, 100, "#f8f1df" if execution else "#eff5f3"),
            text(66, y+40, title, 28, weight="700"),
            text(66, y+78, detail, 23)]
    if y < 780:
        svg.append(arrow(y+105, y+123, 375))
svg += [
    '<path d="M705,831 H753 V310 H712" fill="none" stroke="#166a6f" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#arrow)"/>',
    '<text x="780" y="720" transform="rotate(-90 780 720)" font-size="21" fill="#53686c">Failed candidate: revise and retest</text>',
    arrow(885, 940, 375),
    text(390, 921, "Successful candidate", 20, MUTED),
    box(45, 950, 660, 100, "#166a6f", "#166a6f"),
    text(66, 990, "Expert audit → benchmark admission", 27, "#ffffff", "700"),
    text(66, 1028, "213 validated cases across 10 domains", 24, "#ffffff"),
    text(45, 1088, "Simplified from paper §3–4; feedback can return to earlier stages.", 19, MUTED),
    "</g></svg>",
]
(OUT / "framework.svg").write_text("\n".join(svg))

# Exact entries from Table 2, not values estimated from a figure.
names = ["GPT-5.4", "GPT-5.4 Mini", "Claude Opus 4.6", "Claude Sonnet 4.6",
         "Gemini 2.5 Pro", "Gemini 2.5 Flash", "Qwen 3 72B", "Kimi K2.5"]
values = [
    [82.6, 78.4, 80.9], [100.0, 95.8, 94.3], [78.5, 74.2, 76.8],
    [91.7, 89.2, 88.5], [90.2, 86.4, 88.9], [94.1, 91.3, 92.6],
    [99.1, 96.7, 95.4], [95.2, 92.4, 93.1],
]
hosts = ["OpenClaw", "Claude Code", "Codex"]
with (OUT / "attack-success.csv").open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Backbone", *hosts])
    writer.writerows([[name, *row] for name, row in zip(names, values)])

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 14, "svg.fonttype": "none"})
fig, ax = plt.subplots(figsize=(10, 7.2), facecolor=BG)
fig.subplots_adjust(left=.265, right=.96, top=.78, bottom=.19)
cmap = LinearSegmentedColormap.from_list("skillcascade", ["#f4f8f6", "#9ac9c2", "#125c63"])
norm = Normalize(0, 100)
im = ax.imshow(values, cmap=cmap, norm=norm, aspect="auto")
ax.set_xticks(range(3), hosts, fontsize=15)
ax.set_yticks(range(8), names, fontsize=14)
ax.xaxis.tick_top()
ax.tick_params(axis="both", length=0, pad=12, colors=INK)
for spine in ax.spines.values():
    spine.set_visible(False)
for i, row in enumerate(values):
    for j, value in enumerate(row):
        ax.text(j, i, f"{value:.1f}", ha="center", va="center",
                fontsize=19, weight="bold", color="white")
ax.set_xticks([-.5, .5, 1.5, 2.5], minor=True)
ax.set_yticks([x-.5 for x in range(9)], minor=True)
ax.grid(which="minor", color=BG, linewidth=4)
ax.tick_params(which="minor", bottom=False, left=False, top=False)
cax = fig.add_axes([.265, .115, .695, .018])
bar = fig.colorbar(im, cax=cax, orientation="horizontal", ticks=[0, 25, 50, 75, 100])
bar.outline.set_visible(False)
bar.ax.tick_params(labelsize=11, length=0, colors=MUTED)
fig.text(.04, .93, "Attack success across agent systems", size=23, weight="bold", color=INK)
fig.text(.04, .88, "SkillCascade-Bench · ASR (%) · mean over three runs", size=15, color=MUTED)
fig.text(.04, .035, "Source: arXiv:2609.30383v1, Table 2. Controlled benchmark; not incident prevalence.",
         size=11, color=MUTED)
fig.savefig(OUT / "attack-success.svg", facecolor=BG,
            metadata={"Title": "SkillCascade-Bench attack success rate",
                      "Description": "Exact Table 2 values; color scale spans 0–100 percent."})
plt.close(fig)
print(f"Wrote three figures and their chart data to {OUT}")
