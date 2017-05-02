#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import GUI
from PresetValues import pv

##
## @brief      Clase encargada de la estructura visual de la aplicacion.
##
class VIEW( QMainWindow ):

	# Señales que luego se conectarán con el Presentador..
	signal_SaveProject           	= 	pyqtSignal()
	signal_NewSimple             	= 	pyqtSignal()
	signal_NewComplex            	= 	pyqtSignal()
	signal_Undo                     =   pyqtSignal()
	signal_Redo                     =	pyqtSignal()
	signal_HideMenu                	= 	pyqtSignal()
	signal_Minimalist              	= 	pyqtSignal()
	signal_ZoomIn               	= 	pyqtSignal()
	signal_Zoom100               	= 	pyqtSignal()
	signal_ZoomOut               	= 	pyqtSignal()
	signal_FullScreen            	= 	pyqtSignal()
	signal_TrEs                  	= 	pyqtSignal()
	signal_TrEn                  	= 	pyqtSignal()
	signal_TrFr                  	= 	pyqtSignal()
	signal_TrDe                  	= 	pyqtSignal()
	signal_Name            			= 	pyqtSignal()
	signal_ZInc            			= 	pyqtSignal()
	signal_ZDec            			= 	pyqtSignal()
	signal_Active          			= 	pyqtSignal()
	signal_Visible         			= 	pyqtSignal()
	signal_Delete          			= 	pyqtSignal()
	signal_Resize          			= 	pyqtSignal(int)
	signal_Details         			= 	pyqtSignal()
	signal_SelectAll       			= 	pyqtSignal()
	signal_UnSelectAll       		= 	pyqtSignal()
	signal_simpleTreeItemChange  	= 	pyqtSignal()
	signal_SimpleMenu  				= 	pyqtSignal()
	signal_complexTreeItemChange 	= 	pyqtSignal()
	signal_ComplexMenu 				= 	pyqtSignal()

	# Emisores de las señales anteriores.
	def emit_SaveProject(self):
		self.signal_SaveProject.emit()
	def emit_NewSimple(self):
		self.signal_NewSimple.emit()
	def emit_NewComplex(self):
		self.signal_NewComplex.emit()
	def emit_Undo(self):
		self.signal_Undo.emit()
	def emit_Redo(self):
		self.signal_Redo.emit()
	def emit_Minimalist(self):
		self.signal_Minimalist.emit()
	def emit_HideMenu(self):
		self.signal_HideMenu.emit()
	def emit_ZoomIn(self):
		self.signal_ZoomIn.emit()
	def emit_Zoom100(self):
		self.signal_Zoom100.emit()
	def emit_ZoomOut(self):
		self.signal_ZoomOut.emit()
	def emit_FullScreen(self):
		self.signal_FullScreen.emit()
	def emit_TrEs(self):
		self.signal_TrEs.emit()
	def emit_TrEn(self):
		self.signal_TrEn.emit()
	def emit_TrFr(self):
		self.signal_TrFr.emit()
	def emit_TrDe(self):
		self.signal_TrDe.emit()
	def emit_Name(self):
		self.signal_Name.emit()
	def emit_ZInc(self):
		self.signal_ZInc.emit()
	def emit_ZDec(self):
		self.signal_ZDec.emit()
	def emit_Active(self):
		self.signal_Active.emit()
	def emit_Visible(self):
		self.signal_Visible.emit()
	def emit_Delete(self):
		self.signal_Delete.emit()
	def emit_Resize(self,delta):
		self.signal_Resize.emit(delta)
	def emit_Details(self):
		self.signal_Details.emit()
	def emit_SelectAll(self):
		self.signal_SelectAll.emit()
	def emit_UnSelectAll(self):
		self.signal_UnSelectAll.emit()
	def emit_simpleTreeItemChange(self):
		self.signal_simpleTreeItemChange.emit()
	def emit_SimpleMenu(self):
		self.signal_SimpleMenu.emit()
	def emit_complexTreeItemChange(self):
		self.signal_complexTreeItemChange.emit()
	def emit_ComplexMenu(self):
		self.signal_ComplexMenu.emit()

	##
	## @brief      Constructor del objeto vista, que será la ventana principal.
	##
	## @param      self        Esta ventana.
	## @param      screenRect  Resolucion de la pantalla del usuario.
	##
	def __init__(self,screenRect):

		super().__init__()

		GUI.configWindow(self)

		# Guarda la resolucion de la pantalla del usuario.
		self.screenRect = screenRect

		# Estado anterior a Pantalla Completa.
		self._prevState = Qt.WindowStates

		# Emisores de las señales relacionadas con la aplicacion o proyecto.
		mainEmitters = [ self.emit_SaveProject,
						 self.emit_NewSimple,
						 self.emit_NewComplex,
						 self.close,
						 self.emit_SelectAll,
						 self.emit_UnSelectAll,
						 self.emit_Undo,
						 self.emit_Redo,
						 self.emit_Minimalist,
						 self.emit_ZoomIn,
						 self.emit_Zoom100,
						 self.emit_ZoomOut,
						 self.emit_FullScreen,
						 self.emit_TrEs,
						 self.emit_TrEn,
						 self.emit_TrFr,
						 self.emit_TrDe ]

		# Construir la GUI de la barra de menus.
		# Construir la GUI de la barra de tareas.
		# Lista de acciones ejectuables por dichas barras.
		menubar, self._toolbar, mainActions = GUI.mainBars()
		self.setMenuBar(menubar)
		self.addToolBar(self._toolbar)
		self.connectSignals(mainActions,mainEmitters)

		# Arbol de componentes simples.
		self._simpleTree = GUI.simpleTreeView(
			self.emit_simpleTreeItemChange, # Cuando cambia un valor.
			self.emit_SimpleMenu  # Pulsando boton derecho.
		)

		# Emisores de las señales relacionadas con componentes simples.
		simpleEmitters = [ self.emit_Name,
						   self.emit_ZInc,
						   self.emit_ZDec,
						   self.emit_Active,
						   self.emit_Visible,
						   self.emit_Delete,
						   self.emit_Details ]

		# Menu contextual arbol simple.
		self._simpleMenu, simpleActions = GUI.simpleMenu()
		self.connectSignals(simpleActions,simpleEmitters)

		# Arbol de componentes complejos.
		self._complexTree=GUI.complexTreeView(
			self.emit_complexTreeItemChange, # Cuando cambia un valor.
			self.emit_ComplexMenu  # Pulsando boton derecho.
		) # ........

		# Barra lateral.
		self._simpleDockbar = GUI.simpleDockBar( self._simpleTree )
		self.addDockWidget(Qt.LeftDockWidgetArea, self._simpleDockbar)
		self._complexDockbar = GUI.complexDockBar(self._complexTree)
		self.addDockWidget(Qt.LeftDockWidgetArea,self._complexDockbar)

		# Area de trabajo.
		_workArea = GUI.workArea(screenRect)
		self.setCentralWidget(_workArea)

		_statusbar = QStatusBar()
		self.setStatusBar(_statusbar)


# --------------------------------------------------------------------------- #


	##
	## @brief      Propiedad de lectura de la lista de componentes simples.
	##
	## @param      self  Esta ventana.
	##
	## @return     PyQt5.QtWidgets.QTreeView
	##
	@property
	def simpleTree(self):
		return self._simpleTree

	##
	## @brief      Propiedad de lectura del menu para componentes simples.
	##
	## @param      self  Esta ventana.
	##
	## @return     PyQt.QtWidgets.QMenu
	##
	@property
	def simpleMenu(self):
		return self._simpleMenu

	##
	## @brief      Propiedad de lectura de la lista de componentes complejos.
	##
	## @param      self  Esta ventana.
	##
	## @return     PyQt5.QtWidgets.QTreeView
	##
	@property
	def complexTree(self):
		return self._complexTree

	##
	## @brief      Propiedad de lectura del menu para componentes complejos.
	##
	## @param      self  Esta ventana.
	##
	## @return     PyQt.QtWidgets.QMenu
	##
	@property
	def complexMenu(self):
		return self._complexMenu

	##
	## @brief      Propiedad de lectura del 'viewport'.
	##
	## @param      self  Esta ventana.
	##
	## @return     PyQt.QtWidgets.QGraphicsView
	##
	@property
	def workArea(self):
		return self.centralWidget()

	##
	## @brief      Propiedad de lectura de la escena actual.
	##
	## @param      self  Esta ventana.
	##
	## @return     PyQt.QtWidgets.QGraphicsScene
	##
	@property
	def workScene(self):
		return self.centralWidget().scene()

	# !!!! APAÑO TEMPORAL !!!!
	def resetWorkScene(self):
		scale = self.scale
		workArea = GUI.workArea(self.screenRect)
		workArea.scale(scale,scale)
		self.setCentralWidget(workArea)

	##
	## @brief      Propiedad de lectura del area del lienzo.
	##
	## @param      self  Esta ventana.
	##
	## @return     PyQt5.QtCore.QRectF
	##
	@property
	def viewRectF(self):
		viewRect = self.centralWidget().rect()
		width  = viewRect.width() - viewRect.width()*pv['viewRectMargin']
		height = viewRect.height() - viewRect.height()*pv['viewRectMargin']
		return QRectF(0,0,width,height)

	##
	## @brief      Propiedad de lectura de la escala actual del area de trabajo.
	##
	## @param      self  Esta ventana.
	##
	## @return     qreal
	##
	@property
	def scale(self):
		return self.workArea.transform().m11()

	##
	## @brief      Propiedad de lectura del estado anterior de la ventana.
	##
	## @param      self  Esta ventana
	##
	## @return     PyQt5.QtCore.Qt.WindowStates
	##
	@property
	def prevState(self):
		return self._prevState

	##
	## @brief      Propiedad de escritura del estado anterior de la ventana.
	##
	## @param      self  Esta ventana.
	## @param      self  Estado a guardar.
	##
	## @return     None
	##
	@prevState.setter
	def prevState(self,prevState):
		self._prevState = prevState

	##
	## @brief      Conecta acciones dadas con los emisores corresondientes.
	##
	## @param      self      Esta ventana.
	## @param      actions   Lista de 'QAction's
	## @param      emitters  Lista de funciones.
	##
	## @return     None
	##
	def connectSignals(self,actions,emitters):
		for i in range(min(len(actions),len(emitters))):
			actions[i].triggered.connect(emitters[i])

	##
	## @brief      Restaura al estado anterior cuando se abre esta ventana.
	##
	## @param      self  Esta ventana
	##
	## @return     None
	##
	def openEvent(self):
		settings = QSettings("DCL", "PDT");
		prevRect = settings.value('rect')
		self.setGeometry(prevRect)

	##
	## @brief      Solicita confirmación al intentar cerrar la ventana.
	##
	## @param      self  Esta ventana.
	## @param      ev    El objeto con la informacion que da este evento.
	##
	## @return     None
	##
	def closeEvent(self,ev):
		settings = QSettings("DCL", "PDT");
		settings.setValue("rect", self.geometry());

		reply = GUI.exitDialog(self)
		if reply == QMessageBox.Ok:
			qDebug(pv['endMsg'])
			ev.accept()
		else:
			ev.ignore()

	##
	## @brief      Captura cuando se pulsa una o una combiancion de teclas.
	##
	## @param      self  Esta ventana.
	## @param      ev    El objeto con la informacion que da este evento.
	##
	## @return     None
	##
	def keyPressEvent(self,ev):
		if ev.key() == Qt.Key_Alt:
			self.emit_HideMenu()

		if ev.key() == Qt.Key_Shift and ev.key() == Qt.Key_Up:
			orig = self.workScene.sceneRect()
			orig.setY(orig.y()+25)
			self.workScene.setSceneRect(orig)

		if ev.key() == Qt.Key_Shift and ev.key() == Qt.Key_Down:
			orig = self.workScene.sceneRect()
			orig.setY(orig.y()-25)
			self.workScene.setSceneRect(orig)

			# if ev.key() == Qt.Key_Left:
			# 	orig = self.workScene.sceneRect()
			# 	orig.setX(orig.x()+25)
			# 	self.workScene.setSceneRect(orig)
			# if ev.key() == Qt.Key_Right:
			# 	orig = self.workScene.sceneRect()
			# 	orig.setX(orig.x()-25)
			# 	self.workScene.setSceneRect(orig)
		ev.accept()

