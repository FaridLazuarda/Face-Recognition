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
    reference={}
    for f in files_batch:
        print ('Extracting features from image %s' % f)
        name=f.split('/')[-1]
        reference[name]=extract(f)
    
    """test={}
    for f in files_batch:
        print ('Extracting features from image %s' % f)
        name=f.split('/')[-1]
        test[name]=extract(f)
    """  
    with(open(pickled_ref,'w')) as fp:
        pickle.dump(reference,fp)   
    """
    with(open(pickled_test,'w')) as fp:
        pickle.dump(test,fp)
    """#saving all our feature vectors in txt file



"#####################################################################################"



class Matcher(object):

    def __init__(self):
        with open(pickled_test) as fp:
            self.test=pickle.load(fp)

        with open(pickled_ref) as fp:
            self.ref=pickle.load(fp)

        self.indexref=[]
        self.vectorref=[]
        self.indextest=[]
        self.vectortest=[]
        for k,v in self.test.items():
            self.indextest.append(k)
            self.vectortest.append(v)
        self.vectortest=np.array(self.vectortest)
        self.indextest=np.array(self.indextest)

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

    def matchEcl(self, images_path, topn=5):
        features = extract(images_path)
        img_distances=self.euclid_dist(features)
        print(img_distances)
        # getting top 5 records
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.indexref[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()

    def matchCos(self, image_path, topn=5):
        features = extract(image_path)
        img_distances = self.cosine(features)
        
        # getting top 5 records
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.indexref[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()


"###########################################################################################"



def show_img(path):
    img = Image.open(path)
    img.show()
    
def run():
    reference={}
    test={}
    dist=[]

    files = [os.path.join(image_test, p) for p in sorted(os.listdir(image_test))]
    

    
    # getting 3 random images 
    sample = random.sample(files, 1)
    #batch_extractor(image_ref,reference, test)
    ma = Matcher()
    
    for s in sample:
        print ('Query image ==========================================')
        
        print(s)
        show_img(s)
        
        
        name, match = ma.matchCos(s,topn=5)
        print(name)
        print(match)
        print ('Result images ========================================')
        for i in range(5):
            # we got cosine distance, less cosine distance between vectors
            # more they similar, thus we subtruct it from 1 to get match value
            print("Show image")
            
            show_img(os.path.join(image_ref,name[i]))
    

run()
