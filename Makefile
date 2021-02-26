# Set .env
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

clean:
	rm -rf data
	rm -rf magma

data/raw.tgz:
	mkdir -p data
	rsync $(REMOTE_HOST_LOGIN)@$(REMOTE_HOST):$(RAW_DATA_PATH) data/raw.tgz

data/raw/touchfile: data/raw.tgz
	mkdir -p data/raw
	tar -xf data/raw.tgz -C data/raw
	touch data/raw/touchfile

data/syngo/touchfile: data/raw/touchfile
	mkdir -p data/syngo
	unzip data/raw/SynGO_bulk_download_release_20180731.zip \
		-d data/syngo
	touch data/syngo/touchfile 

data/syngo.tsv: data/syngo/touchfile
	mkdir -p data/features
	python src/syngo_features.py

data/processed/touchfile: data/raw/touchfile
	mkdir -p data/processed
	python src/process_raw.py

data/magma/scz.genes.annot: magma/touchfile
	mkdir -p data/magma
	magma/magma --annotate \
		--snp-loc data/processed/snp_locs.tsv \
		--gene-loc data/processed/gene_locs.tsv \
		--out data/magma/scz

data/magma/scz.genes.out: data/magma/scz.genes.annot
	magma/magma \
		--bfile data/raw/g1000_eur \
		--gene-annot data/magma/scz.genes.annot \
		--pval data/processed/gwas_p_vals.tsv ncol=Neff \
		--gene-model snp-wise=mean \
		--out data/magma/scz



venv: venv/touchfile

venv/touchfile: requirements.txt
	python3 -m venv ./venv
	. venv/bin/activate && pip install -Ur requirements.txt
	touch venv/touchfile

zstats: data/raw/meta_results_2021_01_19_17_56_47.csv data/raw/gene_locs.tsv
	python src/pvals_to_stats.py

pops:
	ln -s /broad/finucanelab/carlos/scz_pops/pops pops
	ln -s /broad/finucanelab/carlos/scz_pops/data/pops data/pops
	touch pops/touchfile

features: pops/touchfile data/scz.genes.out data/scz.genes.raw
	python pops/pops.feature_selection.py \
		--features data/pops/PoPS.features.txt.gz \
		--gene_results data/scz \
		--out data/scz

scores: data/scz.features
	mkdir -p data/scores
	touch data/scores/touchfile
	qsub src/submit_make_scores.sh

results: data/scores/touchfile
	python src/munge_genes.py