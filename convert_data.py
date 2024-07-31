#!/usr/bin/python3
# _*_ coding: utf-8 _*_
# @Time    : 2024/7/31 17:55
# @Author  : gsunwu@163.com
# @File    : prepare_data.py
# @Description:
# !/usr/bin/python3
# _*_ coding: utf-8 _*_
# @Time    : 2023/8/29 11:14
# @Author  : gsunwu@163.com
# @File    : data_collection.py
# @Description:
import os
from pysearchlib.share.uts_results_tools import FileMetricsLoader, ResultsConf
from pysearchlib.utils.util_common import UC
import click


@click.command()
@click.option('--home', default=1, help='The directory containing the results from command `make run_all_experiments`')
def main(home):
    collecting_results(home)


def collecting_results(home):
    for _dir in os.listdir(home):
        _exp_dir = os.path.join(home, _dir)
        target_file = _exp_dir + ".bz2"
        if os.path.exists(target_file):
            print(f"File already exists: {target_file}")
            continue
        if os.path.isdir(_exp_dir):
            ml = FileMetricsLoader(exp_home=_exp_dir, save_home=home)
            ml.load_metrics(save_origin=True)


if __name__ == '__main__':
    main()
    UC.done()
