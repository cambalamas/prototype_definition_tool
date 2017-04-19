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


		# ----------------------------------------------------------------- #
		#					   GUI :: MENU CONTEXTUAL 						#
		# ----------------------------------------------------------------- #

		self.contextMenu = QMenu('MENU: Arbol de componentes')

		# ACCION: Incrementar profundidad del objeto.
		cmAct = self.contextMenu.addAction('INCREMENTA Profundidad')
		cmAct.triggered.connect(self.incZ)

		# ACCION: Decrementar profundidad del objeto.
		cmAct = self.contextMenu.addAction('DECREMENTA Profundidad')
		cmAct.triggered.connect(self.decZ)

		# Dibuja una linea horizontal.
		self.contextMenu.addSeparator()

		# ACCION: Activa / Desactiva el objeto.
		cmAct = self.contextMenu.addAction('Rota estado: ACTIVO')
		cmAct.triggered.connect(self.toggleActive)

		# ACCION: Muestra / Oculta el objeto.
		cmAct = self.contextMenu.addAction('Rota estado: VISIBLE')
		cmAct.triggered.connect(self.toggleVisible)

		# Dibuja una linea horizontal.
		self.contextMenu.addSeparator()

		# ACCION: Borra el objeto de la escena y el modelo.
		cmAct = self.contextMenu.addAction('BORRA el elemento')
		cmAct.triggered.connect(self.removeItem)

		# Dibuja una linea horizontal.
		self.contextMenu.addSeparator()

		# ACCION: Dialogo con los detalles del objeto.
		cmAct = self.contextMenu.addAction('Informacion detallada...')
		cmAct.triggered.connect(self.detailsDialog)


	"""
	Menu contextual activado con el boton derecho donde se muestran
	las distintas acciones que se pueden ejecutar sobre los componentes
	que se encuentran en la lista.
	"""
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
		obj.removeItem()

	def detailsDialog(self):
		obj = ELogic.getSimpleComp(self.selectedID)
		obj.detailsDialog()
