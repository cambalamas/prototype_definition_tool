#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, i18n
from copy import copy

import GUI
import PARSER
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from SIMPLE import SimpleComponent


class PRESENTER( object ):
	def __init__(self,view,model):

		self._view = view
		self._model = model


	##
	# SEÑALES DE LA VISTA.
	##

	""" Recupera la interfaz definida del modelo y se comunica con
	el experto en XML para generar el archivo correspondiente """

	def listener_SaveProject(self):
		interface = self._model.interface
		EParser.save(interface)


	""" Abre un cuadro de dialogo para que el usuario seleccione las imagenes que quiera en cualquier formato rasterizado como BMP, JPG
	o el preferido, PNG. """

	def listener_NewSimple(self):
		# El metodo multiplataforma de obtener el 'HOME' del usuario.
		home = os.path.expanduser('~')
		# Recogemos las imagenes seleccionadas del cuadro de dialogo.
		imgPathSet = QFileDialog.getOpenFileNames(self._view,'Pick imgs!',home)

		# En base a las rutas recogidas.
		if imgPathSet[0]:
			for imgPath in imgPathSet[0]:
				item = SimpleComponent(imgPath)
				if item is not None:
					# Agregamos el item a: MODELO
					self._model.newComponent(item)

					# --- lo que sigue debe hacerse despues
					# --- de que el model trabaje
					# --- y en base a los datos del model.

					# Actualizamos la vista: TREEVIEW
					updateTrees(self._view)
					# Agregamos el item a: ESCENA
					self._view.getScene().addItem(item)


	""" Abre un dialogo para configurar los distintos estados, de un
	componente complejo, definir el evento que produce la transicion
	entre ellos y la imagen en el caso de los componentes simples """

	def listener_NewComplex(self):
		pass


	""" Oculta la barra de menus, pero sin perder la validez de los
	atajos de teclado definidos para sus acciones. """

	def listener_HideMenu(self):
		menuBar = self._view.menuBar()
		if menuBar.height() is not 0:
			menuBar.setFixedHeight(0)
		else:
			menuBar.setFixedHeight(menuBar.sizeHint().height())

		qCritical('wow')


	""" Aumenta la escala de la escena. """

	def listener_ZoomIn(self):
		mod = self._view.getScaleMod()
		# Calculamos la escala resultante de decrementar.
		inc = self._view.getScale() * mod

		# Si no pasamos el minimo permitido.
		if inc < self._view.getScaleMax():
			# Reducimos la escala en base al factor de escalado.
			self._view.centralWidget().scale(mod,mod)
			# Actualizamos la variable de control.
			self._view.setScale(inc)


	""" Disminuye la escala de la escena. """

	def listener_ZoomOut(self):
		mod = self._view.getScaleMod()
		# Calculamos la escala resultante de decrementar.
		dec = self._view.getScale() / mod

		# Si no pasamos el minimo permitido.
		if dec > self._view.getScaleMin():
			# Reducimos la escala en base al factor de escalado.
			self._view.centralWidget().scale(1/mod,1/mod)
			# Actualizamos la variable de control.
			self._view.setScale(dec)


	""" Restaurar el nivel de Zoom al 100% """

	def listener_Zoom100(self):

		scale = self._view.getScale()
		# Realizamos el reset en base a la escala actual.
		self._view.centralWidget().scale(1/scale,1/scale)
		# Actualizamos la variable de control.
		self._view.setScale(scale/scale)


	""" Sencillo -toggle- para cambiar entre la vista de
	pantalla completa y la que anteriormente establecida. """

	def listener_FullScreen(self):
		if self._view.isFullScreen():
			# Restablezco el estado anterior.
			self._view.setWindowState(self._view.getPrevWindowState())
		else :
			# Guardo el estado actual.
			self._view.setPrevWindowState(self._view.windowState())
			# Cambiamos la ventana a pantalla completa.
			self._view.showFullScreen()



	""" Configura 'locale' de i18n para ver la interfaz en Español """

	def listener_TrEs(self):
		i18n.set('locale', 'es')

	""" Configura 'locale' de i18n para ver la interfaz en Ingles """

	def listener_TrEn(self):
		i18n.set('locale', 'en')

	""" Configura 'locale' de i18n para ver la interfaz en Frances """

	def listener_TrFr(self):
		i18n.set('locale', 'fr')

	""" Configura 'locale' de i18n para ver la interfaz en Aleman """

	def listener_TrDe(self):
		i18n.set('locale', 'de')



	""" Cuando alguno de los campos que permiten edicion de una fila
	del arbol sufre cualquier cambio, sera evaluado desde aqui. """

	def listener_simpleTreeItemChange(self):
		tree = self._view.getSimpleTree()
		indexList = tree.selectedIndexes()

		for index in indexList:

			# Fila correspondiente al item seleccionado.
			row = tree.model().itemFromIndex(index)

			# Recupero los datos cambiado.
			name = row.data(0)

			if row.data(1) == Qt.Checked:
				visible = True
			else:
				visible = False

			if row.data(2) == Qt.Checked:
				active = True
			else:
				active = False

			# Recuperamos el id 'ocultado' en el hijo.
			compID = row.child(0,0).data(Qt.UserRole)

			# Guardamos la modificacion en la estructura de datos.
			compData = { 'Name':name,
						 'Visible':visible,
						 'Active':active }

			# Actualizamos el modelo.
			self._model.modComponent(compId,compData)



	""" Menu contextual activado con el boton derecho donde se muestran
	las distintas acciones que se pueden ejecutar sobre los componentes
	que se encuentran en la lista. """

	def listener_simpleTreeInvokeMenu(self): # TO-DO
		tree = self._view.getSimpleTree()
		indexList = tree.selectedIndexes()

		for index in indexList:

			# Obtenemos el ID, que hemos situado en la posicion Zero.
			selected = self.model().itemFromIndex(indexList[0])
			self.selectedID = selected.child(0,0).data(Qt.UserRole)

			# Y Mostramos el menu contextual correspondiente.
		self._view.getSimpleTreeMenu().exec(self._view.cursor().pos())


	def listener_complexTreeItemChange(self):
		pass

	def listener_complexTreeInvokeMenu(self):
		pass



	##
	# SEÑALES DE COMPONENTES SIMPLES.
	##


	def listener_SimpleZInc(self):
		# Hacer los arboles como clases separadas para poder controlar
		# las leves discrepancias de acceiones a realizar, en la misma señal
		# segun si viene de arbol o de compSimple.
		w1 = self._view.getSimpleTree()
		w2 = self._view.getComplexTree()
		w1Rect = w1.geometry()
		w1Mouse = w1.mapFromGlobal(QCursor.pos())
		print(w1Rect.contains(w1Mouse))
		pass

	def listener_SimpleZDec(self):
		pass

	def listener_SimpleActive(self):
		pass

	def listener_SimpleVisible(self):
		pass

	def listener_SimpleDelete(self):
		pass

	def listener_SimpleDetail(self):
		pass

















## CODIGO A REUBICAR.
# --------------------------------------------------------------------------


	# ----------------------------------------------------------------------- #
	#					 	- ACTUALIZADORES DEL MODELO - 				   	  #
	# ----------------------------------------------------------------------- #


	''' Solicitud de borrado invocada desde el propio objeto.'''

	def directDelSimpleComp(item):
		# Borrar del almacenaje.
		self._model.delSimpleComp(item)
		# Borrar de la escena.
		self._view.centralWidget().scene().removeItem(item)
		# Actualizamos la vista: TREEVIEW
		updateTrees(self._view)



	# ----------------------------------------------------------------------- #
	#					 		 	- ARBOLES - 				   			  #
	# ----------------------------------------------------------------------- #


	''' Dado un arbol devuelve el ID del item seleccionado '''

	# def getTreeSelectedItemID(tree):
	# 	indexList = tree.selectedIndexes()
	# 	if indexList is not None:
	# 		firstCol = tree.model().itemFromIndex(index[0])
	# 		itemID = firstCol.child(0,0).data(Qt.UserRole)
	# 		return itemID


	''' Actualiza los arboles en base a EModel. '''

	def updateTrees():
		model = self._view.simpleCompsTree.model()

		# Borramos el contenido actual del arbol.
		model.removeRows(0, model.rowCount())

		# Rellenamos el arbol en base al contenido de la cola.
		for elem in self._model.getSimpleCompStorage():

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

	def simpleCompsTreeItemChanged():
		tree = self._view.simpleCompsTree
		indexList = tree.selectedIndexes()
		if indexList is not None:
			# Recupero el dato cambiado. (Solo se permite cambiar el nombre)
			firstColData = tree.model().itemFromIndex(indexList[0]).data(0)
			# Columna donde 'ocultamos' el id del objeto.
			firstCol = tree.model().itemFromIndex(indexList[0])
			# Recuperamos el id 'ocultado' en el hijo.
			itemID = firstCol.child(0,0).data(Qt.UserRole)

			# Guardamos la modificacion en la estructura de datos.
			item = self._model.getSimpleComp(itemID)
			item.setName(firstColData)
