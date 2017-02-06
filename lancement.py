import _thread 
from reveil import *
from time import *
def boucleReveil():
	r = Reveil()
	print("Boucle Reveil")
	r.boucleInfinie()

_thread.start_new_thread(boucleReveil,())
while True:
	pass