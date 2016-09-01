#!/usr/bin/env python
from __future__ import division
import math
import re
import json
import random
import copy
import numpy as np
import sys
caffe_root = '/home/sh/caffe-ief-train/'
sys.path.insert(0, caffe_root + 'python')

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
        #print  'Processing the image: ', fileName
        pointData = json.loads(dataSplit[1])

        pointCount = 0
        for i in range(16):
            if pointsName[i] in pointData:
                pointCount += 1
        if pointCount == 16:
            f.write(data)
            #f.write('\n')
    f.close()

def fit_pose_full(fit_pose_file, fit_pose_full_file):
    #fit_pose_file = '/home/data/ddpose/fit_pose.txt'
    f = open(fit_pose_file)
    fit_poses = f.readlines()
    f.close()

    #fit_pose_full_file = '/home/data/ddpose/fit_pose_full.txt'
    f = open(fit_pose_full_file, 'w')

    pointsName = ['R_ANKLE','R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','PELVIS','THORAX','NECK','HEAD','R_WRIST',\
                'R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST']

    for fit_pose in fit_poses:
        fit_pose_split = re.split('\|', fit_pose)
        fit_pose_img_name = fit_pose_split[0]
        fit_pose_points = json.loads(fit_pose_split[1])

        for i in range(16):
            if pointsName[i] not in fit_pose_points:
               fit_pose_points[pointsName[i]][0] = float('nan')
               fit_pose_points[pointsName[i]][1] = float('nan')
        f.write(fit_pose_img_name + '|' + json.dumps(fit_pose_points))
        f.write('\n')
    f.close()


def controller_fun(poses, controls, MAX_STEP_NORM):
    pointsName = ['R_ANKLE','R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','PELVIS','THORAX','NECK','HEAD','R_WRIST',\
                'R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST']

    new_poses = copy.deepcopy(controls)
    for i in range(16):
        if pointsName[i] in controls:
            direction_x, direction_y = controls[pointsName[i]]
            poses_x, poses_y = poses[pointsName[i]]
            new_poses_x = poses_x + MAX_STEP_NORM * direction_x
            new_poses_y = poses_y + MAX_STEP_NORM * direction_y
            new_poses[pointsName[i]][0] = new_poses_x
            new_poses[pointsName[i]][1] = new_poses_y
        else:
            new_poses_x = 0
            new_poses_y = 0

    return new_poses


def targets_and_controller_update(poses, target_poses, MAX_STEP_NORM):
    pointsName = ['R_ANKLE','R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','PELVIS','THORAX','NECK','HEAD','R_WRIST',\
                'R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST']

    targets_correction = copy.deepcopy(poses)
    #targets_correction = target_poses
    for i in range(16):
        if pointsName[i] in target_poses:
            initial_x,initial_y = poses[pointsName[i]]
            target_x, target_y = target_poses[pointsName[i]]
            dist = math.sqrt((target_x - initial_x)**2 + (target_y - initial_y)**2)
            ratios = max(1, dist/MAX_STEP_NORM)
            correction_x = (target_x - initial_x)/ratios
            correction_y = (target_y - initial_y)/ratios
            correction_x = correction_x/MAX_STEP_NORM
            correction_y = correction_y/MAX_STEP_NORM
            targets_correction[pointsName[i]][0] = correction_x
            targets_correction[pointsName[i]][1] = correction_y
        else:
            if pointsName[i] in targets_correction:
                targets_correction.pop(pointsName[i])
        #print targets_correction

    return targets_correction

def targets_and_controller(poses, target_poses, MAX_STEP_NORM):
    pointsName = ['R_ANKLE','R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','PELVIS','THORAX','NECK','HEAD','R_WRIST',\
                'R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST']

    targets_correction = copy.deepcopy(poses)
    for i in range(16):
        if pointsName[i] in target_poses:
            #print 'poses: -------', poses
            initial_x,initial_y = poses[pointsName[i]]
            target_x, target_y = target_poses[pointsName[i]]
            dist = math.sqrt((target_x - initial_x)**2 + (target_y - initial_y)**2)
            ratios = max(1, dist/MAX_STEP_NORM)
            correction_x = (target_x - initial_x)/ratios
            correction_y = (target_y - initial_y)/ratios
            correction_x = correction_x/MAX_STEP_NORM
            correction_y = correction_y/MAX_STEP_NORM
        else:
            correction_x = 0
            correction_y = 0
        targets_correction[pointsName[i]][0] = correction_x
        targets_correction[pointsName[i]][1] = correction_y
        #print targets_correction

    return targets_correction

def init_new_poses_nonan(orig_gt_poses_file, gt_poses_nonan_file,new_init_poses_file):
    #
    #orig_gt_poses_file = '/home/data/ddpose/fit_pose.txt'
    #gt_poses_nonan_file = '/home/data/ddpose/full_pose.txt'

    #fit_pose_full(orig_gt_poses_file, gt_poses_nonan_file) # nonan process
    full_pose_detection(orig_gt_poses_file, gt_poses_nonan_file)

    f = open(orig_gt_poses_file)
    orig_gt_poses = f.readlines()
    f.close()

    f = open(gt_poses_nonan_file)
    gt_poses_nonan = f.readlines()
    f.close()

    #new_init_poses_file = '/home/data/ddpose/init_pose_step.txt'
    f = open(new_init_poses_file, 'w')

    for orig_gt_pose in orig_gt_poses:
        strinfo = re.compile('\'')
        orig_gt_pose = strinfo.sub('\"',orig_gt_pose)
        orig_gt_pose_split = re.split('\|', orig_gt_pose)
        orig_gt_pose_name = orig_gt_pose_split[0]
        #print  'Processing the image: ', orig_gt_pose_name
        pointData = json.loads(orig_gt_pose_split[1])

        new_init_pose = str(random.sample(gt_poses_nonan, 1))
        new_init_pose_split = re.split('\|', new_init_pose)
        #print new_init_pose_split[1][:-4]
        new_init_poses = json.loads(new_init_pose_split[1][:-4])

        f.write(orig_gt_pose_name + '|' + json.dumps(new_init_poses))
        f.write('\n')
    f.close()

def update_data_shuffle(new_init_poses_file,fit_pose_file,new_fit_pose,stage, MAX_STEP_NORM):
    #new_init_poses_file = '/home/data/ddpose/init_pose_step.txt' #
    f = open(new_init_poses_file)
    new_init_poses = f.readlines()
    f.close()

    #fit_pose_file = '/home/data/ddpose/fit_pose.txt' #
    f = open(fit_pose_file)
    gt_poses = f.readlines()
    f.close()

    #new_fit_pose = '/home/data/ddpose/new_fit_pose.txt' #
    f = open(new_fit_pose, 'w')
    #fs = open(new_init_poses_file, 'w')

    i = 0
    for gt_pose in gt_poses:
        strinfo = re.compile('\'')
        gt_pose = strinfo.sub('\"',gt_pose)
        target_pose_split = re.split('\|', gt_pose)
        target_pose_name = target_pose_split[0]
        target_pose = json.loads(target_pose_split[1])

        init_poses = new_init_poses[i]
        #print init_poses
        init_pose_split = re.split('\|', init_poses)
        assert init_pose_split[0] == target_pose_name
        init_pose = json.loads(init_pose_split[1])

        i += 1
        init_pose_s = copy.deepcopy(init_pose)
        for s in range(stage):
            targets_controller = targets_and_controller_update(copy.deepcopy(init_pose_s), target_pose, MAX_STEP_NORM) #
            pred_controller = targets_controller

            new_pose = controller_fun(init_pose_s, pred_controller, MAX_STEP_NORM)

            new_target_pose = new_pose
            if s != stage-1:
                new_init_pose = new_pose
                init_pose_s = new_init_pose

            #print new_target_pose

        f.write(target_pose_name + '|' + json.dumps(new_target_pose))
        f.write('\n')
    f.close()

def compute_correction_train(stage, MAX_STEP_NORM):

    target_train_poses_file = '/home/data/ddpose/train.txt'
    full_train_poses_file = '/home/data/ddpose/full_train_pose.txt'
    new_train_init_poses_file = '/home/data/ddpose/init_train_pose_step.txt' # has multi
    init_new_poses_nonan(target_train_poses_file, full_train_poses_file,new_train_init_poses_file)

    new_train_pose_file = '/home/data/ddpose/new_train.txt' #
    update_data_shuffle(new_train_init_poses_file, target_train_poses_file, new_train_pose_file,stage, MAX_STEP_NORM) # new pose, yt


    f = open(new_train_init_poses_file)
    new_train_init = f.readlines()
    f.close()

    f = open(new_train_pose_file)
    target_train_poses = f.readlines()
    f.close()

    train_correttion_file = '/home/data/ddpose/trainCorrection.txt'
    f = open(train_correttion_file,'w')

    i = 0
    for gt_pose in target_train_poses:
        strinfo = re.compile('\'')
        gt_pose = strinfo.sub('\"',gt_pose)
        target_pose_split = re.split('\|', gt_pose)
        target_pose_name = target_pose_split[0]
        target_pose = json.loads(target_pose_split[1])

        init_poses = new_train_init[i]
        #print init_poses
        init_pose_split = re.split('\|', init_poses)
        assert init_pose_split[0] == target_pose_name
        init_pose = json.loads(init_pose_split[1])

        i += 1
        targets_controller = targets_and_controller(init_pose, target_pose, MAX_STEP_NORM) #
        f.write(target_pose_name + '|' + json.dumps(targets_controller))
        f.write('\n')
    f.close()

def compute_correction_test(stage, MAX_STEP_NORM):

    target_train_poses_file = '/home/data/ddpose/test.txt'
    full_train_poses_file = '/home/data/ddpose/full_test_pose.txt'
    new_train_init_poses_file = '/home/data/ddpose/init_test_pose_step.txt' # has multi
    init_new_poses_nonan(target_train_poses_file, full_train_poses_file,new_train_init_poses_file)

    new_train_pose_file = '/home/data/ddpose/new_test.txt' #
    update_data_shuffle(new_train_init_poses_file, target_train_poses_file, new_train_pose_file,stage, MAX_STEP_NORM) # new pose, yt

    # f = open(new_train_init_poses_file)
    # new_train_init = f.readlines()
    # f.close()

    # f = open(new_train_pose_file)
    # target_train_poses = f.readlines()
    # f.close()

    # train_correttion_file = '/home/data/ddpose/testCorrection.txt'
    # f = open(train_correttion_file,'w')

    # i = 0
    # for gt_pose in target_train_poses:
    #     strinfo = re.compile('\'')
    #     gt_pose = strinfo.sub('\"',gt_pose)
    #     target_pose_split = re.split('\|', gt_pose)
    #     target_pose_name = target_pose_split[0]
    #     target_pose = json.loads(target_pose_split[1])

    #     init_poses = new_train_init[i]
    #     #print init_poses
    #     init_pose_split = re.split('\|', init_poses)
    #     assert init_pose_split[0] == target_pose_name
    #     init_pose = json.loads(init_pose_split[1])

    #     i += 1
    #     targets_controller = targets_and_controller(init_pose, target_pose, MAX_STEP_NORM) #
    #     f.write(target_pose_name + '|' + json.dumps(targets_controller))
    #     f.write('\n')
    # f.close()

def compute_correction_init1(target_poses_file,center_pose_file,correttion_file):

    #target_poses_file = '/home/data/ddpose/train.txt'
    #center_pose_file = '/home/data/ddpose/pose_center.txt' #

    f = open(target_poses_file)
    target_poses = f.readlines()
    f.close()

    f = open(center_pose_file)
    center_pose = json.loads(f.readline())
    f.close()

    #correttion_file = '/home/data/ddpose/testCorrection.txt'
    f = open(correttion_file,'w')

    for gt_pose in target_poses:
        strinfo = re.compile('\'')
        gt_pose = strinfo.sub('\"',gt_pose)
        target_pose_split = re.split('\|', gt_pose)
        target_pose_name = target_pose_split[0]
        target_pose = json.loads(target_pose_split[1])

        targets_controller = targets_and_controller(center_pose, target_pose, MAX_STEP_NORM) #
        f.write(target_pose_name + '|' + json.dumps(targets_controller))
        f.write('\n')
    f.close()


def compute_correction_mod(initPoseTrain_file, targetPoseTrain_file, train_correttion_file):
    f = open(initPoseTrain_file)
    new_train_init = f.readlines()
    f.close()

    f = open(targetPoseTrain_file)
    target_train_poses = f.readlines()
    f.close()

    #train_correttion_file = '/home/data/ddpose/trainCorrection1.txt'
    f = open(train_correttion_file,'w')

    i = 0
    for gt_pose in target_train_poses:
        strinfo = re.compile('\'')
        gt_pose = strinfo.sub('\"',gt_pose)
        target_pose_split = re.split('\|', gt_pose)
        target_pose_name = target_pose_split[0]
        target_pose = json.loads(target_pose_split[1])

        init_poses = new_train_init[i]
        #print init_poses
        init_pose_split = re.split('\|', init_poses)
        assert init_pose_split[0] == target_pose_name
        init_pose = json.loads(init_pose_split[1])

        i += 1
        targets_controller = targets_and_controller(init_pose, target_pose, MAX_STEP_NORM) #
        f.write(target_pose_name + '|' + json.dumps(targets_controller))
        f.write('\n')


if __name__ == "__main__":

    T = 4
    epoches = 27
    MAX_STEP_NORM = 20
    stages = [1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4]
    initPose_file = '/home/data/ddpose/initTrainPose.txt'
    targetPose_file = '/home/data/ddpose/targetTrainPose.txt'
    f1 = open(initPose_file, 'w')
    f2 = open(targetPose_file, 'w')

    initPoseTest_file = '/home/data/ddpose/initTestPose.txt'
    targetPoseTest_file = '/home/data/ddpose/targetTestPose.txt'
    f3 = open(initPoseTest_file, 'w')
    f4 = open(targetPoseTest_file, 'w')

    for i in range(6):
        stage = stages[i]
        print 'epoch: --', i
        if i == 0:
            center_pose_file = '/home/data/ddpose/pose_center.txt'
            train_target_poses_file = '/home/data/ddpose/train.txt'
            train_correttion_file = '/home/data/ddpose/trainCorrection.txt'
            compute_correction_init1(train_target_poses_file,center_pose_file, train_correttion_file)

            ff0 = open(center_pose_file)
            center_pose = json.loads(ff0.readline())
            ff0.close()

            ff1 = open(train_target_poses_file)
            train_target_poses = ff1.readlines()
            ff1.close()

            for train_target_pose in train_target_poses:
                strinfo = re.compile('\'')
                train_target_pose = strinfo.sub('\"',train_target_pose)
                target_pose_split = re.split('\|', train_target_pose)
                target_pose_name = target_pose_split[0]

                f1.write(target_pose_name + '|' + json.dumps(center_pose))
                f1.write('\n')

                target_pose = json.loads(target_pose_split[1])
                f2.write(target_pose_name + '|' + json.dumps(target_pose))
                f2.write('\n')


            test_target_poses_file = '/home/data/ddpose/test.txt'
            test_correttion_file = '/home/data/ddpose/testCorrection.txt'
            compute_correction_init1(test_target_poses_file,center_pose_file, test_correttion_file)

            ff1 = open(test_target_poses_file)
            test_target_poses = ff1.readlines()
            ff1.close()

            for test_target_pose in test_target_poses:
                strinfo = re.compile('\'')
                test_target_pose = strinfo.sub('\"',test_target_pose)
                test_pose_split = re.split('\|', test_target_pose)
                target_pose_name = test_pose_split[0]

                f3.write(target_pose_name + '|' + json.dumps(center_pose))
                f3.write('\n')

                target_pose = json.loads(test_pose_split[1])
                f4.write(target_pose_name + '|' + json.dumps(target_pose))
                f4.write('\n')

        else:
            compute_correction_train(stage, MAX_STEP_NORM)
            #compute_correction_test(stage, MAX_STEP_NORM)
            new_train_init_poses_file = '/home/data/ddpose/init_train_pose_step.txt'
            new_train_pose_file = '/home/data/ddpose/new_train.txt' #

            ff2 = open(new_train_init_poses_file)
            init_train_poses = ff2.readlines()
            ff2.close()

            for init_train_pose in init_train_poses:
                strinfo = re.compile('\'')
                init_train_pose = strinfo.sub('\"',init_train_pose)
                init_pose_split = re.split('\|', init_train_pose)
                init_pose_name = init_pose_split[0]

                init_pose_temp = json.loads(init_pose_split[1])
                f1.write(init_pose_name + '|' + json.dumps(init_pose_temp))
                f1.write('\n')

            ff3 = open(new_train_pose_file)
            target_train_poses = ff3.readlines()
            ff3.close()

            for target_train_pose in target_train_poses:
                strinfo = re.compile('\'')
                target_train_pose = strinfo.sub('\"',target_train_pose)
                target_pose_split = re.split('\|', target_train_pose)
                target_pose_name = target_pose_split[0]

                target_pose_temp = json.loads(target_pose_split[1])
                f2.write(target_pose_name + '|' + json.dumps(target_pose_temp))
                f2.write('\n')


            #--------------------------
            compute_correction_test(stage, MAX_STEP_NORM)
            new_test_init_poses_file = '/home/data/ddpose/init_test_pose_step.txt'
            new_test_pose_file = '/home/data/ddpose/new_test.txt' #

            ff2 = open(new_test_init_poses_file)
            init_test_poses = ff2.readlines()
            ff2.close()

            for init_test_pose in init_test_poses:
                strinfo = re.compile('\'')
                init_test_pose = strinfo.sub('\"',init_test_pose)
                init_pose_split = re.split('\|', init_test_pose)
                init_pose_name = init_pose_split[0]

                init_pose_temp = json.loads(init_pose_split[1])
                f3.write(init_pose_name + '|' + json.dumps(init_pose_temp))
                f3.write('\n')

            ff3 = open(new_test_pose_file)
            target_test_poses = ff3.readlines()
            ff3.close()

            for target_test_pose in target_test_poses:
                strinfo = re.compile('\'')
                target_test_pose = strinfo.sub('\"',target_test_pose)
                target_pose_split = re.split('\|', target_test_pose)
                target_pose_name = target_pose_split[0]

                target_pose_temp = json.loads(target_pose_split[1])
                f4.write(target_pose_name + '|' + json.dumps(target_pose_temp))
                f4.write('\n')

    f1.close()
    f2.close()
    f3.close()
    f4.close()
    print 'Done.'

    train_correttion_file = '/home/data/ddpose/trainCorrection1.txt'
    compute_correction_mod(initPose_file, targetPose_file, train_correttion_file)

    test_correttion_file = '/home/data/ddpose/testCorrection1.txt'
    compute_correction_mod(initPoseTest_file, targetPoseTest_file, test_correttion_file)
