#!/usr/bin/python3
# _*_ coding: utf-8 _*_
# @Time    : 2023/9/12 09:37
# @Author  : gsunwu@163.com
# @File    : example_pyod.py
# @Description:
"""
index	sr	VUS_ROC
0	8	0.616815804
1	16	0.578078863
2	32	0.60975608
3	64	0.725382617
4	128	0.738366176
5	256	0.70718911
6	512	0.814988886
7	1024	0.812873488


"""

import sys

import pandas as pd
import torch

from sklearn.preprocessing import MinMaxScaler

from benchmark_models.pyod.models.vae import VAE
from pysearchlib.share.ExcelOutKeys import EK
from pysearchlib.share.exp_helper import JobConfV1
from pysearchlib.utils.util_common import UC
from pysearchlib.utils.util_gnuplot import UTSViewGnuplot
from pysearchlib.utils.util_pandas import PDUtil

from pysearchlib.metrics.uts.uts_metric_helper import UTSMetricHelper
from pysearchlib.utils.util_joblib import JLUtil

window_size = 64
_dataset, _data_id = ["ECG", "MBA_ECG805_data.out"]
from pysearchlib.utils.util_log import get_logger

log = get_logger()
mem = JLUtil.get_memory()

from pysearchlib.share.exp_config import ExpConf

outs = []

for _sr in JobConfV1.SAMPLE_RATES_DEBUGS:
    # conf = ExpConf(dataset_name="ECG",data_id="MBA_ECG14046_data.out",data_sample_rate=_sr,fold_index=1)
    # conf = ExpConf(model_name="VAE",dataset_name="ECG",data_id="MBA_ECG14046_data_46.out",data_sample_rate=_sr,fold_index=1)
    conf = ExpConf(model_name="VAE", dataset_name="SVDB", data_id="801.test.csv@1.out", data_sample_rate=_sr,
                   fold_index=1)
    train_x, train_y, test_x, test_y = conf.load_data()

    cuda = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Cuda: {cuda}")
    model = VAE(epochs=50)
    model.fit(train_x)
    score = model.score(test_x)
    # Post-processing

    ugp = UTSViewGnuplot()
    ugp.plot_uts_data_v3(test_x[:, -1], test_y, score, file_name=f"VAE_{_sr}")
    score = MinMaxScaler(feature_range=(0, 1)).fit_transform(score.reshape(-1, 1)).ravel()
    metrics = UTSMetricHelper.get_metrics_all(test_y, score, window_size=window_size, metric_type="vus")
    print(metrics)
    outs.append([_sr, metrics[EK.VUS_ROC]])

pdf = pd.DataFrame(outs)
pdf.columns = ["sr", EK.VUS_ROC]
PDUtil.save_to_excel(pdf, "res", home=UC.get_entrance_directory())
