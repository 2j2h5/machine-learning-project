# Lab 8 Report — 20201068 이지호

## 1. What I did

I implemented the four TODO blocks exactly to their docstrings. The one addition is a private helper,
`_slice_report(config, seed)` in `src/lab08.py`. `main()` does not call it. It runs `error_analysis`
on the validation predictions of *any* configuration, and I used it to check whether the best ablation
factor fixes the worst slice (§4). Everything was run on Python 3.10.21 with the pinned requirements.

## 2. Results

**Table 1. Each factor changed on its own, five seeds each.** Read the difference column against the
std column first: a difference is a finding only if it is larger than the seed-to-seed spread, and the
std column is what measures that spread.

| Variant | Mean F1 | Std F1 | Difference from base | Larger than the base spread? |
|---------|---------|--------|----------------------|------------------------------|
| base | 0.6439 | 0.0230 | 0.0000 | — |
| features=with_region | 0.7355 | 0.0270 | +0.0916 | yes, 4.0 base std |
| features=core | 0.4741 | 0.0302 | −0.1698 | yes, 7.4 base std |
| model=tree | 0.5292 | 0.0431 | −0.1147 | yes, 5.0 base std |
| class_weight=balanced | 0.6787 | 0.0180 | +0.0348 | 1.5 base std, but the ±1 std intervals overlap |
| scale=False | 0.6358 | 0.0210 | −0.0081 | no, 0.35 base std |

**Table 2. The base config sliced by region, seed 42.** The `n` column decides whether an accuracy
counts as evidence at all: overseas has only 10 validation rows, so its 0.100 is not a result.

| Region | n | Accuracy | Precision | Recall | F1 |
|--------|---|----------|-----------|--------|----|
| island | 89 | 0.4382 | 0.8485 | 0.3836 | 0.5283 |
| metro | 213 | 0.8685 | 0.7222 | 0.3611 | 0.4815 |
| overseas | 10 | 0.1000 | 0.1000 | 1.0000 | 0.1818 |
| rural | 130 | 0.7308 | 0.7529 | 0.8205 | 0.7853 |
| suburb | 158 | 0.8038 | 0.7333 | 0.6346 | 0.6804 |
| **overall** | **600** | **0.7450** | **0.7277** | **0.5792** | **0.6450** |

## 3. Figures

![Figure 1](../figures/fig1.png)

**Figure 1. Accuracy per region against the overall accuracy.** Island (n = 89) is furthest below the
line, 0.307 under the overall 0.745. Overseas (hatched) is lower still, but its 10 rows carry a 95%
interval of up to ±0.3, so I draw no conclusion from it.

![Figure 2](../figures/fig2.png)

**Figure 2. One factor changed at a time, mean ±1 std over five seeds.** features=with_region clears the
base band from above, and features=core and model=tree clear it from below. scale=False sits inside the
band, and the error bar of class_weight=balanced still reaches it.

![Figure 3](../figures/fig3.png)

**Figure 3. Five seeds each for the base and the challenger.** The two point sets only just separate
(best base seed 0.665, worst challenger seed 0.667), and the mean ± std intervals overlap
(0.679 − 0.018 = 0.661 ≤ 0.644 + 0.023 = 0.667). So five seeds suggest an improvement but do not show one.

## 4. Interpretation

The largest change is **features=core, −0.170 F1, 7.4 base standard deviations** (Table 1,
Figure 2). Dropping dispatch hour, courier load, weather and weekend removes most of the signal. The
largest gain is features=with_region, +0.092 (4.0 base std). The tree also loses 5.0 std: at depth 4 it
underfits, and it has the widest spread (0.043) because the 70% feature subset at each split moves
with the seed.

**scale=False lands inside the seed noise** (−0.008, 0.35 base std). Logistic regression reaches nearly
the same fit with or without standardization here. With seed 42 alone I would have read its −0.008 as
"scaling helps". Reading class_weight=balanced on seed 45 alone, I would have reported +0.058, about
1.7 times its five-seed mean gain of +0.035. That gain is 1.5 base std, yet the intervals overlap
(`ranking_second_overlaps_best = true`, Figure 3). The variant trades precision (0.711 → 0.653,
five-seed mean) for recall (0.588 → 0.707), and its accuracy even drops slightly (0.739 → 0.732).

**Island is the worst region large enough to judge** (n = 89, accuracy 0.438, Table 2, Figure 1).
82% of island validation deliveries are late, but the base predicts "late" for only 37% of them,
because the base feature set has no region information. Without island, overall accuracy would be
0.798; island makes up 15% of the validation rows and pulls the average down to 0.745. The ablation
factor features=with_region addresses it directly: with `_slice_report` at seed 42, island accuracy
rises from 0.438 to 0.798 and recall from 0.384 to 0.973. The worst slice then becomes rural, with a
gap of only 0.083.

**I refuse to draw a conclusion from the overseas row of Table 2.** Its accuracy of 0.100 and recall of
1.000 come from 10 rows, one of which is a late delivery. Every metric there can swing by tens of points
with a single prediction.

**Accuracy and recall tell different stories in metro.** Metro has the highest accuracy (0.869) and the
lowest recall (0.361). Only 17% of metro deliveries are late, so predicting "on time" is right most of
the time, and accuracy is dominated by that majority. Recall looks only at the late deliveries, and the
model catches about a third of them. Both statements are true at once.

## 5. Limitations

The "not separated" verdict for class_weight=balanced rests on five seeds and an interval test that
ignores pairing. Base and challenger share the same split for each seed, and the challenger is higher
on **all five** seeds (+0.015 to +0.058). A paired comparison over per-seed differences, or ten more
seeds that shrink the std estimates, could turn it into a real finding. The island fix from
with_region is also measured on seed 42 only.

## AI & external-code usage

| Tool / Source | Part used for | What I modified & verified myself |
|---------------|---------------|-----------------------------------|
| Claude Code (Anthropic, model Claude Opus 5.5) | Implementing Tasks 1–4 and `_slice_report` in `src/lab08.py`; the three notebook plot cells; drafting this report and `README.md` | Ran `pytest tests/` (6/6 pass) and `check_submission.py`; checked every number in Tables 1–2 and §4 against `results.json` and a re-run. |
