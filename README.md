The source code
of ["On Data Efficiency of Univariate Time Series Anomaly Detection Models"](https://journalofbigdata.springeropen.com/articles/10.1186/s40537-024-00940-7)
published on Journal of Big Data.

## Reproduction

Five steps to reproduce our results.

1. To prepare the environment, follow these steps: 1) Create a Python environment by running pip install -r requirements.txt; 2) Download the dataset from https://www.thedatum.org/datasets/TSB-UAD-Public.zip; 3) Unzip the dataset to a directory and set this directory as the value of the DATASET_HOME environment variable.

2. Run all experiments with the command `make run_all_experiments` (tested on `ubuntu 20.04 LTS`). It may run for a few
   days. It outputs a set of directories containing the experiment results.

3. Move all directories, i.e.,  `v4010_64_02_fastuts_vus_roc_0.001_random`, to a `HOME` directory. The `HOME` directory
   is specified by `UtilSys.RUNTIME_HOME`, i.e. `UtilSys.RUNTIME_HOME="./runtime`.

4. Convert all directories to metric files by running `python convert_data.py --home HOME`.

5. Move the results file to `figs_and_tables/data` and execute `main.py` or `main.ipynb` under the
   directory `figs_and_tables`. Appendix A lists the generated files.

You can run `dev_test.py` to view the completed runflows and output log. If the environment is set up correctly, the
following files will be generated in the ./runtime directory:

```
drwxrwxrwx  3 x  staff     96 Jul 31 19:22 v_debug_dev_test_vus_roc_0.001_random
-rw-r--r--  1 x  staff   6822 Jul 31 19:31 v_debug_dev_test_vus_roc_0.001_random.bz2
-rw-r--r--  1 x  staff  17028 Jul 31 19:31 v_debug_dev_test_vus_roc_0.001_random.xlsx
-rw-r--r--@ 1 x  staff  22605 Jul 31 19:31 v_debug_dev_test_vus_roc_0.001_random_original_metrics.xlsx

```

- `v_debug_dev_test_vus_roc_0.001_random`:  Directory for calculated metrics; each metric is saved in a .bz2 file.
- `v_debug_dev_test_vus_roc_0.001_random_original_metrics.xls`: File containing all metrics from the
  v_debug_dev_test_vus_roc_0.001_random directory.
- `v_debug_dev_test_vus_roc_0.001_random.{bz2,xlsx}`: Aggregation files
  for `v_debug_dev_test_vus_roc_0.001_random_original_metrics.xls`, saved in two formats for ease of viewing and
  calculation.

**Note**: for the main figures and tables on the original paper, you can reproduce them using the following scripts.

Figures {1,4,5,6}:

```
figs_and_tables/fig.1/main.py
figs_and_tables/fig.4/main.py
figs_and_tables/fig.5/main.ipynb
figs_and_tables/fig.6/main.ipynb
```

Tables {3,4,5,6,7}
```
figs_and_tables/tab.3/main.ipynb
figs_and_tables/tab.4,5/main.py
figs_and_tables/tab.6/main.py
figs_and_tables/tab.7/main.ipynb
```

## Appendix A

All output metrics files.

```
├── v4000_01_baseline_vus_roc_0.001_random.bz2
├── v4000_01_baseline_vus_roc_0.001_random.xlsx
├── v4000_01_baseline_vus_roc_0.001_random_original_metrics.xlsx
├── v4002_00_observation_sup1_vus_roc_0.001_random.bz2
├── v4002_00_observation_sup1_vus_roc_0.001_random.xlsx
├── v4002_00_observation_sup1_vus_roc_0.001_random_original_metrics.xlsx
├── v4010_1024_02_fastuts_vus_roc_0.001_dist1.bz2
├── v4010_1024_02_fastuts_vus_roc_0.001_dist1.xlsx
├── v4010_1024_02_fastuts_vus_roc_0.001_dist1_original_metrics.xlsx
├── v4010_1024_02_fastuts_vus_roc_0.001_lhs.bz2
├── v4010_1024_02_fastuts_vus_roc_0.001_lhs.xlsx
├── v4010_1024_02_fastuts_vus_roc_0.001_lhs_original_metrics.xlsx
├── v4010_1024_02_fastuts_vus_roc_0.001_random.bz2
├── v4010_1024_02_fastuts_vus_roc_0.001_random.xlsx
├── v4010_1024_02_fastuts_vus_roc_0.001_random_original_metrics.xlsx
├── v4010_128_02_fastuts_vus_roc_0.001_dist1.bz2
├── v4010_128_02_fastuts_vus_roc_0.001_dist1.xlsx
├── v4010_128_02_fastuts_vus_roc_0.001_dist1_original_metrics.xlsx
├── v4010_128_02_fastuts_vus_roc_0.001_lhs.bz2
├── v4010_128_02_fastuts_vus_roc_0.001_lhs.xlsx
├── v4010_128_02_fastuts_vus_roc_0.001_lhs_original_metrics.xlsx
├── v4010_128_02_fastuts_vus_roc_0.001_random.bz2
├── v4010_128_02_fastuts_vus_roc_0.001_random.xlsx
├── v4010_128_02_fastuts_vus_roc_0.001_random_original_metrics.xlsx
├── v4010_256_02_fastuts_vus_roc_0.001_dist1.bz2
├── v4010_256_02_fastuts_vus_roc_0.001_dist1.xlsx
├── v4010_256_02_fastuts_vus_roc_0.001_dist1_original_metrics.xlsx
├── v4010_256_02_fastuts_vus_roc_0.001_lhs.bz2
├── v4010_256_02_fastuts_vus_roc_0.001_lhs.xlsx
├── v4010_256_02_fastuts_vus_roc_0.001_lhs_original_metrics.xlsx
├── v4010_256_02_fastuts_vus_roc_0.001_random.bz2
├── v4010_256_02_fastuts_vus_roc_0.001_random.xlsx
├── v4010_256_02_fastuts_vus_roc_0.001_random_original_metrics.xlsx
├── v4010_512_02_fastuts_vus_roc_0.001_dist1.bz2
├── v4010_512_02_fastuts_vus_roc_0.001_dist1.xlsx
├── v4010_512_02_fastuts_vus_roc_0.001_dist1_original_metrics.xlsx
├── v4010_512_02_fastuts_vus_roc_0.001_lhs.bz2
├── v4010_512_02_fastuts_vus_roc_0.001_lhs.xlsx
├── v4010_512_02_fastuts_vus_roc_0.001_lhs_original_metrics.xlsx
├── v4010_512_02_fastuts_vus_roc_0.001_random.bz2
├── v4010_512_02_fastuts_vus_roc_0.001_random.xlsx
├── v4010_512_02_fastuts_vus_roc_0.001_random_original_metrics.xlsx
├── v4010_64_02_fastuts_vus_roc_0.001_dist1.bz2
├── v4010_64_02_fastuts_vus_roc_0.001_dist1.xlsx
├── v4010_64_02_fastuts_vus_roc_0.001_dist1_original_metrics.xlsx
├── v4010_64_02_fastuts_vus_roc_0.001_lhs.bz2
├── v4010_64_02_fastuts_vus_roc_0.001_lhs.xlsx
├── v4010_64_02_fastuts_vus_roc_0.001_lhs_original_metrics.xlsx
├── v4010_64_02_fastuts_vus_roc_0.001_random.bz2
├── v4010_64_02_fastuts_vus_roc_0.001_random.xlsx
├── v4010_64_02_fastuts_vus_roc_0.001_random_original_metrics.xlsx
├── v4020_03_fastuts_sup1_rf_0.001_random 2
├── v4020_03_fastuts_sup1_rf_0.001_random.bz2
├── v4020_03_fastuts_sup1_rf_0.001_random.xlsx
├── v4020_03_fastuts_sup1_rf_0.001_random_original_metrics.xlsx
├── v4020_03_fastuts_sup1_rf_0.01_random.bz2
├── v4020_03_fastuts_sup1_rf_0.01_random.xlsx
├── v4020_03_fastuts_sup1_rf_0.01_random_original_metrics.xlsx
├── v4020_03_fastuts_sup1_rf_0.1_random.bz2
├── v4020_03_fastuts_sup1_rf_0.1_random.xlsx
├── v4020_03_fastuts_sup1_rf_0.1_random_original_metrics.xlsx
├── v4020_03_fastuts_sup1_rf_0.5_random.bz2
├── v4020_03_fastuts_sup1_rf_0.5_random.xlsx
├── v4020_03_fastuts_sup1_rf_0.5_random_original_metrics.xlsx
├── v4020_03_fastuts_sup1_vus_pr_0.001_random.bz2
├── v4020_03_fastuts_sup1_vus_pr_0.001_random.xlsx
├── v4020_03_fastuts_sup1_vus_pr_0.001_random_original_metrics.xlsx
├── v4020_03_fastuts_sup1_vus_pr_0.01_random.bz2
├── v4020_03_fastuts_sup1_vus_pr_0.01_random.xlsx
├── v4020_03_fastuts_sup1_vus_pr_0.01_random_original_metrics.xlsx
├── v4020_03_fastuts_sup1_vus_pr_0.1_random.bz2
├── v4020_03_fastuts_sup1_vus_pr_0.1_random.xlsx
├── v4020_03_fastuts_sup1_vus_pr_0.1_random_original_metrics.xlsx
├── v4020_03_fastuts_sup1_vus_pr_0.5_random.bz2
├── v4020_03_fastuts_sup1_vus_pr_0.5_random.xlsx
├── v4020_03_fastuts_sup1_vus_pr_0.5_random_original_metrics.xlsx
├── v4020_03_fastuts_sup1_vus_roc_0.001_random.bz2
├── v4020_03_fastuts_sup1_vus_roc_0.001_random.xlsx
├── v4020_03_fastuts_sup1_vus_roc_0.001_random_original_metrics.xlsx
├── v4020_03_fastuts_sup1_vus_roc_0.01_random.bz2
├── v4020_03_fastuts_sup1_vus_roc_0.01_random.xlsx
├── v4020_03_fastuts_sup1_vus_roc_0.01_random_original_metrics.xlsx
├── v4020_03_fastuts_sup1_vus_roc_0.1_random.bz2
├── v4020_03_fastuts_sup1_vus_roc_0.1_random.xlsx
├── v4020_03_fastuts_sup1_vus_roc_0.1_random_original_metrics.xlsx
├── v4020_03_fastuts_sup1_vus_roc_0.5_random.bz2
├── v4020_03_fastuts_sup1_vus_roc_0.5_random.xlsx
└── v4020_03_fastuts_sup1_vus_roc_0.5_random_original_metrics.xlsx
```

 