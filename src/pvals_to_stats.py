import pathlib

import pandas as pd
from scipy import stats

wd = pathlib.Path(__file__).parent.absolute()
pvals_df = pd.read_csv(f'{wd}/../data/meta_results_2021_01_19_17_56_47.csv')
pvals_df.set_index('Gene', inplace=True)
stats_ = pvals_df['P meta'].dropna()
eps = 0.99
stats_ = 0.5 + eps * (stats_ - 0.5)

stats_.rename('P', inplace=True)

stats_df = stats_.to_frame()
stats_df['GENE'] = stats_df.index
stats_df.reset_index(drop=True, inplace=True)
stats_df['ZSTAT'] = stats_df['P'].apply(stats.norm.isf)

stats_df.to_csv(f'{wd}/../data/scz.genes.out', index=False)