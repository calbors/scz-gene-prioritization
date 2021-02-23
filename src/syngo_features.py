from utils import get_project_root

import pandas as pd

data_dir = get_project_root() + '/data'

syngo_ontologies_df = pd.read_excel(data_dir + '/syngo/syngo_ontologies.xlsx')
syngo_genes_df = pd.read_excel(data_dir + '/syngo/syngo_genes.xlsx')

# Map from ontology to HGNC
genes_list = list(
    syngo_ontologies_df['genes - hgnc_id']
    .fillna('')
    .apply(lambda s: s.split(';'))
    )
ontology_to_hgnc = pd.Series(genes_list, index=syngo_ontologies_df['GO term ID'])

# Map from HGNC to ENSEMBL
hgnc_to_ensembl = pd.Series(
    list(syngo_genes_df['ensembl_id']),
    index=syngo_genes_df['hgnc_id']
    ).to_dict()

# Compose maps and invert
ontology_to_ensembl = ontology_to_hgnc.apply(
    lambda l: [hgnc_to_ensembl[k] for k in l if k != '']
    )

# Make SynGO feature matrix
# features_df = to_features(ensembl_to_ontology)
features_df = pd.DataFrame(index=list(ontology_to_ensembl.keys()))
    
for k, v in ontology_to_ensembl.items():
    for k_ in v:
        if k_ not in features_df.columns.to_list():
            features_df[k_] = 0

        features_df.loc[k, k_] = 1

features_df = features_df.T

print(features_df)

# features_df.to_csv(f'{wd}/data/features.csv')