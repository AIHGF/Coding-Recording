#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2016-07-21

'''
random selecting some images
'''
import os
import re
import shutil
import random

if __name__ == '__main__':

    # Read the json data from text file
    f = open('image.txt','r')
    # print f.read()
    datas = f.readlines()
    print len(datas)
    #print datas[1]

    slices = random.sample(datas, 200)
    #print slices
    for data in slices:
        datasplit = re.split('.jpg', data)
        fileName = datasplit[0]
        fileName = fileName+'.jpg'
        print 'Processing the image: ', fileName
        
        shutil.move(fileName,"./test/")    #移动fileName图片到test文件夹
