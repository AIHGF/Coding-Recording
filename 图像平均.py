#!/usr/bin/env python
# 图像平均是一种简单的减少图像噪声的方式，多用于艺术特效
# 从图像列表中计算出一幅平均图像
# 假设所有图像具有相同大小，累加图像，然后除以图像数目，以计算平均图像

def compute_average(imlist):
    '''
    计算图像列表的平均图像
    '''
    # 打开第一幅图像，将其存储在浮点型数组
    for img_name in img_list[1:]:
        try:
          average_img += array(Image.open(img_name))
        except:
          print img_name + '...skipped'
    average_img /= len(img_list)
    
    # 返回 unit8 类型的平均图像
    return array(average_img, 'unit8')
