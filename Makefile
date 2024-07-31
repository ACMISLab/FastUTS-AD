export JOBS_TYPE=ml
test:
	python 00_observation_sup1.py
	python 01_baseline.py
	python 02_fastuts.py
	python 03_fastuts_sup1.py

run_all_experiments:
	JOBS_TYPE=ml python 00_observation_sup1.py
	JOBS_TYPE=ml python 01_baseline.py
	JOBS_TYPE=ml python 02_fastuts.py
	JOBS_TYPE=ml python 03_fastuts_sup1.py

	JOBS_TYPE=dl python 00_observation_sup1.py
	JOBS_TYPE=dl python 01_baseline.py
	JOBS_TYPE=dl python 02_fastuts.py
	JOBS_TYPE=dl python 03_fastuts_sup1.py

debug:
	python dev_test.py