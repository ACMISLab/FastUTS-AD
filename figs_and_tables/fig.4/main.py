#!/usr/bin/python3
# _*_ coding: utf-8 _*_
# @Time    : 2023/9/22 21:03
# @Author  : gsunwu@163.com
# @File    : plot.py
# @Description:
import pandas as pd

from pysearchlib.utils.util_gnuplot import Gnuplot
from pysearchlib.utils.util_joblib import JLUtil
JLUtil.clear_all_calche()
df = pd.read_excel("overfitting.xlsx")

gp = Gnuplot()
gp.set_output_pdf(pdf_file_name="Fig.4", w=4, h=2)
gp.add_data(df)
gp.enable_y2tics()
gp.unset('unset y2tics')
gp.unset('unset ytics ')
gp.set('set ylabel "Loss"')
gp.set('set key outside center top maxrows 1')
gp.set('set xlabel "The percentage of training windows"')
gp.plot(
    'plot $df using 0:3:xticlabels(2)  axis x1y1 with lp  pt 10 lc 15 title "Training loss",""  using 0:4 axis x1y2 with lp lc 17 pt 16 title "Test loss"')
gp.write_to_file()
gp.show()
