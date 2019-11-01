from PIL import Image
import os, os.path

imgs = []
path = "C:\Users\Farid Lazuarda\Documents\Code\Face-Recognition\PINS"
valid_images = [".jpg",".gif",".png",".tga"]
for f in os.listdir(path):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    imgs.append(Image.open(os.path.join(path,f))