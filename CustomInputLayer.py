import caffe
import os.path as osp
import ast
import numpy as np
from PIL import Image
import json

class CustomInputLayer(caffe.Layer):

    def setup(self, bottom, top):
        params = eval(self.param_str)
        self.input_file = params['input_file']
        self.indices = open(self.input_file).read().splitlines()

        self.center_dict = ast.literal_eval(open(params['center_point']).read())
        self.center_file = params['center_file']

        self.batch_size = params['batch_size']

        #
        self.batch_loader = BatchLoader(params, None)

        # reshape tops
        # dataShape = (3, 224, 224)
        # labelShape = (32, 1, 1)
        # maskShape = (32, 1, 1)
        # centerShape = (16, 2, 1)

        top[0].reshape(self.batch_size, 3, 224, 224)
        top[1].reshape(self.batch_size, 32, 1, 1)
        top[2].reshape(self.batch_size, 16, 2, 1)
        top[3].reshape(self.batch_size, 32, 1, 1)
        # top[0].reshape(self.batch_size, dataShape)
        # top[1].reshape(self.batch_size, labelShape)
        # top[2].reshape(self.batch_size, centerShape)
        # top[3].reshape(self.batch_size, maskShape)

        #print("----")

        # center_ = np.zeros((len(self.center_dict.keys()), 2, 1), dtype = np.float32)
        # i = 0
        # for key in sorted(self.center_dict.keys()):
        #     center_[i][0][0] = float(self.center_dict[key][0])
        #     center_[i][1][0] = float(self.center_dict[key][1])
        #     i += 1
        # self.center = center_


    def forward(self, bottom, top):
        """
        Load data

        """
        for itt in range(self.batch_size):
            # Use the batch loader to load the next image
            data, label, mask, center = self.batch_loader.load_next_image()
            # Add directly to the caffe data layer
            top[0].data[itt, ...] = data
            top[1].data[itt, ...] = label
            top[2].data[itt, ...] = center
            top[3].data[itt, ...] = mask

    def reshape(self, bottom, top):
        pass

    def backward(self, bottom, top):
        pass

class BatchLoader(object):

    def __init__(self, params, result):
        self.center_dict = ast.literal_eval(open(params['center_point']).read())
        self.batch_size = params['batch_size']
        self.mean = np.array(params['mean'])
        self.input_file = params['input_file']
        self.indexlist = [line.split('|') for line in open(self.input_file).read().splitlines()]

        self.center_file = params['center_file']
        self.center_idxlist = [line.split('|') for line in open(self.center_file).read().splitlines()]

        self._cur = 0  # current image

        print "BatchLoader initialized with {} images".format(len(self.indexlist))

    def load_next_image(self):
        """
        Load the next image in a batch

        """
        # Did we finish an epoch?
        if self._cur == len(self.indexlist):
            self._cur = 0
            #shuffle(self.indexlist)

        # Load an image
        index = self.indexlist[self._cur][0] # Get the image index
        image_file_name = index
        im = Image.open(image_file_name)
        data = np.array(im, dtype = np.float32)
        data = data[:,:,::-1]
        data -= self.mean
        data = data.transpose((2,0,1))

        label_dict = json.loads(self.indexlist[self._cur][1])
        for key in self.center_dict.keys():
            if key not in label_dict:
                label_dict[key] = [0, 0]
        label = np.zeros((len(label_dict.keys())*2, 1, 1), dtype = np.float32)
        mask = np.zeros((len(label_dict.keys())*2, 1, 1), dtype = np.float32)
        i = 0
        for key in sorted(label_dict.keys()):
            label[i*2][0][0] = float(label_dict[key][0])
            label[i*2+1][0][0] = float(label_dict[key][1])
            mask[i*2][0][0] = 0 if label_dict[key][0]==0 else 1
            mask[i*2+1][0][0] = 0 if label_dict[key][1]==0 else 1
            i += 1

        assert  image_file_name == self.center_idxlist[self._cur][0]
        point_dict = json.loads(self.center_idxlist[self._cur][1])
        for key in self.center_dict.keys():
            if key not in point_dict:
                point_dict[key] = [0, 0]
        center = np.zeros((len(self.center_dict.keys()), 2, 1), dtype = np.float32)
        i = 0
        for key in sorted(point_dict.keys()):
            center[i][0][0] = float(point_dict[key][0])
            center[i][1][0] = float(point_dict[key][1])
            i += 1

        self._cur += 1

        return data, label, mask, center

    def load_center(self):
        pass
