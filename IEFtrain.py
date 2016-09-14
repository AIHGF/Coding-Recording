#!/usr/bin/env python

import sys
import os
import re
import json
import random
import math
import numpy as np

thisDir = os.path.dirname(__file__)
caffe_path = os.path.join(thisDir, '..', '..','python')
sys.path.insert(0, caffe_path)

import caffe

def full_pose_detection(poseFile,poseFullFile):
    #poseFile = '/home/data/ddpose/fit_pose.txt'
    f = open(poseFile)
    posesData = f.readlines()
    f.close()

    #poseFullFile = '/home/data/ddpose/full_fit_pose.txt'
    f = open(poseFullFile,'w')

    pointsName = ['R_ANKLE','R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','PELVIS','THORAX','NECK','HEAD','R_WRIST',\
                'R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST']

    for data in posesData:
        strinfo = re.compile('\'')
        data = strinfo.sub('\"',data)
        dataSplit = re.split('\|', data)
        fileName = dataSplit[0]
        print  'Processing the image: ', fileName
        pointData = json.loads(dataSplit[1])

        pointCount = 0
        for i in range(16):
            if pointsName[i] in pointData:
                pointCount += 1
        if pointCount == 16:
            f.write(data)
            #f.write('\n')
    f.close()

def targets_controllers(poses, target_pose):
    pass

def update_data_epoch(cropPoseFile,centerPoseFile, correctionFile):
    #cropPoseFile = '/home/data/ddpose/fit_pose.txt'
    f = open(cropPoseFile)
    datas = f.readlines()
    f.close()

    #centerPoseFile = '/home/data/ddpose/pose_center.txt'
    f = open(centerPoseFile)
    centerPose = json.loads(f.readline())
    f.close()

    pointsName = ['R_ANKLE','R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','PELVIS','THORAX','NECK','HEAD','R_WRIST',\
                'R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST']

    #correctionFile = '/home/data/ddpose/trainCorrection.txt'
    f = open(correctionFile,'w')

    MAX_STEP_NORM = 20
    for data in datas:
        strinfo = re.compile('\'')
        data = strinfo.sub('\"',data)
        dataSplit = re.split('\|', data)
        fileName = dataSplit[0]
        print  'Processing the image: ', fileName
        pointData = json.loads(dataSplit[1])

        targetCorrection = centerPose
        for i in range(16):
            if pointsName[i] in pointData:
                point_x,point_y = pointData[pointsName[i]]
                center_x, center_y = centerPose[pointsName[i]]
                dist = math.sqrt((point_x - center_x)**2 + (point_y - center_y)**2)
                ratios = max(1, dist/MAX_STEP_NORM)
                target_x = (point_x - center_x)/ratios
                target_y = (point_y - center_y)/ratios
                target_x = target_x/MAX_STEP_NORM
                target_y = target_y/MAX_STEP_NORM
            else:
                target_x = 0
                target_y = 0
            targetCorrection[pointsName[i]][0] = target_x
            targetCorrection[pointsName[i]][1] = target_y
        #print targetCorrection
        f.write(fileName + '|' + str(targetCorrection))
        f.write('\n')
    f.close()


def update_data_epoches(poseFullFile, poseFile, newInitPoseFile):
    pointsName = ['R_ANKLE','R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','PELVIS','THORAX','NECK','HEAD','R_WRIST',\
                'R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST']

    #poseFullFile = '/home/data/ddpose/full_fit_pose.txt'
    f = open(poseFullFile)
    fullPosesData = f.readlines()
    f.close()

    #poseFile = '/home/data/ddpose/fit_pose.txt'
    f = open(poseFile)
    posesData = f.readlines()
    f.close()

    #newInitPoseFile = '/home/data/ddpose/trainCorrection.txt'
    f = open(newInitPoseFile,'w')

    MAX_STEP_NORM = 20

    for data in posesData:
        strinfo = re.compile('\'')
        data = strinfo.sub('\"',data)
        dataSplit = re.split('\|', data)
        fileName = dataSplit[0]
        print  'Processing the image: ', fileName
        pointData = json.loads(dataSplit[1])

        newInitPose = str(random.sample(fullPosesData, 1))
        newDataSplit = re.split('\|', newInitPose)
        print newDataSplit[1][:-4]
        newPointData = json.loads(newDataSplit[1][:-4])

        targetCorrection = newPointData
        for i in range(16):
            if pointsName[i] in pointData:
                point_x,point_y = pointData[pointsName[i]]
                center_x, center_y = newPointData[pointsName[i]]
                dist = math.sqrt((point_x - center_x)**2 + (point_y - center_y)**2)
                ratios = max(1, dist/MAX_STEP_NORM)
                target_x = (point_x - center_x)/ratios
                target_y = (point_y - center_y)/ratios
                target_x = target_x/MAX_STEP_NORM
                target_y = target_y/MAX_STEP_NORM

                newCenter_x = center_x + target_x * MAX_STEP_NORM
                newCenter_y = center_y + target_y * MAX_STEP_NORM
                newDist = math.sqrt((point_x - newCenter_x)**2 + (point_y - newCenter_y)**2)
                newRatios = max(1, newDist/MAX_STEP_NORM)
                targetCorrection_x = (point_x - newCenter_x)/newRatios
                targetCorrection_y = (point_y - newCenter_y)/newRatios
                targetCorrection_x = targetCorrection_x/MAX_STEP_NORM
                targetCorrection_y = targetCorrection_y/MAX_STEP_NORM

            else:
                #target_x = 0
                #target_y = 0
                targetCorrection_x = 0
                targetCorrection_y = 0
            targetCorrection[pointsName[i]][0] = targetCorrection_x
            targetCorrection[pointsName[i]][1] = targetCorrection_y
        #print targetCorrection

        f.write(fileName + '|' + str(targetCorrection))
        f.write('\n')
    f.close()

def train_test_txt(epoch):
    # poseFileTrain = '/home/data/ddpose/train.txt'
    # poseFullFileTrain = '/home/data/ddpose/full_train_pose.txt'
    # full_pose_detection(poseFileTrain, poseFullFileTrain)
    #
    # poseFileTest = '/home/data/ddpose/test.txt'
    # poseFullFileTest = '/home/data/ddpose/full_test_pose.txt'
    # full_pose_detection(poseFileTest, poseFullFileTest)

    if epoch == 0:
        poseFullFile = '/home/data/ddpose/pose_center.txt'

        cropPoseFileTrain = '/home/data/ddpose/train.txt'
        correctionFileTrain = '/home/data/ddpose/trainCorrection.txt'
        update_data_epoch(cropPoseFileTrain,poseFullFile,correctionFileTrain)

        cropPoseFileTest = '/home/data/ddpose/test.txt'
        correctionFileTest = '/home/data/ddpose/testCorrection.txt'
        update_data_epoch(cropPoseFileTest,poseFullFile,correctionFileTest)

    else:
        poseFullFileTrain = '/home/data/ddpose/full_train_pose.txt'
        poseFileTrain = '/home/data/ddpose/train.txt'
        newInitPoseFileTrain = '/home/data/ddpose/trainCorrection.txt'
        update_data_epoches(poseFullFileTrain,poseFileTrain,newInitPoseFileTrain)

        poseFullFileTest = '/home/data/ddpose/full_test_pose.txt'
        poseFileTest = '/home/data/ddpose/test.txt'
        newInitPoseFileTest = '/home/data/ddpose/testCorrection.txt'
        update_data_epoches(poseFullFileTest,poseFileTest,newInitPoseFileTest)


def getSolverPrototxt(base_lr):
    folder_name = '/home/sh/caffe-ief-train/models/ief'
    string = 'net: "/home/sh/caffe-ief-train/models/ief/ief-googlenet-dec2015.prototxt"\n\
# The base learning rate, momentum and the weight decay of the network.\n\
test_iter: 100\n\
test_interval: 1000\n\
test_initialization: false\n\
average_loss: 100\n\
base_lr: %f\n\
momentum: 0.9\n\
weight_decay: 0.0005\n\
# The learning rate policy\n\
lr_policy: "fixed"\n\
#lr_policy: "step"\n\
#gamma: 0.333\n\
# Display every 100 iterations\n\
display: 100\n\
# The maximum number of iterations\n\
max_iter: 3000\n\
# snapshot intermediate results\n\
snapshot: 1000\n\
snapshot_prefix: "%s/pose"\n\
# solver mode: CPU or GPU\n\
solver_mode: GPU\n' % (base_lr,folder_name)
    return string

if __name__ == "__main__":
    #
    poseFileTrain = '/home/data/ddpose/train.txt'
    poseFullFileTrain = '/home/data/ddpose/full_train_pose.txt'
    full_pose_detection(poseFileTrain, poseFullFileTrain)

    poseFileTest = '/home/data/ddpose/test.txt'
    poseFullFileTest = '/home/data/ddpose/full_test_pose.txt'
    full_pose_detection(poseFileTest, poseFullFileTest)
    #

    caffe.set_device(0)
    caffe.set_mode_gpu()

    T = 4
    epoches = 27
    stages = [1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4]
    lr = 0.002
    n_ep = 6
    learningRate = [0.002,  0.002,  0.002,  0.002,  0.002,  0.002, \
                    0.002,  0.002,  0.002,  0.002,  0.002,  0.002, \
                    0.002,  0.002,  0.002,  0.002,  0.002,  0.002, \
                    0.002,  0.002,  0.002,  0.002,  0.002,  0.002,  0.0002,  0.0002,  0.0002]
    trainLoss = np.zeros(epoches)

    epoches = 1
    for epoch in range(epoches):
        stage = stages[epoch]

        train_test_txt(epoch)

        base_lr = learningRate[epoch]

        solverTxt = '/home/sh/caffe-ief-train/models/ief/solver.prototxt'
        with open(solverTxt, 'w') as f:
            solver_string = getSolverPrototxt(base_lr)
            print 'writing solver.prototxt'
            f.write('%s' % solver_string)

        if epoch == 0:
            solver = caffe.SGDSolver('/home/sh/caffe-ief-train/models/ief/solver.prototxt')
            solver.step(5000)
        else:
            solver = caffe.SGDSolver('/home/sh/caffe-ief-train/models/ief/solver.prototxt')
            solver.net.copy_from('/home/sh/caffe-ief-train/models/ief/pose_iter_5000.caffemodel')
            solver.step(5000)

        trainLoss[epoch] = solver.net.blobs['top_loss'].data

        print '----trainLoss:  ', trainLoss

