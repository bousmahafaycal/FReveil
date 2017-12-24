import _thread 
from threading import Thread
from reveil import *
from time import *
from arduino import *
from config import *
from serveur import *

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

class ThreadServeur(Thread):
	def run(self):
		a = Serveur()
		a.boucleInfinie()

conf =  Config()
conf.cleanUpAudio()

a = ThreadReveil()
b = ThreadArduino()
c = ThreadServeur()

a.start()
b.start ()
c.start()

a.join()
b.join()
c.join()



