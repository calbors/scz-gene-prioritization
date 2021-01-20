venv: venv/touchfile

venv/touchfile: requirements.txt
	python3 -m venv ./venv
	. venv/bin/activate && pip install -Ur requirements.txt
	touch venv/touchfile

zstats: data/meta_results_2021_01_19_17_56_47.csv
	python src/pvals_to_stats.py

pops:
	mkdir pops
	wget -O pops/features.zip https://www.dropbox.com/sh/dz4haeo48s34sex/AAAun_PLqCt_0Qp3x9b9tk5oa/data?dl=0&subfolder_nav_tracking=1

clean:
	rm -rf venv
	rm -rf pops

