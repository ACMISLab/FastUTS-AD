import argparse

from pysearchlib.share.exp_config import ExpConf
from pysearchlib.share.exp_helper import train_models_kfold_v2
from pysearchlib.utils.util_tf import enable_reproducible_result_tf2, enable_growth_memory_tf2

parser = argparse.ArgumentParser()
parser.add_argument("--params", type=str)
args = parser.parse_args()

conf = ExpConf.decode_configs_bs64(args.params)
if conf.is_lstm_model():
    enable_reproducible_result_tf2()
    enable_growth_memory_tf2()

train_models_kfold_v2(conf)
