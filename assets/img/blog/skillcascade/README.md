# SkillCascade blog artwork

For `data/blog/2026-10-20-skill-cascading-attacks.md`.

## Sources and regeneration

- `hero.png`: generated with the built-in `image_gen` tool on 2026-10-20. A conceptual illustration, not evidence or a result figure. The exact generation prompt is below.
- `warning-cascade.svg`: explanatory redraw of the prescription-review example in the introduction of [arXiv:2609.30383v1](https://arxiv.org/pdf/2609.30383v1).
- `framework.svg`: simplified account of the five agent roles, sandbox execution, and expert audit in sections 3–4 of the paper. Feedback is compressed into a single illustrative return arrow.
- `attack-success.svg`: heatmap of all 24 ASR entries in Table 2, with a fixed 0–100% color scale. Numeric data are stored in `attack-success.csv`. No error bars are invented.

Regenerate the three SVG files and CSV with:

```sh
python3 scripts/build_skillcascade_blog_figures.py
```

The authoring script requires Matplotlib. It is not a website runtime dependency.

## Exact image generation prompt

> Use case: stylized-concept. Asset type: wide editorial hero illustration for an English research blog about the paper 'Stealth Apart, Harm Together: Skill Cascading Attacks on Skill-Based Agent Systems'. Primary request: sophisticated scientific editorial artwork illustrating multiple individually ordinary AI skill modules combining into a hazardous whole. Composition: panoramic landscape 3:2, three small floating translucent ivory modular glass blocks arranged left to right, connected by a continuous fine teal ribbon; the ribbon subtly turns amber then vermilion as it flows through the blocks and ends in a restrained red warning-shaped triangular prism. Each block has abstract document-like lines engraved inside, and an understated teal verification mark outside; they are modules, not computers or robots. Visually convey local approval versus harmful composition without suggesting empirical measurements. Warm off-white background, dark teal, slate, muted vermilion accent, soft isometric studio lighting, fine paper grain, generous negative space, polished editorial cover suitable for an academic personal website. No words, no letters, no numbers, no charts, no logos, no watermarks, no hackers, no skulls. This is a conceptual illustration, not a result plot.
