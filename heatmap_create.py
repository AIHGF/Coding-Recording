#!/usr/bin/env python 
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

#from pyheatmap.heatmap import HeatMap
import heatmap
import random

if __name__ == "__main__":    
    pts = []
    for x in range(400):
        pts.append((random.random(), random.random() ))

    print "Processing %d points..." % len(pts)

    hm = heatmap.Heatmap()
    img = hm.heatmap(pts)
    img.save("classic.png")
