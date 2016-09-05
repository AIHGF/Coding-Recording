#!/usr/bin/env python

import scipy.io as sio
import numpy as np
import json

def epoch_data_process(mat_file, mode, f1, f2, f3):
    pointsName = ['R_ANKLE','R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','PELVIS','THORAX','NECK','HEAD','R_WRIST',\
                'R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST']
    pose_dict = {'R_ANKLE':[1,1],'R_KNEE':[1,1],'R_HIP':[1,1],'L_HIP':[1,1],'L_KNEE':[1,1],'L_ANKLE':[1,1],'PELVIS':[1,1],\
             'THORAX':[1,1],'NECK':[1,1],'HEAD':[1,1],'R_WRIST':[1,1],'R_ELBOW':[1,1],'R_SHOULDER':[1,1],'L_SHOULDER':[1,1],\
             'L_ELBOW':[1,1],'L_WRIST':[1,1]}
    target_controls_dict = {'R_ANKLE':[1,1],'R_KNEE':[1,1],'R_HIP':[1,1],'L_HIP':[1,1],'L_KNEE':[1,1],'L_ANKLE':[1,1],'PELVIS':[1,1],\
             'THORAX':[1,1],'NECK':[1,1],'HEAD':[1,1],'R_WRIST':[1,1],'R_ELBOW':[1,1],'R_SHOULDER':[1,1],'L_SHOULDER':[1,1],\
             'L_ELBOW':[1,1],'L_WRIST':[1,1]}
    target_dict = {'R_ANKLE':[1,1],'R_KNEE':[1,1],'R_HIP':[1,1],'L_HIP':[1,1],'L_KNEE':[1,1],'L_ANKLE':[1,1],'PELVIS':[1,1],\
             'THORAX':[1,1],'NECK':[1,1],'HEAD':[1,1],'R_WRIST':[1,1],'R_ELBOW':[1,1],'R_SHOULDER':[1,1],'L_SHOULDER':[1,1],\
             'L_ELBOW':[1,1],'L_WRIST':[1,1]}

    if mode == 'train':
        train_data = sio.loadmat(mat_file)

        # 'train_data_epoch_indexlist',
        # 'train_data_epoch_initial_poses_train',
        # 'train_data_epoch_targets_poses_train',
        # 'train_data_epoch_seed_pose',
        # 'train_data_epoch_stage',
        # 'train_data_epoch_target_controls_train',
        # 'train_data_epoch_img_names')

        initial_poses_train = train_data['train_data_epoch_initial_poses_train']
        target_poses_train = train_data['train_data_epoch_targets_poses_train']
        target_controls_train = train_data['train_data_epoch_target_controls_train']
        img_names_train = train_data['train_data_epoch_img_names']
        train_stage = train_data['train_data_epoch_stage']
        print 'train_stage: ---------', train_stage

        # init_train_poses_file = '/home/data/ddpose/test/init_train.txt'
        # target_control_train_file = '/home/data/ddpose/test/targetCorrection_train.txt'
        # f1 = open(init_train_poses_file, 'w')
        # f2 = open(target_control_train_file, 'w')
        num_train_samples = len(target_poses_train)
        for i in range(num_train_samples):
            print 'processing: ---', i+1, 'th train image'
            init_train_sample = initial_poses_train[i][0]
            target_train_sample = target_poses_train[i][0]
            target_control = target_controls_train[0][i]
            for j in range(16):
                if type(init_train_sample[j][0]) == np.ndarray:
                    pose_dict[pointsName[j]][0] = init_train_sample[j][0][0]
                    pose_dict[pointsName[j]][1] = init_train_sample[j][1][0]
                else:
                    pose_dict[pointsName[j]][0] = init_train_sample[j][0]
                    pose_dict[pointsName[j]][1] = init_train_sample[j][1]

                if type(target_train_sample[j][0]) == np.ndarray:
                    target_dict[pointsName[j]][0] = target_train_sample[j][0][0]
                    target_dict[pointsName[j]][1] = target_train_sample[j][1][0]
                else:
                    target_dict[pointsName[j]][0] = target_train_sample[j][0]
                    target_dict[pointsName[j]][1] = target_train_sample[j][1]

                target_controls_dict[pointsName[j]][0] = target_control[j][0]
                target_controls_dict[pointsName[j]][1] = target_control[j + 16][0]

            img_name = str(img_names_train[0][i])[5:-2]
            init_train_img_name = '/home/sh/IEF-dd' + img_name

            f1.write(init_train_img_name + '|' + str(pose_dict))
            f1.write('\n')

            f2.write(init_train_img_name + '|' + str(target_controls_dict))
            f2.write('\n')

            f3.write(init_train_img_name + '|' + str(target_dict))
            f3.write('\n')
        #f1.close()
        #f2.close()

    elif mode == 'val':
        val_data = sio.loadmat(mat_file)
        # 'val_data_epoch_indexlist',
        # 'val_data_epoch_initial_poses_val',
        # 'val_data_epoch_targets_poses_val',
        # 'val_data_epoch_stage',
        # 'val_data_epoch_target_controls_val',
        # 'val_data_epoch_img_names')

        initial_poses_val = val_data['val_data_epoch_initial_poses_val']
        target_poses_val = val_data['val_data_epoch_targets_poses_val']
        target_controls_val = val_data['val_data_epoch_target_controls_val']
        img_names_val = val_data['val_data_epoch_img_names']
        val_stage = val_data['val_data_epoch_stage']
        print 'val_stage: -------', val_stage

        # init_val_poses_file = '/home/data/ddpose/test/init_val.txt'
        # target_control_val_file = '/home/data/ddpose/test/targetCorrection_val.txt'
        # f1 = open(init_val_poses_file, 'w')
        # f2 = open(target_control_val_file, 'w')
        num_val_samples = len(target_poses_val)
        for i in range(num_val_samples):
            print 'processing: ---', i+1, 'th val image'
            init_val_sample = initial_poses_val[i][0]
            target_val_sample = target_poses_val[i][0]
            target_control = target_controls_val[0][i]
            for j in range(16):
                if type(init_val_sample[j][0]) == np.ndarray:
                    pose_dict[pointsName[j]][0] = init_val_sample[j][0][0]
                    pose_dict[pointsName[j]][1] = init_val_sample[j][1][0]
                else:
                    pose_dict[pointsName[j]][0] = init_val_sample[j][0]
                    pose_dict[pointsName[j]][1] = init_val_sample[j][1]

                if type(init_val_sample[j][0]) == np.ndarray:
                    target_dict[pointsName[j]][0] = target_val_sample[j][0][0]
                    target_dict[pointsName[j]][1] = target_val_sample[j][1][0]
                else:
                    target_dict[pointsName[j]][0] = target_val_sample[j][0]
                    target_dict[pointsName[j]][1] = target_val_sample[j][1]

                target_controls_dict[pointsName[j]][0] = target_control[j][0]
                target_controls_dict[pointsName[j]][1] = target_control[j + 16][0]

            img_name = str(img_names_val[0][i])[5:-2]
            init_val_img_name = '/home/sh/IEF-dd' + img_name

            f1.write(init_val_img_name + '|' + str(pose_dict))
            f1.write('\n')

            f2.write(init_val_img_name + '|' + str(target_controls_dict))
            f2.write('\n')

            f3.write(init_val_img_name + '|' + str(target_dict))
            f3.write('\n')
        # f1.close()
        # f2.close()
    print 'Done.'

if __name__ == '__main__':

    init_train_poses_file = '/home/data/ddpose/test/init_train.txt'
    target_train_poses_file = '/home/data/ddpose/test/target_train.txt'
    target_control_train_file = '/home/data/ddpose/test/targetCorrection_train.txt'
    f1 = open(init_train_poses_file, 'w')
    f2 = open(target_control_train_file, 'w')
    f3 = open(target_train_poses_file, 'w')

    init_val_poses_file = '/home/data/ddpose/test/init_val.txt'
    target_val_poses_file = '/home/data/ddpose/test/target_val.txt'
    target_control_val_file = '/home/data/ddpose/test/targetCorrection_val.txt'
    f4 = open(init_val_poses_file, 'w')
    f5 = open(target_control_val_file, 'w')
    f6 = open(target_val_poses_file, 'w')

    epoches = 27
    for epoch in range(27):
        train_mat_file = '/devdata/results/test/train_data_epoch' + str(epoch+1) + '.mat'
        epoch_data_process(train_mat_file, 'train', f1, f2, f3)

        val_mat_file = '/devdata/results/test/val_data_epoch' + str(epoch+1) + '.mat'
        epoch_data_process(val_mat_file, 'val', f4, f5, f6)

    f1.close()
    f2.close()
    f3.close()
    f4.close()

#-------------------------------------------------------------------

# train_mat_file = '/home/sh/IEF-dd/test/train_data_epoch1.mat'
# train_data = sio.loadmat(train_mat_file)
#
# # 'train_data_epoch_indexlist',
# # 'train_data_epoch_initial_poses_train',
# # 'train_data_epoch_targets_poses_train',
# # 'train_data_epoch_seed_pose',
# # 'train_data_epoch_stage',
# # 'train_data_epoch_target_controls_train',
# # 'train_data_epoch_img_names')
# seed_pose = train_data['train_data_epoch_seed_pose']
# initial_poses_train = train_data['train_data_epoch_initial_poses_train']
# target_poses_train = train_data['train_data_epoch_targets_poses_train']
# target_controls = train_data['train_data_epoch_target_controls_train']
# img_names_train = train_data['train_data_epoch_img_names']
# train_stage = train_data['train_data_epoch_stage']
# print train_stage
#
# pointsName = ['R_ANKLE','R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','PELVIS','THORAX','NECK','HEAD','R_WRIST',\
#                 'R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST']
# pose_dict = {'R_ANKLE':[1,1],'R_KNEE':[1,1],'R_HIP':[1,1],'L_HIP':[1,1],'L_KNEE':[1,1],'L_ANKLE':[1,1],'PELVIS':[1,1],\
#              'THORAX':[1,1],'NECK':[1,1],'HEAD':[1,1],'R_WRIST':[1,1],'R_ELBOW':[1,1],'R_SHOULDER':[1,1],'L_SHOULDER':[1,1],\
#              'L_ELBOW':[1,1],'L_WRIST':[1,1]}
#
# init_train_poses_file = '/home/data/ddpose/test/init_train.txt'
# f = open(init_train_poses_file, 'w')
# num_train_samples = len(target_poses_train)
# for i in range(num_train_samples):
#     init_train_sample = initial_poses_train[i][0]
#     for j in range(16):
#         pose_dict[pointsName[j]][0] = init_train_sample[j][0]
#         pose_dict[pointsName[j]][1] = init_train_sample[j][1]
#
#     img_name = str(img_names_train[0][i])[5:-2]
#     init_train_img_name = '/home/sh/IEF-dd' + img_name
#
#     #print json.dumps(pose_dict)
#     f.write(init_train_img_name + '|' + str(pose_dict))
#     f.write('\n')
# f.close()



