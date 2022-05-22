import time
import xmlrpc.client
import sys
proxy = xmlrpc.client.ServerProxy("http://localhost:3030/")

print("Test client for WebService functionality")
for i in range(1,2):
    start_time = time.time()
    response = proxy.service('hi')
    end_time = time.time()
    print(end_time - start_time)


