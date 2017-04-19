import pandas, numpy
import math
import matplotlib.pyplot as plt
import os
import scipy.ndimage
import urllib
import urllib.request
import socket

timeout = 10
socket.setdefaulttimeout(timeout)

home = 'C:/Users/OPEN/Documents/NanZHAO/Projet CIR Fraude/'

annonces_photos = pandas.read_json(os.path.join(home, 'data/photos.json'))
annonces_photos['exist'] = 'True'
#annonces_photos = annonces_photos.sort_values('exist')
log_file = open(os.path.join(home, 'code/log.txt'), 'w')


def download_images(annonces_photos, index, annonce, image_folder):
	id = str(int(annonce['postId']))
	#print ("Downloading %s ..." %id)
	log_file.write("Downloading "+ id+ "...\n")
	urls = annonce['photos']
	ok = True
	for url in urls:
		image_path = os.path.join(image_folder, id+'_'+url.split('images.craigslist.org/')[1]) 
		if os.path.isfile(image_path):
			#print ("Skipping existing file: " , image_path)
			log_file.write("Skipping existing file: " +image_path+ "\n")
			continue
		try:
			result = urllib.request.urlopen(url)
		except urllib.error.HTTPError as err:
			#print("Type error: ", err.code)
			#print("photo %s does not exist." %url)
			log_file.write("Type error: "+ str(err.code)+ "\n")
			log_file.write("photo "+ url+ " does not exist.\n")
			ok = False
		if ok==True:    
			file = open(image_path, 'wb')
			file.write(result.read())
			file.close()
			#print("Done %s" %image_path)
			log_file.write("Done "+ image_path+ "\n")
		if ok == False:
			#print("Annonce %s does not exist." %id)
			log_file.write("Annonce "+ id+ " does not exist.\n")
			annonces_photos.loc[index, 'exist'] = annonces_photos.loc[index, 'exist'].replace('True', 'False')
	#print("**********************************************")
	log_file.write("**********************************************")
	
	
def get_annonces_photos(df):
	image_folder = os.path.join(home, 'data/store/')
	if not os.path.exists(image_folder):
		os.makedirs(image_folder)
	count = 0
	for index, row in df.sort_values('postId').iterrows():
		count = count + 1
		if (count%490) == 0:
			percentage = count/490
			print("\n")
			print("*****************************************************")
			print(percentage, "% annonces are treated. " )
			print("*****************************************************")
			print("\n")
			log_file.write("\n")
			log_file.write("*****************************************************\n")
			log_file.write(str(percentage)+ "% annonces are treated. \n" )
			log_file.write("*****************************************************\n")
			log_file.write("\n")
		download_images(df, index, row, image_folder)
		
	return (df)
		
df = get_annonces_photos(annonces_photos)

print(df[df['exist']=='False'].head())
print(len(df[df['exist']=='False']))

df.to_json(os.path.join(home, 'data/photos_done.json'))
log_file.close()
