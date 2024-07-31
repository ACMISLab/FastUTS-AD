import os.path
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typeguard import typechecked

from pysearchlib.share.exp_helper import ExpConf
from pysearchlib.utils.util_common import UtilComm
from pysearchlib.utils.util_directory import make_dirs
from pysearchlib.utils.util_file import grf
from pysearchlib.utils.util_system import UtilSys
from pysearchlib.utils.util_univariate_time_series import ModelPerformanceHelper

from pysearchlib.utils.util_log import get_logger
from pysearchlib.share.dataset_loader import DatasetLoader

log = get_logger()


class UnivariateTimeSeriesView:
    def __init__(self,
                 name=None,
                 is_save_fig=False,
                 dataset_name=None,
                 dataset_id=None,
                 conf: ExpConf = None,
                 max_length=10000,
                 home=UtilComm.get_runtime_directory(),
                 dl=None

                 ):
        """
        name: The name of file

        """
        self._image_save_name = name
        self._is_save_fig = is_save_fig
        self._dataset_name = dataset_name
        self._dataset_id = dataset_id
        self._home = home
        self._max_length = max_length
        self._conf = conf
        self._dl = dl

    @staticmethod
    def plot_kpi_with_anomaly_score_row1(x, label, score):
        """
        Plot the x, label and score in a row.

        Parameters
        ----------
        x : list
            1D array for univariate time series
        label : list
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        score :
            1D array, the score corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=(120, 4), tight_layout=True)

        def onclick(event):
            print('%s click: button=%s, x=%s, y=%s, xdata=%s, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))

        # print the information when click on the mouse key
        fig.canvas.mpl_connect("button_press_event", onclick)
        #
        # Plot the source data
        ax1: Axes = fig.add_subplot(1, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x", label="data")
        ax1.set_ylabel("Source Value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        # PLot the scores data
        ax = ax1.twinx()
        ax.plot(score, marker="^", label="score")
        ax.set_ylabel("Score")
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))
        plt.show()

    @staticmethod
    def plot_kpi_with_anomaly_score_row2(x, label, score):
        """
        Plot the x, label and score in two rows.

        1-th row: the source univariate time series. blue means normal, red means anomaly.
        2-th row: the anomaly score

        Parameters
        ----------
        x : list
            1D array for univariate time series
        label : list
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        score :
            1D array, the score corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=(20, 4), tight_layout=True)

        #
        # Plot the source data
        ax1: Axes = fig.add_subplot(2, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x", label="data")
        ax1.set_ylabel("Source Value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        # PLot the scores data
        ax: Axes = fig.add_subplot(2, 1, 2)
        ax.plot(score, marker="^", label="score")
        ax.set_ylabel("Score")
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))
        plt.show()

    @typechecked
    def plot_x_label_score_row2(self, x: np.ndarray, label: np.ndarray, score: np.ndarray):
        """
        Plot the x, label and score in two rows.

        1-th row: the source univariate time series. blue means normal, red means anomaly.
        2-th row: the anomaly score

        Parameters
        ----------
        x : list
            1D array for univariate time series
        label : list
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        score :
            1D array, the score corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=(20, 4), tight_layout=True)

        #
        # Plot the source data
        ax1: Axes = fig.add_subplot(2, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x", label="data")
        ax1.set_ylabel("Source Value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        # PLot the scores data
        ax: Axes = fig.add_subplot(2, 1, 2)
        ax.plot(score, marker="^", label="score")
        ax.set_ylabel("Score")
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))
        self._save_fig(fig)

    def plot_x_label_score_metrics_row2(self, x: np.ndarray, label: np.ndarray, score: np.ndarray, metrics: dict):
        """
        Plot the x, label and score in two rows.

        1-th row: the source univariate time series. blue means normal, red means anomaly.
        2-th row: the anomaly score

        Parameters
        ----------
        x : list
            1D array for univariate time series
        label : list
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        score :
            1D array, the score corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        if self._max_length != -1:
            x = x[:self._max_length]
            label = label[:self._max_length]
            score = score[:self._max_length]

        score = np.asarray(score, dtype=np.float32)
        fig: Figure = plt.figure(figsize=(20, 8), tight_layout=True)

        #
        # Plot the source data
        ax1: Axes = fig.add_subplot(2, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x", label="data")
        ax1.set_ylabel("Source Value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        # PLot the scores data
        ax: Axes = fig.add_subplot(2, 1, 2)
        ax.plot(score, marker="^", label="score")
        ax.set_ylabel("Score")
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        title_str = ""
        if metrics is not None:
            for i, (key, val) in enumerate(metrics.items()):
                if str(val).isnumeric():
                    title_str += f"{key}:{np.round(float(val), 4)}" + " " * 10
                else:
                    title_str += f"{key}:{val}" + " " * 10
                # title_str += "\n"
                if i > 1 and i % 5 == 0:
                    title_str += "\n"

            fig.suptitle(title_str)
        self._save_fig(fig)

    @staticmethod
    def plot_kpi_x_recon_x_score(x, label, recon_x, score):
        """
        Plot the x, recon x, and score in two rows.

        1-th row: the source univariate time series. blue means normal, red means anomaly.
        2-th row: the anomaly score

        Parameters
        ----------
        recon_x :  np.ndarray
            1D array
        x : np.ndarray
            1D array for univariate time series
        label : np.ndarray
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        score :np.ndarray
            1D array, the score corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=(20, 4), tight_layout=True)

        #
        # Plot the source data
        ax1: Axes = fig.add_subplot(3, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x", label="x data")
        ax1.set_ylabel("value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        ax2: Axes = fig.add_subplot(3, 1, 2)
        ax2.scatter(range(len(x)), recon_x, marker="x", label="recon x")
        ax2.set_ylabel("value")
        ax2.legend(loc='lower left')
        ax2.set_ylim(ax1.get_ylim())

        # PLot the scores data
        ax3: Axes = fig.add_subplot(3, 1, 3)
        ax3.plot(score, marker="^", label="score")
        ax3.set_ylabel("Score")
        ax3.legend(loc='center left')
        plt.show()

    @staticmethod
    def plot_kpi_x_and_x_bar(x, x_bar, title=None):
        """
        Plot the x, label and score in two rows.

        1-th row: the source univariate time series. blue means normal, red means anomaly.
        2-th row: the anomaly score

        Parameters
        ----------
        title :
        x : list
            1D array for univariate time series
        x_bar : list
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=(20, 4), tight_layout=True)

        #
        # Plot the source data
        ax1: Axes = fig.add_subplot(2, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, marker="x", label="data")
        ax1.set_ylabel("x")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        # PLot the scores data
        ax: Axes = fig.add_subplot(2, 1, 2)
        ax.plot(x_bar, marker="^", label="recon x")
        ax.set_ylabel("x bar")
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))
        plt.show()

    def plot_kpi_with_anomaly_score_row2_with_best_threshold(self, x: np.ndarray, label: np.ndarray, score: np.ndarray):
        """
        Plot the x, label and score in two rows.

        1-th row: the source univariate time series. blue means normal, red means anomaly.
        2-th row: the anomaly score

        Parameters
        ----------
        x: np.ndarray
            1D array for univariate time series
        label: np.ndarray
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        score: np.ndarray
            1D array, the score corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=(20, 4), tight_layout=True)

        # Plot the source data
        ax1: Axes = fig.add_subplot(2, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x",
                    label="blue: normal data; red: abnormal data")
        ax1.set_ylabel("Source Value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        best_aff = ModelPerformanceHelper.find_best_affiliation_score_and_threshold(label, score)
        # PLot the scores data
        ax: Axes = fig.add_subplot(2, 1, 2, sharex=ax1)
        ax.plot(score, marker="^", label="anomaly score")
        ax.hlines(best_aff.threshold, 0, len(label), colors="red", linestyles='dashed', label="best threshold")
        ax.set_ylabel("score")
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=2)
        score_patch = patches.Patch(color='blue',
                                    label=f"best aff f1: {best_aff.f1}, prec: {best_aff.precision}, recall: {best_aff.recall}")
        # ax.annotate(f"best aff f1: {best_aff.f1}, prec: {best_aff.precision}, recall: {best_aff.recall}",
        #             xy=(0.5, ax.get_ylim()[0] + 0.1))
        ax.set_xlim(0)
        ax.legend(handles=[score_patch], loc="lower center", bbox_to_anchor=(0.5, -0.5))
        return fig

    @DeprecationWarning
    @staticmethod
    def plot_kpi(x, label):
        """
        Plot the x, label  in two rows


        Parameters
        ----------
        x : list
            1D array for univariate time series
        label : list
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=(20, 4), tight_layout=True)

        # Plot the source data
        ax1: Axes = fig.add_subplot(1, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x", label="data")
        ax1.set_ylabel("Source Value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        plt.show()

    @typechecked
    def plot_x_label(self, x: np.ndarray, label: np.ndarray, fig_size=(20, 4)):
        """
        Plot the x, label  in two rows


        Parameters
        ----------
        x : nd.ndarray
            1D array for univariate time series
        label : nd.ndarray
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        fig_size: tuple

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=fig_size, tight_layout=True)
        # Plot the source data
        ax1: Axes = fig.add_subplot(1, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x", label="data")
        ax1.set_ylabel("Value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))
        ax1.set_title(self._get_image_image_name_from_dl(self._dl))
        if self._is_save_fig:
            self._save_fig(fig)
        else:
            plt.show()
            return fig

    def plot_a_sliding_window(self, x: np.ndarray, y_i=0, fig_size=(20, 4)):
        """
        Plot the x, label  in two rows


        Parameters
        ----------
        x : nd.ndarray
            1D array for univariate time series
        label : nd.ndarray
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        fig_size: tuple

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=fig_size, tight_layout=True)
        # Plot the source data
        ax1: Axes = fig.add_subplot(1, 1, 1)
        ax1.plot(x)
        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.set_ylabel("Value")

        if self._is_save_fig:
            self._save_fig(fig)
        else:
            plt.show()
            return fig

    def plot_kpi_with_anomaly_score_row2_with_best_threshold_torch_data_loader(self, dataloader, score, save_fig=True):
        if len(dataloader.dataset.data.shape) == 2:
            x = dataloader.dataset.data[:, -1]
        else:
            x = dataloader.dataset.data[:, 0, -1]

        label = dataloader.dataset.label
        fig = self.plot_kpi_with_anomaly_score_row2_with_best_threshold(x, label, score)

        if save_fig:
            self._save_fig(fig)
        else:
            plt.show()

    def plot_kpi_with_anomaly_score_row2_with_best_threshold_numpy(self, x, label, score, save_fig=True):
        fig = self.plot_kpi_with_anomaly_score_row2_with_best_threshold(x, label, score)
        if save_fig:
            self._save_fig(fig)
        else:
            plt.show()

    def _save_fig(self, fig):
        if not self._is_save_fig:
            plt.show()
            return

            # Notice: do not change this name, it used in the examples.
        if self._home is None:
            self._home = os.path.join(os.path.abspath(sys.argv[0]), "runtime/plot_images")

        if self._dl is not None:
            self._image_save_name = self._get_image_image_name_from_dl(self._dl)
        f_name = os.path.join(self._home, "plot_errors", self._image_save_name + ".png")
        make_dirs(os.path.dirname(f_name))
        UtilSys.is_debug_mode() and log.info(f"Pig image saved to {os.path.abspath(f_name)}")
        fig.savefig(f_name)

    def _get_dataset_name(self):
        if self._dl is not None:
            return self._dl._dataset_name
        else:
            return "unknown_dataset"

    def _get_image_image_name_from_dl(self, dl: DatasetLoader):
        return f"{dl._dataset_name}_{dl._data_id}"


class UTSPlot:
    def __init__(self,
                 filename=None,
                 is_save_fig=True,
                 dataset_name=None,
                 dataset_id=None,
                 conf: ExpConf = None,
                 max_length=10000,
                 home=UtilComm.get_runtime_directory()
                 ):
        """
        name: The name of file

        """
        self._file_name = filename
        self._is_save_fig = is_save_fig
        self._dataset_name = dataset_name
        self._dataset_id = dataset_id
        self._home = home
        self._max_length = max_length
        self._conf = conf

    @staticmethod
    def plot_kpi_with_anomaly_score_row1(x, label, score):
        """
        Plot the x, label and score in a row.

        Parameters
        ----------
        x : list
            1D array for univariate time series
        label : list
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        score :
            1D array, the score corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=(120, 4), tight_layout=True)

        def onclick(event):
            print('%s click: button=%s, x=%s, y=%s, xdata=%s, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))

        # print the information when click on the mouse key
        fig.canvas.mpl_connect("button_press_event", onclick)
        #
        # Plot the source data
        ax1: Axes = fig.add_subplot(1, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x", label="data")
        ax1.set_ylabel("Source Value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        # PLot the scores data
        ax = ax1.twinx()
        ax.plot(score, marker="^", label="score")
        ax.set_ylabel("Score")
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))
        plt.show()

    @staticmethod
    def plot_kpi_with_anomaly_score_row2(x, label, score):
        """
        Plot the x, label and score in two rows.

        1-th row: the source univariate time series. blue means normal, red means anomaly.
        2-th row: the anomaly score

        Parameters
        ----------
        x : list
            1D array for univariate time series
        label : list
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        score :
            1D array, the score corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=(20, 4), tight_layout=True)

        #
        # Plot the source data
        ax1: Axes = fig.add_subplot(2, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x", label="data")
        ax1.set_ylabel("Source Value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        # PLot the scores data
        ax: Axes = fig.add_subplot(2, 1, 2)
        ax.plot(score, marker="^", label="score")
        ax.set_ylabel("Score")
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))
        plt.show()

    @typechecked
    def plot_x_label_score_row2(self, x: np.ndarray, label: np.ndarray, score: np.ndarray):
        """
        Plot the x, label and score in two rows.

        1-th row: the source univariate time series. blue means normal, red means anomaly.
        2-th row: the anomaly score

        Parameters
        ----------
        x : list
            1D array for univariate time series
        label : list
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        score :
            1D array, the score corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=(20, 4), tight_layout=True)

        #
        # Plot the source data
        ax1: Axes = fig.add_subplot(2, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x", label="data")
        ax1.set_ylabel("Source Value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        # PLot the scores data
        ax: Axes = fig.add_subplot(2, 1, 2)
        ax.plot(score, marker="^", label="score")
        ax.set_ylabel("Score")
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))
        self._save_fig(fig)

    def plot_x_label_score_metrics_row2(self, x: np.ndarray, label: np.ndarray, score: np.ndarray, metrics: dict):
        """
        Plot the x, label and score in two rows.

        1-th row: the source univariate time series. blue means normal, red means anomaly.
        2-th row: the anomaly score

        Parameters
        ----------
        x : list
            1D array for univariate time series
        label : list
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        score :
            1D array, the score corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        if self._max_length != -1:
            x = x[:self._max_length]
            label = label[:self._max_length]
            score = score[:self._max_length]

        score = np.asarray(score, dtype=np.float32)
        fig: Figure = plt.figure(figsize=(20, 8), tight_layout=True)

        #
        # Plot the source data
        ax1: Axes = fig.add_subplot(2, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x", label="data")
        ax1.set_ylabel("Source Value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        # PLot the scores data
        ax: Axes = fig.add_subplot(2, 1, 2)
        ax.plot(score, marker="^", label="score")
        ax.set_ylabel("Score")
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        title_str = ""
        if metrics is not None:
            for i, (key, val) in enumerate(metrics.items()):
                if str(val).isnumeric():
                    title_str += f"{key}:{np.round(float(val), 4)}" + " " * 10
                else:
                    title_str += f"{key}:{val}" + " " * 10
                # title_str += "\n"
                if i > 1 and i % 5 == 0:
                    title_str += "\n"

            fig.suptitle(title_str)
        self._save_fig(fig)

    @staticmethod
    def plot_kpi_x_recon_x_score(x, label, recon_x, score):
        """
        Plot the x, recon x, and score in two rows.

        1-th row: the source univariate time series. blue means normal, red means anomaly.
        2-th row: the anomaly score

        Parameters
        ----------
        recon_x :  np.ndarray
            1D array
        x : np.ndarray
            1D array for univariate time series
        label : np.ndarray
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        score :np.ndarray
            1D array, the score corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=(20, 4), tight_layout=True)

        #
        # Plot the source data
        ax1: Axes = fig.add_subplot(3, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x", label="x data")
        ax1.set_ylabel("value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        ax2: Axes = fig.add_subplot(3, 1, 2)
        ax2.scatter(range(len(x)), recon_x, marker="x", label="recon x")
        ax2.set_ylabel("value")
        ax2.legend(loc='lower left')
        ax2.set_ylim(ax1.get_ylim())

        # PLot the scores data
        ax3: Axes = fig.add_subplot(3, 1, 3)
        ax3.plot(score, marker="^", label="score")
        ax3.set_ylabel("Score")
        ax3.legend(loc='center left')
        plt.show()

    @staticmethod
    def plot_kpi_x_and_x_bar(x, x_bar, title=None):
        """
        Plot the x, label and score in two rows.

        1-th row: the source univariate time series. blue means normal, red means anomaly.
        2-th row: the anomaly score

        Parameters
        ----------
        title :
        x : list
            1D array for univariate time series
        x_bar : list
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=(20, 4), tight_layout=True)

        #
        # Plot the source data
        ax1: Axes = fig.add_subplot(2, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, marker="x", label="data")
        ax1.set_ylabel("x")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        # PLot the scores data
        ax: Axes = fig.add_subplot(2, 1, 2)
        ax.plot(x_bar, marker="^", label="recon x")
        ax.set_ylabel("x bar")
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))
        plt.show()

    def plot_kpi_with_anomaly_score_row2_with_best_threshold(self, x: np.ndarray, label: np.ndarray, score: np.ndarray):
        """
        Plot the x, label and score in two rows.

        1-th row: the source univariate time series. blue means normal, red means anomaly.
        2-th row: the anomaly score

        Parameters
        ----------
        x: np.ndarray
            1D array for univariate time series
        label: np.ndarray
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        score: np.ndarray
            1D array, the score corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=(20, 4), tight_layout=True)

        # Plot the source data
        ax1: Axes = fig.add_subplot(2, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x",
                    label="blue: normal data; red: abnormal data")
        ax1.set_ylabel("Source Value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        best_aff = ModelPerformanceHelper.find_best_affiliation_score_and_threshold(label, score)
        # PLot the scores data
        ax: Axes = fig.add_subplot(2, 1, 2, sharex=ax1)
        ax.plot(score, marker="^", label="anomaly score")
        ax.hlines(best_aff.threshold, 0, len(label), colors="red", linestyles='dashed', label="best threshold")
        ax.set_ylabel("score")
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=2)
        score_patch = patches.Patch(color='blue',
                                    label=f"best aff f1: {best_aff.f1}, prec: {best_aff.precision}, recall: {best_aff.recall}")
        # ax.annotate(f"best aff f1: {best_aff.f1}, prec: {best_aff.precision}, recall: {best_aff.recall}",
        #             xy=(0.5, ax.get_ylim()[0] + 0.1))
        ax.set_xlim(0)
        ax.legend(handles=[score_patch], loc="lower center", bbox_to_anchor=(0.5, -0.5))
        return fig

    @DeprecationWarning
    @staticmethod
    def plot_kpi(x, label):
        """
        Plot the x, label  in two rows


        Parameters
        ----------
        x : list
            1D array for univariate time series
        label : list
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=(20, 4), tight_layout=True)

        # Plot the source data
        ax1: Axes = fig.add_subplot(1, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x", label="data")
        ax1.set_ylabel("Source Value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))

        plt.show()

    @typechecked
    def plot_x_label(self, x: np.ndarray, label: np.ndarray, fig_size=(20, 4)):
        """
        Plot the x, label  in two rows


        Parameters
        ----------
        x : nd.ndarray
            1D array for univariate time series
        label : nd.ndarray
            1D array, the label corresponding each x, i.e., anomaly (1) or normal (0),
        fig_size: tuple

        Returns
        -------
        Figure


        """
        # 创建图
        fig: Figure = plt.figure(figsize=fig_size, tight_layout=True)

        # Plot the source data
        ax1: Axes = fig.add_subplot(1, 1, 1)

        # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
        ax1.scatter(range(len(x)), x, c=np.where(label > 0, 'red', 'blue'), marker="x", label="data")
        ax1.set_ylabel("Value")
        ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))
        if self._is_save_fig:
            self._save_fig(fig)
        else:
            plt.show()
            return fig

    def plot_kpi_with_anomaly_score_row2_with_best_threshold_torch_data_loader(self, dataloader, score, save_fig=True):
        if len(dataloader.dataset.data.shape) == 2:
            x = dataloader.dataset.data[:, -1]
        else:
            x = dataloader.dataset.data[:, 0, -1]

        label = dataloader.dataset.label
        fig = self.plot_kpi_with_anomaly_score_row2_with_best_threshold(x, label, score)

        if save_fig:
            self._save_fig(fig)
        else:
            plt.show()

    def plot_kpi_with_anomaly_score_row2_with_best_threshold_numpy(self, x, label, score, save_fig=True):
        fig = self.plot_kpi_with_anomaly_score_row2_with_best_threshold(x, label, score)
        if save_fig:
            self._save_fig(fig)
        else:
            plt.show()

    def _save_fig(self, fig):
        if not self._is_save_fig:
            plt.show()
            return

            # Notice: do not change this name, it used in the examples.
        if self._home is None:
            self._home = os.path.join(os.path.abspath(sys.argv[0]), "runtime/plot_images")

        make_dirs(self._home)
        f_name = grf(name=self._file_name,
                     ext=".png",
                     home=self._home)
        UtilSys.is_debug_mode() and log.info(f"Pig image saved to {os.path.abspath(f_name)}")
        fig.savefig(f_name)
