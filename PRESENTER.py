#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import i18n
from threading import Timer
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI, PARSER, SIMPLE
from PresetValues import pv

## @brief      Clase que define la logica de negocio de la aplicacion.
class PRESENTER( object ):


# .-------------.
# | Constructor |
# --------------------------------------------------------------------------- #

	## @brief      Constructor de el Presentador.
	## @param      self   Presentador.
	## @param      view   La ventana principal.
	## @param      model  El acceso a la capa de persistencia.
	def __init__(self,view,model):
		# Ventana principal.
		self.__view = view
		# Gestion de datos y persistencia.
		self.__model = model
		# Flags para evitar drenaje de RAM.
		self.__saveFlagMove = True
		self.__saveFlagResize = True


# .----------------------------------------.
# | Acceso 'publico' la variables privadas |
# --------------------------------------------------------------------------- #

	## @brief      Propiedad de lectura de la variable vista.
	## @param      self  Presentador.
	## @return     VIEW.VIEW
	@property
	def view(self):
		return self.__view

	## @brief      Propiedad de lectura de la variable modelo.
	## @param      self  Presentador.
	## @return     MODEL.MODEL
	@property
	def model(self):
		return self.__model


# .--------------------------.
# | Señales del menu Archivo |
# --------------------------------------------------------------------------- #

	## @brief      Guarda la interfaz actual en XML.
	## @param      self  Presentador.
	## @return     None
	def listener_SaveProject(self):
		pass # PARSER.save(self.model.interface)

	## @brief      Crea un nuevo componente simple.
	## @param      self  Presentador.
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
	## @param      self  Presentador.
	## @return     None
	def listener_NewComplex(self):
		pass


# .-------------------------.
# | Señales del menu Editar |
# --------------------------------------------------------------------------- #

	## @brief      Establece True la propiedad 'selected' de todos los comps.
	## @param      self  Presentador.
	## @return     None
	def listener_SelectAll(self):
		for item in self.view.workScene.items():
			item.setSelected(True)

	## @brief      Establece False la propiedad 'selected' de todos los comps.
	## @param      self  Presentador.
	## @return     None
	def listener_UnSelectAll(self):
		for item in self._selectedItems():
			item.setSelected(False)

	## @brief      Devuelve el area de trabajo a su estado anterior.
	## @param      self  Presentador.
	## @return     None
	def listener_Undo(self):
		self.model.undo()

	## @brief      Devuelve el area de trabajo a un estado posterior.
	## @param      self  Presentador.
	## @return     None
	def listener_Redo(self):
		self.model.redo()


# .------------------------.
# | Señales del menu Vista |
# --------------------------------------------------------------------------- #

	## @brief      Oculta todos las widgets.
	## @param      self  Presentador.
	## @return     None
	def listener_Minimalist(self):
		mtb = self.view.toolbar
		sdb = self.view.simpleDockbar
		cdb = self.view.complexDockbar
		stb = self.view.statusBar()
		if( mtb.isVisible()
		   		== sdb.isVisible()
		   		== cdb.isVisible()
		   		== stb.isVisible()
		   		== True):
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
	## @param      self  Presentador.
	## @return     None
	def listener_HideMenu(self):
		menuBar = self.view.menuBar()
		if menuBar.height() is not 0:
			menuBar.setFixedHeight(0)
		else:
			menuBar.setFixedHeight(menuBar.sizeHint().height())

	## @brief      Aumenta la escala de la escena.
	## @param      self  Presentador.
	## @return     None
	def listener_ZoomIn(self):
		print(self.view.workArea.transform().mapRect(self.view.contentsRect()))
		if not self.view.scale * pv['viewModScale'] > pv['viewMaxScale']:
			self.view.workArea.scale(pv['viewModScale'],pv['viewModScale'])

	## @brief      Restaurar el nivel de Zoom al 100%.
	## @param      self  Presentador.
	## @return     None
	def listener_Zoom100(self):
		print(self.view.workArea.transform().mapRect(self.view.contentsRect()))
		self.view.workArea.scale(1/self.view.scale,1/self.view.scale)

	## @brief      Disminuye la escala de la escena.
	## @param      self  Presentador.
	## @return     None
	def listener_ZoomOut(self):
		print(self.view.workArea.transform().mapRect(self.view.contentsRect()))
		if not self.view.scale / pv['viewModScale'] < pv['viewMinScale']:
			self.view.workArea.scale(1/pv['viewModScale'],1/pv['viewModScale'])

	## @brief      Rota entre pantalla completa y el estado anterior.
	## @param      self  Presentador.
	## @return     None
	def listener_FullScreen(self):
		if self.view.isFullScreen():
			self.view.setWindowState(self.view.prevState)
		else:
			self.view.prevState = self.view.windowState()
			self.view.showFullScreen()


# .---------------------------------------.
# | Señales 'menu' de componentes simples |
# --------------------------------------------------------------------------- #

	## @brief      Invoca el menu contextual de los componentes simples.
	## @param      self  Presentador.
	## @return     None
	def listener_SimpleMenu(self):
		if self._isOver(self.view.simpleTree):
			self.listener_UnSelectAll()
			for index in self.view.simpleTree.selectedIndexes():
				row = self.view.simpleTree.model().itemFromIndex(index)
				if row.child(0,0) is not None:
					id = row.child(0,0).data(Qt.UserRole)
					comp = self.model.getComponentById(id)
					comp.setSelected(True)
		self.view.simpleMenu.exec(self.view.cursor().pos())

	## @brief      Dialogo para cambiar el nombre los comps. seleccionados.
	## @param      self  Presentador.
	## @return     None
	def listener_Name(self):
		self.model.saveState()
		newName, noCancel = GUI.nameDialog(self.view)
		if noCancel:
			if len(self._selectedItems()) > 1:
				i = 0
				for item in self._selectedItems():
					i += 1
					item.name = str(i)+'_'+newName
			else:
				for item in self._selectedItems():
					item.name = newName
			# Actualiza los datos en el arbol de componentes.
			self._updateTree()

	## @brief      Mueve una posición al frente los componentes seleccionados.
	## @param      self  Presentador.
	## @return     None
	def listener_ZInc(self):
		self.model.saveState()
		for item in self._selectedItems():
			newZ = item.getPosZ() + pv['zJump']
			item.setZValue(newZ)
		# Actualiza los datos en el arbol de componentes.
		self._updateTree()

	## @brief      Mueve una posición al fondo los componentes seleccionados.
	## @param      self  Presentador.
	## @return     None
	def listener_ZDec(self):
		self.model.saveState()
		for item in self._selectedItems():
			newZ = item.getPosZ() - pv['zJump']
			if newZ >= 0:
				item.setZValue(newZ)
		# Actualiza los datos en el arbol de componentes.
		self._updateTree()

	## @brief      Rota el estado Activo de los componentes seleccionados.
	## @param      self  Presentador.
	## @return     None
	def listener_Active(self):
		self.model.saveState()
		for item in self._selectedItems():
			toggle = not item.active
			item.active = toggle
			item.activeEffect()
		# Actualiza los datos en el arbol de componentes.
		self._updateTree()

	## @brief      Rota el estado Visible de los componentes seleccionados.
	## @param      self  Presentador.
	## @return     None
	def listener_Visible(self):
		self.model.saveState()
		for item in self._selectedItems():
			item.visible = not item.visible
			item.visibleEffect()
		# Actualiza los datos en el arbol de componentes.
		self._updateTree()

	## @brief      Elimina por completo los componentes seleccionados.
	## @param      self  Presentador.
	## @return     None
	def listener_Delete(self):
		self.model.saveState()
		self.model.delComponent(self._selectedItems())

	## @brief      Abre un cuadro de dialogo con el ToString del componente.
	## @param      self  Presentador.
	## @return     None
	def listener_Details(self):
		for item in self._selectedItems():
			item.detailsDialog()


# .-------------------------------------------.
# | Señales 'callback' de componentes simples |
# --------------------------------------------------------------------------- #

	## @brief      Mueve los comps. seleccinados segun el despl. del cursor.
	## @param      self  Presentador.
	## @param      posO  Posición de origen.
	## @param      posD  Posición de destiono.
	## @return     None
	def listener_Move(self,posO,posD):
		despl = posD - posO
		if self.__saveFlagMove:
			self.__saveFlagMove = False
			self.model.saveState()
			Timer(pv['moveTimer'],self._thMoveFlag).start()
		for item in self._selectedItems():
			x = despl.x() * item.scale()
			y = despl.y() * item.scale()
			item.moveBy(x,y)
			print(item.pos())

	## @brief      Escala virtualmente los comps. según el giro de la rueda.
	## @param      self   Presentador.
	## @param      delta  Giro de la rueda (+: Adelante / -: Atrás)
	## @return     None
	def listener_Resize(self,delta):
		if self.__saveFlagResize:
			self.__saveFlagResize = False
			self.model.saveState()
			Timer(pv['resizeTimer'],self._thResizeFlag).start()
		# offsetX = lambda x,sign: x.offset().x() + pv['imgModScale'] *sign
		# offsetY = lambda y,sign: y.offset().y() + pv['imgModScale'] *sign
		if delta > 0:
			for item in self._selectedItems():
				if not item.scale() * pv['imgModScale'] > pv['imgMaxScale']:
					# item.setOffset(offsetX(item,1), offsetY(item,1))
					item.setScale(item.scale() * pv['imgModScale'])
					print(item.offset().x(),item.offset().y())
		else:
			for item in self._selectedItems():
				if not item.scale() / pv['imgModScale'] < pv['imgMinScale']:
					# item.setOffset(offsetX(item,-1), offsetY(item,-1))
					item.setScale(item.scale() / pv['imgModScale'])
					print(item.offset().x(),item.offset().y())
		# Actualiza los datos en el arbol de componentes.
		self._updateTree()


# .---------------------------------------.
# | Señales 'menu' de componente complejo |
# --------------------------------------------------------------------------- #

	## @brief      Invoca el menu contextual de los componentes complejos.
	## @param      self  Presentador.
	## @return     None
	def listener_ComplexMenu(self):
		pass


# .--------------------.
# | Señales del Modelo |
# --------------------------------------------------------------------------- #

	## @brief      Crea la escena segun el modelo al recibir la notificación.
	## @param      self  Presentador.
	## @return     None
	def listener_modelUpdated(self):
		scene = self.model.copyScene()
		self.view.resetWorkScene()
		for component in scene:
			self.view.workScene.addItem(component)
		self.model.scene = scene
		# Actualiza los datos en el arbol de componentes.
		self._updateTree()


# .--------------------------------.
# | Logicas externas a las señales |
# --------------------------------------------------------------------------- #

	## @brief      Resetea el flag que controla guardar estado al redimesionar.
	## @param      self  El componente simple.
	## @return     None
	def _thResizeFlag(self):
		self.__saveFlagResize = True

	## @brief      Resetea el flag que controla guardar estado al mover.
	## @param      self  El componente simple.
	## @return     None
	def _thMoveFlag(self):
		self.__saveFlagMove = True

	## @brief      Comprueba si el cursor se encuentra sobre un widget dado.
	## @param      self    Presentador.
	## @param      widget  El widget sobre el que hacer la comprobacion.
	## @return     True si esta encima, False en caso contrario.
	def _isOver(self,widget):
		mouse = widget.mapFromGlobal(QCursor.pos())
		return widget.geometry().contains(mouse)

	## @brief      Devuelve los items seleccionados en la escena.
	## @param      self  Presentador.
	## @return     <list> de componentes. (Simples y Complejos)
	def _selectedItems(self):
		selectedItems = []
		for item in self.view.workScene.items():
			if item.isSelected():
				selectedItems.append(item)
		return selectedItems

	## @brief      Actualiza los arboles de la aplicacion.
	## @param      self  Presentador.
	## @return     None
	def _updateTree(self):
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
