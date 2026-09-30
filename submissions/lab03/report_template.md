# Lab 3 Report — 20201068 이지호

## 1. What I did

I implemented the four TODO blocks following the docstrings exactly. Two private helpers were added: `_sq_dists`, for squared distances, and `_log_gauss`, a Cholesky-based log-density that needs no explicit matrix inverse. One `np.random.Generator` (seed 42) is threaded through every step, so the figures match `results.json` exactly.

## 2. Results

**Table 1. Key numbers from `results.json`.** The interpretation in §4 hangs on the ARI gap: 0.61 for K-means vs 0.91 for the GMM.

| Metric | Value |
|--------|-------|
| ARI, K-means / GMM | 0.6082 / 0.9104 |
| K-means inertia | 281.8135 |
| Log-likelihood, first / final / min consecutive change | −939.085 / −653.7012 / −7e−9 |
| BIC at k = 3 / 4 / 5 | 2244.17 / **1595.47** / 1645.83 |
| Selected k (BIC minimum) | 4 |

## 3. Figures

![](fig1.png)

**Figure 1. The scene colored by K-means labels (left) and by GMM labels (right), k = 4.** K-means splits the long box (229 / 142 points) and merges half of it with the shell. The GMM recovers the rod perfectly and errs only where the shell touches its neighbours.

![](fig2.png)

**Figure 2. EM log-likelihood vs iteration.** The trace rises steeply for about 10 iterations, then stays flat. It is monotone up to −7·10⁻⁹, a small effect of the `reg·I` term.

![](fig3.png)

**Figure 3. BIC vs number of components k.** The minimum is at k = 4. To the left, the model underfits; to the right, each extra component costs more in penalty than it gains in likelihood.

## 4. Interpretation

K-means uses Euclidean distance, which implicitly treats every cluster as an isotropic ball of equal size. The box is about 2.4 units long but thin, so its ends lie closer to a neighbouring center than to its own. K-means therefore cuts the box and gives half of it to the shell (Figure 1), for an ARI of 0.61 (Table 1). The full-covariance GMM learns one shape per component. The fitted standard deviations along the principal axes are 0.12 / 0.13 / 0.58 for the box, 0.10 / 0.10 / 0.48 for the rod, 0.05 / 0.24 / 0.34 for the plate, and 0.18 / 0.19 / 0.20 for the shell. These ellipsoids keep each object whole, and ARI rises to 0.91.

EM is monotone (Figure 2) because each E-step makes the lower bound tight and each M-step maximizes it. Likelihood alone keeps rising with k: −654 at k = 4 and −595 at k = 8. BIC, however, charges 10 parameters per extra component, about 10·ln 1614 ≈ 74. Going from k = 4 to 5 lowers −2·ll by only about 23.5, so BIC turns upward after k = 4 (Figure 3).

Points at contacts between objects get split responsibilities. Of the 1614 points, 225 have a maximum responsibility below 0.9, and 56 of the GMM's 57 errors are among them.

## 5. Limitations

The GMM's advantage rests on the objects being anisotropic. With similar-sized spheres, K-means should match it while using far fewer parameters. Two objects touching along a large face could be absorbed by one elongated Gaussian, and BIC would then likely pick k = 3.

## AI & external-code usage

| Tool / Source | Part used for | What I modified & verified myself |
|---------------|---------------|-----------------------------------|
| Claude Code (Claude Opus 5.5, Anthropic) | Overall direction for the tasks, and writing and editing of this report and the README | I designed and implemented the main logic in `src/lab03.py` myself (K-means++, EM, BIC, the experiment); verified it against the docstrings, the 6 public tests, and `check_submission.py` |
