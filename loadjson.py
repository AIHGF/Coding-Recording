#!/usr/bin/python
# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
json with text
'''
import io
import re
import numpy as np
import json

if __name__ == '__main__':

    annName = ('PELVIS','THORAX','NECK','HEAD','R_ANKLE',\
    'R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','R_WRIST',\
    'R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST')
    annID = [6,7,8,9,0,1,2,3,4,5,10,11,12,13,14,15]
    # Read the json data from text file
    f = open('pose.txt','r')
    # print f.read()
    datas = f.readlines()
    i = 1

    strr = '201605092650b4d7e1e14b4d927c3562f0c28ec9'#.jpg'
    #strr = 'selqjd'
    for data in datas:
        #print len(datas)
        #print 'Processing the image: ', str(i)
        #print data
        #print data
        datasplit = re.split('.jpg', data)
        poseName = datasplit[0]
        posePoint = datasplit[1]
        posePoint = eval(posePoint[1:-1])
        #del posePoint['HEAD']
        #d = eval(posePoint)
        #print poseName
        if strr in poseName:
            print posePoint
            posePoint2D = np.zeros((2,16))
            for i in range(16):
                jointName = annName[i]
                if jointName in posePoint:
                    posePoint2D[:,i] = posePoint[jointName]
                else:
                    posePoint2D[:,i] = [0,0]

    print posePoint2D



