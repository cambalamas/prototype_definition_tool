#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import queue

# Pila para el historial de Deshacer.
__undo = queue.LifoQueue()

# Pila para el historial de Rehacer.
__redo = queue.LifoQueue()

# ALTA.
def saveStateFromUndo(self,state):
	if __undo:
		__redo.put(state)

def saveStateFromRedo(self,state):
	if __redo:
		__undo.put(state)

def saveState(self,state):
	__undo.put(state)
	__redo.clear()

# CONSULTA y GESTION.
def getPrevState(self):
	if __undo:
		toUndo = __undo.get()
		return toUndo

# CONSULTA y GESTION.
def getNextState(self):
	if __redo:
		toRedo = __redo.get()
		return toRedo



# ----------------------------------------------------------------------- #
#					 		 	- LOGICA HISTORIAL - 				   	  #
# ----------------------------------------------------------------------- #


''' Guarda el estado anterior, para permitr el 'Ctrl+Z' '''

def saveState():
	state = getCurState(__V)
	__M.saveState(state)

def saveStateFromUndo():
	state = getCurState(__V)
	__M.saveStateFromUndo(state)

def saveStateFromRedo():
	state = getCurState(__V)
	__M.saveStateFromRedo(state)

def getCurState(__V):

	# Creamos una copia de las escena actual.
	scene = []

	# Creamos una copia de la cola de componentes simples actual.
	simpleStorage = []
	for item in __M.getSimpleCompStorage():
		scItem = copy(item)
		scene.append(scItem)
		simpleStorage.append(scItem)

	# Creamos una copia de la cola de componentes complejos actual.
	complexStorage = []
	for item in __M.getComplexCompStorage():
		ccItem = copy(item)
		scene.append(ccItem)
		complexStorage.append(ccItem)

	# Volteamos el array para respetar el orden de la pila.
	scene.reverse()

	# Devolvemos dichas copias en forma de tupla.
	return (scene,deque(simpleStorage),deque(complexStorage))


''' Recupera el anterior estado en el historico de Deshacer. '''

def getPrevState(__V):

	saveStateFromUndo(__V)

	# Recuperamos la tupla del estado anterior.
	toUndo = __M.getPrevState()

	if toUndo is not None:
		# Asignamos lo que representa cada elemento.
		prevScene 			= toUndo[0]
		prevSimpleStorage 	= toUndo[1]
		prevComplexStorage 	= toUndo[2]

		# Recuperamos el estado de la escena.
		__V.centralWidget().scene().clear()
		for item in prevScene:
			print(item)
			print(prevSimpleStorage)
			__V.centralWidget().scene().addItem(item)
		# Recuperamos el estado de la cola de componentes simples.
		__M.setSimpleCompStorage(prevSimpleStorage)
		# Recuperamos el estado de la cola de componentes complejos.
		__M.setComplexCompStorage(prevComplexStorage)

		# Actualizamos la informacion mostrada en el Arbol.
		updateTrees(__V)


''' Recupera el siguiente estado en el historico de Rehacer. '''

def getNextState(__V):

	saveStateFromRedo(__V)

	# Recuperamos la tupla del estado anterior.
	toRedo = __M.getNextState()

	if toRedo is not None:
		# Asignamos lo que representa cada elemento.
		nextScene 			= toRedo[0]
		nextSimpleStorage 	= toRedo[1]
		nextComplexStorage 	= toRedo[2]

		# Recuperamos el estado de la escena.
		__V.centralWidget().scene().clear()
		for item in nextScene:
			print(item)
			print(nextSimpleStorage)
			__V.centralWidget().scene().addItem(item)
		# Recuperamos el estado de la cola de componentes simples.
		__M.setSimpleCompStorage(nextSimpleStorage)
		# Recuperamos el estado de la cola de componentes complejos.
		__M.setComplexCompStorage(nextComplexStorage)

		# Actualizamos la informacion mostrada en el Arbol.
		updateTrees(__V)
