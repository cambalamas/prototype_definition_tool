#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import i18n
from threading import Timer
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI, HIST, PARSER, SIMPLE
from PresetValues import pv

## @brief      Clase que define la logica de negocio de la aplicacion.
class PRESENTER( object ):

	## @brief      Constructor del objeto Presentador.
	## @param      self   El objeto presentador.
	## @param      view   La ventana principal.
	## @param      model  El acceso a la capa de persistencia.
	def __init__(self,view,model):
		# Ventana principal.
		self._view = view
		# Gestion de datos y persistencia.
		self._model = model
		# Flags para evitar drenaje de RAM.
		self.saveFlagMove = True
		self.saveFlagResize = True

	## @brief      Propiedad de lectura de la variable vista.
	## @param      self  El objeto presentador.
	## @return     VIEW.VIEW
	@property
	def view(self):
		return self._view

	## @brief      Propiedad de lectura de la variable modelo.
	## @param      self  El objeto presentador.
	## @return     MODEL.MODEL
	@property
	def model(self):
		return self._model


	# --- Señales del menu Archivo.

	## @brief      Guarda la interfaz actual en XML.
	## @param      self  El objeto presentador.
	## @return     None
	def listener_SaveProject(self):
		pass # PARSER.save(self.model.interface)

	## @brief      Crea un nuevo componente simple.
	## @param      self  El objeto presentador.
	## @return     None
	def listener_NewSimple(self):
		home = os.path.expanduser(pv['defaultPath'])
		imgPathSet = GUI.imgDialog(self.view,home) # ret: ([<path>],<formato>)
		if imgPathSet[0]:
			self.model.saveState()
			for imgPath in imgPathSet[0]:
				item = SIMPLE.SimpleComponent(imgPath) # Crea comp simpmle.
				if item is not None:
					item.setZValue(1.0)
					self.model.newComponent(item) # Lo agrega a la pila.

	## @brief      Crea un nuevo componente complejo.
	## @param      self  El objeto presentador.
	## @return     None
	def listener_NewComplex(self):
		pass


	# --- Señales del menu Editar.

	## @brief      Devuelve el area de trabajo a su estado anterior.
	## @param      self  El objeto presentador.
	## @return     None
	def listener_Undo(self):
		self.model.undo()

	## @brief      Devuelve el area de trabajo a un estado posterior.
	## @param      self  El objeto presentador.
	## @return     None
	def listener_Redo(self):
		self.model.redo()


	# --- Señales del menu Vista.

	## @brief      Oculta todos las widgets.
	## @param      self  El objeto presentador.
	## @return     None
	def listener_Minimalist(self):
		mtb = self.view._toolbar
		sdb = self.view._simpleDockbar
		cdb = self.view._complexDockbar
		stb = self.view.statusBar()
		if(mtb.isVisible() == sdb.isVisible()
		   == cdb.isVisible() == stb.isVisible() == True):
			mtb.setVisible(False)
			sdb.setVisible(False)
			cdb.setVisible(False)
			stb.setVisible(False)
		else:
			mtb.setVisible(True)
			sdb.setVisible(True)
			cdb.setVisible(True)
			stb.setVisible(True)

	## @brief      Oculta la barra de menus.
	## @param      self  El objeto presentador.
	## @return     None
	def listener_HideMenu(self):
		menuBar = self.view.menuBar()
		if menuBar.height() is not 0:
			menuBar.setFixedHeight(0)
		else:
			menuBar.setFixedHeight(menuBar.sizeHint().height())

	## @brief      Aumenta la escala de la escena.
	## @param      self  El objeto presentador.
	## @return     None
	def listener_ZoomIn(self):
		print(self.view.workArea.transform().mapRect(self.view.contentsRect()))
		if not self.view.scale * pv['viewModScale'] > pv['viewMaxScale']:
			self.view.workArea.scale(pv['viewModScale'],pv['viewModScale'])

	## @brief      Restaurar el nivel de Zoom al 100%.
	## @param      self  El objeto presentador.
	## @return     None
	def listener_Zoom100(self):
		print(self.view.workArea.transform().mapRect(self.view.contentsRect()))
		self.view.workArea.scale(1/self.view.scale,1/self.view.scale)

	## @brief      Disminuye la escala de la escena.
	## @param      self  El objeto presentador.
	## @return     None
	def listener_ZoomOut(self):
		print(self.view.workArea.transform().mapRect(self.view.contentsRect()))
		if not self.view.scale / pv['viewModScale'] < pv['viewMinScale']:
			self.view.workArea.scale(1/pv['viewModScale'],1/pv['viewModScale'])

	## @brief      Rota entre pantalla completa y el estado anterior.
	## @param      self  El objeto presentador.
	## @return     None
	def listener_FullScreen(self):
		if self.view.isFullScreen():
			self.view.setWindowState(self.view.prevState)
		else:
			self.view.prevState = self.view.windowState()
			self.view.showFullScreen()





	# --- Señales de componentes.

	def listener_Name(self):
		self.model.saveState()
		newName, noCancel = GUI.nameDialog(self.view)
		if noCancel:
			if len(self.selectedItems()) > 1:
				i = 0
				for item in self.selectedItems():
					i += 1
					item.name = str(i)+'_'+newName
			else:
				for item in self.selectedItems():
					item.name = newName
			self.updateTree()

	def listener_ZInc(self):
		self.model.saveState()
		for item in self.selectedItems():
			newZ = item.getPosZ() + pv['zJump']
			item.setZValue(newZ)
		self.updateTree()

	def listener_ZDec(self):
		self.model.saveState()
		for item in self.selectedItems():
			newZ = item.getPosZ() - pv['zJump']
			if newZ >= 0:
				item.setZValue(newZ)
		self.updateTree()

	def listener_Active(self):
		self.model.saveState()
		for item in self.selectedItems():
			toggle = not item.active
			item.active = toggle
			item.activeEffect()
		self.updateTree()

	def listener_Visible(self):
		self.model.saveState()
		for item in self.selectedItems():
			item.visible = not item.visible
			item.visibleEffect()
		self.updateTree()

	def listener_Delete(self):
		self.model.saveState()
		self.model.delComponent(self.selectedItems())

	def listener_Move(self,posO,posD):
		despl = posD - posO
		if self.saveFlagMove:
			self.saveFlagMove = False
			self.model.saveState()
			Timer(pv['moveTimer'],self.thMoveFlag).start()
		for item in self.selectedItems():
			x = despl.x() * item.scale()
			y = despl.y() * item.scale()
			item.moveBy(x,y)
			print(item.pos())


	def listener_Resize(self,delta):
		if self.saveFlagResize:
			self.saveFlagResize = False
			self.model.saveState()
			Timer(pv['resizeTimer'],self.thResizeFlag).start()
		if delta > 0:
			for item in self.selectedItems():
				if not item.scale() * pv['imgModScale'] > pv['imgMaxScale']:
					item.setScale(item.scale() * pv['imgModScale'])
		else:
			for item in self.selectedItems():
				if not item.scale() / pv['imgModScale'] < pv['imgMinScale']:
					item.setScale(item.scale() / pv['imgModScale'])

		self.updateTree()

	def listener_Details(self):
		for item in self.selectedItems():
			item.detailsDialog()

	def listener_SelectAll(self):
		for item in self.view.workScene.items():
			item.setSelected(True)

	def listener_UnSelectAll(self):
		for item in self.selectedItems():
			item.setSelected(False)


	""" Menu contextual activado con el boton derecho donde se muestran
	las distintas acciones que se pueden ejecutar sobre componentes simples. """

	def listener_SimpleMenu(self):
		if self.isOver(self.view.simpleTree):
			self.listener_UnSelectAll()
			for index in self.view.simpleTree.selectedIndexes():
				row = self.view.simpleTree.model().itemFromIndex(index)
				if row.child(0,0) is not None:
					id = row.child(0,0).data(Qt.UserRole)
					comp = self.model.getComponentById(id)
					comp.setSelected(True)
		self.view.simpleMenu.exec(self.view.cursor().pos())

	def listener_ComplexMenu(self):
		pass



	# --- Señales del Modelo.

	## @brief      Crea la escena segun el modelo al recibir la notificación.
	## @param      self  El objeto presentador.
	## @return     None
	def listener_modelUpdated(self):
		scene = self.model.copyScene()
		self.view.resetWorkScene()
		for component in scene:
			self.view.workScene.addItem(component)
		self.model.scene = scene
		self.updateTree()



	# --- Logicas externas a las señales.

	## @brief      Resetea el flag que controla guardar estado al redimesionar.
	## @param      self  El componente simple.
	## @return     None
	def thResizeFlag(self):
		self.saveFlagResize = True

	## @brief      Resetea el flag que controla guardar estado al mover.
	## @param      self  El componente simple.
	## @return     None
	def thMoveFlag(self):
		self.saveFlagMove = True

	## @brief      Comprueba si el cursor se encuentra sobre un widget dado.
	## @param      self    El objeto presentador.
	## @param      widget  El widget sobre el que hacer la comprobacion.
	## @return     True si esta encima, False en caso contrario.
	def isOver(self,widget):
		mouse = widget.mapFromGlobal(QCursor.pos())
		return widget.geometry().contains(mouse)

	## @brief      Devuelve los items seleccionados en la escena.
	## @param      self  El objeto presentador.
	## @return     <list> de componentes. (Simples y Complejos)
	def selectedItems(self):
		selectedItems = []
		for item in self.view.workScene.items():
			if item.isSelected():
				selectedItems.append(item)
		return selectedItems

	## @brief      Actualiza los arboles de la aplicacion.
	## @param      self  El objeto presentador.
	## @return     None
	def updateTree(self):
		treeModel = self.view.simpleTree.model()
		treeModel.removeRows(0, treeModel.rowCount()) # Vaciamos el arbol.
		for elem in self.model.scene:
			# Nombre del elemento.
			col1 = QStandardItem(elem.name)
			col1.setEditable(False)
			# Estado Visible del elemento.
			col2 = QStandardItem()
			col2.setEditable(False)
			if elem.visible == True:
				col2.setCheckState(Qt.Checked)
			else:
				col2.setCheckState(Qt.Unchecked)
			# Estado Acvtivo del elemento.
			col3 = QStandardItem()
			col3.setEditable(False)
			if elem.active == True:
				col3.setCheckState(Qt.Checked)
			else:
				col3.setCheckState(Qt.Unchecked)
			# Posicion Z para facilitar el control de la profundidad.
			col4 = QStandardItem(str(elem.getPosZ()))
			col4.setEditable(False)
			# Guardamos el ID de forma oculta.
			child = QStandardItem()
			child.setData(elem.id,Qt.UserRole)
			col1.setChild(0,0,child)
			# Componemos la fila y la agregamos al arbol.
			treeModel.appendRow( [col1 , col2, col3, col4] )
