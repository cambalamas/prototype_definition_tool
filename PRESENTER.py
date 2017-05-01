#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import i18n
from copy import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import GUI, PARSER, SIMPLE
from PresetValues import pv


##
## @brief      Clase que define la logica de negocio de la aplicacion.
##
class PRESENTER( object ):

	##
	## @brief      Constructor del objeto Presentador.
	##
	## @param      self   Este objeto.
	## @param      view   La ventana principal.
	## @param      model  El acceso a la capa de persistencia.
	##
	def __init__(self,view,model):

		self._view = view

		self._model = model

	##
	## @brief      Propiedad de lectura de la variable vista.
	##
	## @param      self  Este objeto.
	##
	## @return     VIEW.VIEW
	##
	@property
	def view(self):
		return self._view

	##
	## @brief      Propiedad de lectura de la variable modelo.
	##
	## @param      self  Este objeto.
	##
	## @return     MODEL.MODEL
	##
	@property
	def model(self):
		return self._model


	# --- Señales del menu Archivo.

	##
	## @brief      Guarda la interfaz actual en XML.
	##
	## @param      self  Este objeto.
	##
	## @return     None
	##
	def listener_SaveProject(self):
		pass # PARSER.save(self.model.interface)

	##
	## @brief      Crea un nuevo componente simple.
	##
	## @param      self  Este objeto.
	##
	## @return     None
	##
	def listener_NewSimple(self):
		home = os.path.expanduser(pv['defaultPath'])
		imgPathSet = GUI.imgDialog(self.view,home) # ret: ([<path>],<formato>)
		if imgPathSet[0]:
			for imgPath in imgPathSet[0]:
				item = SIMPLE.SimpleComponent(imgPath) # Crea comp simpmle.
				if item is not None:
					self.model.newComponent(item) # Lo agrega a la pila.

	##
	## @brief      Crea un nuevo componente complejo.
	##
	## @param      self  Este objeto.
	##
	## @return     None
	##
	def listener_NewComplex(self):
		pass


	# --- Señales del menu Editar.

	##
	## @brief      Devuelve el area de trabajo a su estado anterior.
	##
	## @param      self  Este objeto.
	##
	## @return     None
	##
	def listener_Undo(self):
		pass # Llamar al patron experto HIST.

	##
	## @brief      Devuelve el area de trabajo a
	##
	## @param      self  The object
	##
	## @return     { description_of_the_return_value }
	##
	def listener_Redo(self):
		pass # Llamar al patron experto HIST.


	# --- Señales del menu Vista.

	##
	## @brief      Oculta todos las widgets.
	##
	## @param      self  Este objeto.
	##
	## @return     None
	##
	def listener_Minimalist(self):
		pass

	##
	## @brief      Oculta la barra de menus.
	##
	## @param      self  Este objeto.
	##
	## @return     None
	##
	def listener_HideMenu(self):
		qDebug('hide')
		menuBar = self.view.menuBar()
		if menuBar.height() is not 0:
			menuBar.setFixedHeight(0)
		else:
			menuBar.setFixedHeight(menuBar.sizeHint().height())

	##
	## @brief      Aumenta la escala de la escena.
	##
	## @param      self  Este objeto.
	##
	## @return     None
	##
	def listener_ZoomIn(self):
		if not self.view.scale * pv['viewModScale'] > pv['viewMaxScale']:
			self.view.workArea.scale(pv['viewModScale'],pv['viewModScale'])

	##
	## @brief      Restaurar el nivel de Zoom al 100%.
	##
	## @param      self  Este objeto.
	##
	## @return     None
	##
	def listener_Zoom100(self):
		self.view.workArea.scale(1/self.view.scale,1/self.view.scale)

	##
	## @brief      Disminuye la escala de la escena.
	##
	## @param      self  Este objeto.
	##
	## @return     None
	##
	def listener_ZoomOut(self):
		if not self.view.scale / pv['viewModScale'] < pv['viewMinScale']:
			self.view.workArea.scale(1/pv['viewModScale'],1/pv['viewModScale'])

	##
	## @brief      Rota entre pantalla completa y el estado anterior.
	##
	## @param      self  Este objeto.
	##
	## @return     None
	##
	def listener_FullScreen(self):
		if self.view.isFullScreen():
			self.view.setWindowState(self.view.prevState)
		else:
			self.view.prevState = self.view.windowState()
			self.view.showFullScreen()


	# --- Señales del menu Ayuda.

	##
	## @brief      Configura 'locale' de i18n para ver la interfaz en Español.
	##
	## @param      self  Este objeto
	##
	## @return     None
	##
	def listener_TrEs(self):
		i18n.set('locale', 'es')

	##
	## @brief      Configura 'locale' de i18n para ver la interfaz en Ingles.
	##
	## @param      self  Este objeto.
	##
	## @return     None
	##
	def listener_TrEn(self):
		i18n.set('locale', 'en')

	##
	## @brief      Configura 'locale' de i18n para ver la interfaz en Frances.
	##
	## @param      self  Este objeto.
	##
	## @return     None
	##
	def listener_TrFr(self):
		i18n.set('locale', 'fr')

	##
	## @brief      Configura 'locale' de i18n para ver la interfaz en Aleman.
	##
	## @param      self  Este objeto.
	##
	## @return     None
	##
	def listener_TrDe(self):
		i18n.set('locale', 'de')


	# --- Señales de componentes.

	def listener_ZInc(self):
		for item in self.selectedItems():
			newZ = item.getPosZ() + pv['zJump']
			item.setZValue(newZ)

	def listener_ZDec(self):
		for item in self.selectedItems():
			newZ = item.getPosZ() - pv['zJump']
			if newZ > 0:
				item.setZValue(newZ)
			else: # Si Z es 0 y quier bajar un elem tengo que subir el resto.
				for elem in self.view.workScene.items():
					if elem != item: # Sin afectar al objeto que quiero bajar.
						zUp = elem.getPosZ() + pv['zJump']
						elem.setZValue(zUp)

	def listener_Active(self):
		for item in self.selectedItems():
			toggle = not item.active
			item.active = toggle
			item.activeEffect()

	def listener_Visible(self):
		for item in self.selectedItems():
			toggle = not item.getVisible()
			item.setVisible(toggle)

	def listener_Delete(self):
		self.model.delComponent(self.selectedItems())

	def listener_Resize(self,delta):
		if delta > 0:
			for item in self.selectedItems():
				if not item.scale() * pv['imgModScale'] > pv['imgMaxScale']:
					item.setScale(item.scale() * pv['imgModScale'])
		else:
			for item in self.selectedItems():
				if not item.scale() / pv['imgModScale'] < pv['imgMinScale']:
					item.setScale(item.scale() / pv['imgModScale'])

	""" Menu contextual activado con el boton derecho donde se muestran
	las distintas acciones que se pueden ejecutar sobre componentes simples. """

	def listener_SimpleMenu(self):
		self.view.simpleMenu.exec(self.view.cursor().pos())


	# --- Señales de arboles.

	""" Cuando alguno de los campos que permiten edicion de una fila
	del arbol sufre cualquier cambio, sera evaluado desde aqui. """

	def listener_simpleTreeItemChange(self):
		pass

	def listener_complexTreeItemChange(self):
		pass

	def listener_complexTreeInvokeMenu(self):
		pass


	# --- Señales del Modelo.

	##
	## @brief      Crea la escena segun el modelo al recibir la notificación.
	##
	## @param      self  Este objeto.
	##
	## @return     None
	##
	def listener_modelUpdated(self):
		scene = [copy(x) for x in self.model.scene]
		tree = self.view.simpleTree.model()
		self.view.resetWorkScene()
		tree.removeRows(0, tree.rowCount())
		for component in scene:
			self.view.workScene.addItem(component)
			treePtr =  QStandardItem(component.name)
			treePtr.setData(component,1)
			self.view.simpleTree.model().appendRow(treePtr)
		self.model.scene = scene



	# --- Logicas externas a las señales.

	##
	## @brief      Comprueba si el cursor se encuentra sobre un widget dado.
	##
	## @param      self    Este objeto.
	## @param      widget  El widget sobre el que hacer la comprobacion.
	##
	## @return     True si esta encima, False en caso contrario.
	##
	def isOver(self,widget):
		mouse = widget.mapFromGlobal(QCursor.pos())
		return widget.geometry().contains(mouse)

	##
	## @brief      Devuelve los items seleccionados en la escena.
	##
	## @param      self  Este objeto.
	##
	## @return     <list> de componentes. (Simples y Complejos)
	##
	def selectedItems(self):
		selectedItems = []
		for item in self.view.workScene.items():
			if item.isSelected():
				selectedItems.append(item)
		return selectedItems
