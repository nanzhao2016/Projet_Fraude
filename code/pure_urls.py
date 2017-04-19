import pandas, numpy
import math
import matplotlib.pyplot as plt
import os, timeit
import scipy.ndimage
import urllib
import urllib.request
import socket
import multiprocessing as mp
import logging

timeout = 10
socket.setdefaulttimeout(timeout)
home = 'C:/Users/OPEN/Documents/NanZHAO/Projet CIR Fraude/'
process_number = 10
logging.basicConfig(filename = os.path.join(home, 'code/downloading.log'), level = logging.INFO)

annonces = pandas.read_json(os.path.join(home, 'data/urls.json'))
annonces['exist'] = 'True'
annonces['flag'] = 0




indexlist = annonces.sort_values('postId', ascending=False).index.tolist()


def download(idx, image_folder):
	id = str(int(annonces.loc[idx, 'postId']))
	url = annonces.loc[idx, 'urls']
	#flag = annonces.loc[idx, 'flag']
	
	ok = True	
	#log_file = open(filename, "a")
	res = (idx, True)
	#print("entre: ", res)
	image_path = os.path.join(image_folder, id+'_'+url.split('images.craigslist.org/')[1]) 
	
	if os.path.isfile(image_path):
		#print("Skipping existing file :" + image_path + "\n")
		#log_file.write("Skipping existing file :" + image_path + "\n")
		logging.info("Skipping existing file :" + image_path + "\n")
		annonces.loc[idx, 'flag'] = 1
		count = annonces['flag'].sum()
		#print(count)
		if (count % 2090) == 0:
			percentage = process_number*count/2090
			print("\n")
			print("*****************************************************")
			print(percentage, "% annonces are treated. " )
			print("*****************************************************")
			print("\n")
			logging.info(str(percentage) + "% annonces are treated. " )
		return(res)
	
	try:
		result = urllib.request.urlopen(url)
	except urllib.error.HTTPError as err:
		#print("Type error: "+ str(err.code)+ "\n")
		#print("photo "+ url+ " does not exist.\n")
		logging.info("Type error: "+ str(err.code)+ "\n")
		logging.info("photo "+ url+ " does not exist.\n")
		#annonces.loc[idx, 'exist'] = annonces.loc[idx, 'exist'].replace('True', 'False')
		#annonces_deleted = annonces_deleted.append(annonces.loc[idx])
		#annonces_deleted.append(idx)
		res = (idx, False)
		ok = False
	
	#print(ok)
	#log_file.write(ok)

	#if ok == False:
		#print("Annonce "+ id+ " does not exist.\n")
		#log_file.write("Annonce "+ id+ " does not exist.\n")
		#annonces.loc[idx, 'exist'] = annonces.loc[idx, 'exist'].replace('True', 'False')
	
	if ok == True:
		image_file = open(image_path, 'wb')
		image_file.write(result.read())
		image_file.close()
		#print("Done "+ image_path+ "\n")
		logging.info("Done "+ image_path)
		
	annonces.loc[idx, 'flag'] = 1
	count = annonces['flag'].sum()
	#print(count)
	if (count % 2090) == 0:
		percentage = process_number*count/2090
		print("\n")
		print("*****************************************************")
		print(percentage, "% annonces are treated. " )
		print("*****************************************************")
		print("\n")
		logging.info(str(percentage) + "% annonces are treated. " )
	
	
	#print('fin:', res)
	return(res)



if __name__== "__main__":
	start = timeit.default_timer()
	image_folder = os.path.join(home, 'data/store/')
	urls_list= []
	#annonces_deleted = pandas.DataFrame(columns=annonces.columns)
	if not os.path.exists(image_folder):
		os.makedirs(image_folder)
	
	#print(len(indexlist))
	#q = Queue()
	
	p = mp.Pool(process_number)
	#filename ='C:/Users/OPEN/Documents/NanZHAO/Projet CIR Fraude/code/test_log.txt'
	for idx in indexlist:
	#for idx in range(101):
		res = p.apply_async(download, (idx, image_folder))
		urls_list.append(res.get(timeout=10))
		 #p.map_async(write, [q, filename])
			
	p.close()
	p.join()
	stop = timeit.default_timer()
	print("Execution time: ", (stop-start))
	data = pandas.DataFrame(urls_list, columns= ('index', 'exist'))
	data = data[data['exist']==False]
	print(data.shape)
	
	annonces_deleted = pandas.DataFrame(columns=annonces.columns)
	for i in data['index']:
		annonces_deleted = annonces_deleted.append(annonces.loc[i])
	annonces_deleted.to_json(os.path.join(home, 'data/urls_empty.json'))
	
	#print(annonces_deleted.head())
	#print(len(annonces_deleted))
	#annonces_deleted.to_json(os.path.join(home, 'data/urls_empty.json'))
	
	"""
	number1 = len(annonces_deleted)
	print(number1)
	#print(annonces_deleted)
	print(annonces_deleted[0:3])
	thefile = open(os.path.join(home, 'code/list.txt'), 'w')
	for item in annonces_deleted:
		thefile.write("%s\n" % item)

	data = pandas.DataFrame(annonces_deleted, columns=('id', 'exist'))
	number2 = len(data[data['exist']==False])
	print(number2)
	if number2 > 0 :
		data.to_json(os.path.join(home, 'data/urls_empty.json'))
	"""
	

