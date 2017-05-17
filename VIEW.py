#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import GUI
from SIMPLE import SimpleComponent as sc
from PresetValues import pv

## @brief      Clase encargada de la estructura visual de la aplicacion.
class VIEW( QMainWindow ):


# .---------.
# | Señales |
# -------------------------------------------------------------------------- #

	# File menu
	signal_SaveProject           	= 	pyqtSignal()
	signal_NewSimple             	= 	pyqtSignal()
	signal_NewComplex            	= 	pyqtSignal()
	# Edit menu
	signal_SelectAll       			= 	pyqtSignal()
	signal_UnSelectAll       		= 	pyqtSignal()
	signal_Undo                     =   pyqtSignal()
	signal_Redo                     =	pyqtSignal()
	# View menu
	signal_HideMenu                	= 	pyqtSignal()
	signal_Minimalist              	= 	pyqtSignal()
	signal_ZoomIn               	= 	pyqtSignal()
	signal_Zoom100               	= 	pyqtSignal()
	signal_ZoomOut               	= 	pyqtSignal()
	signal_FullScreen            	= 	pyqtSignal()
	signal_SceneCenter            	= 	pyqtSignal()
	# Simple menu
	signal_SimpleMenu  				= 	pyqtSignal()
	signal_Details         			= 	pyqtSignal()
	signal_Center          			= 	pyqtSignal()
	signal_Name            			= 	pyqtSignal()
	signal_ZInc            			= 	pyqtSignal()
	signal_ZDec            			= 	pyqtSignal()
	signal_Active          			= 	pyqtSignal()
	signal_Visible         			= 	pyqtSignal()
	signal_Delete          			= 	pyqtSignal()
	# Simple callbacks
	signal_Resize          			= 	pyqtSignal(int)
	signal_Move          			= 	pyqtSignal(QPointF,QPointF,sc)
	# Scene callbacks
	signal_SceneMove 				= 	pyqtSignal(QPointF,QPointF)
	signal_SelectArea 				= 	pyqtSignal(QRect)
	#Tree callbacks
	signal_ItemChanged              =   pyqtSignal(QStandardItem)


# .----------.
# | Emisores |
# -------------------------------------------------------------------------- #

	# File menu
	def emit_SaveProject(self):
		self.signal_SaveProject.emit()
	def emit_NewSimple(self):
		self.signal_NewSimple.emit()
	def emit_NewComplex(self):
		self.signal_NewComplex.emit()
	# Edit menu
	def emit_SelectAll(self):
		self.signal_SelectAll.emit()
	def emit_UnSelectAll(self):
		self.signal_UnSelectAll.emit()
	def emit_Undo(self):
		self.signal_Undo.emit()
	def emit_Redo(self):
		self.signal_Redo.emit()
	# View menu
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
	def emit_SceneCenter(self):
		self.signal_SceneCenter.emit()
	# Simple menu
	def emit_SimpleMenu(self):
		self.signal_SimpleMenu.emit()
	def emit_Details(self):
		self.signal_Details.emit()
	def emit_Center(self):
		self.signal_Center.emit()
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
	# Simple callbacks
	def emit_Resize(self,delta):
		self.signal_Resize.emit(delta)
	def emit_Move(self,posO,posD,sc):
		self.signal_Move.emit(posO,posD,sc)
	# Scene callbacks
	def emit_SceneMove(self,posO,posD):
		self.signal_SceneMove.emit(posO,posD)
	def emit_SelectArea(self,rect):
		self.signal_SelectArea.emit(rect)
	# Tree callbacks
	def emit_ItemChanged(self,item):
		self.signal_ItemChanged.emit(item)


# .-------------.
# | Constructor |
# -------------------------------------------------------------------------- #

	## @brief      Constructor del objeto vista, que será la ventana principal.
	## @param      self        Vista.
	## @param      screenRect  Resolucion de la pantalla del usuario.
	def __init__(self,screenRect):
		super().__init__()

		self.setGeometry(screenRect)

		# Configura el i18n ANTES de cargar interfaz.
		self.ok = GUI.configWindow(self)

		# Guarda la resolucion de la pantalla del usuario.
		self.screenRect = screenRect
		newWidth = self.screenRect.width()*pv['viewRectMargin']
		newHeight = self.screenRect.height()*pv['viewRectMargin']
		self.screenRect.setWidth(newWidth)
		self.screenRect.setHeight(newHeight)

		# Estado anterior a Pantalla Completa.
		self.__prevState = Qt.WindowStates

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
						 self.emit_SceneCenter ]

		# Construir la GUI de la barra de menus.
		# Construir la GUI de la barra de tareas.
		# Lista de acciones ejectuables por dichas barras.
		_menubar, self.__toolbar, mainActions = GUI.mainBars()
		self.setMenuBar(_menubar)
		self.addToolBar(Qt.LeftToolBarArea,self.__toolbar)
		self._connectSignals(mainActions,mainEmitters)

		# Arbol de componentes simples.
		self.__simpleTree = GUI.simpleTreeView( self.emit_ItemChanged,
		                                        self.emit_SimpleMenu )

		# Emisores de las señales relacionadas con componentes simples.
		simpleEmitters = [ self.emit_Details,
						   self.emit_Center,
						   self.emit_Name,
						   self.emit_ZInc,
						   self.emit_ZDec,
						   self.emit_Active,
						   self.emit_Visible,
						   self.emit_Delete ]

		# Menu contextual arbol simple.
		self.__simpleMenu, simpleActions = GUI.simpleMenu()
		self._connectSignals(simpleActions,simpleEmitters)

		# Arbol de componentes complejos.
		# self.__complexTree=GUI.complexTreeView(self.emit_ComplexMenu)

		# Barra lateral.
		self.__simpleDockbar = GUI.complexDockBar( self.__simpleTree )
		self.addDockWidget(Qt.RightDockWidgetArea, self.__simpleDockbar)
		# self.__complexDockbar = GUI.complexDockBar(self.__complexTree)
		# self.addDockWidget(Qt.LeftDockWidgetArea,self.__complexDockbar)

		# Area de trabajo.
		_workArea = GUI.workArea(self.screenRect)
		self.setCentralWidget(_workArea)

		_statusbar = QStatusBar()
		self.setStatusBar(_statusbar)


# .-------------------------------------------.
# | Acceso 'publico' a las variables privadas |
# -------------------------------------------------------------------------- #

	## @brief      Propiedad de lectura del estado anterior de la ventana.
	## @param      self  Esta ventana
	## @return     PyQt5.QtCore.Qt.WindowStates
	@property
	def prevState(self):
		return self.__prevState

	## @brief      Propiedad de escritura del estado anterior de la ventana.
	## @param      self  Vista.
	## @param      self  Estado a guardar.
	## @return     None
	@prevState.setter
	def prevState(self,prevState):
		self.__prevState = prevState

	## @brief      Propiedad de lectura de la lista de componentes simples.
	## @param      self  Vista.
	## @return     PyQt5.QtWidgets.QTreeView
	@property
	def simpleTree(self):
		return self.__simpleTree

	## @brief      Propiedad de lectura del menu para componentes simples.
	## @param      self  Vista.
	## @return     PyQt.QtWidgets.QMenu
	@property
	def simpleMenu(self):
		return self.__simpleMenu

	## @brief      Propiedad de lectura de la lista de componentes complejos.
	## @param      self  Vista.
	## @return     PyQt5.QtWidgets.QTreeView
	@property
	def complexTree(self):
		return self.__complexTree

	## @brief      Propiedad de lectura de la barra de herramientas.
	## @param      self  Vista.
	## @return     PyQt5.QtWidgets.QToolBar
	@property
	def toolbar(self):
		return self.__toolbar

	## @brief      Propiedad de lectura de la 'dockbar' simple.
	## @param      self  Vista.
	## @return     PyQt5.QtWidget.QDockWidget
	@property
	def simpleDockbar(self):
		return self.__simpleDockbar

	## @brief      Propiedad de lectura de la 'dockbar' compleja.
	## @param      self  Vista.
	## @return     PyQt5.QtWidget.QDockWidget
	@property
	def complexDockbar(self):
		return self.__complexDockbar

	## @brief      Propiedad de lectura del menu para componentes complejos.
	## @param      self  Vista.
	## @return     PyQt.QtWidgets.QMenu
	@property
	def complexMenu(self):
		return self.__complexMenu

	## @brief      Propiedad de lectura del 'viewport'.
	## @param      self  Vista.
	## @return     PyQt.QtWidgets.QGraphicsView
	@property
	def workArea(self):
		return self.centralWidget()

	## @brief      Propiedad de lectura de la escena actual.
	## @param      self  Vista.
	## @return     PyQt.QtWidgets.QGraphicsScene
	@property
	def workScene(self):
		return self.workArea.scene()

	## @brief      Propiedad de lectura de la escala del area de trabajo.
	## @param      self  Vista.
	## @return     qreal
	@property
	def scale(self):
		return self.workArea.transform().m11()


# .----------------------.
# | Funciones auxiliares |
# -------------------------------------------------------------------------- #

	## @brief      Conecta acciones dadas con los emisores corresondientes.
	## @param      self      Vista.
	## @param      actions   Lista de 'QAction's
	## @param      emitters  Lista de funciones.
	## @return     None
	def _connectSignals(self,actions,emitters):
		for i in range(min(len(actions),len(emitters))):
			actions[i].triggered.connect(emitters[i])

	## @brief      Borra el contenido de la escena.
	## @param      self  Vista.
	## @return     None
	def resetWorkScene(self):
		# Guardo la ubiacion y estado de la escena
		x = self.workScene.sceneRect().x()
		y = self.workScene.sceneRect().y()
		w = self.workScene.sceneRect().width()
		h = self.workScene.sceneRect().height()

		self.workScene.clear()

		rect = QRectF(self.screenRect)
		borderColor = Qt.black
		fillColor = QColor(pv['sceneColor'])
		self.workScene.addRect(rect,borderColor,fillColor)

		self.workScene.setSceneRect(x,y,w,h)


# .-----------------------.
# | Sobrecarga de eventos |
# -------------------------------------------------------------------------- #

	## @brief      Solicita confirmación al intentar cerrar la ventana.
	## @param      self  Vista.
	## @param      ev    El objeto con la informacion que da este evento.
	## @return     None
	# def closeEvent(self,ev):
	# 	reply = GUI.exitDialog(self)
	# 	if reply == QMessageBox.Ok:
	# 		qDebug(pv['endMsg'])
	# 		ev.accept()
	# 	else:
	# 		ev.ignore()

	## @brief      Captura cuando se pulsa una o una combiancion de teclas.
	## @param      self  Vista.
	## @param      ev    El objeto con la informacion que da este evento.
	## @return     None
	def keyReleaseEvent(self,ev):
		if ev.key() == Qt.Key_Alt: # Al pulsar la tecla Alt.
			self.emit_HideMenu()   # Se Oculta/Muestra la barra de menús.
