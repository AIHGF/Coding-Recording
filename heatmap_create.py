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

def main():
    # 下载测试数据
    url = "https://raw.github.com/oldj/pyheatmap/master/examples/test_data.txt"
    sdata = urllib.urlopen(url).read().split("\n")
    data = []
    for ln in sdata:
        a = ln.split(",")
        if len(a) != 2:
            continue
        a = [int(i) for i in a]
        data.append(a)

    # 开始绘制
    hm = HeatMap(data)
    hm.clickmap(save_as="hit.png")
    hm.heatmap(save_as="heat.png")

if __name__ == "__main__":
    main()
