import multiprocessing as mp
import random
import string
import os, pandas, timeit


random.seed(123)
path = 'C:/Users/OPEN/Documents/NanZHAO/Projet CIR Fraude/code/photos.json'

data = pandas.read_json(path)
output = mp.Queue()
data['flag'] = 0
indexlist = data.sort_values('postId').index.tolist()

def get_information(idx, filename):
	#l.acquire()
	#file = open(filename, "w")
	
	#print("postId: "+ str(data.loc[idx, 'postId']))

	file = open(filename, "a")
	file.write("postId: "+ str(data.loc[idx, 'postId']) + "\n")
	file.write("postId: "+ data.loc[idx, 'photos'][0] + "\n")
	#q.put("postId: "+ str(data.loc[idx, 'postId']) + " " +mp.current_process())
	#file.write("postId: "+ str(data.loc[idx, 'postId']) + " " +mp.current_process())
	data.loc[idx, 'flag'] = 1
	count = data['flag'].sum() 
	if (count % 490) == 0 :
		percentage = 4* count/490
		print("\n")
		print("*****************************************************")
		print(percentage, "% annonces are treated. " )
		print("*****************************************************")
		print("\n")
		"""
		q.put("\n")
		q.put("*****************************************************\n")
		q.put(percentage + "% annonces are treated. \n" )
		q.put("*****************************************************\n")
		q.put("\n")
		"""
	file.close()
	#l.release()

def write(q, filename):
	f = open(filename, 'a')
	while True:
		try:
			line = q.get(block = False)
			f.write(line)
		except:
			break
	f.close()
	
def rand_string(length, output, l):
	l.acquire()
	rand_str = ''.join(random.choice(string.ascii_lowercase+ 
	string.ascii_uppercase + 
	string.digits) for i in range(length))                              
	output.put(rand_str)
	l.release()
    
	

if __name__== "__main__":
	start = timeit.default_timer()
	lock = mp.Lock()
	"""
	#processes = [mp.Process(target=rand_string, args=(5, output, lock)) for x in range(4)]
	processes = [mp.Process(target=get_information, args=(5, output, lock)) for x in range(4)]

	for p in processes:
		p.start()
    
	for p in processes:
		p.join()
    
	results = [output.get() for p in processes]
	print(results)
	"""
	
	print(len(indexlist))
	#q =mp.Queue()
	p = mp.Pool(4)
	filename ='C:/Users/OPEN/Documents/NanZHAO/Projet CIR Fraude/code/test_log.txt'
	for idx in indexlist:
		p.apply_async(get_information, [idx, filename])
		 #p.map_async(write, [q, filename])
			
	p.close()
	p.join()
	stop = timeit.default_timer()
	print("Execution time: ", (stop-start))
