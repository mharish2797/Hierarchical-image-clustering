# -*- coding: utf-8 -*-
"""
Created on Sun May  3 11:30:38 2020

@author: mhari
"""


from skimage.measure import compare_ssim
from skimage.transform import resize
from matplotlib.pyplot import imread
import time
import numpy as np

import os
from fnmatch import fnmatch

from PIL import Image

dimension = 2**5
length, width = dimension, dimension

pattern = "*.jpg"
dir_path = "E:\\Photos\\Latest\\USC\\Test\\"

clusters = list()
data = dict()

def get_image(img_path):
    img = np.array(Image.open(img_path).resize((length, width), Image.NEAREST))
#    img = resize(imread(img_path), (length, width))
    return img
            
for path, subdirs, files in os.walk(dir_path):
    for name in files:
        if fnmatch(name, pattern):
            filename = os.path.join(path, name)
            data[name] = get_image(filename)
            
def has_similar_cluster(candidate):
    candidate_data = data[candidate]
    global clusters
    max_score = float('-inf')
    index = -1
    for i, cluster in enumerate(clusters):
        for item in cluster:
            score, diff = compare_ssim(candidate_data, data[item], full=True, multichannel=True)
            print((candidate, item, score))
            if score > max_score:
                max_score = score
                index = i
    if index >= 0 and max_score > 0.08:
        cluster.append(candidate)
        return True
    
    return False

for item in data:
    if not has_similar_cluster(item):
        clusters.append(list([item]))


#path1 = dir_path + "IMG_20190113_132901.jpg"
#path2 = dir_path + "IMG_20190113_132902.jpg"
#path3 = dir_path + "IMG_20190113_132610.jpg"

#start = time.time()
## get two images - resize both to 1024 x 1024
#
#img_a = get_image(path1)
#img_b = get_image(path3)
#
#print(time.time() - start)
#
## score: {-1:1} measure of the structural similarity between the images
#score, diff = compare_ssim(img_a, img_b, full=True, multichannel=True)
#print(score)
#print(time.time() - start)