import pathlib

import pandas as pd
from scipy import stats

wd = str(pathlib.Path(__file__).parent.absolute()) + '/..'

genes_df = (
    pd.read_csv(f'{wd}/data/raw/gene_locs.tsv', sep='\t')
    .set_index('Gene stable ID')
    )
ensembl_to_name = genes_df['Gene name'].rename('Gene')

chroms = list(range(1, 23))
chrom_dfs = []

for chrom in chroms:
    filename = f'{wd}/data/scores/scz.{chrom}.results'

    if not pathlib.Path(filename).exists():
        continue

    chrom_dfs.append(
        pd.read_csv(filename)
        .set_index('ENSGID')
        .join(genes_df['Gene name'], how='left')
        )

results_df = (
    pd.concat(chrom_dfs)
    .sort_values(by='Score', ascending=False)
    )
results_df.to_csv(f'{wd}/data/results.tsv', sep='\t')

print(results_df)