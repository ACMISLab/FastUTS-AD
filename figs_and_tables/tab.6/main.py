import pandas as pd

from pysearchlib.share.ExcelOutKeys import EK, PaperFormat
from pysearchlib.share.uts_results_tools import load_merge_perf_diff_stop_alpha, ResTools
from pysearchlib.utils.util_common import UC
from pysearchlib.utils.util_exp_result import ER
from pysearchlib.utils.util_latex import LatexTable
from pysearchlib.utils.util_pandas import PDUtil

time_scale = 1 / 3600
# v4020_03_fastuts_sup1_rf_0.1_random.bz2
# v4020_03_fastuts_sup1_rf_0.01_random.bz2
# v4020_03_fastuts_sup1_rf_0.001_random.bz2
# v4020_03_fastuts_sup1_rf_0.5_random.bz2
# v4020_03_fastuts_sup1_vus_pr_0.1_random.bz2
# v4020_03_fastuts_sup1_vus_pr_0.01_random.bz2
# v4020_03_fastuts_sup1_vus_pr_0.001_random.bz2
# v4020_03_fastuts_sup1_vus_pr_0.5_random.bz2
# v4020_03_fastuts_sup1_vus_roc_0.1_random.bz2
# v4020_03_fastuts_sup1_vus_roc_0.01_random.bz2
# v4020_03_fastuts_sup1_vus_roc_0.001_random.bz2
# v4020_03_fastuts_sup1_vus_roc_0.5_random.bz2
df = load_merge_perf_diff_stop_alpha()

# sys.exit(0)
results = []

statistics_values = []
for (_target_perf, _stop_alpha), _data1 in df.groupby(by=[EK.TARGET_PERF, EK.STOP_ALPHA]):
    # results.append([_target_perf, _stop_alpha, _data1[EK.FAST_PERF_MEAN].mean()])
    # 模型+数据集 在 不同 的 target perf 和 stop alpha
    # _data1.groupby(by=[EK.MODEL_NAME, EK.DATASET_NAME]).sum()
    _time = _data1.groupby(by=EK.MODEL_NAME)
    _ori_train_time = _time[EK.FAST_TRAIN_TIME_MEAN].sum() * PaperFormat.TIME_SCALE
    _ori_train_time = _ori_train_time.round(2).mean().round(2)

    _fast_perf = ER.format_perf_mean_and_std(
        ResTools.get_mean(_data1, EK.FAST_PERF_MEAN),
        ResTools.get_mean(_data1, EK.FAST_PERF_STD)
    )
    results.append({
        EK.TARGET_PERF: _target_perf,
        EK.STOP_ALPHA: _stop_alpha,
        EK.FAST_PERF: _fast_perf,
        EK.ORI_TRAIN_TIME: _ori_train_time
    })
    # print(results)
    # sys.exit()
    # statistics_values.append([_target_perf, _stop_alpha] + _data1[EK.FAST_PERF_MEAN].tolist())

res = pd.DataFrame(results)
PDUtil.save_to_excel(res, "stop_avg_perf", home=UC.get_entrance_directory())

_data_uvsroc = res[res[EK.TARGET_PERF] == EK.VUS_ROC]
_data_uvspr = res[res[EK.TARGET_PERF] == EK.VUS_PR]
_data_uvsrf = res[res[EK.TARGET_PERF] == EK.RF]

_target_perf = pd.merge(_data_uvspr, _data_uvsroc, left_on=EK.STOP_ALPHA, right_on=EK.STOP_ALPHA)
_target_perf = pd.merge(_target_perf, _data_uvsrf, left_on=EK.STOP_ALPHA, right_on=EK.STOP_ALPHA)
# 只算vus_roc 的
out_res = _target_perf.iloc[:,
          [1, 2, 3, 5, 6, 8, 9]]
out_res.columns = [
    PaperFormat.STOP_ALPHA,
    PaperFormat.VUS_ROC,
    PaperFormat.SPEED_UP,
    PaperFormat.VUS_PR,
    PaperFormat.SPEED_UP,
    PaperFormat.RF,
    PaperFormat.SPEED_UP
]
lt = LatexTable(out_res,
                caption=r"Average accuracy metrics and training time (hours) at different $\alpha$.",
                label=f"tab:{PaperFormat.get_label_name()}",
                home=PaperFormat.HOME_LATEX_HOME_IET)
latex_header = r"""
\multirow{2}{*}{$\alpha$} 
& \multicolumn{2}{|c}{VUS PR} &  \multicolumn{2}{|c}{VUS ROC} & \multicolumn{2}{|c}{RF} \\
& \multicolumn{1}{|c} {Avg. acc.}& Train. Time & \multicolumn{1}{|c} {Avg. acc.} & Train. Time & \multicolumn{1}{|c} {Avg. acc.} & Train. Time\\
"""

lt.format_model_and_dataset()
lt.enable_ht()
lt.bold_text("0.001")
lt.set_header(latex_header)
lt.bold_text("78.63")
lt.bold_text("44.16")
lt.replace("Avg. acc.", "$ACC_{fast}$")
lt.replace("Train. Time", "$T_{fast}$")
print(lt.latex_txt)
