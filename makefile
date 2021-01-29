venv: venv/touchfile

venv/touchfile: requirements.txt
	python3 -m venv ./venv
	. venv/bin/activate && pip install -Ur requirements.txt
	touch venv/touchfile

clean:
	rm -rf venv
	rm -rf pops

zstats: data/meta_results_2021_01_19_17_56_47.csv
	python src/pvals_to_stats.py

pops:
	ln -s /broad/finucanelab/carlos/scz_pops/pops pops
	ln -s /broad/finucanelab/carlos/scz_pops/data/pops data/pops
	touch pops/touchfile

features: pops/touchfile scz.genes.out scz.raw.out
	python pops/pops.feature_selection.py \
		--features data/pops/PoPS.features.txt.gz \
		--gene_results data/scz \
		--out data/scz