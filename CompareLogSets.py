""" Usage:
    python CompareLogSets.py
    python CompareLogSets.py --real pdc.csv --generated generated.csv --output output/comparison/
    python CompareLogSets.py --factors 10 --rotation none --permutations 999 --seed 1
"""
import argparse
import contextlib
import io
import os
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas
from scipy.linalg import orthogonal_procrustes
from scipy.spatial import ConvexHull, Delaunay
from sklearn.decomposition import PCA

import Constants
import FactorAnalysis
from factor_analyzer.factor_analyzer import FactorAnalyzer

DEFAULT_REAL = Constants.INPUT_PATH + "log_measures_all_pdc_training_logs.csv"
DEFAULT_GENERATED = Constants.INPUT_PATH + "log_complexity_scores_gedi_generated_logs.csv"
DEFAULT_OUTPUT = Constants.OUTPUT_PATH + "comparison/"
HULL_FONT_SIZE = 24
HULL_LABEL_FONT_SIZE = 27
HULL_REAL_COLOR = "#228833"
HULL_GENERATED_COLOR = "#AA3377"


def load_common_measures(real_path, generated_path):
    real = pandas.read_csv(real_path, index_col=0)
    generated = pandas.read_csv(generated_path, index_col=0)
    common = [column for column in real.columns if column in generated.columns]
    real, generated = real[common], generated[common]
    usable = []
    for column in common:
        ok = True
        for data in (real, generated):
            values = pandas.to_numeric(data[column], errors="coerce").to_numpy(dtype=float)
            if not np.all(np.isfinite(values)) or np.isclose(values.std(), 0.0):
                ok = False
        if ok:
            usable.append(column)
    return real[usable].astype(float), generated[usable].astype(float)


def signed_log(data):
    return np.sign(data) * np.log1p(np.abs(data))


def comfy_preprocessing(data):
    analysis = FactorAnalysis.ComplexityFactorAnalysis(data)
    with contextlib.redirect_stdout(io.StringIO()):
        analysis.prepare_data_for_factor_analysis()
        analysis.repeat_calculate_measure_of_sampling_adequacy()
    return list(analysis.complexity_data.columns)


def select_factor_measures(real, generated):
    kept_generated = set(comfy_preprocessing(generated))
    candidates = [column for column in comfy_preprocessing(real) if column in kept_generated]
    kept = comfy_preprocessing(real[candidates])
    kept_generated = set(comfy_preprocessing(generated[kept]))
    return [column for column in kept if column in kept_generated]


def convex_hulls(real, generated, output):
    pooled = np.vstack([real, generated])
    pooled_z = (pooled - pooled.mean(axis=0)) / pooled.std(axis=0)
    pca = PCA(n_components=2).fit(pooled_z)
    projected = pca.transform(pooled_z)
    real_2d, generated_2d = projected[:len(real)], projected[len(real):]
    real_hull, generated_hull = ConvexHull(real_2d), ConvexHull(generated_2d)

    fig, axis = plt.subplots(figsize=(8, 8))
    axis.scatter(real_2d[:, 0], real_2d[:, 1], s=40, alpha=0.9, color=HULL_REAL_COLOR, marker="o", label="Real")
    axis.scatter(generated_2d[:, 0], generated_2d[:, 1], s=40, alpha=0.9, color=HULL_GENERATED_COLOR, marker="X", label="Generated")
    for points, hull, color in ((generated_2d, generated_hull, HULL_GENERATED_COLOR), (real_2d, real_hull, HULL_REAL_COLOR)):
        for simplex in hull.simplices:
            axis.plot(points[simplex, 0], points[simplex, 1], "-", color=color)
        axis.fill(points[hull.vertices, 0], points[hull.vertices, 1], color=color, alpha=0.1)
    ratio = pca.explained_variance_ratio_
    axis.set_xlabel("PC1 ({}% explained variance)".format(np.round(ratio[0] * 100, 2)), fontsize=HULL_LABEL_FONT_SIZE)
    axis.set_ylabel("PC2 ({}% explained variance)".format(np.round(ratio[1] * 100, 2)), fontsize=HULL_LABEL_FONT_SIZE)
    axis.tick_params(axis="both", which="both", labelsize=HULL_FONT_SIZE)
    axis.legend(fontsize=HULL_FONT_SIZE, markerscale=2)
    fig.tight_layout()
    fig.savefig(os.path.join(output, "convex-hull-pca.png"), dpi=300)
    plt.close(fig)

    return {"explained_variance_2d": float(ratio.sum()),
            "generated_to_real_hull_area_ratio": float(generated_hull.volume / real_hull.volume),
            "real_logs_inside_generated_hull": float((Delaunay(generated_2d).find_simplex(real_2d) >= 0).mean())}


def fit_loadings(data, n_factors, rotation):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        analyzer = FactorAnalyzer(n_factors=n_factors, rotation=rotation)
        analyzer.fit(data)
    return analyzer.loadings_


def tucker(x, y, axis=0):
    return np.sum(x * y, axis=axis) / np.sqrt(np.sum(x * x, axis=axis) * np.sum(y * y, axis=axis))


def procrustes_congruence(real_loadings, generated_loadings):
    rotation, _ = orthogonal_procrustes(generated_loadings, real_loadings)
    rotated = generated_loadings @ rotation
    return tucker(real_loadings, rotated, axis=0), tucker(real_loadings.ravel(), rotated.ravel())


def standardise(data):
    return (data - data.mean(axis=0)) / data.std(axis=0)


def congruence(real, generated, args, rng):
    measures = select_factor_measures(real, generated)
    real_x, generated_x = real[measures].to_numpy(), generated[measures].to_numpy()
    per_factor, overall = procrustes_congruence(fit_loadings(real_x, args.factors, args.rotation),
                                                fit_loadings(generated_x, args.factors, args.rotation))

    pooled = np.vstack([standardise(real_x), standardise(generated_x)])
    null = np.empty(args.permutations)
    for i in range(args.permutations):
        order = rng.permutation(len(pooled))
        a = fit_loadings(pooled[order[:len(real_x)]], args.factors, args.rotation)
        b = fit_loadings(pooled[order[len(real_x):]], args.factors, args.rotation)
        null[i] = procrustes_congruence(a, b)[1]

    table = pandas.Series(list(per_factor) + [overall], index=["F" + str(i + 1) for i in range(args.factors)] + ["Overall"],
                          name="procrustes_congruence")
    table.to_csv(os.path.join(args.output, "factor-congruence.csv"))
    return table, {"measures": len(measures),
                   "null_95_range": [float(np.quantile(null, 0.025)), float(np.quantile(null, 0.975))],
                   "p_value": float((1 + np.sum(null <= overall)) / (1 + len(null)))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--real", default=DEFAULT_REAL)
    parser.add_argument("--generated", default=DEFAULT_GENERATED)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--factors", type=int, default=10)
    parser.add_argument("--rotation", default="varimax", help="factor_analyzer rotation, or 'none'")
    parser.add_argument("--permutations", type=int, default=199)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    if args.rotation == "none":
        args.rotation = None
    os.makedirs(args.output, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    real, generated = load_common_measures(args.real, args.generated)
    print("Real logs: {}, generated logs: {}, shared measures: {}".format(len(real), len(generated), real.shape[1]))

    hull = convex_hulls(signed_log(real.to_numpy()), signed_log(generated.to_numpy()), args.output)
    print("Convex hull: {:.1%} explained variance, area ratio {:.1f}, {:.1%} of real logs inside the generated hull".format(
        hull["explained_variance_2d"], hull["generated_to_real_hull_area_ratio"], hull["real_logs_inside_generated_hull"]))

    table, test = congruence(real, generated, args, rng)
    print("\nTucker's congruence after Procrustes rotation ({} measures):".format(test["measures"]))
    print(table.round(2).to_string())
    print("Permutation null 95% range: {:.3f}-{:.3f}, p = {:.3f}".format(*test["null_95_range"], test["p_value"]))
    print("\nResults written to " + args.output)


if __name__ == "__main__":
    main()
