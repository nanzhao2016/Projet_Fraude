from multiprocessing import Pool, TimeoutError
import time
import os

def f(x):
    return (x*x)
	
if __name__ == '__main__':
	pool = Pool(processes=4)
	for i in range(0,5):
		print(i)
		res = pool.apply_async(f, (i,))
		print ("result", res.get(timeout=10))