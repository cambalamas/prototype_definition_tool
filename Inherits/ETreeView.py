#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import ELogic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

"""
Clase creada para sobrecargar los eventos del 'TreeView'
"""
class ETreeView( QTreeView ):
	def __init__(self):
		super().__init__()
		self.selectedID = str()

		# ----------------------------------------------------------------- #
		#						CLASE :: PROPIEDADES 						#
		# ----------------------------------------------------------------- #

		# Oculta las flechas de hijos.
		self.setRootIsDecorated(False)
		# No permite expandir los hijos.
		self.setItemsExpandable(False)
		# Iguala la altura de las filas.
		self.setUniformRowHeights(True)
		# Dibuja el recuadro de seleccion en toda la fila.
		self.setSelectionBehavior(QAbstractItemView.SelectRows)
		# Solo permite seleccionar un elemento a la vez.
		self.setSelectionMode(QAbstractItemView.SingleSelection)






	def contextMenuEvent(self,ev):
		indexList = self.selectedIndexes()

		# Si hay seleccionado un item.
		if indexList:

			# Obtenemos el ID, que hemos situado en la posicion Zero.
			selected = self.model().itemFromIndex(indexList[0])
			self.selectedID = selected.child(0,0).data(Qt.UserRole)

			# Y Mostramos el menu contextual correspondiente.
			self.contextMenu.exec(ev.globalPos())


	"""
	Funciones para las acciones del menu contextual, que en este caso
	invocaran las funciones del propio objeto.
	"""

	def incZ(self):
		obj = ELogic.getSimpleComp(self.selectedID)
		obj.incZ()

	def decZ(self):
		obj = ELogic.getSimpleComp(self.selectedID)
		obj.decZ()

	def toggleActive(self):
		obj = ELogic.getSimpleComp(self.selectedID)
		obj.toggleActive()

	def toggleVisible(self):
		obj = ELogic.getSimpleComp(self.selectedID)
		obj.toggleVisible()

	def removeItem(self):
		obj = ELogic.getSimpleComp(self.selectedID)
		print(obj)
		obj.removeItem()

	def detailsDialog(self):
		obj = ELogic.getSimpleComp(self.selectedID)
		obj.detailsDialog()
