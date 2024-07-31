import os
import subprocess
import time

from flatbuffers.builder import np
from pygnuplot import gnuplot
import pandas as pd
from pygnuplot.gnuplot import Gnuplot
from sklearn.preprocessing import MinMaxScaler

from pysearchlib.share.ExcelOutKeys import ExcelMetricsKeys, EK
from pysearchlib.share.exp_config import ExpConf
from pysearchlib.utils.util_bash import UtilBash
from pysearchlib.utils.util_common import UtilComm, UC
from pysearchlib.utils.util_directory import make_dirs
from pysearchlib.utils.util_numpy import set_display_style
from pysearchlib.utils.util_log import get_logger

log = get_logger()
set_display_style()

"""

using 1:2:xticlabels(<labelcol>)
set xtics rotate by -45

"""


class UG:
    @staticmethod
    def set_xtics(g, labels: list, indexes: list):
        assert len(labels) == len(indexes)
        x_label = _generate_xtics(labels, indexes)
        g.cmd(f'set xtics {x_label}')


def _generate_xtics(label, position):
    """

    Parameters
    ----------
    label : 要显示的文章
    position : 要显示的数据

    Returns
    -------

    """
    xtics = "("
    for _label, _pos in zip(label, position):
        xtics = f"{xtics} \"{_label}\" {_pos},"
    xtics = xtics[:-1] + ")"
    return xtics


def _generate_xlabel(xlabel):
    """
    将
    [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 20429, 20430]

    生成下面的格式
    ( "16.0(0.02)" 1, "32.0(0.04)" 2, "64.0(0.0801)" 3, "128.0(0.1601)" 4, "256.0(0.3202)" 5, "512.0(0.6404)" 6, "1024.0(1.2808)" 7, "2048.0(2.5616)" 8, "4096.0(5.1232)" 9, "8192.0(10.2464)" 10, "16384.0(20.4929)" 11, "32768.0(40.9857)" 12, "65536.0(81.9715)" 13, "79949.0(99.9991)" 14, "Full(79949.75)" 15)

    请记住,x轴用 1,2,3,4,5,...., 也就是 using 0:xx
    Returns
    -------

    """
    _baseline = int(xlabel[-1])
    xtics = "("
    for _index, _label in enumerate(xlabel):
        _label = int(_label)
        percent = np.round((_label / xlabel[-1]) * 100, 2)
        if _label == _baseline:
            xtics = f"{xtics} \"Full({_label})\" {_index + 1},"
        else:
            xtics = f"{xtics} \"{_label}({percent})\" {_index + 1},"
    xtics = xtics[:-1] + ")"
    return xtics


class UTSViewGnuplot:

    def __init__(self, home=os.path.join(UtilComm.get_runtime_directory(), "UTSViewGnuplot")):
        make_dirs(home)
        self._home = home

    def plot_uts_data(self, test_x, test_y, score, exp_conf: ExpConf = None, w=30, h=2):
        # df = pd.DataFrame({
        #     "value": [1, 2, 3, 4],
        #     "label": [0, 0, 7, 0]
        # })
        score = MinMaxScaler(feature_range=(0, 1)).fit_transform(score.reshape(-1, 1)).ravel()
        df = pd.DataFrame({
            "value": test_x[:, -1],
            "label": test_y,
            "score": score
        })
        gp = Gnuplot()
        if exp_conf is not None:
            file_name = exp_conf.get_exp_id()
        else:
            file_name = "test"
        gp.set_output_pdf(file_name, w=w, h=h)
        gp.set_multiplot(2, 1)
        gp.add_data(df)

        gp.set(f'set title "Univariate time series (black: normal, red: abnormal)"')
        gp.set('set ylabel "Value"')
        gp.plot('using 0:1:(($2 > 0) ? 7 : -1) with points lc variable title "value"')
        gp.set('set title "Detection score (the larger the value, the greater the probability that it is an anomaly )"')

        # gp.set(f'set label "{exp_conf.get_plot_label()}" at 0.5,0.95 font ",7" noenhanced')
        gp.set("set yr [0:1]")
        gp.plot('using 0:3 with lines title "score"')
        # gp.write_to_file()
        gp.show()

    @DeprecationWarning
    def plot_uts_data_v2(self, test_x, test_y, score, file_name="test", w=1600, h=300, max_length=None):
        # df = pd.DataFrame({
        #     "value": [1, 2, 3, 4],
        #     "label": [0, 0, 7, 0]
        # })
        score = MinMaxScaler(feature_range=(0, 1)).fit_transform(score.reshape(-1, 1)).ravel()
        df = pd.DataFrame({
            "value": test_x,
            "label": test_y,
            "score": score
        })

        if isinstance(max_length, int):
            df = df.iloc[:max_length, :]
        gp = Gnuplot()
        gp.set_output_jpg(file_name, w=w, h=h)
        gp.set_multiplot(2, 1)
        gp.add_data(df)

        gp.set(f'set title "Univariate time series (black: normal, red: abnormal)"')
        gp.set('set ylabel "Value"')
        gp.plot('using 0:1:(($2 > 0) ? 7 : -1) with lines lc variable title "value"')
        gp.set('set title "Detection score (the larger the value, the greater the probability that it is an anomaly )"')

        # gp.set(f'set label "{exp_conf.get_plot_label()}" at 0.5,0.95 font ",7" noenhanced')
        gp.set("set yr [0:1]")
        gp.plot('using 0:3 with lines title "score"')
        gp.write_to_file()
        gp.show()

    def plot_uts_data_v3(self, test_x, test_y, score, file_name="test", w=1600, h=300, max_length=None):
        score = MinMaxScaler(feature_range=(0, 1)).fit_transform(score.reshape(-1, 1)).ravel()
        df = pd.DataFrame({
            "value": test_x,
            "label": test_y,
            "score": score
        })

        if isinstance(max_length, int):
            df = df.iloc[:max_length, :]
        gp = Gnuplot()
        file_name = os.path.join(self._home, file_name)
        make_dirs(self._home)
        gp.set_output_jpg(file_name, w=w, h=h)
        gp.set_multiplot(2, 1, margin="0.1,0.9,0.1,0.85", spacing="0.2,0.2")
        gp.add_data(df)
        gp.set(f'set xr [0:{df.shape[0]}]')
        gp.set(f'set title "(a) Univariate time series (black: normal, red: abnormal)"')

        # append the model name on the top left
        gp.set(f'set label "{os.path.basename(file_name.upper())}" at screen 0,0.93 font ",16" noenhanced')
        gp.plot('using 0:1:(($2 > 0) ? 7 : -1) with lines lc variable title ""')
        gp.set(f'set title "(b) Detection score (higher score means higher probability of anomalies)"')
        # gp.set("set yr [0:1]")

        gp.plot('using 0:3 with lines title ""')
        # gp.write_to_file()
        gp.show()

    def plot_uts_data_without_score(self, test_x, test_y, fname="test",
                                    title="Univariate time series (black: normal, red: abnormal)",
                                    xlabel="Time index", w=1600, h=4):
        # df = pd.DataFrame({
        #     "value": [1, 2, 3, 4],
        #     "label": [0, 0, 7, 0]
        # })
        assert test_x.ndim == 1
        df = pd.DataFrame({
            "value": test_x,
            "label": test_y,
        })
        gp = Gnuplot()
        fname = os.path.join(self._home, fname)
        gp.set_output_jpg(fname, w=w, h=h)
        gp.add_data(df)

        gp.set(f'set title "{title}"')
        gp.set('set ylabel "Value"')
        gp.set(f'set xlabel "{xlabel}"')
        # gp.plot('using 0:1:(($2 > 0) ? 7 : -1) with lines lc variable ps 1.5 title ""')
        gp.plot('using 0:1:(($2 > 0) ? 7 : -1) with lines lc variable title ""')

        gp.write_to_file()
        gp.show()

    def plot_a_sliding_window(self, xi, save_file_name, width=6, height=3):
        output = os.path.join(self._home, save_file_name)
        make_dirs(os.path.dirname(output))
        df = pd.DataFrame(data={'col1': xi})
        g = gnuplot.Gnuplot(log=True)

        g.plot_data(df, 'using 1:2 with lp lw 2',
                    key=None,
                    border=None,
                    grid="",
                    tics=None,
                    # ylabel='"Value"',
                    # xlabel='"Time Index',
                    terminal=f'pdfcairo font "arial,10" fontscale 1.0 size {width}, {height}',
                    output=f'"{output}"'
                    )

    def plot_a_sliding_window_and_dist(self, xi, di, save_file_name=None):
        output = os.path.join(self._home, save_file_name)
        make_dirs(os.path.dirname(output))
        df = pd.DataFrame(data={'col1': xi, 'col2': di})
        g = gnuplot.Gnuplot(log=True, output=f'"{output}"',
                            term='pngcairo font "arial,12" fontscale 1.0 size 1600, 400',
                            multiplot=''
                            )
        g.cmd("unset key")
        g.plot_data(df,
                    'using 1:2 with lines',
                    title='"Original UTS"',
                    grid="",
                    origin="0, 0.5",
                    size="1,0.5",
                    )
        g.plot_data(df,
                    'using 1:3 with lines',
                    title='"Distance Of UTS"',
                    grid="",
                    origin="0, 0",
                    size="1, 0.5")

    def plot_ori_and_opt_perf(self, ori, opt, save_file_name="ori_and_opt_perf.pdf"):
        output = os.path.join(self._home, save_file_name)
        make_dirs(os.path.dirname(output))
        df = pd.DataFrame(data={'ori': ori,
                                "opt": opt})
        g = gnuplot.Gnuplot(log=True)
        g.cmd('set term pdfcairo size 10,5 font ",20"')
        g.cmd('set key tmargin center horizontal')
        g.cmd('set xlabel "UTS Index"')
        g.cmd('set ylabel "Model Performance"')
        g.cmd('set xrange [-2:]')
        g.plot_data(df,
                    'using 1:2 with points pt 6 lc 6 ps 0.6 title "Ori. AUC"',
                    'using 1:3 with points pt 31 lc 15 ps 0.5 title "Fast. AUC"',
                    output=f'"{output}"'
                    )

    def plot_ori_and_opt_time(self, ori, fast, save_file_name="ori_and_opt_train_time.pdf"):
        output = os.path.join(self._home, save_file_name)
        make_dirs(os.path.dirname(output))
        df = pd.DataFrame(data={
            "title": ["ori", "fast"],
            'ori': [ori, fast]})
        g = gnuplot.Gnuplot(log=True)
        g.cmd('set terminal pdf font ",12"')
        g.cmd('set style data histogram')
        g.cmd('unset key')
        # g.cmd('set xlabel ""')
        g.cmd('set ylabel "Training Time"')
        g.cmd('set xr [0.5:2.5]')
        g.cmd('set xtics ("Ori." 1, "Fast."  2)')
        g.cmd('set yr [0:]')

        g.plot_data(df,
                    'using  3 ',
                    output=f'"{output}"'
                    )

    def plot_ori_fast_dist_time(self, ori, fast, dist, save_file_name="ori_and_opt_train_time.pdf"):
        output = os.path.join(self._home, save_file_name)
        make_dirs(os.path.dirname(output))
        df = pd.DataFrame(data={
            "title": ["ori", "fast", 'dist'],
            'ori': [ori, fast, dist]})
        g = gnuplot.Gnuplot(log=True)
        g.cmd('set terminal pdf font ",12"')
        g.cmd('set style data histogram')
        g.cmd('unset key')
        # g.cmd('set xlabel ""')
        g.cmd('set ylabel "Training Time (sec)"')
        g.cmd('set xr [0.5:3.5]')
        g.cmd('set xtics ("Ori." 1, "Fast."  2, "Dist. " 3)')
        g.cmd('set yr [0:]')

        g.plot_data(df,
                    'using  3 ',
                    output=f'"{output}"'
                    )

    def plot_ori_and_opt_perf_each_model(self, df: pd.DataFrame, save_file_name="ori_and_opt_perf_each_model.pdf",
                                         perf_key=EK.AUC_ROC):
        output = os.path.join(self._home, save_file_name)
        make_dirs(os.path.dirname(output))
        print(f"Save path: {os.path.abspath(output)}")

        for _index, (_model_name, _item) in enumerate(df.groupby(by=EK.MODEL_NAME)):
            _model_name = str(_model_name).upper()
            subs = []
            for _index, (_dataset_name, _small_data) in enumerate(_item.groupby(by=EK.DATASET_NAME)):
                pass

    #            f'using 0:(column("ori_{perf_key}")) with points pt 6 lc 6 ps 0.6 title "Ori. AUC" noenhanced',
    #                                                    f'using 0:(column("fastuts_{perf_key}")) with points pt 31 lc 31 ps 0.6 title "Ori. AUC" noenhanced',

    def plot_perf_vs_data_size(self, df, save_file_name, model_name):
        output = os.path.join(self._home, save_file_name)
        make_dirs(os.path.dirname(output))
        g = gnuplot.Gnuplot(log=True, output=f'"{output}"',
                            term='pdfcairo font "arial,12"')
        # g.cmd('set key tmargin center horizontal')
        g.cmd('set xlabel "Data Size"')
        g.cmd('set ylabel "Model Performance"')
        g.cmd('set key right bottom')
        g.cmd('set yr [0.5:1]')
        g.cmd(f'set title "{model_name}" noenhanced')

        _target = df.loc[:, [ExcelMetricsKeys.DATA_SAMPLE_RATE, (ExcelMetricsKeys.VUS_ROC, "mean")]]
        _target.columns = ['sr', 'roc']
        _label_arr = []
        _index_arr = []
        for _index, (key, val) in enumerate(_target.iterrows()):
            _label_arr.append(ExcelMetricsKeys.convert_sr(val[0]))
            _index_arr.append(_index)
        UG.set_xtics(g, _label_arr, _index_arr)
        g.plot_data(_target,
                    f'using 0:(column("roc")) with lp pt 6 lc 6 ps 0.6 title "Ori. AUC" noenhanced',
                    )


class Gnuplot:
    """
    将 key (legend) 提到顶部中间:
    gp.set("set key at screen 0.5,screen 0.98 center maxrows 1 ")

    设置x轴标签:
    using 1:2:xticlabels(<labelcol>)

    x轴旋转:
    set xtics rotate by -45




    """

    def __init__(self, home=os.path.join(UC.get_entrance_directory(), "plot_uts_and_score")):
        self.gnuplot = subprocess.Popen(['gnuplot', '-p'], shell=True, stdin=subprocess.PIPE)
        self.stdin = self.gnuplot.stdin
        self.write = self.stdin.write
        self.flush = self.stdin.flush
        self.home = home
        make_dirs(self.home)
        self.cmds = []
        self.output_file_name = None

    def __del__(self):
        self._close()

    def enable_y2tics(self):
        self.set("set ytics nomirror")
        self.set("set y2tics")
        return self

    def round_xtics(self):
        self.set('set format x  "%3.2f')
        return self

    def add_label(self, label, x, y):
        self.set(f'set label "{label}" at {x},{y}')
        return self

    def add_text(self, label, x, y):
        return self.add_label(label, x, y)

    def set(self, *args):
        """
        添加 set label "xxx" 这种命令

        可以使用如下方式:
        gp.set('set xlabel "aaaa"')
        or
        gp.set('xlabel "aaaa"')

        Parameters
        ----------
        args :

        Returns
        -------

        """
        for _cmd in args:
            _wcmd = self.clear(_cmd)
            if not _wcmd.startswith("set"):
                _wcmd = "set {}".format(_wcmd)
            self.cmds.append(_wcmd)
        return self

    def write_to_file(self, file=UC.get_filename_entry()):
        if not file.endswith(".gnuplot"):
            file = f"{file}.gnuplot"
        filepath = os.path.join(self.home, file)
        log.info(f"Writing to file {os.path.abspath(filepath)}")
        with open(filepath, 'w') as f:
            f.writelines(self.cmds)
        UtilBash.run_command_print_progress(f"gnuplot {filepath}; echo ok")
        log.info("Plot successfully!")

    def unset(self, *args):
        """
        添加 unset 命令, 使用方式

        gp.unset('unset key')
        or
        gp.unset('key')

        Parameters
        ----------
        args :

        Returns
        -------

        """
        for _cmd in args:
            _wcmd = self.clear(_cmd)
            if not _wcmd.startswith("unset"):
                _wcmd = "unset {}".format(_wcmd)
            self.cmds.append(_wcmd)
        return self

    def add_data(self, df: pd.DataFrame, float_format="%.2f", header=True):
        self.cmds.append(Gnuplot.convert_df(df, header=header, float_format=float_format))
        return self

    def clear(self, _cmd):
        _cmd = _cmd.strip()
        if len(_cmd) == 0:
            return "\n"
        else:
            # print("gnuplot-util:", _cmd)
            return _cmd + "\n"

    @classmethod
    def convert_df(cls, res, header=None, float_format="%.4f"):
        return "$df << EOF\n%sEOF\n" % res.to_csv(sep="\t", header=header, index=None, float_format=float_format)

    def set_output_pdf(self, pdf_file_name: str = "test.pdf", w=8, h=4, font_scale=1.0):
        if not pdf_file_name.endswith(".pdf"):
            pdf_file_name = pdf_file_name + ".pdf"

        pdf_file_path = os.path.join(self.home, pdf_file_name)
        self.output_file_name = os.path.abspath(pdf_file_path)
        # set term pdfcairo size 10,1
        self.set(f'set term pdfcairo size {w},{h}')
        self.set('set output "%s"' % pdf_file_path)
    def set_output_eps(self, pdf_file_name: str = "test.eps", w=8, h=4, font_scale=1.0):
        if not pdf_file_name.endswith(".eps"):
            pdf_file_name = pdf_file_name + ".eps"

        pdf_file_path = os.path.join(self.home, pdf_file_name)
        self.output_file_name = os.path.abspath(pdf_file_path)
        # set term pdfcairo size 10,1
        # set term postscript eps size 12,7
        # self.set(f'set term pdfcairo size {w},{h}')
        self.set(f'set term postscript eps size {w},{h}')
        self.set('set output "%s"' % pdf_file_path)

    def set_output_jpg(self, pdf_file_name: str, w=1000, h=1000 / 1.7, font_scale=1.0):
        # fontscale 1.0
        if not pdf_file_name.endswith(".jpg"):
            pdf_file_name = pdf_file_name + ".jpg"
        pdf_file_path = os.path.join(self.home, pdf_file_name)
        self.output_file_name = os.path.abspath(pdf_file_path)
        # set terminal jpeg size 300,200
        self.set("set terminal jpeg size %s,%s" % (w, h))
        self.set('set output "%s"' % pdf_file_path)

    def set_histogram(self):
        # self.set('set style data histogram')
        # set style histogram clustered gap 1   #//gap 2表示裂隙宽等于矩形宽度的2倍
        self.set('set style histogram clustered gap 1')
        # set style fill pattern border -1 #//fill solid表示完全填充柱体，后面跟0-1的参数，1表示完全填充，border 表示柱体的边线颜色
        self.set('set style fill pattern 2 border -1')
        return self

    def set_multiplot(self, rows, columns, margin="0.05,0.94,0.09,0.92", spacing='0.07,0.08'):
        # set multiplot layout 2,2 columnsfirst title "{/:Bold=15 Multiplot with explicit page margins}" \
        #               margins screen MP_LEFT, MP_RIGHT, MP_BOTTOM, MP_TOP spacing screen MP_GAP
        if margin is not None:

            self.set(f'set multiplot layout {rows},{columns} margins {margin} spacing {spacing}')
        else:
            self.set(f'set multiplot layout {rows},{columns}')
        return self

    def show(self):
        """
        Exec all commands then quit gnuplot.

        Returns
        -------

        """
        for _cmd in self.cmds:
            self.write(_cmd.encode("utf-8"))
            self.flush()
        if self.output_file_name is not None:
            print(f"File is save to {self.output_file_name}")
        self._close()

    def set_title(self, title):
        self.set(f'set title "{title}"')

    def plot(self, cmd):
        """
        using 1:2:xticlabels(<labelcol>)

        水平线: plot 0.8 with lines lc "red" lw 2 title "Baseline"

        Parameters
        ----------
        cmd :

        Returns
        -------

        """
        _cmd = self.clear(cmd)
        if not cmd.startswith("plot"):
            _cmd = "plot $df " + _cmd
        self.cmds.append(_cmd)
        return self

    def _close(self):
        if self.stdin.closed:
            return
        self.write("quit\n".encode("utf-8"))  # close the gnuplot window
        self.flush()
        self.stdin.close()
        self.gnuplot.wait()
        log.info("Exit gnuplot successfully")


# usage examples, please note that we didn't give the output so could only
# see the image flash on the screen. Will introduce how to output the
# image to files.
if __name__ == '__main__':
    # df = pd.DataFrame(data={'col1': [1, 2, 1],
    #                         'col2': [3, 4, 2],
    #                         'col3': [5, 6, 3]})
    #
    # gp = Gnuplot()
    # gp.plot_df(df, "plot $df using 0:1 with lp")
    # time.sleep(10)
    # df = pd.DataFrame({
    #     "value": [1, 2, 3, 4],
    #     "label": [0, 0, 7, 0]
    # })
    #
    # gp = Gnuplot()
    # gp.set_output_pdf(w=4, h=2)
    # gp.add_data(df)
    # gp.plot('using 0:1:(($2 > 0) ? 7 : -1) with points lc variable title ""')
    # gp.write_to_file()
    # gp.show()

    gp = UTSViewGnuplot()
    x = np.random.normal(size=(20,))
    y = np.random.normal(size=(20,)).astype("int")

    gp.plot_uts_data_v3(x * 1000, y, x)
