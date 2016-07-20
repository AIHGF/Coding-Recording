% 2016-07-20

%将结构体形式的matlab mat格式数据转化为json格式的txt文件

clear
load('xxx.mat')
% xxx.mat 为结构体形式
% 
dlmwrite('output.txt',xxx,'-append','delimiter', '');
% xxx为 xxx.mat 内的变量元素
