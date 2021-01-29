import pathlib

import pandas as pd
from scipy import stats

wd = str(pathlib.Path(__file__).parent.absolute()) + '/..'
pvals_df = pd.read_csv(f'{wd}/data/raw/meta_results_2021_01_19_17_56_47.csv')

pvals_df.set_index('Gene', inplace=True)
stats_ = pvals_df['P meta'].dropna()
eps = 1 - 1e-7
stats_ = 0.5 + eps * (stats_ - 0.5)

stats_.rename('P', inplace=True)

stats_df = stats_.to_frame()
stats_df['GENE'] = stats_df.index
stats_df.reset_index(drop=True, inplace=True)
stats_df['ZSTAT'] = stats_df['P'].apply(stats.norm.isf)

locs_df = pd.read_csv(f'{wd}/data/raw/gene_locs.tsv', sep='\t')

stats_df = stats_df.merge(locs_df, how='left', left_on='GENE', right_on='Gene stable ID')
stats_df.drop(columns=['Gene stable ID', 'Gene stable ID version', 'Gene name'], inplace=True)
rename_dict = {
    'Chromosome/scaffold name' : 'CHR',
    'Gene start (bp)' : 'START',
    'Gene end (bp)' : 'STOP'
    }
stats_df.rename(columns=rename_dict, inplace=True)
stats_df['N'] = 1
stats_df['NSNPS'] = 1
stats_df['NPARAM'] = 1
col_list = ['GENE', 'CHR', 'START', 'STOP', 'NSNPS', 'NPARAM', 'N', 'ZSTAT', 'P']
stats_df = stats_df[col_list]

# Sort by chr
chr_order = [f'{i}' for i in range(1, 23)] + ['X']

stats_df['CHR'] = pd.Categorical(stats_df['CHR'], chr_order)
stats_df.sort_values(['CHR', 'START'], inplace=True)
stats_df.reset_index(inplace=True, drop=True)

# Delete this next line once PoPS is fixed
stats_df = stats_df[stats_df['CHR'] != 'X']

raw_data = '' # Str to write into genes.raw

i = 0

for __, row in stats_df.iterrows():
    row_data = ''

    for k in ['GENE', 'CHR', 'START', 'STOP', 'NSNPS', 'NPARAM', 'N']:
        row_data += f'{row[k]} '

    row_data += '0 0 '

    # Pad correlations with zero
    # Only lower triangle is included
    for j in range(i):
        row_data += '0 '

    row_data = row_data.rstrip()

    i += 1
    raw_data += row_data + '\n'

raw_data = raw_data.rstrip()

stats_df.to_csv(f'{wd}/data/scz.genes.out', index=False, sep='\t')

with open(f'{wd}/data/scz.genes.raw', 'w') as fp:
    fp.write('# VERSION = 108\n')
    fp.write('COVAR = NSAMP MAC\n')
    fp.write(raw_data)