The source code
of ["On Data Efficiency of Univariate Time Series Anomaly Detection Models"](https://journalofbigdata.springeropen.com/articles/10.1186/s40537-024-00940-7)
published on Journal of Big Data.

## Abstract
In machine learning (ML) problems, it is widely believed that more training samples lead to improved predictive accuracy but incur higher computational costs. Consequently, achieving better data efficiency, that is, the trade-off between the size of the training set and the accuracy of the output model, becomes a key problem in ML applications. In this research, we systematically investigate the data efficiency of Univariate Time Series Anomaly Detection (UTS-AD) models. We first experimentally examine the performance of nine popular UTS-AD algorithms as a function of the training sample size on several benchmark datasets. Our findings confirm that most algorithms become more accurate when more training samples are used, whereas the marginal gain for adding more samples gradually decreases. Based on the above observations, we propose a novel framework called FastUTS-AD that achieves improved data efficiency and reduced computational overhead compared to existing UTS-AD models with little loss of accuracy. Specifically, FastUTS-AD is compatible with different UTS-AD models, utilizing a sampling- and scaling law-based heuristic method to automatically determine the number of training samples a UTS-AD model needs to achieve predictive performance close to that when all samples in the training set are used. Comprehensive experimental results show that, for the nine popular UTS-AD algorithms tested, FastUTS-AD reduces the number of training samples and the training time by 91.09–91.49% and 93.49–93.82% on average without significant decreases in accuracy.

## Reproduction

To reproduce our results, follow these five steps:

1. **Prepare the environment**. Create a Python environment by running `pip install -r requirements.txt`. Next, download the dataset from [this link](https://www.thedatum.org/datasets/TSB-UAD-Public.zip) and unzip it to a directory. Set this directory as the value of the `DATASET_HOME` environment variable.

2. **Run all experiments**. Execute all experiments using the command `make run_all_experiments` (tested on Ubuntu 20.04 LTS). This process may take several days and will generate directories containing the experiment results.

3. **Collect metrics**. Move all result directories to the `HOME` directory specified by `UtilSys.RUNTIME_HOME`, which can be set as `UtilSys.RUNTIME_HOME="./runtime"`.

4. **Convert metrics**. Convert the directories to metric files by running `python convert_data.py --home HOME`. Then, move the resulting files to `figs_and_tables/data`. Appendix A lists the generated files.

5. **Reproduce figures or tables**. To generate the main figures and tables from the original paper, run the following scripts:
```
# Figures {1,4,5,6}:
figs_and_tables/fig.1/main.py
figs_and_tables/fig.4/main.py
figs_and_tables/fig.5/main.ipynb
figs_and_tables/fig.6/main.ipynb

# Tables {3,4,5,6,7}
figs_and_tables/tab.3/main.ipynb
figs_and_tables/tab.4,5/main.py
figs_and_tables/tab.6/main.py
figs_and_tables/tab.7/main.ipynb
```



**Note**: You can run `dev_test.py` to view the completed run flows and output log. If the environment is set up correctly, the following files will be generated in the `./runtime` directory:
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

##  References
> Sun W, Li H, Liang Q, et al. On data efficiency of univariate time series anomaly detection models[J]. Journal of Big Data, 2024, 11(1): 1-31.
```
@article{sun2024data,
  title={On data efficiency of univariate time series anomaly detection models},
  author={Sun, Wu and Li, Hui and Liang, Qingqing and Zou, Xiaofeng and Chen, Mei and Wang, Yanhao},
  journal={Journal of Big Data},
  volume={11},
  number={1},
  pages={1--31},
  year={2024},
  publisher={SpringerOpen}
}

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

 