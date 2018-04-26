#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
result=os.popen('~/CPU_test/y-cruncher\ v0.7.5.9480-static/y-cruncher <  y.txt ').read()
with open('./out','a') as f:
	f.write(result)
