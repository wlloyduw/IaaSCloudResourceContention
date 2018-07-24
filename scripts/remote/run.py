#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import const
import getopt
from experiment import Experiment
#use ‘<<’ and delimiter play with interactive benchmark
#Experiment(benchmark,cycle,options,experimentID):
def main(argv):
	options=dict([(const.y_cruncher,const.y_cruncher_option),(const.pgbench,const.pgbench_option)])
	ID='0'
	cycle='10'
	benchmark=const.pgbench
	try:
		opts, args = getopt.getopt(argv,"hc:i:t:")
	except getopt.GetoptError:
		print('run.py -c <num of cycles> -i <exp_id> -t <exp_type>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('test.py -c <how many cycles per experiment run>\n\
			 -i <ID should be unique by each time we run.py but shared amoung all instances>')
			sys.exit()
		elif opt in ("-i"):
			ID = arg
		elif opt in ("-c"):
			cycle = arg
		elif opt in ("-t"):
			if arg in options.keys():
				benchmark=arg
	#do experiment HERE!!!
	# e1=Experiment(const.y_cruncher,cycle,options,ID)
	# e1.run()

	e2=Experiment(benchmark,cycle,options,ID)
	e2.run();
	#clean up
	if benchmark in (const.y_cruncher):
		os.system('rm Pi*')

if __name__ == "__main__":
	main(sys.argv[1:])