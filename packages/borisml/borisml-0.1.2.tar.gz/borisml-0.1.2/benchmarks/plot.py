import seaborn
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import pandas as pd
import numpy as np
import umap

import shutil
import glob
import os


REPORT_DIR = './reports/'
OUTPUT_DIR = './outputs/'


def _find_lower_lim(x):
    """Find the next multiple of 10 which is lower than x

    """
    x = int(np.floor((x * 100)))
    while x % 10 > 0:
        x -= 1
    return x / 100.


def _find_upper_lim(x):
    """Find the next multiple of 10 which is larger than x

    """
    x = int(np.ceil(x * 100))
    while x % 10 > 0:
        x += 1
    return x / 100.


def make_box_plot(ax, df, metric, sample_percentage, m, M):
    """Make a box plot which shows the metric for all strategies
       at the given percentage of the data.

    Args:
        ax: matplotlib axes
        df: Pandas dataframe containing the results (see log.py -> Logger)
        metric: The metric to show (e.g. classification-top-1-accuracy)
        sample_percentage: At which percentage of the data to plot
            (e.g. 0.1 for 10%)
        m: lower bound for the x-axis
        M: upper bound for the x-axis

    """

    df_copy = df.loc[abs(df['sample_percentage'] - sample_percentage) < 1e-2]

    seaborn.boxplot(x=metric, y='embedding_model', hue='sampling_strategy',
                    data=df_copy, palette='vlag', ax=ax, width=0.25)

    ax.xaxis.grid(True)
    ax.yaxis.grid(False)
    ax.set(ylabel="")
    ax.set(title=str(int(100 * sample_percentage)) + '% of the Data')

    ax.set(xlim=[m, M])
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.05))
    ax.legend(loc='lower right')


def make_line_plot(ax, df, metric, embedding_model):
    """Make a line plot which shows the metric for all strategies
       at all percentages of the data.

    Args:
        ax: matplotlib axes
        df: Pandas dataframe containing the results (see log.py -> Logger)
        metric: The metric to show (e.g. classification-top-1-accuracy)
        embedding_model: The model for which the plots are made

    """

    df_copy = df.loc[df['embedding_model'] == embedding_model]

    palette = 'colorblind'
    seaborn.lineplot(x='sample_percentage', y=metric, hue='sampling_strategy',
                     data=df_copy, dashes=True, LineWidth=2.,
                     palette=palette, err_style='bars')

    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    ax.set(xlim=[0.1, 1.1])
    ax.set(ylim=[0, 1])
    ax.set(aspect='equal')
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))

    ax.legend(loc='lower right')


def make_scatter_plot(X, y, title):
    """Make a scatter plot of the embeddings in X

    Args:
        X: Embeddings (N x d) numpy array
        y: Labels for coloring
        title: Title for the plot

    """

    trans = umap.UMAP().fit(X)

    seaborn.set_style("darkgrid")

    f, ax = plt.subplots(figsize=(10, 10))
    f.suptitle(title.upper(), x=0., y=.93, horizontalalignment='left')

    seaborn.scatterplot(x=trans.embedding_[:, 0], y=trans.embedding_[:, 1],
                        hue=y.astype(int), legend='full',
                        palette='tab20b')

    ax.set(aspect='equal')

    m = trans.embedding_[:, :2].min()
    M = trans.embedding_[:, :2].max()

    ax.set(xlim=(m-1, M+1))
    ax.set(ylim=(m-1, M+1))

    return f


def make_box_plots(df, metric):
    """Make all box plots for the specified metric

    """

    percentages = df['sample_percentage'].unique()
    n_percentages = len(percentages)
    n_embeddings = len(df['embedding_model'].unique())
    n_samplers = len(df['sampling_strategy'].unique())
    f, axs = plt.subplots(n_percentages, figsize=(10, n_percentages *
                                                  (n_embeddings *
                                                   n_samplers)))

    m = _find_lower_lim(df[metric].min())
    M = _find_upper_lim(df[metric].max())

    if n_percentages < 2:
        axs = [axs]

    for i, percentage in enumerate(percentages):
        make_box_plot(axs[i], df, metric, percentage, m, M)

    f.tight_layout(rect=[0, 0, 1, 0.95])
    f.suptitle(metric.upper(), x=0., y=.98, horizontalalignment='left')

    return f


def make_line_plots(df, metric):
    """Make all line plots for the specified metric

    """

    n_embeddings = len(df['embedding_model'].unique())
    f, axs = plt.subplots(n_embeddings, figsize=(10, 10
                                                 * n_embeddings))

    if n_embeddings < 2:
        axs = [axs]

    for i, model in enumerate(df['embedding_model'].unique()):
        make_line_plot(axs[i], df, metric, model)

    f.tight_layout(rect=[0, 0, 1, 0.9])
    f.suptitle(metric.upper(), x=0., y=.93, horizontalalignment='left')

    return f


def make_plots(df, Xs, path=None):
    """Make all plots and save them if path is specified

    Args:
        df: pandas dataframe which stores the results from a benchmark run
        Xs: list of tuples (X, filename)
            where X is the embedding stored in filename
        path: path to the directory where the plots are to be stored

    """

    seaborn.set_style('darkgrid')

    # box plots
    box_plots = []
    for column in df.columns[5:]:
        f = make_box_plots(df, column)
        box_plots.append(f)

    # save box plots
    if path is not None:
        for f in box_plots:
            name = f._suptitle.get_text()
            name = 'BOX-' + name
            tmp_path = os.path.join(path, name)
            tmp_path = tmp_path + '.pdf'
            f.savefig(tmp_path, format='pdf')
            plt.close(f)

    # line plots
    line_plots = []
    for column in df.columns[5:]:
        f = make_line_plots(df, column)
        line_plots.append(f)

    # save line plots
    if path is not None:
        for f in line_plots:
            name = f._suptitle.get_text()
            name = 'LINE-' + name
            tmp_path = os.path.join(path, name)
            tmp_path = tmp_path + '.pdf'
            f.savefig(tmp_path, format='pdf')
            plt.close(f)

    # make scatter plots
    scatter_plots = []
    for X, filename in Xs:
        f = make_scatter_plot(X[:, :-1], X[:, -1], filename)
        scatter_plots.append(f)

    # save scatter plots
    if path is not None:
        for f in scatter_plots:
            name = f._suptitle.get_text()
            name = 'SCATTER-' + name
            tmp_path = os.path.join(path, name)
            tmp_path = tmp_path + '.pdf'
            f.savefig(tmp_path, format='pdf')
            plt.close(f)


if __name__ == '__main__':

    benchmark_dirs = glob.glob(
        OUTPUT_DIR + '*-*-*/*-*-*/'
    )

    # create report directory
    if not os.path.exists(REPORT_DIR):
        os.mkdir(REPORT_DIR)

    for benchmark_dir in benchmark_dirs:

        report_dir = os.path.join(
            REPORT_DIR,
            '/'.join(benchmark_dir.split('/')[2:])
        )

        if not os.path.exists(report_dir):
            os.makedirs(report_dir)

        print('Processing: ' + benchmark_dir)
        print('Report to : ' + report_dir)

        # read log file
        log_file = glob.glob(benchmark_dir + 'benchmark.*.csv')[-1]
        shutil.copy2(log_file, report_dir)
        df = pd.read_csv(log_file)

        # read embeddings
        Xs = []
        embedding_files = glob.glob(benchmark_dir + 'embeddings-*.csv')
        for embedding_file in embedding_files:
            shutil.copy2(embedding_file, report_dir)
            X = np.loadtxt(embedding_file)
            name = os.path.basename(embedding_file)
            Xs.append((X, name))

        # make plots
        plot_dir = os.path.join(report_dir + 'plots')
        if not os.path.exists(plot_dir):
            os.mkdir(plot_dir)

        make_plots(df, Xs, path=plot_dir)
