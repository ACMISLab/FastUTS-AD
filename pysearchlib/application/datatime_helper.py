import datetime
import pprint
import time

import numpy as np
from numpy.testing import assert_almost_equal

from pysearchlib.utils.util_log import get_logger
from pysearchlib.utils.util_system import UtilSys

log = get_logger()


class DateTimeHelper:
    """
    A class to help recording the running time of an application.

    When app is start, call start() and the timestamp of current is recorded in self._app_start_dt

    If the app done, call end() and the timestamp of current is recorded in self._app_end_dt, etc.

    """

    def __init__(self):
        self._evaluate_start_timestamp = -1
        self._evaluate_end_timestamp = -1
        self._train_end_timestamp = -1
        self._train_start_timestamp = -1
        # The datatime of app to -1
        self._app_start_timestamp = -1

        # The datatime of app start to run
        self._app_end_timestamp = -1

    def start(self):
        """
        Record the timestamp of the app start

        Returns
        -------

        """
        self._app_start_timestamp = self.get_current_timestamp()
        UtilSys.is_debug_mode() and log.info(f"App start at {self._app_start_timestamp}")

    def end(self):
        """
        Record the timestamp as soon as the app finishes (done)

        Returns
        -------

        """
        self._app_end_timestamp = self.get_current_timestamp()
        UtilSys.is_debug_mode() and log.info(f"App end at {self._app_end_timestamp}")

    def train_start(self):
        self._train_start_timestamp = self.get_current_timestamp()
        UtilSys.is_debug_mode() and log.info(f"Train start at {self._train_start_timestamp}")

    def train_end(self):
        self._train_end_timestamp = self.get_current_timestamp()
        UtilSys.is_debug_mode() and log.info(
            f"Train end at {self._train_start_timestamp}, elapsed: "
            f"{self.get_elapse_train()} s")

    def evaluate_end(self):
        self._evaluate_end_timestamp = self.get_current_timestamp()

    def evaluate_start(self):
        self._evaluate_start_timestamp = self.get_current_timestamp()

    @classmethod
    def get_current_timestamp(cls):
        return time.time_ns()

    def collect_metrics(self):
        return {
            "time_app_start": self._app_start_timestamp,
            "time_app_end": self._app_end_timestamp,
            "time_train_start": self._train_start_timestamp,
            'time_train_end': self._train_end_timestamp,
            'time_eval_start': self._evaluate_start_timestamp,
            'time_eval_end': self._evaluate_end_timestamp,
            'elapsed_train': self.get_elapse_train(),
            'elapsed_between_train_start_and_eval_end':
                (self._evaluate_end_timestamp - self._train_start_timestamp) * 1e-9,
        }

    def get_elapse_train(self):
        return np.round(1e-9 * (self._train_end_timestamp - self._train_start_timestamp), 2)


class DTH(DateTimeHelper):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    dt = DateTimeHelper()
    dt.train_start()

    # 经过2.11秒
    sleep_time = 2.13
    print(f"except {sleep_time} s")
    time.sleep(sleep_time)
    dt.train_end()
    pprint.pprint(dt.collect_metrics())

    assert_almost_equal(sleep_time, dt.collect_metrics()['elapsed_train'], decimal=2)
