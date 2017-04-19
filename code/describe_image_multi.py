import pandas, numpy, scipy.ndimage
import os, timeit
import matplotlib.pyplot as plt
import random
import math
import logging
import multiprocessing as mp

home = 'C:/Users/OPEN/Documents/NanZHAO/Projet CIR Fraude/'
path = 'C:/Users/OPEN/Documents/NanZHAO/Projet CIR Fraude/data/store/'  
logging.basicConfig(filename = os.path.join(home, 'code/images_info.log'), level = logging.INFO)
process_number = 40

images_all = os.listdir(path)

def get_image_info(im):
	postId = im.split('_')[0]
	Id = im.split(postId+'_')[1]
	logging.info(Id)
	shapes = scipy.ndimage.imread(os.path.join(path, im)).shape
	height = shapes[0]
	width  = shapes[1]
	if len(shapes) == 3:
		channels = shapes[2]
	else:
		channels = 2
	
	return(pandas.Series({'Id':Id, 'postId':postId, 'height':height, 'width':width, 'channels': channels}))



if __name__ == '__main__':
	start = timeit.default_timer()
	image_info = pandas.DataFrame(columns = ('Id','postId', 'height', 'width', 'channels'))
	count =  0
	p = mp.Pool(process_number)
	for image in images_all:
		res = p.apply_async(get_image_info, (image,)).get(timeout=10)
		#print(res)
		image_info = image_info.append (res, ignore_index=True)
		#image_info.append (res.get(timeout=10))
		#print(image_info.head())
		"""
		count = count + 1
		if (count%2075) == 0:
			print(" %d percentage is done." %(count/2075) )
		"""	
	print(image_info.head())
	print(len(image_info))
	image_info.to_json(os.path.join(home, 'data/images_info.json'))
	stop = timeit.default_timer()
	print("Execution time: ", (stop-start))