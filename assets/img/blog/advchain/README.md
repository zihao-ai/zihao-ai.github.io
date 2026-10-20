# AdvChain research blog assets

Blog: `data/blog/2025-09-29-advchain.md`.
Primary source: **AdvChain: Adversarial Chain-of-Thought Tuning for Robust Safety Alignment of Large Reasoning Models**, arXiv:2509.24269**v1**, submitted September 29, 2025.

- Version record: https://arxiv.org/abs/2509.24269v1
- Official full paper: https://arxiv.org/pdf/2509.24269v1
- Paper retrieved and reviewed on October 20, 2026. Blog date follows the first arXiv release; its footer explicitly labels the article retrospective.

## Provenance

| Asset | Evidence source | What it represents |
| --- | --- | --- |
| `hero-diagram.png` | See `hero-prompt.md` | AI-generated technical explainer, never a result figure. |
| `two-directions.svg` | §3, pp. 3–4 | Original explanatory diagram of harmful drift and unnecessary refusal. No empirical values or implied frequency. |
| `recovery-training.svg` | §4, pp. 5–6; §5.1, p. 6 | Original explanatory diagram of the two correction types and the published 800/200 sample split. |
| `general-safety.svg` | Table 1, p. 7 | Exact ASR columns for every method in the DeepSeek-R1-7B and Qwen3-4B sections. Other model-size sections are explicitly outside this figure. |
| `safety-utility.svg` | Tables 2–3, p. 8 | CoT-Hijack ASR versus XSTest ORR for every method reported in those tables. Each axis retains its own evaluation set and denominator; no combined score. |
| `reasoning-capability.svg` | Table 4, p. 8 | All six base-versus-AdvChain Pass@1 comparisons, without averaging. |
| `general-safety-table1.csv` | Table 1, p. 7 | Numerical source for the safety heatmap. |
| `safety-utility-tables2-3.csv` | Tables 2–3, p. 8 | Both Table 2 metrics and both Table 3 metrics; the scatter uses only CoT-Hijack ASR and XSTest ORR. |
| `reasoning-table4.csv` | Table 4, p. 8 | Exact values for the reasoning comparison. |

All numerical values were manually transcribed from the official PDF text and checked against the source tables. CSVs retain two decimal places. Names are shortened to the method name within their separately labeled model family; “Base” means the named untuned family checkpoint. No chart depicts estimated raw data, interpolation, extrapolation, a synthesized average, or statistical significance.

## Metric interpretation and plotting choices

- ASR: fraction of evaluated harmful prompts whose final answer is judged unsafe by LlamaGuard3. Lower is better.
- ORR: fraction of evaluated benign prompts identified as refused through keyword matching. Lower is better.
- RR on harmful prompts is a separate keyword-based measurement, not `100 − ASR`.
- Pass@1: single-attempt correct-solution rate. Higher is better.
- CoT-Hijack has 150 samples. Other sample counts are not inferred from rounded rates.
- Source Tables 1–4 do not report uncertainty intervals. No error bars or equivalence claims have been invented.
- Heatmap: common linear 0–100 color normalization; exact numbers printed in each cell.
- Scatter: identical axis limits across the two model-family panels; method labels and distinct base/AdvChain markers supplement color.
- Capability chart: zero-baseline paired horizontal bars, exact labels, common scale.
- The source's selected-failure stepwise plots are explained in prose; no numerical trajectory has been fabricated from them.

## Reproduction and review

Run `python scripts/build_advchain_blog_figures.py` with Matplotlib installed. The script emits five SVGs and three CSVs into this folder, leaving the hero and its provenance untouched. During production, the runtime was `/tmp/skillcascade-blog/venv/bin/python`.

The two mechanism SVGs are native vector markup; the numerical charts use Matplotlib. The website has no Python runtime dependency. Every figure is wrapped in semantic HTML with an explicit size, alt description, and source-aware caption in the blog. Numerical CSV downloads provide a machine-readable alternative.

Visual review: rendered each SVG at **760 px wide** with `rsvg-convert`, then inspected the resulting PNGs for clipping, legibility, labels, and data encodings. Review renders are temporary files in `/tmp/advchain-blog/`. The cover was also visually inspected. No paper figure was raster-cropped or altered.

Cover revision: abstract artwork was replaced by `hero-diagram.png` on 2026-10-20. The new cover names the paper and shows its specific problem and mechanism. Original artwork remains recoverable in Git history.
