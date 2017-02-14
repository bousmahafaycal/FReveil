import _thread 
from threading import Thread
from reveil import *
from time import *
"""def boucleReveil():
	r = Reveil()
	print("Boucle Reveil")
	r.boucleInfinie()"""

#a = _thread.start_new_thread(boucleReveil,())

class ThreadReveil(Thread):
	def run(self):
		r = Reveil()
		r.boucleInfinie()

a = ThreadReveil()
a.start()
a.join()



