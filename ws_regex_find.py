from cgitb import text
import os
import sys
import re
import time

sys.path.append(os.environ['PYDFHOME'])
from pyDF import *

report = []
files = []
path = '/files'


def find_word(args):
    qtd = 0
    file_list = text_list()
    for i in range (len(file_list)):
        fname = file_list[i]
        print(args)
        name = fname.split('/')[-1]
        with open(fname, 'r') as f:
            text = f.read()
            matches = re.findall(args[0], text)
            if len(matches) > 0:
                files.append(fname.split('/')[-1])
            print('{} matches of {} in file {}'.format(len(matches), args[0], name))
        qtd = qtd + len(matches)
    return qtd

def text_list():
	fnames=[]
	root_path = os.getcwd() + path
	for current, directories, files in os.walk(root_path):
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
file_list = text_list()
#feed_files = SourceWS(file_list)
#file_list = text_list()
sched = SchedulerWS(graph, n_workers, mpi_enabled = False)
req_node, resp_node = sched.set_wservice(('localhost', 3030))

find_word_in_files = FilterTagged(find_word, 1)


#graph.add(feed_files)
graph.add(find_word_in_files)
graph.add(req_node)
graph.add(resp_node)

#feed_files.add_edge(find_word_in_files, 0)
#req_node.add_edge(feed_files, 0)
req_node.add_edge(find_word_in_files, 1)
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
