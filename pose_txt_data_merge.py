#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
random selecting some images
'''
import os
import re
import shutil
import random

if __name__ == '__main__':

    # Read the json data from text file
    f = open('pose.txt','r')
    datas = f.readlines()
    f.close()
    #print datas

    f_one = open('one_person.txt','r')
    f_one_pose = open("one_pose.txt", 'w')
    # print f.read()
    datas_one = f_one.readlines()
    print len(datas_one)
    
    for fzdata in datas_one:
    	fzdatasplit = re.split('/ddpose/', fzdata)
    	fzdatasplit = fzdatasplit[1]
    	#print 'fzdatasplit:',fzdatasplit
    	#f_one_pose.write(fzdatasplit)
    	a = fzdatasplit[-35:-1]
    	#print 'a',str(a)

    	for data in datas:
    		imageName = re.split('.jpg', data)
    		imagesName = imageName[0]+'.jpg'
    		b = imagesName[-34:]
    		#print 'b',str(b)
    		
    		if str(a)==str(b):
    			print 'Hello world!'
    			fzstring = imagesName + imageName[1]
    			print fzstring
    			f_one_pose.write(fzstring)

    f_one_pose.close()


#    slices = random.sample(datas, 500)
#    #print slices
#    for data in slices:
#        datasplit = re.split('.jpg', data)
#        fileName = datasplit[0]
#        fileName = fileName+'.jpg'
#        #print 'Processing the image: ', fileName
#        
#        #shutil.move(fileName,"./test/")    
