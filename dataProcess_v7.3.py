train_mat_file = '/devdata/workspace/test/train_data_epoch1.mat'
f = h5py.File(train_mat_file)
print f.keys()


# c = sio.loadmat('/devdata/workspace/test/c.mat')
# imc = c['c']

# data = [f[element[899]][:] for element in f['inputs_train']]
# im = data[1][7,:,:,:]
# im = im.transpose((2,1,0))
txtFile = '/home/data/ddpose/test_pose/train.txt'
ft = open(txtFile, 'w')

ref_dict = {'im':'', 'init_pos':'', 'label_control':''}
train_data = f['inputs_train']
for i in range(900):
    print '------------------', i
    data = [f[element[i]][:] for element in train_data]
    ims = data[1]
    init_poss = data[3] # kp_pos
    label_controls = data[5] # correction
    nums = len(init_poss)
    print 'num of ims', nums

    for j in range(nums):
        data_dict = copy.deepcopy(ref_dict)
        im = ims[j,:,:,:]
        im = im.transpose((2,1,0))

        init_pos = init_poss[j,:,:]
        label_control = label_controls[j,:]

        im = im.tolist()
        init_pos = init_pos.tolist()
        label_control = label_control.tolist()

        data_dict['im'] = im
        data_dict['init_pos'] = init_pos
        data_dict['label_control'] = label_control

        strr = json.dumps(data_dict)
        #print type(strr)
        ft.write(strr)
        ft.write('\n')
ft.close()
print 'Done.'


