#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import queue

	# Pila para el historial de Deshacer.
	self.__undo = queue.LifoQueue()

	# Pila para el historial de Rehacer.
	self.__redo = queue.LifoQueue()

	# ALTA.
	def saveStateFromUndo(self,state):
		if self.__undo:
			self.__redo.put(state)

	def saveStateFromRedo(self,state):
		if self.__redo:
			self.__undo.put(state)

	def saveState(self,state):
		self.__undo.put(state)
		self.__redo.clear()

	# CONSULTA y GESTION.
	def getPrevState(self):
		if self.__undo:
			toUndo = self.__undo.get()
			return toUndo

	# CONSULTA y GESTION.
	def getNextState(self):
		if self.__redo:
			toRedo = self.__redo.get()
			return toRedo



	# ----------------------------------------------------------------------- #
	#					 		 	- LOGICA HISTORIAL - 				   	  #
	# ----------------------------------------------------------------------- #


	''' Guarda el estado anterior, para permitr el 'Ctrl+Z' '''

	def saveState():
		state = getCurState(self._view)
		self._model.saveState(state)

	def saveStateFromUndo():
		state = getCurState(self._view)
		self._model.saveStateFromUndo(state)

	def saveStateFromRedo():
		state = getCurState(self._view)
		self._model.saveStateFromRedo(state)

	def getCurState(self._view):

		# Creamos una copia de las escena actual.
		scene = []

		# Creamos una copia de la cola de componentes simples actual.
		simpleStorage = []
		for item in self._model.getSimpleCompStorage():
			scItem = copy(item)
			scene.append(scItem)
			simpleStorage.append(scItem)

		# Creamos una copia de la cola de componentes complejos actual.
		complexStorage = []
		for item in self._model.getComplexCompStorage():
			ccItem = copy(item)
			scene.append(ccItem)
			complexStorage.append(ccItem)

		# Volteamos el array para respetar el orden de la pila.
		scene.reverse()

		# Devolvemos dichas copias en forma de tupla.
		return (scene,deque(simpleStorage),deque(complexStorage))


	''' Recupera el anterior estado en el historico de Deshacer. '''

	def getPrevState(self._view):

		saveStateFromUndo(self._view)

		# Recuperamos la tupla del estado anterior.
		toUndo = self._model.getPrevState()

		if toUndo is not None:
			# Asignamos lo que representa cada elemento.
			prevScene 			= toUndo[0]
			prevSimpleStorage 	= toUndo[1]
			prevComplexStorage 	= toUndo[2]

			# Recuperamos el estado de la escena.
			self._view.centralWidget().scene().clear()
			for item in prevScene:
				print(item)
				print(prevSimpleStorage)
				self._view.centralWidget().scene().addItem(item)
			# Recuperamos el estado de la cola de componentes simples.
			self._model.setSimpleCompStorage(prevSimpleStorage)
			# Recuperamos el estado de la cola de componentes complejos.
			self._model.setComplexCompStorage(prevComplexStorage)

			# Actualizamos la informacion mostrada en el Arbol.
			updateTrees(self._view)


	''' Recupera el siguiente estado en el historico de Rehacer. '''

	def getNextState(self._view):

		saveStateFromRedo(self._view)

		# Recuperamos la tupla del estado anterior.
		toRedo = self._model.getNextState()

		if toRedo is not None:
			# Asignamos lo que representa cada elemento.
			nextScene 			= toRedo[0]
			nextSimpleStorage 	= toRedo[1]
			nextComplexStorage 	= toRedo[2]

			# Recuperamos el estado de la escena.
			self._view.centralWidget().scene().clear()
			for item in nextScene:
				print(item)
				print(nextSimpleStorage)
				self._view.centralWidget().scene().addItem(item)
			# Recuperamos el estado de la cola de componentes simples.
			self._model.setSimpleCompStorage(nextSimpleStorage)
			# Recuperamos el estado de la cola de componentes complejos.
			self._model.setComplexCompStorage(nextComplexStorage)

			# Actualizamos la informacion mostrada en el Arbol.
			updateTrees(self._view)
