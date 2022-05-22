import xmlrpc.client
import sys
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

print("Test client for WebService functionality")
response = proxy.service(['happy', '/mnt/c/Users/ric10/Desktop/Profissional/git/sistemas-distribuidos/files'])

print(response)