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


	''' Acceso a las colecciones desde invocaciones externas '''

	def getSimpleCompStorage(self):
		return self.__simpleCompStorage

	def getComplexCompStorage(self):
		return self.__complexCompStorage


	''' Manejo de la coleccion de Componentes Simples '''

	# ALTA
	def newSimpleComp(self,scItem):
		self.__simpleCompStorage.append(scItem)

	# BAJA
	def delSimpleComp(self,scItem):
		self.__simpleCompStorage.remove(scItem)

	# CONSULTA
	def getSimpleComp(self,scID):
		for elem in self.__simpleCompStorage:
			if elem.getID() == scID:
				return elem


	''' Manejo de la coleccion de Componentes Complejos '''

	# ALTA
	def newSimpleComp(self,scItem):
		self.__simpleCompStorage.append(scItem)

	# BAJA
	def delSimpleComp(self,scItem):
		self.__simpleCompStorage.remove(scItem)

	# CONSULTA
	def getSimpleComp(self,scID):
		for elem in self.__simpleCompStorage:
			if elem.getID() == scID:
				return elem
