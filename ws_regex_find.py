import os
import sys
import re
import time

sys.path.append(os.environ['PYDFHOME'])
from pyDF import *

report = []
files = []

def find_word(args):
	# feed_files = Source(file_list)
	# file_list = text_list(sys.argv[2])[:n_files]
	return args
	# fname = args[0]
	# name = fname.split('/')[-1]
	# with open(args[0], 'r') as f:
	# 	text = f.read()
	# 	matches = re.findall(args[1], text)
	# 	if len(matches) > 0:
	# 		files.append(args[0].split('/')[-1])
	# 	print('{} matches of {} in file {}'.format(len(matches), args[1], args[0].split('/')[-1]))
	# return len(matches)

def text_list(rootdir):
	fnames=[]
	
	for current, directories, files in os.walk(rootdir):
		for f in files:
			fnames.append(current + '/' + f)
			
	fnames.sort()
	
	return fnames

def find_word_without_worker(args):
	global files
	for i in range (1, len(args)):
		with open(args[i], 'r') as f:
			text = f.read()
			matches = re.findall(sys.argv[1], text)
			if len(matches) > 0:
				files.append(args[0].split('/')[-1])
		print('{} matches of {} in file {}'.format(len(matches), sys.argv[1], args[0].split('/')[-1]))

n_workers = int(sys.argv[1])
graph = DFGraph()
sched = SchedulerWS(graph, n_workers, mpi_enabled = False)
req_node, resp_node = sched.set_wservice(('localhost', 8000))

find_word_in_files = FilterTagged(find_word, 2)

graph.add(req_node)
graph.add(find_word_in_files)
graph.add(resp_node)

req_node.add_edge(find_word_in_files, 0)
find_word_in_files.add_edge(resp_node, 0)

start_time = time.time()
sched.start()
end_time = time.time()

# report.append({"num_workers": n_workers,
# "execution_time": end_time - start_time,
# "num_files_searched": n_files,
# "searched_string": sys.argv[1],
# "with_sucuri": True})

# file_list = text_list(sys.argv[2])
# start_time = time.time()
# find_word_without_worker(file_list)
# end_time = time.time()
# report.append({"num_workers": 0, "execution_time": end_time - start_time, "num_files_searched": 10, "searched_string": sys.argv[1], "with_sucuri": False})
# pd.DataFrame(report).to_csv('report.csv', index=False)
