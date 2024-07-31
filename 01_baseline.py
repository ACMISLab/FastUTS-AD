import logging
import os.path
from pysearchlib.utils.util_single_program import single_program
from pysearchlib.share.exp_helper import generate_jobs_baseline, \
    start_jobs, get_observation_args, JobConfV1
from pysearchlib.utils.util_log import get_logger
import warnings
warnings.filterwarnings("ignore")
log = get_logger(logging.ERROR)
os.environ['EXP_VERSION'] = "V4000"
os.environ['SCRIPT_HOME'] = os.path.abspath(os.path.dirname(__file__))
if __name__ == '__main__':
    single_program()
    args = get_observation_args()
    args.datasets = JobConfV1.DATASET_SELECTED_ALL
    args.sample_rates = ['-1']
    jobs_array = generate_jobs_baseline(args)
    start_jobs(jobs_array, parallel_on_each_device=8)
