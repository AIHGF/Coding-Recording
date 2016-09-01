#!/usr/bin/env python

# PCA 产生的投影矩阵可视为将原始坐标变换到现有的坐标系，坐标系中的各个坐标按照重要性递减排列

from PIL import Image
from numpy import *
from pylab import *

def pca(X):
  '''
  主成分分析：
  输入： 矩阵X， 其中该矩阵中存储训练数据， 每一行为一条训练数据
  输出： 投影矩阵（按照唯独重要性排序）、方差和均值
  '''
  # 获取整数
  num_data, dim = X.shape
  
  # 数据中心化
  mean_X = X.mean(axis=0)
  X = X - mean_X
  
  if dim > num_data:
    # 第一种方式，紧凑技巧
    M = dot(X, X.T) # 协方差矩阵
    e, EV = linalg.eigh(M) # 特征值和特征向量
    tmp = dot(X.T, EV).T  # 紧凑技巧？？？
    V = tmp[::-1] # 最后的特征向量是所需要的，故将其逆转
    S = sqrt(e)[::-1] # 特征值按照递增顺序排列， 故需将其逆转
    for i in range(V.shape[1]):
      V[:,i] /= S
    else:
    # 使用 SVD 方法 - 矩阵维数较大时，计算非常慢
    U, S, V = linalg.svd(X)
    V = V[:num_data] # 仅仅返回前 num_data 维数据才合理
  
  # 返回投影矩阵、方差和均值
  return V, S, mean_X

def main():
  im = array(Image.open(img_list[0])) # 打开一幅图像，获取其大小
  m, n = im.shape[0:2] # 获取图像大小
  img_num = len(img_list) # 获取图像的数目
  
  # 创建矩阵，保存所有压平后的图像数据
  img_matrix = array([array(Image.open(im)).flatten() for im in img_list], 'f')
  
  # 执行PCA操作
  V, S, img_mean = pca(img_matrix)
  
  # 显示一些图像（均值图像和前7个模式）
  figure()
  gray()
  subplot(2,4,1)
  imshow(img_mean.shape(m,n))
  for i in range(7):
    subplot(2, 4, i+2)
    imshow(V[i].shape(m,n))
    
  show()
