"""Regenerate FVH-Bench blog diagrams and charts from adjacent source CSVs.

Source: arXiv:2610.37722v1, §§3–4, Tables 1–2.
Requires Python 3 and Matplotlib. No website runtime dependencies.
"""
from pathlib import Path
from html import escape
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "assets/img/blog/fvh-bench"
INK, TEAL, MUTED, BG, RED = "#19383c", "#166a6f", "#53686c", "#fdfcfa", "#ad4a32"


def start(height, title, desc):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
            f'<rect width="1000" height="{height}" fill="{BG}"/>',
            '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,1 L8,5 L0,9" fill="none" stroke="#166a6f" stroke-width="1.5"/></marker></defs>',
            '<g font-family="Arial, Helvetica, sans-serif">']


def text(x, y, value, size=24, color=INK, weight="400", anchor="start"):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>'


def box(x, y, w, h, fill="#eff5f3"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="#c9dad6"/>'


def arrow(y1, y2):
    return f'<path d="M500,{y1} V{y2}" fill="none" stroke="{TEAL}" stroke-width="2.5" marker-end="url(#arrow)"/>'


def save(name, svg):
    (OUT / f"{name}.svg").write_text("\n".join(svg + ["</g></svg>\n"]))


def rows(name):
    with (OUT / f"{name}.csv").open() as f:
        return list(csv.DictReader(f))


s = start(1120, "From a harmful function to a curated test", "Four construction agents, iterative review, then independent human curation. 669 of 750 candidates retained.")
s += [text(45, 62, "From a function to a benchmark prompt", 36, weight="700"),
      text(45, 104, "5 visual functions × 10 risk domains guide coverage", 25, MUTED)]
steps = [
    (150, "1  Coverage Planner", "Choose function–domain pairs; use scenario memory."),
    (310, "2  Scenario Designer", "Specify the harmful objective and the artifact’s role."),
    (470, "3  Prompt Composer", "Translate the scenario into an image request."),
    (630, "4  Prompt Reviewer", "Pass, revise, or discard; at most 3 revision rounds."),
    (790, "5  Human curation", "5 independent reviewers; at least 4 must approve."),
]
for y, title, line in steps:
    s += [box(45, y, 910, 118), text(70, y+44, title, 28, weight="700"), text(70, y+86, line)]
for y in [270, 430, 590, 750]:
    s.append(arrow(y, y+32))
s += [text(45, 970, "750 candidates → 669 retained prompts", 30, TEAL, "700"),
      text(45, 1015, "Acceptance checks the request, not successful harmful generation.", 24),
      text(45, 1080, "Source: §3.3 and Appendix A.1 · simplified workflow", 20, MUTED)]
save("construction", s)

s = start(960, "Four metrics, two denominators", "Refusal rate is over all input prompts. PIC, THR and HAU are 1–5 scores conditional on valid assessment of generated images.")
s += [text(45, 65, "Four metrics, two denominators", 38, weight="700"),
      box(45, 110, 910, 143, "#f8f1df"), text(70, 153, "ALL INPUT PROMPTS", 23, TEAL, "700"),
      text(70, 198, "RR: How often does the model refuse?", 29, weight="700"),
      text(70, 233, "Percentage of prompts · technical failures counted separately", 23),
      text(45, 310, "GENERATED IMAGES WITH VALID ASSESSMENTS", 23, TEAL, "700")]
for y, short, question, detail in [
    (345, "PIC", "Did it follow the request?", "Content and visual-form fidelity; this does not judge safety."),
    (505, "THR", "Is the harmful target visibly realized?", "Completeness and clarity of the risk-bearing content."),
    (665, "HAU", "How usable is the harmful artifact?", "Readability, coherence, and support for its intended misuse."),
]:
    s += [box(45, y, 910, 130), text(70, y+40, short+"  ·  1–5", 24, TEAL, "700"),
          text(260, y+40, question, 26, weight="700"), text(70, y+93, detail, 23)]
s += [text(45, 858, "Refusals receive no image score. High scores are not harm probabilities.", 23, RED),
      text(45, 916, "Source: §4.1 · metric definitions", 20, MUTED)]
save("metrics", s)

data = rows("main-results")
s = start(800, "The main generation results", "Across 11 generators: mean refusal rate 2.45%, mean target harm realization 4.46 out of 5, and four models with mean harmful artifact usability above four.")
s += [text(45, 65, "The main generation results", 38, weight="700"),
      text(45, 108, "669 prompts · 11 image generators", 25, MUTED)]
for y, row, detail in zip([155, 340, 525], data, [
    "Average refusal rate across the 11 evaluated generators.",
    "Mean THR across generators; scores apply to generated images.",
    "Models with mean harmful artifact usability (HAU) above 4.",
]):
    s += [box(45, y, 910, 145), text(70, y+60, row["display_value"], 44, TEAL, "700"),
          text(330, y+54, row["label"], 28, weight="700"), text(70, y+112, detail, 23)]
s += [text(45, 725, "THR and HAU use 1–5 ratings, not real-world harm probabilities.", 23, MUTED),
      text(45, 775, "Source: §4.2 and Table 1 · headline results", 20, MUTED)]
save("main-results", s)

style = {"font.family": "DejaVu Sans", "font.size": 13, "text.color": INK,
         "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": INK,
         "axes.edgecolor": "#ccd6d4", "figure.facecolor": BG, "axes.facecolor": BG,
         "svg.fonttype": "none", "svg.hashsalt": "fvh-bench-blog"}


def export(fig, name, title):
    fig.savefig(OUT / f"{name}.svg", metadata={"Date": None, "Title": title})
    plt.close(fig)
    p = OUT / f"{name}.svg"
    p.write_text("\n".join(line.rstrip() for line in p.read_text().splitlines())+"\n")


with plt.rc_context(style):
    data = rows("detector-results")
    fig, ax = plt.subplots(figsize=(12, 6.5))
    fig.subplots_adjust(left=.31, right=.93, top=.72, bottom=.27)
    labels = []
    for row in data:
        labels.append(row["method"]+"\n"+row["backbone"])
    vals = [float(r["recall_percent"]) for r in data]
    colors = [TEAL if r["method"] == "Condition-Decomposed" else "#73898a" for r in data]
    ax.barh(range(len(data)), vals, height=.60, color=colors)
    ax.set_yticks(range(len(data)), labels, fontsize=12)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xticks(range(0, 101, 20))
    ax.set_xlabel("Recall on 500 harmful images (%)", labelpad=12)
    ax.xaxis.grid(True, color="#dde3e1", linewidth=.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0, pad=14)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    for i, v in enumerate(vals):
        ax.text(v+1.0, i, f"{v:.2f}", va="center", fontsize=13)
    fig.text(.04, .94, "Function-aware detection improves recall", size=24, weight="bold")
    fig.text(.04, .87, "General Safety Policy vs. Condition-Decomposed detection", size=15, color=MUTED)
    fig.text(.04, .13, "All four configurations: 0.00% observed false positives on 200 benign controls.", size=12)
    fig.text(.04, .06, "Source: Table 2, p. 6 · Selected comparison; all inputs are image-only.", size=12, color=MUTED)
    export(fig, "detector-results", "Selected FVH-Bench detection results")

print("Wrote four SVG figures to", OUT)
