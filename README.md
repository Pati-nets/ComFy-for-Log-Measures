# ComFy for Log Measures

ComFy performs a factor analysis on complexity measures of event logs (e.g. from
process mining) to identify latent factors behind those measures. Given a CSV
file of per-log complexity scores, it runs Bartlett's test of sphericity and
the measure of sampling adequacy (MSA/KMO) to check whether a factor analysis
is appropriate, then performs the factor analysis itself and exports the
results as `.tex` tables into `output/`.

## Contents

- [Installation (from scratch)](#installation-from-scratch)
- [Updating dependencies](#updating-dependencies)
- [Usage](#usage)
- [Reproducing the paper](#reproducing-the-paper)
  - [Mapping of results to scripts](#mapping-of-results-to-scripts)
  - [Recomputing the measure files from the event logs](#recomputing-the-measure-files-from-the-event-logs)

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
   python main.py
   ```

   See [Usage](#usage) for the interactive steps and
   [Reproducing the paper](#reproducing-the-paper) for the exact settings used in the paper.

## Updating dependencies

Edit [`.conda.yml`](.conda.yml) and re-create the environment:

```bash
conda env remove -n comfy
conda env create -f .conda.yml
```

## Usage
Ensure that the `xes`-files or a `csv`-file containing the results of the log measures you want to analyze are in the folder `input`.
For example, you can use the trainings logs from the process discovery contest, found at (https://www.tf-pm.org/competitions-awards/discovery-contest).
Then, run the program by executing the following command:
```
python main.py
```
If the installation was successful, you will be greeted by the following sight:
![A screenshot showing the start of the program, where the user can select the measures they want to analyze](./images/comfy-logs-startup.png)
You can use the arrow keys to navigate through the options and choose whether you want to analyze .xes files directly or import the results of log measures located in a .csv file.
If you choose the former, the tool will automatically go through all .xes files in the folder `input` and calculate the log measures based on their implementation in the FEEED library.
Choosing the latter lets you specify the location of the .csv file as shown in the following.
![A screenshot showing how to specify the location of a .csv file](./images/comfy-logs-csv-import.png)
Afterward, you can choose which measures you want to analyze. 
If you imported a .csv file, only the measures mentioned in its header are available.
The available measures are grouped in the same way as the FEEED library, so you are not overwhelmed by the total amount of measures.
![A screenshot showing the options when selecting log measures](./images/comfy-logs-measure-selection.png)
As soon as you are happy with your selection, choose the option `I have selected the measures that I want to analyze` and hit enter.
ComFy will then automatically start the analysis by performing two statistical tests:
- Bartlett's test of sphericity, described at (https://en.wikipedia.org/wiki/Bartlett's_test).
- Kaiser-Meyer-Olkin test, described at (https://en.wikipedia.org/wiki/Kaiser-Meyer-Olkin_test).
If one of these tests fails, you will be informed by the tool.
Otherwise, you will next be asked whether you want to perform a Scree test, as described in (https://en.wikipedia.org/wiki/Scree_plot).
![A screenshot showing how the program shows the Scree plot](./images/comfy-logs-scree-plot.png)
Afterward, ComFy will prompt you to input the number of expected factors.
Finally, you can choose the rotation that you want to execute on the raw data to make it easier to interpret.
![A screenshot showing the selectable rotations for the factor analysis](./images/comfy-logs-rotation-selection.png)
ComFy then executes the factor analysis with the specified parameters.
If desired, the program directly shows the factor loadings, descriptive statistics and the communalities by using the Python library `matplotlib`.
![A screenshot showing the factor loadings of the exemplary factor analysis](./images/comfy-logs-show-factor-loadings.png)
Regardless of the user's choice, ComFy will store the results of the factor analysis and the results of all previous tests in a LaTeX file in the folder `output`.
Furthermore, if the values of the log measures were extracted from .xes files, it stores the raw complexity data in a `csv`-file for later reference or further investigations.
![A screenshot showing files in the output folder that result from the executed factor analysis](./images/comfy-logs-export.png)
To see the LaTeX files stored during the analysis of the paper *Cleaning Up the Measure Mess: A Factor Analysis on Event Log Measures*, you may navigate to the folder `paper-results` inside the folder `output`.

## Reproducing the paper

All results of the paper can be reproduced from the two measure files in `input/`. The event logs themselves are only needed to recompute these files.

| File | Content |
|---|---|
| `input/log_complexity_scores_gedi_generated_logs.csv` | Log measures of the 1450 event logs generated with GEDI |
| `input/log_measures_all_pdc_training_logs.csv` | Log measures of the 2112 training logs of the Process Discovery Contest (PDC) 2020–2025 |

### Mapping of results to scripts

| Paper element | Command | Output |
|---|---|---|
| Factor analysis on the generated logs (dimensions, loadings, communalities, descriptive statistics) | `python main.py`: import the `.csv` file `input/log_complexity_scores_gedi_generated_logs.csv`, select all measures, 10 factors, `varimax` | `.tex`/`.pdf` files in `output/`. The files of the paper are in `output/paper-results/varimax/` |
| Factor analysis with other rotations | same as above with one of the rotations `promax`, `oblimin`, `oblimax`, `quartimin`, `quartimax`, `equamax`, or `no rotation` | `output/paper-results/<rotation>/` (`no-rotation/` for `no rotation`) |
| Fig. *First two principal components … with their convex hulls* (`fig:convex-hull`) | `python CompareLogSets.py` | `output/comparison/convex-hull-pca.png` |
| Coverage numbers in *Comparison of Generated and PDC Event Logs* (125 measures, hull area ratio 5.0, 92.1% inside, 50% explained variance) | `python CompareLogSets.py` | printed to the terminal |
| Tab. *Tucker's congruence* (`tab:congruence`) and the permutation test (199 permutations) | `python CompareLogSets.py` | Null range and p-value printed to the terminal: `output/comparison/factor-congruence.csv` |
| Fig. *Distributions of the representative measures* (`fig:dimension-distributions`) and the per-dimension maxima | `python PlotDimensionDistributions.py input/log_complexity_scores_gedi_generated_logs.csv input/log_measures_all_pdc_training_logs.csv -o output/comparison/dimension-distributions.pdf` | Maxima printed to the terminal: `output/comparison/dimension-distributions.pdf`|

`CompareLogSets.py` takes about 5 minutes because of the permutation test. Use `--permutations` to change their number.

### Recomputing the measure files from the event logs

1. **Generated logs.** [`log-generator/event_log_generator.py`](log-generator/event_log_generator.py) writes one GEDI target file per measure to `log-generator/targets/` (`generate_targets`) and calls GEDI on each of them (`generate_event_logs`). This requires an installation of [GEDI](https://github.com/lmu-dbs/gedi).
2. **Measures.** [`log-generator/measure_evaluator.py`](log-generator/measure_evaluator.py) computes the log measures with [FEEED](https://github.com/lmu-dbs/feeed) for all `.xes` files and writes `log_complexity_scores_<folder>.csv`.
3. **PDC logs.** The training logs are available from the [Process Discovery Contest](https://www.tf-pm.org/competitions-awards/discovery-contest). The directory `input/` contains four examples. Running `python main.py` with the option to calculate the measures from `.xes` files computes the measure file for all logs in `input/`.

