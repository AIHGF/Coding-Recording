# 2016-07-20

import numpy as np
import math


def dist_fun(vec1, vec2):
    # Calculate the distance of two vector -- vector1 & vector2
    dist = math.sqrt((vec1[0]-vec2[0])**2 + (vec1[1]-vec2[1])**2)
    return dist

import re
def dis_calc(filename,fres):
    im = scm.imread(filename)
    pose = np.load(fres['raw'])
    kplabels = ['R_ANKLE','R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','PELVIS','THORAX','NECK','HEAD','R_WRIST',\
                'R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST']
    print 'Processing the image: ', filename
    imagename = re.split('image_testdd/',filename)
    imagename = imagename[1]
    imagename = imagename[:-4]

    f = open('pose.txt','r')
    datas = f.readlines()
    f.close()
    for data in datas:
        #print data
        datasplit = re.split('.jpg', data)
        poseName = datasplit[0]
        posePoint = datasplit[1]
        posePoint = eval(posePoint[1:-1])
        if imagename in poseName:
            #print posePoint
            posePoint2D = np.zeros((2,16)) # groundtruth 2D human joint points
            #if len(posePoint) == 16:
            for i in range(16):
                jointName = kplabels[i]
                if jointName in posePoint:
                    posePoint2D[:,i] = posePoint[jointName]
                else:
                    posePoint2D[:,i] = [0,0]
            print 'posePoint2D = ', posePoint2D

    ##
    kpts = pose.squeeze().transpose((1,0)) # predicted 2D points
    print 'predictedPoint2D = ', kpts
    pad = 5
    mnX, mnY  = np.min(kpts, axis=1)
    mxX, mxY  = np.max(kpts, axis=1)
    dx, dy    = abs(min(0, mnX)) + pad,  abs(min(0, mnY)) + pad
    dd   = np.array([dx, dy]).reshape(2,1)
    kpts = kpts + dd
    # rankle
    #dis_rankle = dist_fun((kpts[0,1],kpts[1,1]), )
    # rknee
    #dis_rknee = dist_fun((kpts[0,2],kpts[1,2]), )

    pointDist = np.zeros((1,16)) # distance
    for i in range(16):
        pointDist[:,i] = dist_fun((kpts[0,i],kpts[1,i]), posePoint2D[:,i])
        print 'Joint: ', kplabels[i], '---Distance = ', pointDist[:,i]

    print 'JointsDistance: ',pointDist

    return  pointDist
