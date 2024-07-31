
import argparse
import os
import sys
from pysearchlib.share.exp_helper import main_fast_uts
from pysearchlib.utils.util_tf import enable_reproducible_result_tf2, enable_growth_memory_tf2

sys.path.append(os.path.join(os.path.dirname(__file__), "../libs/datasets"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../libs/py-search-lib"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../libs/timeseries-models"))
from pysearchlib.utils.util_numpy import enable_numpy_reproduce
from pysearchlib.utils.util_system import UtilSys

parser = argparse.ArgumentParser()
parser.add_argument("--params", type=str)
args = parser.parse_args()
from pysearchlib.utils.util_log import get_logger

log = get_logger()

from pysearchlib.share.exp_config import ExpConf

if __name__ == '__main__':

    conf = ExpConf.decode_configs_bs64(args.params)
    if conf.is_lstm_model():
        enable_reproducible_result_tf2()
        enable_growth_memory_tf2()
    enable_numpy_reproduce(conf.seed)
    UtilSys.is_debug_mode() and log.info(f"Start to train exp [{conf.get_exp_id()}] at {conf.get_parameters()}")
    if conf.is_compute_metrics():
        UtilSys.is_debug_mode() and log.info(f"Exp [{conf.get_exp_id()}] has finished")
    else:
        main_fast_uts(conf)
        UtilSys.is_debug_mode() and log.info("=" * 64)
