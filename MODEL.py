#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque

class MODEL( object ):
	def __init__(self):
		super().__init__()

		# Diccionario, con los datos para definir la escena.
		self.__scene = deque()

	# GETTER.
	def getSceneStorage(self):
		return self.__simpleCompStorage

	# SETTER.
	def setSceneStorage(self,newVal):
		self.__simpleCompStorage = newVal

	# ALTA.
	def newComponent(self,component):
		self.__scene.append(component)

	# BAJA.
	def delComponent(self,component):
		self.__scene.remove(component)

	# MODIFICACION.
	def modComponent(self,compId,updateData):
		self.__scene.get(compId).update(updateData)

	# CONSULTA.
	def getComponent(self,compId):
		for elem in self.__simpleCompStorage:
			if elem.getID() == scID:
				return elem
