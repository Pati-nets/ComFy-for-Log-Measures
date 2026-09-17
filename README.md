# ComFy for Log Measures

ComFy performs a factor analysis on complexity measures of event logs (e.g. from
process mining) to identify latent factors behind those measures. Given a CSV
file of per-log complexity scores, it runs Bartlett's test of sphericity and
the measure of sampling adequacy (MSA/KMO) to check whether a factor analysis
is appropriate, then performs the factor analysis itself and exports the
results as `.tex` tables into `output/`.

## Installation (from scratch)

This project pins an exact environment via conda/[Miniconda](https://docs.conda.io/en/latest/miniconda.html).

1. **Install conda**, if you don't already have it. Any distribution works
   (Miniconda, Anaconda, Miniforge). Verify it's on your `PATH`:

   ```bash
   conda --version
   ```

2. **Create the project's environment** from the repo root. This reads
   [`.conda.yml`](.conda.yml), which uses Python 3.14
   and every pip dependency (`pandas`, `questionary`, `factor-analyzer`,
   `feeed`, `scikit-learn`):

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
   (one row per event log, one column per complexity measure). On success, it prints Bartlett's test and MSA diagnostics to the terminal and writes four
   `.tex` files to `output/`.

## Updating dependencies

Edit [`.conda.yml`](.conda.yml) and re-create the environment:

```bash
conda env remove -n comfy
conda env create -f .conda.yml
```
