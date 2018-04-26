#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import const
import getopt
from experiment import Experiment
#use ‘<<’ and delimiter play with interactive benchmark
#Experiment(benchmark,cycle,parameter,experimentID):
def main(argv):
	parameter=dict([(const.y_cruncher,'EOF\n0\n1\n1\nEOF\n'),(const.sysbench,'')])
	ID='0'
	cycle='10'
	try:
		opts, args = getopt.getopt(argv,"hc:i:")
	except getopt.GetoptError:
		print('run.py -c <num of cycles> -i <exp_id>')
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


	e1=Experiment(const.y_cruncher,cycle,parameter,ID)
	e1.run()
	e2=Experiment(const.y_cruncher,cycle,parameter,ID)
	e3=None
	e4=None

if __name__ == "__main__":
	main(sys.argv[1:])