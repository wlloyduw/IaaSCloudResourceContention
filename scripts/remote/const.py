#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a module contains constants that may use in script'

__author__ = 'E&D'


class _const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError(
                "Can't rebind const instance attribute (%s)" % name)
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ConstError(
                "Can't unbind const instance attribute (%s)" % name)
        raise AttributeError("const instance has no attribute '%s'" % name)


import sys
sys.modules[__name__] = _const()

# benchmark namespace
mbw = sys.modules[__name__].mbw = 'mbw'
bandwidth = sys.modules[__name__].bandwidth = 'bandwidth'
iperf3 = sys.modules[__name__].iperf3 = 'iperf3'
bonnie = sys.modules[__name__].bonnie = 'bonnie'
stress_ng = sys.modules[__name__].stress_ng = 'stress_ng'
sysbench = sys.modules[__name__].sysbench = 'sysbench'
y_cruncher = sys.modules[__name__].y_cruncher = 'y_cruncher'
pgbench = sys.modules[__name__].pgbench = 'pgbench'
dic = sys.modules[__name__].command = dict()

# running options of y_cruncher # 7.379s on c4.large
# the 3rd position decide the number of digits 1 - 25m, 2 - 50m, 3 - 100m, 4 - 250m, 7 - 2.5b
dic[y_cruncher] = '/home/ubuntu/CPU_test/y-cruncher\ v0.7.5.9480-static/y-cruncher <<'
y_cruncher_option = sys.modules[__name__].y_cruncher_option = 'EOF\n0\n1\n1\nEOF\n'
# running options of pgbench # need 61s on c4.large
dic[pgbench] = 'pgbench'
pgbench_option = sys.modules[__name__].pgbench_option = ' --client=10 --jobs=10 --time=60  ubuntu'
# running options of sysbench # 8.480s on c4.large
# sysbench do not need <cycle> option, already has built-in mechanism to calculate avg
dic[sysbench] = 'sysbench'
sysbench_option = sys.modules[__name__].sysbench_option = ' --test=cpu --cpu-max-prime=2000000 --num-threads=2 --max-requests=10 run'

# supported bench marks
sys.modules[__name__].supportedBenchmarks = dict([(y_cruncher, y_cruncher_option),
                                                  (pgbench, pgbench_option),
                                                  (sysbench, sysbench_option)])

# dir
sys.modules[__name__].datadir = '/home/ubuntu/SCRIPT/scripts/remote/data/'
sys.modules[__name__].plugindir = '/home/ubuntu/SCRIPT/scripts/remote/plugin'
# Flags
sys.modules[__name__].plugins = False  # enable call rudata
# sys.modules[__name__].pginit = True   #move pgsql to local disk mnt point
