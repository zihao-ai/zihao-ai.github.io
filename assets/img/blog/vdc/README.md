# Blog figure provenance

Source: https://arxiv.org/pdf/2309.16211v2

label-gap.svg: conceptual explanation of corrupted-label signal and clean-label limitation.
pipeline.svg: simplified §4, implementation details §5.1.
noise-detection.svg/.csv: all six VDC dataset/noise entries, Table4.
hybrid-detection.svg/.csv: all methods, Average columns Table5; poisoning/noise ratios follow table header and §5.2.3.
after-cleaning.svg/.csv: all methods, Average columns Table6.
TPR, FPR, ASR and ACC remain distinct. No results inferred from generated images.

Regenerate the ten EARBench/VDC supporting figures with:

```sh
python scripts/build_earbench_vdc_blog_figures.py
```

Requires matplotlib. Native SVG diagrams use Python standard-library XML strings; plots use matplotlib with zero-based axes. CSV files preserve source values, with approximate values labeled. No uncertainty intervals are invented. Covers were generated with OpenAI imagegen; see hero-prompt.md for full prompt. They are technical method illustrations. Original generated files retained outside the repository.

Cover revision: abstract artwork was replaced by `hero-diagram.png` on 2026-10-20. The new cover names the paper and shows its specific problem and mechanism. Original artwork remains recoverable in Git history.
