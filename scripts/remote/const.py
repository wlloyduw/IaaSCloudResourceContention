#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a module contains constants that may use in script'

__author__ = 'E&D'

class _const:
	class ConstError(TypeError):
		pass

	def __setattr__(self, name, value):
		if name in self.__dict__:
			raise self.ConstError("Can't rebind const instance attribute (%s)" % name)
		self.__dict__[name] = value
	def __delattr__(self, name):
		if name in self.__dict__:
			raise self.ConstError("Can't unbind const instance attribute (%s)"%name)
		raise AttributeError("const instance has no attribute '%s'"%name)

import sys
sys.modules[__name__] = _const()


mbw=sys.modules[__name__].mbw='mbw'
bandwidth=sys.modules[__name__].bandwidth='bandwidth'
iperf3=sys.modules[__name__].iperf3='iperf3'
bonnie=sys.modules[__name__].bonnie='bonnie'
stress_ng=sys.modules[__name__].stress_ng='stress_ng'
sysbench=sys.modules[__name__].sysbench='sysbench'
y_cruncher=sys.modules[__name__].y_cruncher='y_cruncher'

dic=sys.modules[__name__].command=dict()
dic[y_cruncher]='~/CPU_test/y-cruncher\ v0.7.5.9480-static/y-cruncher <<'
