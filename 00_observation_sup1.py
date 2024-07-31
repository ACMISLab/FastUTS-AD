import logging
import os
from pysearchlib.utils.util_single_program import single_program
from pysearchlib.share.exp_helper import generate_jobs_baseline, \
    start_jobs, get_observation_args
from pysearchlib.utils.util_log import get_logger
log = get_logger(logging.ERROR)
import warnings
warnings.filterwarnings("ignore")
os.environ['EXP_VERSION'] = "V4002"
os.environ['SCRIPT_HOME'] = os.path.abspath(os.path.dirname(__file__))
if __name__ == '__main__':
    single_program()
    args = get_observation_args()
    jobs_array = generate_jobs_baseline(args)
    start_jobs(jobs_array, parallel_on_each_device=4)
