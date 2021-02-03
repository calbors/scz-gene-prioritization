import pathlib

import pandas as pd
from scipy import stats

wd = str(pathlib.Path(__file__).parent.absolute()) + '/..'

genes_df = (
    pd.read_csv(f'{wd}/data/raw/gene_locs.tsv', sep='\t')
    .set_index('Gene stable ID')
    )
ensembl_to_name = genes_df['Gene name']

print(ensembl_to_name)

chroms = list(range(1, 23))
chrom_dfs = []

for chrom in chroms:
    fn = f'{wd}/data/scores/scz.{chrom}.results'

    if not pathlib.Path(fn).exists():
        continue

    print(pd.read_csv(fn).set_index('ENSGID'))

    chrom_dfs.append(
        pd.read_csv(fn)
        .set_index('ENSGID')
        .join(ensembl_to_name, how='left')
        )

results_df = (
    pd.concat(chrom_dfs)
    .sort_values(by='Score', ascending=False)
    )
results_df.to_csv(f'{wd}/data/results.tsv', sep='\t')

print(results_df)