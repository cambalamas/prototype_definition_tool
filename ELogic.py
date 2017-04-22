#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
from copy import copy
from collections import deque

from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import EParser
from EStorage import EModel
from Inherits.ESimple import ESimple


__M = EModel() # Instancia un modelo.



# --------------------------------------------------------------------------- #
#					 		   - PROYECTO - 				   				  #
# --------------------------------------------------------------------------- #

def saveProject():
	xml = etree.Element('Interface')
	for elem in __M.getSimpleCompStorage():
		if str(type(e)) == "<class 'ESimple.ESimple'>":
			xml.append(EParser.simple2xml(elem))
	if xml is not None:
		print( prettify(xml) )



# --------------------------------------------------------------------------- #
#					 		 	- HISTORIAL - 				   				  #
# --------------------------------------------------------------------------- #


''' Guarda el estado anterior, para permitr el 'Ctrl+Z' '''

def saveState(__V):

	scene = []
	for item in __V.centralWidget().scene().items():
		qgItem = copy(item)
		scene.append(qgItem)


	simpleStorage 	= [ x for x in __M.getSimpleCompStorage()  ]
	complexStorage	= [ x for x in __M.getComplexCompStorage() ]

	state = (scene,deque(simpleStorage),deque(complexStorage))
	__M.saveState(state)


''' Recupera el anterior estado en el historico de Deshacer. '''

def getPrevState(__V):

	# Recuperamos la tupla del estado anterior.
	toUndo = __M.getPrevState()

	# Asignamos lo que representa cada elemento.
	prevScene 			= toUndo[0]
	prevSimpleStorage 	= toUndo[1]
	prevComplexStorage 	= toUndo[2]

	# Recuperamos el estado de la escena.
	__V.centralWidget().scene().clear()
	for item in prevScene:
		__V.centralWidget().scene().addItem(item)
	# Recuperamos el estado de la cola de componentes simples.
	__M.setSimpleCompStorage(prevSimpleStorage)
	# Recuperamos el estado de la cola de componentes complejos.
	__M.setComplexCompStorage(prevComplexStorage)

	# Actualizamos la informacion mostrada en el Arbol.
	# updateTrees(__V)


''' Recupera el siguiente estado en el historico de Rehacer. '''

def getNextState(__V):

	# Recuperamos la tupla del estado anterior.
	toRedo = __M.getNextState()

	# Asignamos lo que representa cada elemento.
	nextScene 			= toRedo[0]
	nextSimpleStorage 	= toRedo[1]
	nextComplexStorage 	= toRedo[2]

	# Recuperamos el estado de la escena.
	__V.centralWidget().scene().clear()
	for item in nextScene:
		__V.centralWidget().scene().addItem(item)
	# Recuperamos el estado de la cola de componentes simples.
	__M.setSimpleCompStorage(nextSimpleStorage)
	# Recuperamos el estado de la cola de componentes complejos.
	__M.setComplexCompStorage(nextComplexStorage)

	# Actualizamos la informacion mostrada en el Arbol.
	# updateTrees(__V)



# --------------------------------------------------------------------------- #
#					 		  - COMPONENTES - 				   				  #
# --------------------------------------------------------------------------- #


''' Recupera de la coleccion un objeto por su ID. '''

def getSimpleComp(itemID):
	return __M.getSimpleComp(itemID)


''' Agrega a los contenedores correspondientes un nuevo Componente Simple. '''

def newSimpleComp(imgPathSet,__V):
	saveState(__V)
	if imgPathSet[0]:
		for imgPath in imgPathSet[0]:
			item = ESimple(imgPath)
			if item is not None:
				# Agregamos el item a: MODELO
				__M.newSimpleComp(item)
				# Actualizamos la vista: TREEVIEW
				updateTrees(__V)
				# Agregamos el item a: ESCENA
				__V.centralWidget().scene().addItem(item)


''' Solicitud de borrado invocada desde el propio objeto.'''

def directDelSimpleComp(item,__V):
	# Borrar del almacenaje.
	__M.delSimpleComp(item)
	# Borrar de la escena.
	__V.centralWidget().scene().removeItem(item)
	# Actualizamos la vista: TREEVIEW
	updateTrees(__V)



# --------------------------------------------------------------------------- #
#					 		 	- ARBOLES - 				   				  #
# --------------------------------------------------------------------------- #


''' Dado un arbol devuelve el ID del item seleccionado '''

# def getTreeSelectedItemID(tree):
# 	indexList = tree.selectedIndexes()
# 	if indexList is not None:
# 		firstCol = tree.model().itemFromIndex(index[0])
# 		itemID = firstCol.child(0,0).data(Qt.UserRole)
# 		return itemID


''' Actualiza los arboles en base a EModel. '''

def updateTrees(__V):
	model = __V.simpleCompsTree.model()

	# Borramos el contenido actual del arbol.
	model.removeRows(0, model.rowCount())

	# Rellenamos el arbol en base al contenido de la cola.
	for elem in __M.getSimpleCompStorage():

		# Nombre del elemento.
		col1 = QStandardItem(elem.getName())

		# Estado Visible del elemento.
		col2 = QStandardItem()
		col2.setEditable(False)
		# Estado del check.
		if elem.getVisible() == True:
			col2.setCheckState(Qt.Checked)
		else:
			col2.setCheckState(Qt.Unchecked)

		# Estado Acvtivo del elemento.
		col3 = QStandardItem()
		col3.setEditable(False)
		# Estado del check.
		if elem.getActive() == True:
			col3.setCheckState(Qt.Checked)
		else:
			col3.setCheckState(Qt.Unchecked)

		# Posicion Z para facilitar el control de la profundidad.
		col4 = QStandardItem(str(elem.getPosZ()))
		col4.setEditable(False)

		# Guardamos el ID de forma oculta.
		child = QStandardItem()
		child.setData(elem.getID(),Qt.UserRole)
		col1.setChild(0,0,child)

		# Componemos la fila y la agregamos al arbol.
		model.appendRow( [col1 , col2, col3, col4] )


''' Atiende a la señal 'ItemCanged' del modelo qt del treeview '''

def simpleCompsTreeItemChanged(__V):
	tree = __V.simpleCompsTree
	indexList = tree.selectedIndexes()
	if indexList is not None:
		# Recupero el dato cambiado. (Solo se permite cambiar el nombre)
		firstColData = tree.model().itemFromIndex(indexList[0]).data(0)
		# Columna donde 'ocultamos' el id del objeto.
		firstCol = tree.model().itemFromIndex(indexList[0])
		# Recuperamos el id 'ocultado' en el hijo.
		itemID = firstCol.child(0,0).data(Qt.UserRole)

		# Guardamos la modificacion en la estructura de datos.
		item = __M.getSimpleComp(itemID)
		item.setName(firstColData)
