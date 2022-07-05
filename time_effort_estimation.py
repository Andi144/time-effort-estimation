import argparse
import os.path
from glob import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_duration_histograms(input_path: str, data_col_index: int, ncols: int, figsize: tuple, output_file: str):
    files = sorted(glob(os.path.join(input_path, "*.csv"))) if os.path.isdir(input_path) else [input_path]
    nrows = int(np.ceil(len(files) / ncols))
    ncols = min(ncols, len(files))
    if figsize is None:
        figsize = (ncols * 5, nrows * 5)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, squeeze=False, figsize=figsize, constrained_layout=True)
    axes = axes.flatten()
    
    for ax, file in zip(axes, files):
        df = pd.read_csv(file, dtype=float)
        durations = df.iloc[:, data_col_index].values
        sns.histplot(durations, binwidth=2, binrange=(0, round(max(durations))), ax=ax)
        ax.set_title(f"{os.path.basename(file)}\n"
                     f"{len(durations)} responses; mean = {np.mean(durations):.1f}; "
                     f"median = {np.median(durations):.1f}")
        ax.set_xlabel("Estimated Hours")
    for i in range(min(len(axes), len(files)), max(len(axes), len(files))):
        axes[i].set_visible(False)
    
    if output_file is None:
        if os.path.isfile(input_path):
            input_path = os.path.dirname(input_path)
        output_file = os.path.join(input_path, "time_effort_estimation.png")
    fig.savefig(output_file)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=str,
                        help="Path to CSV file that contains the time effort estimation (duration in hours). The CSV "
                             "file must have a column with the duration (which column can be specified with its index "
                             "'data_col_index'). The path can also point to a directory, in which case all CSV files "
                             "in this directory (non-recursively) will be processed.")
    parser.add_argument("--data_col_index", type=int, default=1,
                        help="Index of the column that contains the duration in hours (actual data). Default: 1")
    parser.add_argument("--figsize", type=float, nargs="+", default=None,
                        help="The size of the plot figure given as two numbers (width and height). If not specified, "
                             "the figure size will be automatically determined based on the number of subplots.")
    parser.add_argument("--ncols", type=int, default=3, help="Number of subplot columns. Default: 3")
    parser.add_argument("--output_file", type=str, default=None,
                        help="Path to plot output file. The file extension determines which kind of plot output will "
                             "be created. If not specified, the plot output file will be created in the same "
                             "parent directory of 'input_path' if it is a file or directly in 'input_path' if it is "
                             "a directory. The default filename will be 'time_effort_estimation.png'.")
    args = parser.parse_args()
    if args.figsize is not None:
        if len(args.figsize) != 2:
            raise ValueError("'figsize' must have exactly two numbers (width and height)")
        args.figsize = tuple(args.figsize)
    plot_duration_histograms(args.input_path, args.data_col_index, args.ncols, args.figsize, args.output_file)
