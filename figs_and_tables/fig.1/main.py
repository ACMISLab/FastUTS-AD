# 915_observation.zip
import os.path

from pysearchlib.share.observation_helper import plot_overview_v6
from pysearchlib.utils.util_joblib import JLUtil

JLUtil.clear_all_calche()
if __name__ == '__main__':
    # v4002_00_observation_vus_roc_0.001_random
    file_name = f"../data/v4002_00_observation_sup1_vus_roc_0.001_random.bz2"
    print(os.path.abspath(file_name))
    plot_overview_v6(file_name)
