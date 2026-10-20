# SkillCascade blog artwork

For `data/blog/2026-10-20-skill-cascading-attacks.md`.

## Sources and regeneration

- `hero-diagram.png`: generated with the built-in `image_gen` tool on 2026-10-20. A technical infographic illustrating the prescription-review cascade, not evidence or a result figure. The exact generation prompt is in `hero-prompt.md`.
- `warning-cascade.svg`: explanatory redraw of the prescription-review example in the introduction of [arXiv:2609.30383v1](https://arxiv.org/pdf/2609.30383v1).
- `framework.svg`: simplified account of the five agent roles, sandbox execution, and expert audit in sections 3–4 of the paper. Feedback is compressed into a single illustrative return arrow.
- `attack-success.svg`: heatmap of all 24 ASR entries in Table 2, with a fixed 0–100% color scale. Numeric data are stored in `attack-success.csv`. No error bars are invented.

Regenerate the three SVG files and CSV with:

```sh
python3 scripts/build_skillcascade_blog_figures.py
```

The authoring script requires Matplotlib. It is not a website runtime dependency.

## Cover generation

See `hero-prompt.md` for the exact prompt used to generate the replacement technical infographic. It illustrates the prescription-review cascade from the paper introduction.

Cover revision: abstract artwork was replaced by `hero-diagram.png` on 2026-10-20. The new cover names the paper and shows its specific problem and mechanism. Original artwork remains recoverable in Git history.
