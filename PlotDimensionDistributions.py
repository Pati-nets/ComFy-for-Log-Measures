""" Usage:
    python plot_dimension_distributions.py generated.csv pdc.csv -o dims.pdf
    python plot_dimension_distributions.py generated.csv pdc.csv --scores -o dims.pdf
"""
import argparse
import textwrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

# Dimension name -> (CSV column, label). Column names follow LatexExporter.py.
DIMENSIONS = {
    "Event Log Volume":               ("epa_variant_entropy",            "epa-var"),
    "Neighborhood Complexity":        ("number_of_successions",          "succ"),
    "Activity Frequency":             ("start_activities_q1",            "A-start-Q1"),
    "Activity Repetition":            ("start_activities_std",           "A-start-dev"),
    "Trace Length":                   ("simple_trace_diversity",         "s-T-div"),
    "Subsequence Repetition":         ("avg_loops_per_trace",            "loop-avg-#"),
    "Trace Dissimilarity":            ("epa_normalized_variant_entropy", "epa-n-var"),
    "Relative Activity Frequency":    ("rel_unique_end_activities",      "A-end-rel"),
    "Trace Length Variety":           ("trace_len_kurtosis_hist",        "TL-hist-kurt"),
    "Relative Number of Repetitions": ("avg_traces_with_repetition",     "rep-rel-#"),
}
COLORS = {"Generated": "#AA3377", "PDC": "#228833"} 


def signed_log(x):
    """Log-transform that keeps sign and zeros, for heavily skewed measures."""
    return np.sign(x) * np.log1p(np.abs(x))


def representative_values(gen, pdc):
    cols = [c for c, _ in DIMENSIONS.values()]
    missing = [c for c in cols if c not in gen or c not in pdc]
    if missing:
        raise SystemExit(f"Columns not found in both CSVs: {missing}")
    labels = [f"{dim}\n({label})" for dim, (_, label) in DIMENSIONS.items()]
    return (signed_log(gen[cols]).set_axis(labels, axis=1),
            signed_log(pdc[cols]).set_axis(labels, axis=1))


def factor_scores(gen, pdc, measures, rotation):
    """Fit the model on the generated logs, then score both sets with it.

    PDC logs are standardized with the generated logs' mean and SD, so both
    sets are placed in the same factor space.
    """
    from factor_analyzer import FactorAnalyzer
    g = signed_log(gen[measures])
    p = signed_log(pdc[measures])
    mu, sd = g.mean(), g.std()
    fa = FactorAnalyzer(n_factors=len(DIMENSIONS), rotation=rotation)
    fa.fit((g - mu) / sd)
    labels = list(DIMENSIONS)  # assumes factor order = dimension order; check the loadings
    return (pd.DataFrame(fa.transform((g - mu) / sd), columns=labels),
            pd.DataFrame(fa.transform((p - mu) / sd), columns=labels))


def wrap_title(col, width=15):
    """Wrap the dimension name; keep the measure label on its own line."""
    name, _, rest = col.partition("\n")
    return "\n".join(textwrap.wrap(name, width) + ([rest] if rest else []))


def plot(gen, pdc, out, xlabel):
    plt.rcParams.update({"font.size": 7, "axes.linewidth": 0.6,
                         "ytick.major.width": 0.6, "ytick.major.size": 2.5})
    fig, axes = plt.subplots(2, 5, figsize=(4.8, 2.75), constrained_layout=True)
    fig.get_layout_engine().set(w_pad=0.02, h_pad=0.04, wspace=0.04, hspace=0.06)
    for ax, col in zip(axes.flat, gen.columns):
        data = [gen[col].dropna(), pdc[col].dropna()]
        parts = ax.violinplot(data, positions=[0, 1], showextrema=False, widths=0.85)
        for body, name in zip(parts["bodies"], COLORS):
            body.set_facecolor(COLORS[name])
            body.set_edgecolor(COLORS[name])
            body.set_alpha(0.55)
        ax.boxplot(data, positions=[0, 1], widths=0.16, showfliers=False,
                   medianprops={"color": "black", "linewidth": 0.8},
                   whiskerprops={"linewidth": 0.6},
                   capprops={"linewidth": 0}, boxprops={"linewidth": 0.6})
        d = ks_2samp(*data).statistic
        ax.set_title(wrap_title(col), fontsize=7, linespacing=1.1)
        lo, hi = ax.get_ylim()
        ax.set_ylim(lo, hi + 0.18 * (hi - lo))  # headroom for the D label
        ax.text(0.5, 0.99, f"D = {d:.2f}", transform=ax.transAxes,
                ha="center", va="top", fontsize=6.5)
        ax.set_xticks([])
        ax.set_xlim(-0.6, 1.6)
        ax.tick_params(axis="y", labelsize=6, pad=1.5)
        ax.yaxis.set_major_locator(plt.MaxNLocator(3))  # fewer ticks on the short axes
        ax.spines[["top", "right"]].set_visible(False)
    for ax in axes[:, 0]:
        ax.set_ylabel(xlabel, fontsize=7)
    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=c, alpha=0.55, edgecolor=c)
               for c in COLORS.values()]
    fig.legend(handles, list(COLORS), loc="outside lower center", ncol=2,
               fontsize=7, frameon=False, handlelength=1.2, columnspacing=1.5)
    fig.savefig(out, bbox_inches="tight", pad_inches=0.02)
    print(f"Saved {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("generated_csv")
    ap.add_argument("pdc_csv")
    ap.add_argument("-o", "--out", default="dimension-distributions.pdf")
    ap.add_argument("--scores", action="store_true",
                    help="plot factor scores instead of representative measures")
    ap.add_argument("--measures", help="text file with the retained measures, one per line "
                                       "(required with --scores)")
    ap.add_argument("--rotation", default="varimax")
    args = ap.parse_args()

    gen, pdc = pd.read_csv(args.generated_csv), pd.read_csv(args.pdc_csv)
    if args.scores:
        if not args.measures:
            raise SystemExit("--scores needs --measures (the measures retained in the paper)")
        measures = [m.strip() for m in open(args.measures) if m.strip()]
        g, p = factor_scores(gen, pdc, measures, args.rotation)
        plot(g, p, args.out, "factor score")
    else:
        print_ranges(gen, pdc)
        g, p = representative_values(gen, pdc)
        plot(g, p, args.out, "value (signed log)")


def print_ranges(gen, pdc):
    """Per dimension: generated and PDC maximum, and the share of PDC logs above the generated maximum."""
    for dim, (col, _) in DIMENSIONS.items():
        above = (pdc[col] > gen[col].max()).mean()
        print(f"{dim:32s} {col:32s} gen max {gen[col].max():12.4g}  PDC max {pdc[col].max():12.4g}  "
              f"PDC above gen max {above:6.1%}")


if __name__ == "__main__":
    main()
