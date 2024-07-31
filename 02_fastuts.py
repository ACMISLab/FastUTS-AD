import os
import sys
from pysearchlib.utils.util_single_program import single_program
from pysearchlib.utils.util_system import US
from pysearchlib.utils.util_tasks import UtilTasks
from pysearchlib.share.exp_helper import parse_args, generate_jobs_fast_uts, JobConfV1, get_models
from pysearchlib.utils.util_log import get_logger
import warnings
warnings.filterwarnings("ignore")
os.environ['SCRIPT_HOME'] = os.path.abspath(os.path.dirname(__file__))
log = get_logger()
if __name__ == '__main__':
    single_program()
    _exp_versions = JobConfV1.SAMPLE_GAP_VERSIONS
    tks = UtilTasks()
    for key, _data_sample_rates in _exp_versions.items():
        JobConfV1.EXP_VERSION = key
        for _method in JobConfV1.SAMPLE_METHODS:
            param = [
                        "--stop_alpha", JobConfV1.STOP_ALPHA_DEFAULT,
                        "--opt_target", JobConfV1.OPT_TARGET_DEFAULT,
                        "--data_sample_method", _method,
                        "--datasets", ] + JobConfV1.DATASET_SELECTED_ALL + [
                        "--kfold", JobConfV1.K_FOLD,
                        "--models", ] + get_models() + [
                        "--epoch", JobConfV1.EPOCH,
                        "--anomaly_window_type", JobConfV1.ANOMALY_WINDOW_TYPE,
                        "--fastuts_sample_rate"] + _data_sample_rates[1:] + [
                        "--batch_size", JobConfV1.BATCH_SIZE,
                        "--dataset_top", JobConfV1.SELECTED_N_UNIVARIATE,
                    ]
            args = parse_args(param)
            original_jobs = generate_jobs_fast_uts(args)
            # start_fastuts_jobs(original_jobs)
            for job in original_jobs:
                tks.append(job)
    # if US.is_macos():
    #     tks.save_to_excel()

    tks.launch()
    print("✅Done!")
