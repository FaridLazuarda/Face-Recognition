import cv2
import numpy as np
import scipy
from matplotlib.pyplot import imread
import pickle
import random
import os
import matplotlib.pyplot as plt

image_path = r"PINS"
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
            
def batch_extractor(images_path, pickled_db_path="features.pck"):
    files_batch = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    print(files_batch)
    result = {}
    for f in files_batch:
        print ('Extracting features from image %s' % f)
        print(extract(f))
    
    # saving all our feature vectors in pickled file



"#####################################################################################"



class Matcher(object):

    def __init__(self, pickled_db_path="features.pck"):
        with open(pickled_db_path) as fp:
            self.data = pickle.load(fp)
        self.names = []
        self.matrix = []
        for k, v in self.data.iteritems():
            self.names.append(k)
            self.matrix.append(v)
        self.matrix = np.array(self.matrix)
        self.names = np.array(self.names)

    def cos_cdist(self, vector):
        # getting cosine distance between search image and images database
        v = vector.reshape(1, -1)
        return scipy.spatial.distance.cdist(self.matrix, v, 'cosine').reshape(-1)

    def match(self, image_path, topn=5):
        features = extract_features(image_path)
        img_distances = self.cos_cdist(features)
        # getting top 5 records
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()



"###########################################################################################"



def show_img(path):
    img = imread(image_path, mode="RGB")
    plt.imshow(img)
    plt.show()
    
def run():
    images_path = image_path
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    # getting 3 random images 
    sample = random.sample(files, 3)
    
    for i in files:
        batch_extractor(i)


run()
