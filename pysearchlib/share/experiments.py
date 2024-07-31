"""
Args:
--hps: json string or file
    if  json string is provided, then it is converted to base64, otherwise keep original data.



Examples:

```python
import os
from ExpHelper import ExpHelper
from experiments import nni_experiments

exp_name = "exp1_aiops_iforest_similar_test_v02"
exp_data_sample_rate = ["1", "1/32"]
exp_aiops_kpi_ids = ExpHelper.AIOPS_KPIS_SELECTED_NINE
_cur_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(_cur_dir)

parameters = []
parameters = parameters + ["--exp_name", exp_name]
parameters = parameters + ["--data_sample_rate"] + exp_data_sample_rate
parameters = parameters + ["--data_id"] + exp_aiops_kpi_ids
parameters = parameters + ["--exp_home", _cur_dir]
parameters = parameters + ["--dataset", "IOpsCompetition"]
parameters = parameters + ["--max_trial_number", "1"]
parameters = parameters + ["--trial_concurrency", "1"]
parameters = parameters + ["--hps", "conf/isolation_forest_best.json"]
parameters = parameters + ["--model_entry_file", "main_iforest.py"]
parameters = parameters + ["--data_sample_method", "random"]
parameters = parameters + ["--nni_tuner", "RS"]
nni_experiments(parameters)
```

"""
import argparse
import os.path
import pprint
import traceback

from pysearchlib.common import Emjoi
from pysearchlib.share.NNIExpGenerator import NNIExpGenerator
from pysearchlib.utils.util_argparse import get_number_of_experiments
from pysearchlib.utils.util_args import parse_str_to_float
from pysearchlib.utils.util_feishu import send_msg_to_feishu, report_error_trace_to_feishu
from pysearchlib.utils.util_hash import get_str_hash
from pysearchlib.utils.util_log import get_logger
from pysearchlib.utils.util_message import log_start_msg, log_finished_msg
from pysearchlib.utils.util_network import get_host_ip
from pysearchlib.utils.util_nni import export_all_experiment
from pysearchlib.utils.util_process import single_process_check, set_process_title
from pysearchlib.utils.util_resume import ResumeHelper
from pysearchlib.utils.util_system import UtilSys

set_process_title("experiments")
single_process_check(pid_file="experiment.pid")
log = get_logger()


def parse_experiments_args(command_args=None):
    """

    Parameters
    ----------
    command_args : list
        A list like "['--foo', 3 ]", which can be generated by '--foo 3'.split().

    Returns
    -------

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp_name", default=f"debug_experiments")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--exp_home", default=os.path.dirname(os.path.abspath(__file__)))
    parser.add_argument("--n_experiment_restart", default=3, type=int,
                        help="How many times to restart the experiment when failed.")
    parser.add_argument("--repeat", default=1, type=int,
                        help="Number of repeated runs."
                             "In order to see the difference of the model metric in repeated runs.")
    # Multi value options
    parser.add_argument("--max_trial_number", default=[1], nargs='+')
    parser.add_argument("--trial_concurrency", default=[3], nargs='+')
    parser.add_argument("--model_entry_file", default="main_sk.py")
    parser.add_argument("--model", default=['IsolationForest'], action="store", nargs="+")
    parser.add_argument("--search_space_file",
                        help="The  search space file  containing hyperparameter for a model."
                             "\n When the model is COCA, the the search space file will be "
                             "automatically generated as coca.json."
                             "\n If you are in debug mode,you can specify the search space file,"
                             "but you can only specify a model by --model",
                        )
    parser.add_argument("--dataset", default=["IOpsCompetition"],
                        help="One of DatasetName.XX.value", nargs='+')
    parser.add_argument("--data_id", default=["a07ac296-de40-3a7c-8df3-91f642cc14d0"],
                        help="The data id in the m_dataset", nargs='+')
    parser.add_argument("--seed", default=[0], help="The random seed", nargs='+')
    parser.add_argument("--data_sample_method", nargs='+', default=("random",),
                        help="The sample method to sampling training data, e.g., RS")
    parser.add_argument("--data_sample_rate", nargs='+',
                        default=(1,),
                        help="The sample rate for training data,e.g.,1/4")
    parser.add_argument("--nni_tuner", default=("Random",),
                        nargs='+',
                        help="The nni_tuner of NNI", )
    parser.add_argument("--gpus", default=None)
    parser.add_argument("--hps", default=None, help="The hyperparameters passed to models")
    if command_args is not None:
        # noinspection PyTypeChecker
        args, ext_args = parser.parse_known_args(command_args)
    else:
        args, ext_args = parser.parse_known_args()

    if len(ext_args) > 0:
        raise RuntimeError(f"Parameter {ext_args} is not available.")
    return args


def check_enviroment():
    assert os.environ.get("PYTHONHASHSEED") is not None, "PYTHONHASHSEED must be set. You can set by: " \
                                                         "\nexport PYTHONHASHSEED=0"


def nni_experiments(command_options=None):
    try:
        args = parse_experiments_args(command_options)
        _n_experiments = get_number_of_experiments(args)
        msg = f"Start experiment at params [{get_host_ip()}]: \n{pprint.pformat(args.__dict__)}\n\n"
        log_start_msg(msg)
        send_msg_to_feishu(msg)
        # start with 1
        iter_counter = 0
        if len(args.model) > 1 and args.search_space_file is not None:
            raise RuntimeError("When --model has multiple values, the --search_space_file cant be specified")
        rh = ResumeHelper(get_str_hash(str(args.__dict__)))

        _nni_exp_home = None
        for max_trial_number_ in args.max_trial_number:
            for trial_concurrency_ in args.trial_concurrency:
                for model_ in args.model:
                    for dataset_ in args.dataset:
                        for seed_ in args.seed:
                            for data_sample_method_ in args.data_sample_method:
                                for data_sample_rate_ in args.data_sample_rate:
                                    for nni_tuner_ in args.nni_tuner:
                                        for repeat_index_ in range(args.repeat):
                                            for data_id_ in args.data_id:
                                                # The iter_counter is used for
                                                # identifying the experiment such as -seed 0 0.
                                                iter_counter += 1
                                                if rh.get_latest_index() is not None and iter_counter <= rh.get_latest_index():
                                                    UtilSys.is_debug_mode() and log.info(
                                                        f"Iteration counter {iter_counter} has done!")
                                                    # continue
                                                    pass
                                                try:
                                                    cg = NNIExpGenerator(
                                                        n_experiment_restart=args.n_experiment_restart,
                                                        home=args.exp_home,
                                                        max_trial_number=max_trial_number_,
                                                        trial_concurrency=trial_concurrency_,
                                                        model_entry_file=args.model_entry_file,
                                                        model=model_,
                                                        search_space_file=args.search_space_file,
                                                        exp_name=args.exp_name,
                                                        seed=seed_,
                                                        data_sample_rate=parse_str_to_float(data_sample_rate_),
                                                        data_sample_method=data_sample_method_,
                                                        dry_run=args.dry_run,
                                                        dataset=dataset_,
                                                        data_id=data_id_,
                                                        nni_tuner=nni_tuner_,
                                                        gpus=args.gpus,
                                                        iter_counter=iter_counter,
                                                        n_experiments=_n_experiments,
                                                        _mp_hps=args.hps
                                                    )

                                                    if _nni_exp_home is None:
                                                        _nni_exp_home = cg.get_nni_experiments_home()
                                                    if args.dry_run is not True:
                                                        cg.start()
                                                        rh.record(iter_counter)
                                                    else:
                                                        msg = f"{Emjoi.SUCCESS} Dry run successfully!"
                                                        send_msg_to_feishu(msg)
                                                        UtilSys.is_debug_mode() and log.info(msg)

                                                except Exception as e:
                                                    report_error_trace_to_feishu()
                                                    raise e

        msg = f"Finished experiment at params [{get_host_ip()}]:\n{pprint.pformat(args.__dict__)}\n\n"
        log_finished_msg(msg)

        UtilSys.is_debug_mode() and log.info("Export experiment metrics.")
        export_all_experiment(_nni_exp_home, experiment_working_directory=_nni_exp_home)
        UtilSys.is_debug_mode() and log.info("Export experiment done.")
        send_msg_to_feishu(msg)
    except Exception as e:
        send_msg_to_feishu(str(pprint.pformat(e)))
        log.error(pprint.pformat(traceback.format_exc()))


if __name__ == '__main__':
    nni_experiments()
