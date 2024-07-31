import pandas as pd

from pysearchlib.share.ExcelOutKeys import EK
from pysearchlib.share.uts_results_tools import get_hypo_test_p, load_merge_perf_default
from pysearchlib.utils.util_common import UC
from pysearchlib.utils.util_exp_result import ER
from pysearchlib.utils.util_latex import LatexTable
from pysearchlib.utils.util_log import get_logger
from pysearchlib.utils.util_pandas import PDUtil

log = get_logger()

# 深度学习和机器学习的合并数据
perf_model_over_uts = load_merge_perf_default()

output_target = []
headers = None
for (_target_perf, _model_name), _data1 in perf_model_over_uts.groupby(by=[EK.TARGET_PERF, EK.MODEL_NAME]):

    arr2 = []
    for _dataset_name, _data_2 in _data1.groupby(by=EK.DATASET_NAME):
        p_value = get_hypo_test_p(list(_data_2[EK.ORI_PERF_MEAN]), list(_data_2[EK.FAST_PERF_MEAN].values))
        arr2.append({
            EK.DATASET_NAME: _dataset_name,
            EK.P_VALUE: ER.format_perf_mean_and_std(
                _data_2[EK.FAST_BEST_SR].mean(),
                _data_2[EK.FAST_BEST_SR].std(),
                decimal=2
            ),
        })
    dataset_df = pd.DataFrame(arr2).sort_values(by=EK.DATASET_NAME)
    if headers is None:
        headers = dataset_df[EK.DATASET_NAME].tolist()

    assert dataset_df[EK.DATASET_NAME].tolist() == headers

    values = dataset_df[EK.P_VALUE].tolist()
    values.insert(0, _model_name)
    values.insert(1, _target_perf)
    output_target.append(values)
headers.insert(0, "Model")
headers.insert(1, EK.TARGET_PERF)

t_pd = pd.DataFrame(output_target, columns=headers)

data_1 = t_pd[t_pd[EK.TARGET_PERF] == "VUS_ROC"]
data_2 = t_pd[t_pd[EK.TARGET_PERF] == "VUS_PR"]

for _target_perf, _data in t_pd.groupby(by=EK.TARGET_PERF):
    _data = _data.drop(EK.TARGET_PERF, axis=1)
    _data = _data.round(decimals=3)
    _data = PDUtil.append_avg_at_the_bottom(_data)
    _data = PDUtil.append_avg_on_the_right(_data)

    caption = f"$s_r^*$ (\%) for each model and dataset ({str(_target_perf).replace('_', ' ')})."
    label = f"tab:data-ratio-{str(_target_perf).replace('_', '')}".lower()
    lt = LatexTable(_data,
                    caption=caption,
                    label=label)

    lt.wide_table()
    lt.format_model_and_dataset()
    lt.enable_ht()
    lt.bold_text("87.22±23.44")
    lt.bold_text("72.81±26.50")
    lt.bold_text("83.83±22.64")
    # lt.bold_text("LHS")
    # lt.bold_text("45.32(±13.52)")
    # lt.bold_text("77.50(±7.11)")
    lt.to_latex(f"data-ratio-on-model-and-datasets-{_target_perf}.tex")
    # file_path = f"/Users/sunwu/SW-Research/sw-research-code/A01-papers/01_less_is_nore_pvldb/data_new/data-ratio-on-model-and-datasets-{_target_perf}.tex"

    # lt = LatexTable(_data, caption, label)

    # latex = _data.to_latex(index=False, label=label, caption=caption, float_format="%.2f")
    # lt.to_latex(file_path)

    # min_val = "{:.3f}".format(_data.iloc[:, 1:].values.min())
    # latex = latex.replace(f"{min_val}", f"\\textbf{{{min_val}}}")
    # latex = latex.replace("table}", "table*}")

    # latex = latex.replace("Avg.", "\midrule\n Avg.")

    # with open(file_path, "w") as f:
    #     f.write(latex)

    PDUtil.save_to_excel(_data, f"data-ratio-{_target_perf}_output", home=UC.get_entrance_directory())
PDUtil.save_to_excel(perf_model_over_uts, f"perf_model_over_uts", home=UC.get_entrance_directory())
