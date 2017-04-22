#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# import sys, inspect, traceback

# from collections import deque


# class EHist( object ):
# 	def __init__(self):
# 		super().__init__()

# 		# Doble cola para el historial de Deshacer. LIFO = (append y pop)
# 		self.__undo = deque()

# 		# Doble cola para el historial de Rehacer.  FIFO = (append y pop left)
# 		self.__redo = deque()


# 	# Agrega una funcion a la
# 	def addToUndo(self,funcStr):


# 	def getUndo(self):
# 		func = self.__undo.pop()
# 		exec(func)


# 	def history(f):
# 		def wrap(*args):
# 			funcStr = f.__name__+'('

# 			if args is not None:
# 				for arg in args:
# 					if type(arg) == str:
# 						funcStr += '\''+str(arg)+'\','
# 					else:
# 						funcStr += str(arg)+','
# 				return funcStr[:-1]+')'

# 			else:
# 				return funcStr[:-1]+')'

# 		addToUndo(wrap)



import inspect
import traceback

def funcParser(funcName,*args):
	funcStr = funcName+'('
	if args is not None:
		for arg in args:
			if type(arg) == str:
				funcStr += '\''+str(arg)+'\','
			else:
				funcStr += str(arg)+','
		return funcStr[:-1]+')'
	else:
		return funcStr[:-1]+')'

def n():
    return traceback.extract_stack(None, 2)[0][2]

def a():
    frame = inspect.currentframe().f_back
    args, _, _, values = inspect.getargvalues(frame)
    return ([(values[i]) for i in args])


def h():
    F = traceback.extract_stack(None, 2)[0][2]

    frame = inspect.currentframe().f_back
    args, _, _, values = inspect.getargvalues(frame)
    A = ([(values[i]) for i in args])

    print( F, A )



def patata(*args):
	print(*args)
	print(n())
	# print(a())
	# F, A = h()
	fStr = funcParser(n(),*args)
	print(fStr)



if __name__ == '__main__':
	patata('hola','adios')
