#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
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


sys.modules[__name__] = _const()

# benchmark namespace
mbw = sys.modules[__name__].mbw = 'mbw'
bandwidth = sys.modules[__name__].bandwidth = 'bandwidth'
iperf3 = sys.modules[__name__].iperf3 = 'iperf3'
bonnie = sys.modules[__name__].bonnie = 'bonnie'
stress_ng = sys.modules[__name__].stress_ng = 'stress_ng'
sysbench = sys.modules[__name__].sysbench = 'sysbench'
cachebench = sys.modules[__name__].cachebench = 'cachebench'
cachebenchw = sys.modules[__name__].cachebenchw = 'cachebenchw'
cachebenchb = sys.modules[__name__].cachebenchb = 'cachebenchb'
stream = sys.modules[__name__].stream = 'stream'
pmbench = sys.modules[__name__].pmbench = 'pmbench'
pmbenchw = sys.modules[__name__].pmbenchw = 'pmbenchw'
pmbenchw50 = sys.modules[__name__].pmbenchw50 = 'pmbenchw50'
pmbenchw20r80 = sys.modules[__name__].pmbenchw20r80 = 'pmbenchw20r80'
y_cruncher = sys.modules[__name__].y_cruncher = 'y_cruncher'
y_cruncherc3 = sys.modules[__name__].y_cruncherc3 = 'y_cruncherc3'
y_cruncherc4 = sys.modules[__name__].y_cruncherc4 = 'y_cruncherc4'
y_cruncherz1d = sys.modules[__name__].y_cruncherz1d = 'y_cruncherz1d'
y_cruncherm5d = sys.modules[__name__].y_cruncherm5d = 'y_cruncherm5d'
pgbench = sys.modules[__name__].pgbench = 'pgbench'
sysbench_ram = sys.modules[__name__].sysbench_ram = 'sysbench_ram'
# Zening's change ZZZ
sklearn = sys.modules[__name__].sklearn = 'sklearn'
apache_siege = sys.modules[__name__].apache_siege = 'apache_siege'
compilebench = sys.modules[__name__].compilebench = 'compilebench'


dic = sys.modules[__name__].command = dict()

# running options of y_cruncher # 7.379s on c4.large
# the 3rd position decide the number of digits 1 - 25m, 2 - 50m, 3 - 100m, 4 - 250m, 7 - 2.5b
dic[y_cruncher] = '/home/ubuntu/CPU_test/y-cruncher\ v0.7.5.9480-static/y-cruncher <<'
dic[y_cruncherc3] = '/home/ubuntu/CPU_test/y-cruncher\ v0.7.5.9480-static/y-cruncher <<'
dic[y_cruncherc4] = '/home/ubuntu/CPU_test/y-cruncher\ v0.7.5.9480-static/y-cruncher <<'
dic[y_cruncherz1d] = '/home/ubuntu/CPU_test/y-cruncher\ v0.7.5.9480-static/y-cruncher <<'
dic[y_cruncherm5d] = '/home/ubuntu/CPU_test/y-cruncher\ v0.7.5.9480-static/y-cruncher <<'
#
# FIX ME FIX ME ----------- !
# Had to add an extra '0\n' to get to work on z1d - IS THIS REQUIRED for c3/c4 ????
#
y_cruncher_option = sys.modules[__name__].y_cruncher_option = 'EOF\n0\n0\n1\n1\nEOF\n'
y_cruncherc3_option = sys.modules[__name__].y_cruncherc3_option = 'EOF\n0\n1\n1\nEOF\n'
y_cruncherc4_option = sys.modules[__name__].y_cruncherc4_option = 'EOF\n0\n1\n1\nEOF\n'
y_cruncherz1d_option = sys.modules[__name__].y_cruncherz1d_option = 'EOF\n0\n0\n1\n1\nEOF\n'
#y_cruncherz1d_option = sys.modules[__name__].y_cruncherm5d_option = 'EOF\n0\n0\n1\n1\nEOF\n'
y_cruncherm5d_option = sys.modules[__name__].y_cruncherm5d_option = 'EOF\n0\n0\n1\n1\nEOF\n'
#y_cruncher_option = sys.modules[__name__].y_cruncher_option = 'EOF\n0\n1\n1\nEOF\n'
# running options of pgbench # need 61s on c4.large
dic[pgbench] = 'pgbench'
pgbench_option = sys.modules[__name__].pgbench_option = ' --client=10 --jobs=10 --time=60  ubuntu'
# running options of sysbench # 8.480s on c4.large
# sysbench do not need <cycle> option, already has built-in mechanism to calculate avg
dic[sysbench] = 'sysbench'
sysbench_option = sys.modules[__name__].sysbench_option = ' --test=cpu --cpu-max-prime=2000000 --num-threads=2 --max-requests=10 run'
# sysbench --test=memory --memory-block-size=1K --num-threads=2 --memory-total-size=10G run
dic[sysbench_ram] = 'sysbench'
sysbench_ram_option = sys.modules[__name__].sysbench_ram_option = ' --num-threads=2 --test=memory --memory-block-size=1M --memory-total-size=100G run'
# stress-ng --malloc 100 --malloc-ops 100000 --malloc-bytes 40000000 --fault 10 --fault-ops 100
dic[stress_ng] = 'stress-ng'
stress_ng_option = sys.modules[__name__].stress_ng_option = ' stress-ng --malloc 1000 --malloc-ops 100000 --malloc-bytes 40000000 --fault 1024 --fault-ops 500000'
dic[cachebench] = './cachebench'
dic[cachebenchw] = './cachebench'
dic[cachebenchb] = './cachebench'
cachebench_option = sys.modules[__name__].cachebench_option = ' -r -m32 -e1 -x0 -d2'
cachebenchw_option = sys.modules[__name__].cachebenchw_option = ' -w -m32 -e1 -x0 -d2'
cachebenchb_option = sys.modules[__name__].cachebenchb_option = ' -b -m32 -e1 -x0 -d2'
#stream_option = sys.modules[__name__].stream_option = ' -o -DSTREAM_ARRAY_SIZE=100000000 -fopenmp -mcmodel=medium stream.c -o stream | export OMP_NUM_THREADS=2 | time ./stream'
#stream_option = sys.modules[__name__].stream_option = ' -o -DSTREAM_ARRAY_SIZE=100000000 -fopenmp -mcmodel=medium stream.c -o stream | export OMP_NUM_THREADS=2 | for i in {1..10}; do time ./stream; done'
dic[stream] = 'time'
stream_option = sys.modules[__name__].stream_option = ' /home/ubuntu/SCRIPT/scripts/remote/stream_parser2_new.sh'
dic[pmbench] = 'time'
dic[pmbenchw] = 'time'
dic[pmbenchw50] = 'time'
dic[pmbenchw20r80] = 'time'
pmbench_option = sys.modules[__name__].pmbench_option = ' /home/ubuntu/SCRIPT/scripts/remote/pmbench.sh'
pmbenchw_option = sys.modules[__name__].pmbenchw_option = ' ./pmbenchw.sh'
pmbenchw50_option = sys.modules[__name__].pmbenchw50_option = ' ./pmbenchw50.sh'
pmbenchw20r80_option = sys.modules[__name__].pmbenchw20r80_option = ' /home/ubuntu/SCRIPT/scripts/remote/pmbenchw20r80.sh'

# Zening's change ZZZ
dic[sklearn] = 'time'
dic[apache_siege] = 'time'
dic[compilebench] = 'time'
sklearn_option = sys.modules[__name__].sklearn_option = ' /home/ubuntu/SCRIPT/scripts/remote/sklearn.sh'
apache_siege_option = sys.modules[__name__].apache_siege_option = ' /home/ubuntu/SCRIPT/scripts/remote/apache_siege.sh'
compilebench_option = sys.modules[__name__].compilebench_option = ' /home/ubuntu/SCRIPT/scripts/remote/compilebench.sh'

# 10.9424s on c4.large
# supported bench marks
# Zening's change ZZZ
sys.modules[__name__].supportedBenchmarks = dict([(y_cruncher, y_cruncher_option),
                                                  (y_cruncherc3,
                                                   y_cruncherc3_option),
                                                  (y_cruncherc4,
                                                   y_cruncherc4_option),
                                                  (y_cruncherz1d,
                                                   y_cruncherz1d_option),
                                                  (y_cruncherm5d,
                                                   y_cruncherm5d_option),
                                                  (pgbench, pgbench_option),
                                                  (sysbench, sysbench_option),
                                                  (sysbench_ram,
                                                   sysbench_ram_option),
                                                  (stress_ng, stress_ng_option),
                                                  (cachebench, cachebench_option),
                                                  (cachebenchw, cachebenchw_option),
                                                  (cachebenchb, cachebenchb_option),
                                                  (stream, stream_option),
                                                  (pmbench, pmbench_option),
                                                  (pmbenchw, pmbenchw_option),
                                                  (pmbenchw20r80,
                                                   pmbenchw20r80_option),
                                                  (pmbenchw50, pmbenchw50_option),
                                                  (sklearn, sklearn_option),
                                                  (apache_siege,
                                                   apache_siege_option),
                                                  (compilebench, compilebench_option)])
# dir
sys.modules[__name__].datadir = '/home/ubuntu/SCRIPT/scripts/remote/data/'
sys.modules[__name__].plugindir = '/home/ubuntu/SCRIPT/scripts/remote/plugin'
sys.modules[__name__].remotedir = '/home/ubuntu/SCRIPT/scripts/remote/'
sys.modules[__name__].logdir = '/home/ubuntu/SCRIPT/logs/'
# Flags
sys.modules[__name__].plugins = False  # enable call rudata
# sys.modules[__name__].pginit = True   #move pgsql to local disk mnt point
