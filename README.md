# ComFy for Log Measures

ComFy performs a factor analysis on complexity measures of event logs (e.g. from
process mining) to identify latent factors behind those measures. Given a CSV
file of per-log complexity scores, it runs Bartlett's test of sphericity and
the measure of sampling adequacy (MSA/KMO) to check whether a factor analysis
is appropriate, then performs the factor analysis itself and exports the
results as `.tex` tables into `output/`.

## Installation (from scratch)

The dependencies (`factor-analyzer` in particular) only work reliably with
specific versions of `scikit-learn` and Python, so this project pins an exact
environment via conda/[Miniconda](https://docs.conda.io/en/latest/miniconda.html)
rather than relying on whatever is already on your machine.

1. **Install conda**, if you don't already have it. Any distribution works
   (Miniconda, Anaconda, Miniforge). Verify it's on your `PATH`:

   ```bash
   conda --version
   ```

2. **Create the project's environment** from the repo root. This reads
   [`.conda.yml`](.conda.yml), which pins Python 3.12 and every pip
   dependency (`pandas`, `questionary`, `factor-analyzer`, `feeed`, and a
   `scikit-learn<1.6.0` pin — see note below):

   ```bash
   conda env create -f .conda.yml
   ```

3. **Activate the environment** (needed in every new terminal session before
   running the script):

   ```bash
   conda activate comfy
   ```

4. **Run the analysis**:

   ```bash
   python test.py
   ```

   This expects an input CSV at `./input/log_measures_all_pdc_training_logs.csv`
   (one row per event log, one column per complexity measure). On success, it
   prints Bartlett's test and MSA diagnostics to the terminal and writes four
   `.tex` files to `output/`.

### Why `scikit-learn<1.6.0` is pinned

`factor-analyzer` 0.5.1 calls `sklearn.utils.check_array(..., force_all_finite=...)`.
That parameter was renamed to `ensure_all_finite` starting with scikit-learn
1.6 and removed entirely by 1.8, which makes `factor-analyzer` crash with
`TypeError: check_array() got an unexpected keyword argument 'force_all_finite'`
on a newer, unpinned scikit-learn. If you ever bump dependencies, re-check
this compatibility (or switch to a `factor-analyzer` release that has fixed
it, if one exists) rather than leaving scikit-learn unpinned.

## Updating dependencies

Edit [`.conda.yml`](.conda.yml) and re-create the environment:

```bash
conda env remove -n comfy
conda env create -f .conda.yml
```

Keeping dependencies pinned by an environment file (rather than installing
ad hoc with `pip`) is what makes a run on one machine reproducible on
another.
