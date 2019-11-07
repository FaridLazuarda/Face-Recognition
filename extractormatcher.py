import cv2
import numpy as np
import scipy
import scipy.spatial
from matplotlib.pyplot import imread
import pickle
import random
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
from fungsi import *
from PIL import Image

image_test = r"Face-Recognition/database/test"
image_ref = r"Face-Recognition/database/base"

pickled_ref="reference.pck"
pickled_test="test.pck"

def extract(images_path):
    image = imread(images_path)
    alg = cv2.AKAZE_create()
    kps = alg.detect(image)
    kps = sorted(kps, key=lambda x: -x.response)[:32]
    kps, dsc = alg.compute(image, kps)
    dsc = dsc.flatten()
    needed_size = (32 * 64)
    if dsc.size < needed_size:
        dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])

    return dsc
            
def batch_extractor(images_path, reference, test):
    files_batch = [os.path.join(images_path, p) for p in (os.listdir(images_path))]
    print(files_batch)
    n=len(files_batch)
    reference={}
    for f in files_batch:
        print ('Extracting features from image %s' % f)
        name=f.split('/')[-1]
        reference[name]=extract(f)

    with(open(pickled_ref,'w')) as fp:
        pickle.dump(reference,fp)   



"#####################################################################################"



class Matcher(object):

    def __init__(self):
        with open(pickled_ref) as fp:
            self.ref=pickle.load(fp)

        self.indexref=[]
        self.vectorref=[]
        
        for k,v in self.ref.items():
            self.indexref.append(k)
            self.vectorref.append(v)
        self.vectorref=np.array(self.vectorref)
        self.indexref=np.array(self.indexref)


    def euclid_dist(self, vector):
        # getting cosine distance between search image and images database
        v = vector.reshape(1, -1)
        dist=[]
        for value in self.vectorref:
            distance=Ecl_dist(v[0],value)
            dist.append(distance)
        return np.array(dist).reshape(-1)

    def cosine(self, vector):
        v = vector.reshape(1,-1)
        similar=[]
        for value in self.vectorref:
            similarity=Cos_simil(v[0],value)
            similar.append(similarity)
        return np.array(similar).reshape(-1)

    def matchEcl(self, images_path, topn):
        dsc = extract(images_path)
        distance =self.euclid_dist(dsc)
        
        ids = np.argsort(distance)[:topn].tolist()
        path = self.indexref[ids].tolist()

        name = path
        match = distance[ids].tolist()
        return name, match
    def matchCos(self, images_path, topn):
        dsc = extract(images_path)
        distance =self.cosine(dsc)
        
        ids = np.argsort(distance)[:topn].tolist()
        path = self.indexref[ids].tolist()

        name = path
        match = distance[ids].tolist()
        return name, match


"###########################################################################################"



    

