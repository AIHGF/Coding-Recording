#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import os.path as osp

images_dir = '/home/data/ddpose/dd_pose/'
pose_file = '/home/data/ddpose/pose.txt'
pose_exist_file = '/home/data/ddpose/pose_exist.txt'
pose = open(pose_file, 'r')
pose_exist = open(pose_exist_file, 'w')
for ps in pose:
	image_path = ps.split('|')[0]
	image_path = osp.join(images_dir, image_path)
	if os.path.exists(image_path):
		pose_exist.write(ps)
pose_exist.close()
