#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

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
#					 		  - COMPONENTES - 				   				  #
# --------------------------------------------------------------------------- #

def getSimpleComp(itemID):
	return __M.getSimpleComp(itemID)

def newSimpleComp(imgPathSet,__V):
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

def directDelSimpleComp(item,__V):
	# Borrar del almacenaje.
	__M.delSimpleComp(item)
	# Borrar de la escena.
	__V.centralWidget().scene().removeItem(item)
	# Actualizamos la vista: TREEVIEW
	updateTrees(__V)



# --------------------------------------------------------------------------- #
#					 		 	- HISTORIAL - 				   				  #
# --------------------------------------------------------------------------- #

	def regNewAction(funcStr):
		self.__M.regNewAction(funcStr)

	def getPrevState(__V):
		## !!!!! HAY QUE LIMPIAR __V
		__M.getPrevState()
		for func in __M.getUndoStorage():
			exec(func)

	def getNextState():
		toRedo = __M.getNextState()
		exec(toRedo)


	# Decorador
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

		regNewAction(wrap)



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
