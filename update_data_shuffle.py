#!/usr/bin/env python
from __future__ import division
import math
import re
import json
import random
import copy

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

#[new_initial_poses, new_target_poses] = update_data_shuffle_nonan(initial_poses, gt_poses, stage, ids, opts, params)

def controller_fun(poses, controls, MAX_STEP_NORM):
    #assert poses.shape == 32
    #assert  controls.shape[0] == 32

    pointsName = ['R_ANKLE','R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','PELVIS','THORAX','NECK','HEAD','R_WRIST',\
                'R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST']

    new_poses = poses
    for i in range(16):
        if pointsName[i] in poses:
            direction_x, direction_y = controls[pointsName[i]]
            poses_x, poses_y = poses[pointsName[i]]
            new_poses_x = poses_x + MAX_STEP_NORM * direction_x
            new_poses_y = poses_y + MAX_STEP_NORM * direction_y
        else:
            new_poses_x = float('nan')
            new_poses_y = float('nan')
        new_poses[pointsName[i]][0] = new_poses_x
        new_poses[pointsName[i]][1] = new_poses_y
    return new_poses


def targets_and_controller(poses, target_poses, MAX_STEP_NORM):
    pointsName = ['R_ANKLE','R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','PELVIS','THORAX','NECK','HEAD','R_WRIST',\
                'R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST']

    targets_correction = poses
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
    full_pose_detection(orig_gt_poses_file, gt_poses_nonan_file) ###

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
            targets_controller = targets_and_controller(copy.deepcopy(init_pose_s), target_pose, MAX_STEP_NORM) #
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

if __name__ == "__main__":

    orig_gt_poses_file = '/home/data/ddpose/train.txt'
    gt_poses_nonan_file = '/home/data/ddpose/full_train_pose.txt'
    new_init_poses_file = '/home/data/ddpose/init_train_pose_step.txt'
    init_new_poses_nonan(orig_gt_poses_file, gt_poses_nonan_file,new_init_poses_file)

    fit_pose_file = '/home/data/ddpose/train.txt' #
    new_fit_pose = '/home/data/ddpose/new_train.txt' #
    stage = 4
    MAX_STEP_NORM = 20
    update_data_shuffle(new_init_poses_file,fit_pose_file,new_fit_pose,stage, MAX_STEP_NORM)

