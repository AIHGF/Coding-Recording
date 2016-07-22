#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
random selecting some images
'''
import os

if __name__ == '__main__':
    fddmpii = open("ddmpii.txt", 'w')

    fdd = open('ddone_pose.txt','r')
    dddatas = fdd.readlines()
    fdd.close()
    print len(dddatas)
    for da in dddatas:
        fddmpii.write(da)

    fmpii = open('mpii.txt','r')
    mpiidatas = fmpii.readlines()
    fmpii.close()
    print len(mpiidatas)
    for dt in mpiidatas:
        fddmpii.write(dt)

    fddmpii.close()
 
