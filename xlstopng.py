import csv
import os
import re
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

sys.path.append(os.environ['PYDFHOME'])

from pyDF import *

save_diretorio = 'pdfs'



#ler arquivo xls: read_excel()



def xls2image(args):
	fname = args[0]
	name = fname.split('/')[-1]
	df = pd.read_excel(args[0])
	fig, ax =plt.subplots(figsize=(12,4))
	ax.axis('tight')
	ax.axis('off')
	the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
	name = save_diretorio + '/' + name.split('.')[0] + '.pdf'
	pp = PdfPages(name)
	pp.savefig(fig, bbox_inches='tight')
	pp.close()
	return name

def xls_list(rootdir):
	fnames=[]
	
	for current, directories, files in os.walk(rootdir):
		for f in files:
			fnames.append(current + '/' + f)
			
	fnames.sort()
	
	return fnames
	
def print_name(args):
	fname = args[0]
	
	return "Converted "+ fname
	

nprocs = int(sys.argv[1])
file_list = xls_list(sys.argv[2])[:1000]

graph = DFGraph()
sched = Scheduler(graph, nprocs, mpi_enabled = False)

feed_files = Source(file_list)
convert_file = FilterTagged(xls2image,1)
pname = Serializer(print_name, 1)

graph.add(feed_files)
graph.add(convert_file)
graph.add(pname)

feed_files.add_edge(convert_file, 0)
convert_file.add_edge(pname, 0)

sched.start()

