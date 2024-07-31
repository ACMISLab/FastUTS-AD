#!/usr/bin/python3
# _*_ coding: utf-8 _*_
# @Time    : 2023/8/30 20:36
# @Author  : gsunwu@163.com
# @File    : finall_statics.py
# @Description:
import pandas as pd

from pysearchlib.share.ExcelOutKeys import EK, PaperFormat
from pysearchlib.share.uts_results_tools import ResultsConf, get_hypo_test_p, \
    ResTools
from pysearchlib.share.exp_helper import JobConfV1
from pysearchlib.utils.util_common import UC
from pysearchlib.utils.util_gnuplot import Gnuplot
from pysearchlib.utils.util_pandas import PDUtil


class OverallStatics:
    def __init__(self, target_perf):
        """

        Parameters
        ----------
        target_perf : str
             VUS_ROC and VUS_PR
        """
        self.target_perf = target_perf

    def load_data_effect_of_sample_method_and_interval(self):
        out = []
        for _v in ["v4010_64", "v4010_128", "v4010_256", "v4010_512", "v4010_1024"]:
            target_perf = self.target_perf
            JobConfV1.EXP_VERSION = _v
            rd = ResultsConf(version=JobConfV1.EXP_VERSION)

            for _target_file in rd.get_diff_sample_method():
                df = ResTools.get_post_process_metrics(target=_target_file,
                                                       baseline=rd.get_baseline(),
                                                       target_perf=target_perf)
                _round = 2
                _n_all = df.shape[0]
                _static_result = {
                    "抽样方法": df[EK.DATA_SAMPLE_METHOD][0],
                    "抽样间隔": _v.split("_")[-1],
                    "总实验数量": df.shape[0],
                    "模型性能降低1%的实验数量": (df[df['is_decrease_1%'] == 1].shape[0] / _n_all) * 100,
                    "模型性能降低5%的实验数量": (df[df['is_decrease_5%'] == 1].shape[0] / _n_all) * 100,
                    "模型性能降低10%的实验数量": (df[df['is_decrease_10%'] == 1].shape[0] / _n_all) * 100,
                    "模型性能降低15%的实验数量": (df[df['is_decrease_15%'] == 1].shape[0] / _n_all) * 100,
                    "数据处理时间(sec)": df["dist_cal. time (sec)"].sum(),
                    "Ori. 训练时间(sec)": df['ori_time'].sum(),
                    "FastUTS 训练时间(sec)": df['fastuts_time'].sum(),
                    "训练速度提升倍数": df['ori_time'].sum() / (
                            df['fastuts_time'].sum() + df["dist_cal. time (sec)"].sum()),
                    "ori acc. mean.": df[f'ori_acc'].mean().round(_round) * 100,
                    "ori auc. std.": df[f'ori_acc'].std().round(_round) * 100,
                    "fastuts auc. avg.": df[f'fastuts_acc'].mean().round(_round) * 100,
                    "fastuts auc. std.": df[f'fastuts_acc'].std().round(_round) * 100,
                    "train ratio": df['train_ratio'].mean(),
                    "p-value(ori. vs fastuts)": get_hypo_test_p(df[f'ori_acc'].to_list(),
                                                                df[f'fastuts_acc'].to_list())
                }
                out.append(_static_result)

        return pd.DataFrame(out)

    def plot_effect_of_sample_method_and_interval(self):
        df = self.load_data_effect_of_sample_method_and_interval()
        PDUtil.save_to_excel(df, f"overall_statistics_{self.target_perf}", home=UC.get_entrance_directory())
        out_file_name = f"effect_of_sample_method_and_interval_{self.target_perf}"
        gp = Gnuplot(home=PaperFormat.HOME_LATEX_HOME_IET)
        gp.set_output_pdf(pdf_file_name=out_file_name, w=8, h=2, font_scale=1.0)
        gp.set_multiplot(1, 3, margin="0.07,0.91,0.20,0.80", spacing='0.1,0.1')
        gp.enable_y2tics()
        for _index, (_sample_method, _item) in enumerate(df.groupby(by="抽样方法")):
            _item["FastUTS 训练时间(sec)"] = _item["FastUTS 训练时间(sec)"] / 60 / 60
            _item = _item.loc[:, ["抽样间隔", "FastUTS 训练时间(sec)", "fastuts auc. avg.", "ori acc. mean."]]
            # _item = _item.loc[:,
            #         ["抽样间隔", "FastUTS 训练时间(sec)", "模型性能降低5%的实验数量", "模型性能降低10%的实验数量"]]

            gp.add_data(_item)

            if _index == 0:
                gp.set("set key at screen 0.5,screen 0.97 center maxrows 1 ")
            else:
                gp.set("set key off ")

            gp.set(f'set title "({_index + 1}) {PaperFormat.format_value(_sample_method)}"')
            gp.set('set xlabel "Sampling gap"')
            if _index == 0:
                gp.set('set ylabel "Training time (hour)"')
            else:
                gp.set('set ylabel ""')

            if _index == 2:
                gp.set('set y2label "Accuracy"')
            else:
                gp.set('set y2label ""')

            if self.target_perf == EK.VUS_ROC:
                gp.set('set y2r [68.0:73.5]')
            if self.target_perf == EK.VUS_PR:
                gp.set('set y2r [40.0:42.1]')
            if self.target_perf == EK.RF:
                gp.set('set y2r [21.5:24.1]')

            # gp.set('set yr [10:160]')
            _perf_metrics_name = self.target_perf.replace("_", " ")
            gp.plot(
                'plot $df  using 0:2:xticlabels(1)  axis x1y1 with lp title "Training time",'
                f'"" using 0:3  axis x1y2 with  lp  lc 7 title "{_perf_metrics_name}" noenhanced'
            )
        gp.write_to_file()
        gp.show()


if __name__ == '__main__':
    outs = []
    os1 = OverallStatics(target_perf=EK.VUS_ROC)
    os1.plot_effect_of_sample_method_and_interval()
    os1 = OverallStatics(target_perf=EK.VUS_PR)
    os1.plot_effect_of_sample_method_and_interval()
    os1 = OverallStatics(target_perf=EK.RF)
    os1.plot_effect_of_sample_method_and_interval()
    # os1 = OverallStatics(opt_target=EK.RPRECISION)
    # os1.plot_effect_of_sample_method_and_interval()
