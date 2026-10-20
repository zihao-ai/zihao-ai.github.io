# BrandFusion blog figures

Primary source: **BrandFusion: A Multi-Agent Framework for Seamless Brand Integration in Text-to-Video Generation**, arXiv:2603.02816v2 (11 March 2026), https://arxiv.org/pdf/2603.02816v2. First release: 3 March 2026. Page numbers below are physical PDF pages (including cover/contents pages).

The associated blog is `data/blog/2026-03-03-brandfusion.md`. It contains six figures in total: the separate AI-generated cover plus the five visuals rebuilt here.

## Rebuild

Run `python scripts/build_brandfusion_blog_figures.py` from a checkout with Python, matplotlib, Pillow, and ffmpeg. The current font path for montage annotations is macOS Arial; adjust `font_path` for other operating systems. The script performs no network access or model generation. Temporary PNG previews go to `/tmp`; published assets go to this directory.

## Evidence and transformations

- `workflow.svg`: native SVG explanatory redraw of §4, PDF pp. 3–5. The critic evaluates the rewritten prompt, before video rendering. The simplified diagram includes the feedback-to-memory relation as text, and explicitly labels optional model adaptation.
- `video-examples.jpg`: full-frame extracts from four **actual generated Veo3 videos** in this repository's project gallery, arranged as an explicitly labeled 2×2 composite. Sources and exact timestamps are in `video-frames.csv`. Full frames are uniformly resized from 1280×720 to 680×383; no cropping, local enhancement, logo replacement, object insertion/removal, or generative retouching. Original watermarks remain. Selection is qualitative and curated, not randomized. The original MP4s remain in `brandfusion/examples/`; the montage does not establish temporal consistency or aggregate performance.
- `main-results.svg`: Table 1 (p. 6), Brand Presence Rate and Naturalness Score for all four methods and all three known-brand video models. `table-1.csv` preserves **all six metrics** from that table. Raw BPR values remain fractions, not percentages. Naturalness is the paper's automated LLM-evaluated 1–5 score. Bar baselines are zero; the naturalness scale's valid data range is 1–5. No error bars because the source does not supply intervals.
- `match-levels.svg`: Table 3 (p. 7), naturalness across three discrete contextual-compatibility categories. `table-3.csv` preserves both semantic and naturalness values. Lines are category connectors, not interpolated time-series evidence. The axis shows the valid naturalness range with slight label padding.
- `agent-ablation.svg`: Table 5 (p. 22), Veo3 naturalness by component removal. `table-5.csv` preserves every metric in the source table. Bars have a zero baseline for honest length comparison even though naturalness ratings use 1–5.
- `hero-diagram.png` and `hero-prompt.md`: separately generated technical explainer and prompt provenance. The cover is not an empirical model output, and its caption says so.

All charts preserve published precision; there is no inferred uncertainty, resampling, smoothing, significance test, or new experiment. Hatching supplements color on grouped bars; match-level curves use distinct markers. SVG text stays editable. Captions and alt text provide data context, and CSV links expose the numerical source data.

## Review

The authoring pass inspected the extracted frames and rendered previews of the montage and each plot, fixed overlapping match-level labels, and inspected the workflow SVG after rendering at full height with rsvg-convert (the initial macOS Quick Look thumbnail was cropped). Methodology and exact numerical claims were checked against text extracted from the versioned PDF. The scientific-visualization skill's integrity checklist informed source preservation, axis choice, and visual inspection; no claim of formal accessibility certification or journal compliance is made.

Cover revision: abstract artwork was replaced by `hero-diagram.png` on 2026-10-20. The new cover names the paper and shows its specific problem and mechanism. Original artwork remains recoverable in Git history.
