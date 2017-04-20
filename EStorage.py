#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque

class EModel( object ):
	def __init__(self):
		super().__init__()

		# Doble cola para Componentes Simples.
		self.__simpleCompStorage = deque()

		# Doble cola para Componentes Complejos.
		self.__complexCompStorage = deque()

		# Doble cola para el historial de Deshacer. LIFO = (append y pop)
		self.__undo = deque()

		# Doble cola para el historial de Rehacer.  FIFO = (append y pop left)
		self.__redo = deque()


	''' Acceso a las colecciones desde invocaciones externas '''

	def getSimpleCompStorage(self):
		return self.__simpleCompStorage

	def getComplexCompStorage(self):
		return self.__complexCompStorage

	def getUndoStorage(self):
		return self.__undo

	def getRedoStorage(self):
		return self.__redo


	''' Manejo de la coleccion del Historial de Acciones '''

	# ALTA.
	def regNewAction(self,funcStr):
		self.__undo.append(funcStr)
		self.__redo.clear()

	# CONSULTA y GESTION.
	def getPrevState(self):
		toUndo = self.__undo.pop()
		self.__redo.append(toUndo)


	# CONSULTA y GESTION.
	def getNextState(self):
		toRedo = self.__redo.popleft()
		self.__redo.append(toRedo)
		return toRedo



	''' Manejo de la coleccion de Componentes Simples '''

	# ALTA.
	def newSimpleComp(self,scItem):
		self.__simpleCompStorage.append(scItem)

	# BAJA.
	def delSimpleComp(self,scItem):
		self.__simpleCompStorage.remove(scItem)

	# CONSULTA.
	def getSimpleComp(self,scID):
		for elem in self.__simpleCompStorage:
			if elem.getID() == scID:
				return elem


	''' Manejo de la coleccion de Componentes Complejos '''

	# ALTA.
	def newSimpleComp(self,scItem):
		self.__simpleCompStorage.append(scItem)

	# BAJA.
	def delSimpleComp(self,scItem):
		self.__simpleCompStorage.remove(scItem)

	# CONSULTA.
	def getSimpleComp(self,scID):
		for elem in self.__simpleCompStorage:
			if elem.getID() == scID:
				return elem
