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

def folder_extractor(image_path):


