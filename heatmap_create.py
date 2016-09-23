#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''
Installiation：
1.pip 安装：
pip install pyheatmap
2.easy_install 安装：
easy_install pyheatmap
3.源码安装：
git clone git://github.com/oldj/pyheatmap.git
cd pyheatmap
python setup.py install
'''
#From: https://github.com/oldj/pyheatmap

import urllib
from pyheatmap.heatmap import HeatMap
import random

def make_test_data():

    width = 400
    height = 300

    # 随机生成测试数据
    data = []
    r = 50
    for i in range(4):
        data.append([
            random.randint(0, width - 1),
            random.randint(0, height - 1),
            ])
    for i in xrange(12):
        data2 = []
        for x, y in data:
            x2 = x + random.randint(-r, r)
            y2 = y + random.randint(-r, r)
            data2.append([x2, y2])
        data.extend(data2)
    print(len(data))
    return data

    # f = open("test_data.txt", "w")
    # for x, y in data:
    #     f.write("%d,%d\n" % (x, y))
    # f.close()

def main():

    data = make_test_data()

    # 开始绘制
    hm = HeatMap(data)
    hm.clickmap(save_as="hit.png")
    hm.heatmap(save_as="heat.png")

if __name__ == "__main__":
    main()
