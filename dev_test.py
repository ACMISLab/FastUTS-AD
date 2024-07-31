import os
os.environ['EXP_VERSION'] = "V_DEBUG"
os.environ['JOBS_TYPE'] = "ml"
os.environ['SCRIPT_HOME'] = os.path.abspath(os.path.dirname(__file__))
os.environ['PY_DEBUG'] = '1'

import warnings
import shutil
from convert_data import collecting_results
from pysearchlib.share.exp_helper import generate_jobs_baseline, \
    start_jobs, JobConfV1, parse_args
from pysearchlib.utils.util_log import get_logger
from pysearchlib.utils.util_single_program import single_program
from pysearchlib.utils.util_system import UtilSys

log = get_logger()
warnings.filterwarnings("ignore")
UtilSys.RUNTIME_HOME = "./runtime"
if __name__ == '__main__':
    log.info("Clearn old resources")
    if os.path.exists(UtilSys.RUNTIME_HOME):
        shutil.rmtree(UtilSys.RUNTIME_HOME)

    single_program()

    # run the program
    params = [
                 "--datasets", ] + ['NAB'] + [
                 "--kfold", "5",
                 "--models", ] + ['hbos'] + [
                 "--epoch", "10",
                 "--batch_size", JobConfV1.BATCH_SIZE,
                 "--data_sample_method", JobConfV1.RANDOM_SAMPLE,
                 "--anomaly_window_type", JobConfV1.ANOMALY_WINDOW_TYPE,
                 "--sample_rates"] + ['32', '64'] + [
                 "--dataset_top", "1",
             ]
    args = parse_args(params)
    jobs_array = generate_jobs_baseline(args)
    start_jobs(jobs_array, parallel_on_each_device=1, debug_on_macos=False)

    # metrics gathering
    collecting_results(UtilSys.RUNTIME_HOME)
    log.info("Done")
