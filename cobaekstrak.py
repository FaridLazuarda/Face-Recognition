import cv2
import numpy as np
import scipy
from matplotlib.pyplot import imread
import pickle
import random
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
from fungsi import *
from PIL import Image

image_path = r"C:\Users\Farid Lazuarda\Documents\Code\Face-Recognition\COPINS"
image_dir = os.listdir(image_path)

def extract(images_path):
    image = imread(images_path)
            
    alg = cv2.KAZE_create()
                # Dinding image keypoints
    kps = alg.detect(image)
                # Getting first 32 of them. 
                # Number of keypoints is varies depend on image size and color pallet
                # Sorting them based on keypoint response value(bigger is better)
    kps = sorted(kps, key=lambda x: -x.response)[:32]
                # computing descriptors vector
    kps, dsc = alg.compute(image, kps)
                # Flatten all of them in one big vector - our feature vector
    dsc = dsc.flatten()
                # Making descriptor of same size
                # Descriptor vector size is 64
    needed_size = (32 * 64)
    if dsc.size < needed_size:
                    # if we have less the 32 descriptors then just adding zeros at the
                    # end of our feature vector
        dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])

    return dsc
            
def batch_extractor(images_path, reference, test):
    files_batch = [os.path.join(images_path, p) for p in (os.listdir(images_path))]
    print(files_batch)
    n=len(files_batch)
    r=8*n/10
    r = math.ceil(r)

    ref = open("reference.txt", "a")
    tst = open("test.txt", "a")

    for f in range (0,r):
        print ('Extracting features from image %s' % f)
        name=files_batch[f]
        reference[name]=extract(files_batch[f])
        ref.write(str(name))
        ref.write(" ")
        for i in reference[name] :    
            ref.write(str(i))
            ref.write(" ")
        ref.write("\n")

    for f in range(r,n):
        print ('Extracting features from image %s' % f)
        name=files_batch[f]
        test[name]=extract(files_batch[f])
        tst.write(str(name))
        tst.write(" ")
        for i in test[name] :
            tst.write(str(i))
            tst.write(" ")
        tst.write("\n")
    # saving all our feature vectors in pickled file



"#####################################################################################"



class Matcher(object):

    def __init__(self):
        dataref = open("reference.txt", "r")
        datatst = open("test.txt", "r")
        self.ref={}
        self.tst={}

        for l in dataref:
            a=l.split(' ')
            vector=[]
            for i in range(2049):
                if(i==0):
                    key=a[i]
                else:
                    vector.append(a[i])

            self.ref[key]=vector

        for l in datatst:
            a=l.split(' ')
            vector=[]
            for i in range(2049):
                if(i==0):
                    key=a[i]
                else:
                    vector.append(a[i])

            self.tst[key]=vector


    def matchEcl(self, images_path, topn=5):
        ecl={}
        for k,v in self.tst.items():
            print(k)
            print(v)
        for k,v in self.ref.items():
            x=self.ref[k]
            y=self.tst[images_path]
            a=Ecl_dist(x,y)
            ecl[k]=a
        # getting top 5 records
        sorted_ecl=sorted(ecl.items(), key=lambda kv: kv[1])

        return sorted_ecl

    def matchCos(self, image_path, topn=5):
        features = extract_features(images_path)
        img_distances = self.Cos_simil(features)
        # getting top 5 records
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()


"###########################################################################################"



def show_img(path):
    img = Image.open(path)
    img.show()
    
def run():
    reference={}
    test={}
    dist=[]
    images_path = image_path
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    

    
    # getting 3 random images 
    sample = random.sample(files, 3)
   # for i in files:
    #    batch_extractor(i,reference, test)
    ma = Matcher()
    for s in sample:
        for f in (os.listdir(s)):
            print ('Query image ==========================================')
            img=os.path.join(s,f)
            print(img)
            show_img(img)
            matchEuclid = ma.matchEcl(img, topn=5)
            matchEuclid=matchEuclid[:3]
            print ('Result images ========================================')
            for k,v in matchEuclid:
                # we got cosine distance, less cosine distance between vectors
                # more they similar, thus we subtruct it from 1 to get match value
                print("Show image")
                print(k)
                show_img(k)
    

run()
