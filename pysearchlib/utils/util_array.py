import pandas as pd
from pysearchlib.utils.util_pandas import PDUtil
from pysearchlib.utils.util_common import UtilComm

class ArrSaver:
    """
    接受数组并保存为文件
    """
    def __init__(self,home=UtilComm.get_entrance_directory()):
        self.array=[]

    def append(self, *args):
        print("add element:",args)
        self.array.append(args)

    def save_to_excel(self,columns=None):
        PDUtil.save_to_excel(pd.DataFrame(self.array,columns=columns),"save_arr",home=UtilComm.get_runtime_directory())


if __name__ == '__main__':
    ar=ArrSaver()
    ar.append(1,2,3,"aa")
    ar.save_to_excel()