
import pandas as pd

from pysearchlib.share.ExcelOutKeys import EK, PaperFormat, PF
from pysearchlib.share.uts_results_tools import get_hypo_test_p, \
    ResTools, RT
from pysearchlib.utils.util_exp_result import ER
from pysearchlib.utils.util_latex import LatexTable
from pysearchlib.utils.util_log import get_logger
from pysearchlib.utils.util_pandas import PDUtil

log = get_logger()
time_scale = PaperFormat.TIME_SCALE

perf_model_over_uts = RT.load_overall_results_from_different_opt_target()
PDUtil.save_to_excel(perf_model_over_uts)
model_view_arr = []
time_arr = []

for (_target_perf, _model_name), _data in perf_model_over_uts.groupby(by=[EK.TARGET_PERF, EK.MODEL_NAME]):
    p_value = get_hypo_test_p(list(_data[EK.ORI_PERF_MEAN]), list(_data[EK.FAST_PERF_MEAN].values))
    # _data: 一个模型在所有单变量时间序列上面的性能, 按 target perf 分组

    _metric = {
        EK.TARGET_PERF: _target_perf,
        PF.MODEL: _model_name,
        PF.P_VALUE: p_value,
        PF.BEST_SR: ER.format_perf_mean_and_std(
            ResTools.get_mean(_data, EK.FAST_BEST_SR),
            ResTools.get_std(_data, EK.FAST_BEST_SR),
            decimal=2),
        PF.ORI_PERF: ER.format_perf_mean_and_std(
            ResTools.get_mean(_data, EK.ORI_PERF_MEAN),
            ResTools.get_mean(_data, EK.ORI_PERF_STD),
            decimal=2),
        PF.FAST_PERF: ER.format_perf_mean_and_std(
            ResTools.get_mean(_data, EK.FAST_PERF_MEAN),
            ResTools.get_mean(_data, EK.FAST_PERF_STD),
            decimal=2)}

    _time = {
        EK.TARGET_PERF: _target_perf,
        PF.MODEL: _model_name,
        PF.ORI_TIME: ER.format_perf_mean_and_std(
            ResTools.get_sum(_data, EK.ORI_TRAIN_TIME_MEAN),
            ResTools.get_mean(_data, EK.ORI_TRAIN_TIME_STD),
            decimal=2,
            scale=time_scale,
        ),
        PF.FAST_TIME: ER.format_perf_mean_and_std(
            ResTools.get_sum(_data, EK.FAST_TRAIN_TIME_MEAN),
            ResTools.get_mean(_data, EK.FAST_TRAIN_TIME_STD),
            scale=time_scale,
            decimal=2
        ),
        PF.DATA_PROC_TIME: ER.format_perf_mean_and_std(
            ResTools.get_sum(_data, EK.FAST_DATA_PROCESSING_TIME_MEAN),
            ResTools.get_mean(_data, EK.FAST_DATA_PROCESSING_TIME_STD),
            scale=time_scale,
            decimal=2),
        PF.SPEED_UP: ResTools.calculate_speed_up(_data),
        # EK.SORT_KEY: _data[EK.ORI_PERF_MEAN].mean()
    }
    model_view_arr.append(_metric)
    time_arr.append(_time)

# Table.4
out_arr = pd.DataFrame(model_view_arr)
lt = LatexTable(out_arr,
                caption=r"The overall performance of FastUTS-AD among 9 models and 8 benchmark datasets at different accuracy metrics (VUS ROC, VUS PR, and RF). Time is measured in hours. ",
                label=f"tab:{PaperFormat.get_label_name()}",
                home=PaperFormat.HOME_LATEX_HOME_IET)
lt.format_model_and_dataset()
# lt.wide_table()
# lt.enable_ht()
lt.replace("Model", "AD Methods")
lt.replace("p-value", "$p$ value")
lt.replace("Speedup", "Time Reduction (\%)")
lt.replace("Ori. Acc.", "$ACC_{ori}$")
lt.replace("Fast. Acc.", "$ACC_{fast}$")
lt.replace("Ori. Time", "$T_{ori}$")
lt.replace("Fast. Time", "$T_{fast}$")
lt.replace("Proc. Time", "$T_{dp}$")
print(lt.to_latex())
print("*" * 30)


# Table.5
out_arr = pd.DataFrame(time_arr)
lt = LatexTable(out_arr,
                caption=r"The overall performance of FastUTS-AD among 9 models and 8 benchmark datasets at different accuracy metrics (VUS ROC, VUS PR, and RF). Time is measured in hours. ",
                label=f"tab:{PaperFormat.get_label_name()}",
                home=PaperFormat.HOME_LATEX_HOME_IET)
lt.format_model_and_dataset()
lt.format_model_and_dataset()
# lt.wide_table()
# lt.enable_ht()
lt.replace("Model", "AD Methods")
lt.replace("p-value", "$p$ value")
lt.replace("Speedup", "Time Reduction (\%)")
lt.replace("Ori. Acc.", "$ACC_{ori}$")
lt.replace("Fast. Acc.", "$ACC_{fast}$")
lt.replace("Ori. Time", "$T_{ori}$")
lt.replace("Fast. Time", "$T_{fast}$")
lt.replace("Proc. Time", "$T_{dp}$")
print(lt.to_latex())
