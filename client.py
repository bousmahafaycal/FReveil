#!/usr/bin/env python
# coding: utf-8

import socket

hote = ""
port = 12800

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
soc.connect((hote, port))

clients_input = input("What you want to proceed my dear client?\n")  
soc.send(clients_input.encode("utf8")) # we must encode the string to bytes  
result_bytes = soc.recv(4096) # the number means how the response can be in bytes  
result_string = result_bytes.decode("utf8") # the return will be in bytes, so decode

print("Result from server is {}".format(result_string))  
input("");
print("socket ferme")
soc.close();
