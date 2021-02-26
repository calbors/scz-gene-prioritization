from utils import get_project_root

import pandas as pd

data_dir = get_project_root() + '/data'

# Index used to sort by chromosomes
chroms = [str(i) for i in range(1, 23)] + ['X']
chrom_to_rank = dict(zip(chroms, range(len(chroms))))

# Gene locs
gene_locs_rename_dict = {
    'Gene stable ID' : 'ENSGID',
    'Chromosome/scaffold name' : 'CHR',
    'Gene start (bp)' : 'START',
    'Gene end (bp)' : 'END'
    }
gene_locs_df = (
    pd.read_csv(data_dir + '/raw/gene_locs.tsv', dtype={'CHR' : str}, sep='\t')
    .rename(gene_locs_rename_dict, axis=1)
    .filter(gene_locs_rename_dict.values())
    )
gene_locs_df['chrom_rank'] = gene_locs_df['CHR'].map(chrom_to_rank)
gene_locs_df.sort_values(by=['chrom_rank', 'START'], inplace=True)
gene_locs_df.drop('chrom_rank', axis=1, inplace=True)
gene_locs_df.reset_index(drop=True, inplace=True)
gene_locs_df.to_csv(data_dir + '/processed/gene_locs.tsv', sep='\t', index=False)

# GWAS
autosomes_df = pd.read_csv(
    data_dir + '/raw/PGC3_SCZ_wave3_public.v2.tsv',
    usecols=['SNP', 'P', 'Neff', 'CHR', 'BP'],
    dtype={'CHR' : str},
    sep='\t'
    )
autosomes_df.dropna(inplace=True) # One line is missing info in raw data
x_chrom_df = pd.read_csv(
    data_dir + '/raw/daner_scz_w3_HRC_chrX_deduped_0618a',
    usecols=['SNP', 'P', 'Neff', 'CHR', 'BP'],
    dtype={'CHR' : str},
    sep='\t'
    )
x_chrom_df['CHR'] = 'X'
gwas_df = pd.concat([autosomes_df, x_chrom_df], ignore_index=True)
gwas_df['BP'] = gwas_df['BP'].astype(int)
gwas_df['chrom_rank'] = gwas_df['CHR'].map(chrom_to_rank)
gwas_df.sort_values(by=['chrom_rank', 'BP'], inplace=True)
gwas_df.drop('chrom_rank', axis=1, inplace=True)

gwas_df[['SNP', 'CHR', 'BP']].to_csv(data_dir + '/processed/snp_locs.tsv',
    sep='\t', index=False)
gwas_df[['SNP', 'P', 'Neff']].to_csv(data_dir + '/processed/gwas_p_vals.tsv',
    sep='\t', index=False)

# Exomes
exomes_df = pd.read_csv(data_dir + '/raw/meta_results_2021_01_19_17_56_47.csv',
    usecols=['Gene', 'P meta'])
exomes_df.dropna(inplace=True)
exomes_df.rename({'Gene' : 'ENSGID', 'P meta' : 'P'}, axis=1, inplace=True)
exomes_df.sort_values(by='P', inplace=True)
exomes_df.to_csv(data_dir + '/processed/exomes_p_vals.tsv', sep='\t', index=False)