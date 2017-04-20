#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, inspect, traceback

from collections import deque


class EHist( object ):
	def __init__(self):
		super().__init__()

		# Doble cola para el historial de Deshacer. LIFO = (append y pop)
		self.__undo = deque()

		# Doble cola para el historial de Rehacer.  FIFO = (append y pop left)
		self.__redo = deque()


	# Agrega una funcion a la
	def addToUndo(self,funcStr):


	def getUndo(self):
		func = self.__undo.pop()
		exec(func)


	def history(f):
		def wrap(*args):
			funcStr = f.__name__+'('

			if args is not None:
				for arg in args:
					if type(arg) == str:
						funcStr += '\''+str(arg)+'\','
					else:
						funcStr += str(arg)+','
				return funcStr[:-1]+')'

			else:
				return funcStr[:-1]+')'

		addToUndo(wrap)


	@history
	def p(self, *args):
		print(*args)
