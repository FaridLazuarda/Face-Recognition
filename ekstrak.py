import cv2
import numpy as np
import scipy
from scipy.misc import imread
import pickle as cPickle
import random
import os

def extract(image_path):
	image = imread(image_path, mode="RGB")

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
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]

    result = {}
    for f in files:
        print 'Extracting features from image %s' % f
        name = f.split('/')[-1].lower()
        result[name] = extract_features(f)
    
    # saving all our feature vectors in pickled file
    with open(pickled_db_path, 'w') as fp:
        pickle.dump(result, fp)


