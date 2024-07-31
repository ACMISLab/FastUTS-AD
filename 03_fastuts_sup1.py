import os
import sys
from pysearchlib.utils.util_tasks import UtilTasks
from pysearchlib.share.exp_helper import parse_args, generate_jobs_fast_uts, JobConfV1, get_models
from pysearchlib.utils.util_log import get_logger
from pysearchlib.utils.util_single_program import single_program
import warnings
warnings.filterwarnings("ignore")
log = get_logger()
os.environ['SCRIPT_HOME'] = os.path.abspath(os.path.dirname(__file__))
if __name__ == '__main__':
    single_program()
    tks = UtilTasks()
    JobConfV1.EXP_VERSION = "v4020"
    # Best sampling algorithm and sampling interval: Random, with a sampling interval of 256. Because of the low training time and high performance.
    _method = "random"
    for _opt_target in JobConfV1.OPT_TARGETS:
        for _stop_alpha in JobConfV1.STOP_ALPHA_SUP2:
            param = [
                        "--stop_alpha", _stop_alpha,
                        "--opt_target", _opt_target,
                        "--data_sample_method", _method,
                        "--datasets", ] + JobConfV1.DATASET_SELECTED_ALL + [
                        "--kfold", JobConfV1.K_FOLD,
                        "--models", ] + get_models() + [
                        "--epoch", JobConfV1.EPOCH,
                        "--anomaly_window_type", JobConfV1.ANOMALY_WINDOW_TYPE,
                        "--fastuts_sample_rate"] + JobConfV1.SAMPLE_RATES_V922[1:] + [
                        "--batch_size", JobConfV1.BATCH_SIZE,
                        "--dataset_top", JobConfV1.SELECTED_N_UNIVARIATE,
                    ]
            args = parse_args(param)
            original_jobs = generate_jobs_fast_uts(args)
            for job in original_jobs:
                tks.append(job)
    tks.launch()
    print("✅Done!")
