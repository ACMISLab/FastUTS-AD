#!/usr/bin/python3
# _*_ coding: utf-8 _*_
# @Time    : 2024/5/11 23:33
# @Author  : gsunwu@163.com
# @File    : ExpAnaConf.py
# @Description:

class ANAConf:
    DATA_HOME="/Users/sunwu/Documents/download_metrics/p1"


    @staticmethod
    def convert_number_to_alpha(number:int):
        maps={
            1:'a',
            2:'b',
            3:'c',
            4:'d',
            5:'e',
            6:'f',
            7:'g',
            8:'h',
            9:'i',
            10:'j',
            11:'k',
            12:'l',
        }
        return maps.get(number)

if __name__ == '__main__':
    print(ANAConf.convert_number_to_alpha(1))