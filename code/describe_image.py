import pandas, numpy, scipy.ndimage
import os
import matplotlib.pyplot as plt
import random
import math
import logging

home = 'C:/Users/OPEN/Documents/NanZHAO/Projet CIR Fraude/'
path = 'C:/Users/OPEN/Documents/NanZHAO/Projet CIR Fraude/data/store/'  

logging.basicConfig(filename = os.path.join(home, 'code/images_info.log'), level = logging.INFO)

def sample_images(folder_name, sample_size):
    images = os.listdir(folder_name)
    print ("There are %d images for all the collected annonces. " %len(images))
    images_path = [os.path.join(folder_name, image) for image in images]
    images_sample = random.sample(images_path, sample_size)
    return (images_sample)
	
image_info = pandas.DataFrame(columns = ('Id','postId', 'height', 'width', 'channels'))

images_all = os.listdir(path)

count = 0
for im in images_all:
	postId = im.split('_')[0]
	Id = im.split(postId+'_')[1]
	logging.info(Id)
	shapes = scipy.ndimage.imread(os.path.join(path, im)).shape
	height = shapes[0]
	width  = shapes[1]
    #print(height, width)
	if len(shapes)==3:
		channels = shapes[2]
	else:
		channels = 2
	image_info = image_info.append(pandas.Series({'Id':Id, 'postId':postId, 'height':height, 'width':width, 'channels': channels}), ignore_index=True)
	count = count + 1
	if (count%2075) == 0:
		print(" %d percentage is done." %(count/2075) )
	
print(image_info.head())
print(len(image_info))
image_info.to_json(os.path.join(home, 'data/images_info.json'))