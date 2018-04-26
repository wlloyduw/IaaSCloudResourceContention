#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import const
from experiment import Experiment
#use ‘<<’ and delimiter play with interactive benchmark
parameter=dict([(const.y_cruncher,'EOF\n0\n1\n1\nEOF\n'),(const.sysbench,'')])
e1=Experiment(const.y_cruncher,10,parameter)
e1.run()
e2=None
e3=None
e4=None

