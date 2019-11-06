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

dirname = r'C:\Users\Farid Lazuarda\Documents\Code\Face-Recognition\PINS'
final = []
for fname in os.listdir(dirname):
    im = Image.open(os.path.join(dirname, fname))
    imarray = np.array(im)
    final.append(imarray)

final = np.asarray(final)
print(final)