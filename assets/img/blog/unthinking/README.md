# Unthinking blog figure provenance

Article: `data/blog/2025-02-16-unthinking.md`.

Primary source: [To Think or Not to Think: Exploring the Unthinking Vulnerability in Large Reasoning Models, arXiv:2502.12202v2](https://arxiv.org/pdf/2502.12202v2), revised 2025-05-16. First submission 2025-02-16 determines the blog date; a retrospective-version note is included in the article. Source PDF was downloaded and extracted with `pdftotext -layout`. PDF SHA-256: `3aa7f88180e6cc7aa76636756c207d8c05467b5954668072b31de1f76f14e3bd`.

Verified official repository: https://github.com/zihao-ai/unthinking_vulnerability . The historical `zihao-zhu` URL returned 404 during this task, so the article uses the current repository.

## Assets

| Asset | Source and transformation |
| --- | --- |
| `hero-diagram.png` | AI-generated technical explainer. Separate generation record: `hero-prompt.md`. Not experimental evidence. |
| `thinking-boundary.svg` | Native SVG conceptual redraw based on §§3–5, pp. 3–9. Timeline lengths are schematic, not measured token counts. |
| `control-paths.svg` | Native SVG summary of the two BoT access assumptions (§4) and owner-controlled MoT (§5). No executable payloads or attack procedures. |
| `bot-success.svg` | Matplotlib paired-dot chart, exact ASR entries in Tables 1–2, p. 6. Table 1: default semantic-trigger SFT. Table 2: training-free, per-input white-box optimization. |
| `mot-efficiency.svg` | Matplotlib grouped bars, four DeepSeek-R1 rows of Table 5, p. 8. The s1 comparator is intentionally not plotted. Values are relative generated-token and pass@1 changes, not percentage-point changes or absolute accuracy. |
| `mot-safety.svg` | Matplotlib dumbbells, exact ASR entries of Table 6, p. 9. Four models × three safety datasets; values are Llama-Guard–judged jailbreak outcomes. |

Exact plotted numbers are saved in `bot-success.csv`, `mot-efficiency.csv`, and `mot-safety.csv`. No points were estimated from a raster image. Published percentages retain their published precision in the source arrays; charts may suppress trailing zeros.

## Reproduction

Run `python scripts/build_unthinking_blog_figures.py` from the repository with matplotlib available. The script writes five SVGs and three CSVs here and PNG chart previews under `/tmp/unthinking-blog/`. The production site has no Python dependency. Native diagrams can be rasterized for inspection with `rsvg-convert`.

## Interpretation and checks

- BoT ASR = share of evaluated inputs that bypass thinking; it is not answer error rate.
- C-Acc in §4.3 = share of clean inputs that retain the full thinking process; it is not mathematical answer accuracy.
- Safety ASR in Table 6 = evaluated jailbreak success judged by Llama-Guard. Refusal rate and harmfulness score are separate measurements.
- Table 6 prints an upward arrow for HarmBench ASR, inconsistent with its safety objective. The blog correctly treats lower jailbreak ASR as better; numeric entries are unchanged.
- Figure 4 on p. 7 was visually checked for recovery results: original 100.0% for all three; after alignment 71.2%, 76.8%, 98.2%. The article computes absolute decreases as 28.8, 23.2, 1.8 percentage points instead of repeating the main text's approximate “30%” claim.
- The main text points to Appendix E.2 for MoT cost; the actual MoT analysis is E.3, pp. 28–29. Article links the correct section and does not interpret the cost assumptions as current prices or latency measurements.
- The article avoids strong claims based on Table 12's internally inconsistent monitor-call row and avoids treating Appendix F's prose assertion of 100% as identical to the 98.70% forced-template result in Table 13.
- All five generated figures were rendered and visually inspected. Legend/axis spacing was adjusted after the first preview. Hero inspected for consistency with caption.
- Source grounding and figure validation were performed in the same agent context; no independent numerical review has been claimed.

Cover revision: abstract artwork was replaced by `hero-diagram.png` on 2026-10-20. The new cover names the paper and shows its specific problem and mechanism. Original artwork remains recoverable in Git history.
