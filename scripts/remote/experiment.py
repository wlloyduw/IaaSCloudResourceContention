#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'run.py a experiment.py  with parameter'

import re
import csv
import const
import parsing
import os
class Experiment(object):
	__slots__ = ('benchmark', 'cycle','parameter',\
		'run')
	def __init__(self, benchmark,cycle,*args,**kw):
		self.benchmark = benchmark
		self.cycle=int(cycle)
		self.parameter=kw;
		self.command=args[0]
	def run():
		for i in range(cycle):
			#result=os.popen('~/CPU_test/y-cruncher\ v0.7.5.9480-static/y-cruncher <  y.txt ').read()
			parsing.func(benchmark,os.popen(command))
		pass
		