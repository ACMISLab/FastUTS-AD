import numpy as np
import pandas as pd

from pysearchlib.utils.util_common import UC
from pysearchlib.utils.util_pandas import PDUtil

data = np.random.random((100000, 1))
data = np.round(data, 4)
# test.csv 2.5M
PDUtil.save_to_csv(pd.DataFrame(data), "test")
print(data)
np.savez_compressed(UC.get_runtime_directory() + "/aaa", score=data)
