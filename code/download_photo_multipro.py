import pandas, numpy
import math
import matplotlib.pyplot as plt
import os, timeit
import scipy.ndimage
import urllib
import urllib.request
import socket
import multiprocessing as mp


timeout = 10
socket.setdefaulttimeout(timeout)
home = 'C:/Users/OPEN/Documents/NanZHAO/Projet CIR Fraude/'
process_number = 1

annonces = pandas.read_json(os.path.join(home, 'data/photos.json'))
annonces['exist'] = 'True'
annonces['flag'] = 0


indexlist = annonces.sort_values('postId', ascending=False).index.tolist()

#indexlist = annonces.sort_values('postId').index.tolist()


def download(idx, url, image_folder, id):
	ok = True	
	#log_file = open(filename, "a")
	image_path = os.path.join(image_folder, id+'_'+url.split('images.craigslist.org/')[1]) 
	
	if os.path.isfile(image_path):
		print("Skipping existing file :" + image_path + "\n")
		#log_file.write("Skipping existing file :" + image_path + "\n")
		return(ok)
	
	try:
		result = urllib.request.urlopen(url)
	except urllib.error.HTTPError as err:
		print("Type error: "+ str(err.code)+ "\n")
		print("photo "+ url+ " does not exist.\n")
		#log_file.write("Type error: "+ str(err.code)+ "\n")
		#log_file.write("photo "+ url+ " does not exist.\n")
		ok = False
	
	print(ok)
	#log_file.write(ok)

	if ok == False:
		print("Annonce "+ id+ " does not exist.\n")
		#log_file.write("Annonce "+ id+ " does not exist.\n")
		annonces.loc[idx, 'exist'] = annonces.loc[idx, 'exist'].replace('True', 'False')
	
	if ok == True:
		image_file = open(image_path, 'wb')
		image_file.write(result.read())
		image_file.close()
		print("Done "+ image_path+ "\n")
		#log_file.write("Done "+ image_path+ "\n")
	#log_file.close()
	

def download_photos(idx, image_folder):
	
	id = str(int(annonces.loc[idx, 'postId']))
	print("Downloading "+ id+ "...\n")

		
	urls = annonces.loc[idx, 'photos']
		
	pool = mp.Pool(processes=4)
	for url in urls:
		pool.apply_async(download, [idx, url, image_folder, id])
		
	pool.close()	
	pool.join()
	
	
	print("**********************************************\n")
	annonces.loc[idx, 'flag'] = 1
		
	count = annonces['flag'].sum()
	if (count % 490) == 0:
		percentage = count/490
		print("\n")
		print("*****************************************************")
		print(percentage, "% annonces are treated. " )
		print("*****************************************************")
		print("\n")
	
	
		
if __name__ == '__main__':
	
	start = timeit.default_timer()
	#filename = os.path.join(home, 'code/multiprocess_log.txt')
	image_folder = os.path.join(home, 'data/store/')
	if not os.path.exists(image_folder):
		os.makedirs(image_folder)
		
	print('length: ', len(indexlist))
	#p = mp.Pool(process_number)
	for idx in indexlist:
		download_photos(idx, image_folder)
		
	print(annonces[annonces['exist']=='False'].head())
	print(len(annonces[annonces['exist']=='False']))
	annonces.to_json(os.path.join(home, 'data/photos_done.json'))

	stop = timeit.default_timer()
	print("Execution time: ", (stop-start))
