# Blog figure provenance

Source: https://arxiv.org/pdf/2408.04449v5

planning-gap.svg: conceptual redraw of the kitchen case, §2.5.
framework.svg: simplified four-module framework and methods.
risk-and-effectiveness.svg/.csv: selected exact values from §2.3.1.
prompt-mitigation.svg/.csv: textual-only baseline values §2.3.3 (GPT-4o ≈94.53) / §2.4 (Llama) and approximate explicit mitigation values §2.4/Fig.5. Do not pair GPT-4o overall baseline 94.03 with textual-only mitigation.
evaluation-agreement.svg/.csv: approximate κ values §2.3.5/Fig.4d; 200 instances, five annotators.
No physical robot rollout data are claimed. Dataset size follows §2.2; inconsistent domain totals in Fig.1c are not reproduced.

Regenerate the ten EARBench/VDC supporting figures with:

```sh
python scripts/build_earbench_vdc_blog_figures.py
```

Requires matplotlib. Native SVG diagrams use Python standard-library XML strings; plots use matplotlib with zero-based axes. CSV files preserve source values, with approximate values labeled. No uncertainty intervals are invented. Covers were generated with OpenAI imagegen; see hero-prompt.md for full prompt. They are technical method illustrations. Original generated files retained outside the repository.

Cover revision: abstract artwork was replaced by `hero-diagram.png` on 2026-10-20. The new cover names the paper and shows its specific problem and mechanism. Original artwork remains recoverable in Git history.
