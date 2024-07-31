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
from benchmark_models.tsbuad.models.lstm import lstm
from pysearchlib.share.ExcelOutKeys import EK
from pysearchlib.share.example_helper import ExampleHelper
from pysearchlib.share.exp_helper import JobConfV1
from pysearchlib.metrics.uts.uts_metric_helper import UTSMetricHelper
from pysearchlib.utils.util_common import UC
from pysearchlib.utils.util_gnuplot import UTSViewGnuplot
from pysearchlib.utils.util_pandas import PDUtil
from pysearchlib.utils.util_torch import is_mps_available

from pysearchlib.utils.util_joblib import JLUtil

window_size = 64
from pysearchlib.utils.util_log import get_logger

log = get_logger()
mem = JLUtil.get_memory()

from pysearchlib.share.exp_config import ExpConf

outs = []

for _sr in JobConfV1.SAMPLE_RATES_DEBUGS:
    conf = ExampleHelper.get_exp_conf_ecg(_sr)

    dirty_train_sample_x, dirty_train_sample_y, clean_train_sample_x, clean_train_sample_y, \
        test_x, test_y = conf.load_data_for_lstm_and_cnn()

    cuda = "mps" if is_mps_available() else "cpu"
    print(f"Cuda: {cuda}")

    from benchmark_models.tsbuad.models.lstm import lstm

    model = lstm(slidingwindow=window_size, epochs=1, verbose=10)

    model.fit(clean_train_sample_x)

    score = model.score(test_x)
    score = MinMaxScaler(feature_range=(0, 1)).fit_transform(score.reshape(-1, 1)).ravel()

    ugp = UTSViewGnuplot()
    ugp.plot_uts_data_v3(test_x[:, -1], test_y, score, file_name=f"lstm_{_sr}")
    metrics = UTSMetricHelper.get_metrics_all(test_y, score, window_size=window_size, metric_type="vus")
    outs.append([_sr, metrics[EK.VUS_ROC]])

pdf = pd.DataFrame(outs)
pdf.columns = ["sr", EK.VUS_ROC]
PDUtil.save_to_excel(pdf, "res", home=UC.get_entrance_directory())
