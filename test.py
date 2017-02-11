import _thread

class Test:
	def test(self,nb):
		print(nb)
		module = __import__("outils",fromlist=[None])  # I don't understant that fromlist
		chaine = "<a> aa </a> <a>bb</a>"
		liste = [chaine,"a"]
		#method = getattr(module, "Outils.test")
		eval("module.Outils.test()")
		module.Outils.test()
		#print(method)a


a = Test()
_thread.start_new_thread(a.test,(8,))
try :
	a.test(5)
except:
	print("Erreur")