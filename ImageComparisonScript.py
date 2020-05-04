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
from itertools import product as combo

import networkx as nx
from networkx.algorithms.components.connected import connected_components

import os
from fnmatch import fnmatch

from PIL import Image

dimension = 2**5
length, width = dimension, dimension
THRESHOLD = 0.08
MAX_SCORE = float('inf')
MAX_ITERATIONS = 1000

pattern = "*.jpg"
dir_path = "E:\\Photos\\Latest\\USC\\Fall 2018\\"

clusters = dict()

timeCounter = time.time()

def get_time():
    global timeCounter
    currentTime = time.time() - timeCounter
    timeCounter = time.time()
    return currentTime

def get_image(img_path):
    img = np.array(Image.open(img_path).resize((length, width), Image.NEAREST))
#    img = resize(imread(img_path), (length, width))
    return img
     
CORPUS = dict()
                
for path, subdirs, files in os.walk(dir_path):
    for i, name in enumerate(files):
        if fnmatch(name, pattern):
            filename = os.path.join(path, name)
            clusters[i] = [(name, get_image(filename))]
print("Reading files done in:", get_time())

def generate_value_counter():
    
    cluster_items = list()
    for items in clusters.values():
        cluster_items += items
    for ind1, data1 in cluster_items:
        for ind2, data2 in cluster_items:
            if ind1 < ind2:
                score, diff = compare_ssim(data1, data2, full=True, multichannel=True)
                CORPUS[(ind1, ind2)] = score
                
generate_value_counter()

print("Corpus generated in:", get_time())

def get_similar_score(ind1):
    
    score_set = list()
    for ind2 in clusters:
        if ind1 == ind2:
            continue
        min_score = MAX_SCORE
        merge_index = -1
        combinations = combo(clusters[ind1], clusters[ind2])
        for (f1,data1), (f2, data2) in combinations:
            if f1 < f2:
                score = CORPUS[(f1, f2)]
            else:
                score = CORPUS[(f2, f1)]
            if score < min_score:
                min_score = score
                merge_index = ind2
                
        score_set.append((min_score, merge_index))
    
    max_score, merge_index = max(score_set, key = lambda x: x[0])
    if max_score < THRESHOLD:
        merge_index = -1
    
    return max_score, merge_index

def merge_clusters(ind1, ind2):
    clusters[ind1] += clusters[ind2]
    del (clusters[ind2])

number_of_clusters = len(clusters)

iterations = 0
while iterations < MAX_ITERATIONS:
    iterations += 1
    if iterations % 10 == 0:
        print(iterations)
    candidates = list()
    for index in clusters:
         index_score, mergeable = get_similar_score(index)
         candidates.append((index_score, index, mergeable))
    
    _, mergee, merger = max(candidates, key = lambda x: x[0])
    if merger > -1:
        merge_clusters(mergee, merger)
    
    curr_cluster_number = len(clusters)
    if curr_cluster_number == number_of_clusters:
        break
    number_of_clusters = curr_cluster_number

print(iterations, "iterations completed clustering in", get_time())
