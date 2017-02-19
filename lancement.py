import _thread 
from threading import Thread
from reveil import *
from time import *
from arduino import *

"""def boucleReveil():
	r = Reveil()
	print("Boucle Reveil")
	r.boucleInfinie()"""

#a = _thread.start_new_thread(boucleReveil,())

class ThreadReveil(Thread):
	def run(self):
		r = Reveil()
		r.boucleInfinie()

class ThreadArduino(Thread):
	def run(self):
		a = Arduino()
		a.serveur()

a = ThreadReveil()
b = ThreadArduino()

a.start()
b.start ()

a.join()
b.join()



