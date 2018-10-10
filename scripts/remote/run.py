#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import const
import getopt
from experiment import Experiment
# use ‘<<’ and delimiter play with interactive benchmark
# Experiment(benchmark,cycle,supportedBenchmarks,experimentID):


def main(argv):

    ID = '0'
    cycle = '10'
    benchmark = const.sysbench
    try:
        opts, args = getopt.getopt(argv, "hc:i:t:")
    except getopt.GetoptError:
        print('run.py -c <num of cycles> -i <exp_id> -t <exp_type>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -c <how many cycles per experiment run>\n\
			 -i <ID should be unique by each time we run.py but shared amoung all instances>\n\
			 -t benchmark')
            sys.exit()
        elif opt in ("-i"):
            ID = arg
        elif opt in ("-c"):
            cycle = arg
        elif opt in ("-t"):
            if arg in const.supportedBenchmarks.keys():
                benchmark = arg
    # do experiment HERE!!!
    # e1=Experiment(const.y_cruncher,cycle,supportedBenchmarks,ID)
    # e1.run()

    e2 = Experiment(benchmark, cycle, const.supportedBenchmarks, ID)

    if const.plugins is True:
        # On
        os.system(const.plugindir+'/rudata/rudataall.sh > rudata_all_1.json')
        print("running " + benchmark)
        e2.run()
        os.system(const.plugindir+'/rudata/rudataall.sh > rudata_all_2.json')
    else:
        # Off
        e2.run()

    # clean up
    if benchmark in (const.y_cruncher):
        os.system('rm Pi*')


if __name__ == "__main__":
    main(sys.argv[1:])
