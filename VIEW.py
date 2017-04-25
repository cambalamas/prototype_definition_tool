#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import GUI
import os, sys, i18n
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal

i18n.load_path.append(os.path.join(os.path.dirname(__file__),'Translations'))


class VIEW( QMainWindow ):

	def __init__(self):
		super().__init__()

		GUI.configWindow(self)


		# ----------------------------------------------------------------- #
		#						 CLASE :: VARIABLES 						#
		#					(deberia guardarse en el model?)				#
		# ----------------------------------------------------------------- #

		# Control del factor de escalado.
		self.__viewScale = 1.0
		self.__viewScaleMOD = 1.1
		self.__viewScaleMAX = 15.0
		self.__viewScaleMIN = 0.05

		# Guarda el estado anterior de la ventana.
		self.__previousWindowState = str()


		# ----------------------------------------------------------------- #
		#								SEÑALES								#
		# ----------------------------------------------------------------- #

		self.signal_SaveProject           	= 	pyqtSignal()
		self.signal_NewSimple             	= 	pyqtSignal()
		self.signal_NewComplex            	= 	pyqtSignal()
		self.signal_Close                 	= 	pyqtSignal()

		self.signal_ZoomIn                	= 	pyqtSignal()
		self.signal_ZoomOut               	= 	pyqtSignal()
		self.signal_Zoom100               	= 	pyqtSignal()
		self.signal_FullScreen            	= 	pyqtSignal()

		self.signal_TrEs                  	= 	pyqtSignal()
		self.signal_TrEn                  	= 	pyqtSignal()
		self.signal_TrFr                  	= 	pyqtSignal()
		self.signal_TrDe                  	= 	pyqtSignal()

		self.signal_SimpleZInc            	= 	pyqtSignal()
		self.signal_SimpleZDec            	= 	pyqtSignal()
		self.signal_SimpleActive          	= 	pyqtSignal()
		self.signal_SimpleVisible         	= 	pyqtSignal()
		self.signal_SimpleDelete          	= 	pyqtSignal()
		self.signal_SimpleDetail          	= 	pyqtSignal()

		self.signal_simpleTreeItemChange  	= 	pyqtSignal()
		self.signal_simpleTreeInvokeMenu  	= 	pyqtSignal()

		self.signal_complexTreeItemChange 	= 	pyqtSignal()
		self.signal_complexTreeInvokeMenu 	= 	pyqtSignal()


		# ----------------------------------------------------------------- #
		#						GUI :: BARRA DE MENUS 						#
		# ----------------------------------------------------------------- #

		_menubar = QMenuBar()
		self.setMenuBar(_menubar)

		''' MENU: Archivo. '''
		_mFile = self.menuBar().addMenu('Archivo')
		# Guardar proyecto.
		_save = GUI.saveProjectAction( _mFile, self._emit_SaveProject )
		# Nuevo componente simple.
		_newSimple = GUI.newCompSimpleAction( _mFile, self._emit_NewSimple )
		# Nuevo componente complejo.
		_newComplex = GUI.newCompComplexAction( _mFile, self._emit_NewComplex )
		# Salir de la app.
		_exit = GUI.closeAction( _mFile, self._emit_Close )

		''' MENU: Vista. '''
		_mView = self.menuBar().addMenu('Vista')
		# Aumetar zoom.
		_zoomIn = GUI.zoomInAction( _mView, self._emit_ZoomIn )
		# Disminuir zoom.
		_zoomOut = GUI.zoomOutAction( _mView, self._emit_ZoomOut )
		# Restablece el zoom.
		_zoom100 = GUI.zoom100Action( _mView, self._emit_Zoom100 )
		# Rota entre pantalla completa y el estado anterior.
		_fullScreen = GUI.fullScreenAction( _mView, self._emit_FullScreen )

		''' MENU: Ayuda. '''
		_mHelp = self.menuBar().addMenu('Ayuda')
		# Traducir a Español.
		_trEsAction = GUI.trEsAction( _mHelp, self._emit_TrEs )
		# Traducir a Ingles.
		_trEnAction = GUI.trEnAction( _mHelp, self._emit_TrEn )
		# Traducir a Frances.
		_trFrAction = GUI.trFrAction( _mHelp, self._emit_TrFr )
		# Traducir a Aleman.
		_trDeAction = GUI.trDeAction( _mHelp, self._emit_TrDe )
		# Convierte estas acciones a seleccion exclusiva.
		_mHelpGroup = QActionGroup(_mHelp)
		_mHelpGroup.addAction(_trEsAction)
		_mHelpGroup.addAction(_trEnAction)
		_mHelpGroup.addAction(_trFrAction)
		_mHelpGroup.addAction(_trDeAction)


		# ----------------------------------------------------------------- #
		#					GUI :: BARRA DE HERRAMIENTAS 					#
		# ----------------------------------------------------------------- #

		_toolbar = QToolBar('HERRAMIENTAS')
		self.addToolBar(_toolbar)

		# Guardar proyecto.
		_toolbar.addAction(_save)


		# ----------------------------------------------------------------- #
		#					  GUI :: AREA DE TRABAJO 						#
		# ----------------------------------------------------------------- #

		# QGraphicsView, otorga ventajas como Escala y Profundidad.
		_workArea = QGraphicsView()
		_workArea.setBackgroundBrush(Qt.gray)
		self.setCentralWidget(_workArea)

		# Escena a la que se agregaran los Items con los que trabajamos.
		_workAreaScene = QGraphicsScene(_workArea)
		self.centralWidget().setScene(_workAreaScene)


		# ----------------------------------------------------------------- #
		#					  GUI :: BARRA DE ESTADO 						#
		# ----------------------------------------------------------------- #

		_statusbar = QStatusBar()
		self.setStatusBar(_statusbar)


		# ----------------------------------------------------------------- #
		#				GUI :: MENU CONTEXTUAL ARBOL SIMPLE					#
		# ----------------------------------------------------------------- #

		self._simpleTreeMenu = QMenu('MENU: Arbol de componentes')

		# Incrementar profundidad del objeto.
		GUI.simpleZIncAction( self._simpleTreeMenu,
		                      self._emit_SimpleZInc )

		# Decrementar profundidad del objeto.
		GUI.simpleZDecAction( self._simpleTreeMenu,
		                      self._emit_SimpleZDec )

		self._simpleTreeMenu.addSeparator() # Dibuja una linea horizontal.

		# Activa / Desactiva el objeto.
		GUI.simpleToggleActiveAction( self._simpleTreeMenu,
		                              self._emit_SimpleActive )

		# ACCION: Muestra / Oculta el objeto.
		GUI.simpleToggleVisibleAction( self._simpleTreeMenu,
		                               self._emit_SimpleVisible )

		self._simpleTreeMenu.addSeparator() # Dibuja una linea horizontal.

		# Borra el objeto de la escena y el modelo.
		GUI.simpleDeleteAction( self._simpleTreeMenu,
		                        self._emit_SimpleDelete )

		self._simpleTreeMenu.addSeparator() # Dibuja una linea horizontal.

		# Muestra un pop-up con los detalles del objeto.
		GUI.simpleDetailAction( self._simpleTreeMenu,
		                        self._emit_SimpleDetail )


		# ----------------------------------------------------------------- #
		#				   			GUI :: ARBOLES 							#
		# ----------------------------------------------------------------- #

		# Arbol de componentes simples.
		_simpleHeader = ['Nombre', 'Visb.', 'Act.', 'Z']
		self.__simpleTree = GUI.treeView( _simpleHeader,
		                                  self._emit_simpleTreeItemChange,
		                                  self._emit_simpleTreeInvokeMenu )

		# Arbol de componentes complejos.
		_complexHeader = ['Nombre']
		self.__complexTree = GUI.treeView( _complexHeader,
	                                       self._emit_complexTreeItemChange,
		                                   self._emit_complexTreeInvokeMenu )


		# ----------------------------------------------------------------- #
		#					   GUI :: BARRA LATERAL 						#
		# ----------------------------------------------------------------- #

		_simpleDockbar = GUI.dockBar( 'COMPONENTES SIMPLES',
		                              self.__simpleTree )

		_complexDockbar = GUI.dockBar( 'COMPONENTES COMPLEJOS',
		                               self.__complexTree )

		self.addDockWidget(Qt.LeftDockWidgetArea, _simpleDockbar)

		self.addDockWidget(Qt.LeftDockWidgetArea, _complexDockbar)


	# ----------------------------------------------------------------- #
	#							 GUI :: 'GETTERS' 						#
	# ----------------------------------------------------------------- #

	def getSimpleTree():
		return self.__simpleTree

	def getComplexTree():
		return self.__complexTree

	def getWorkArea():
		return self.centralWidget()

	def getScene():
		return self.centralWidget().scene()


	# ----------------------------------------------------------------- #
	#					  	- CONECTAR SEÑALES -						#
	# ----------------------------------------------------------------- #

	def _emit_SaveProject(self):
		self.signal_SaveProject.emit()

	def _emit_NewSimple(self):
		self.signal_NewSimple.emit()

	def _emit_NewComplex(self):
		self.signal_NewComplex.emit()

	def _emit_Close(self):
		self.signal_Close.emit()

	def _emit_ZoomIn(self):
		self.signal_ZoomIn.emit()

	def _emit_ZoomOut(self):
		self.signal_ZoomOut.emit()

	def _emit_Zoom100(self):
		self.signal_Zoom100.emit()

	def _emit_FullScreen(self):
		self.signal_FullScreen.emit()

	def _emit_TrEs(self):
		self.signal_TrEs.emit()

	def _emit_TrEn(self):
		self.signal_TrEn.emit()

	def _emit_TrFr(self):
		self.signal_TrFr.emit()

	def _emit_TrDe(self):
		self.signal_TrDe.emit()

	def _emit_SimpleZInc(self):
		self.signal_SimpleZInc.emit()

	def _emit_SimpleZDec(self):
		self.signal_SimpleZDec.emit()

	def _emit_SimpleActive(self):
		self.signal_SimpleActive.emit()

	def _emit_SimpleVisible(self):
		self.signal_SimpleVisible.emit()

	def _emit_SimpleDelete(self):
		self.signal_SimpleDelete.emit()

	def _emit_SimpleDetail(self):
		self.signal_SimpleDetail.emit()

	def _emit_simpleTreeItemChange(self):
		self.signal_simpleTreeItemChange.emit()

	def _emit_simpleTreeInvokeMenu(self):
		self.signal_simpleTreeInvokeMenu.emit()

	def _emit_complexTreeItemChange(self):
		self.signal_complexTreeItemChange.emit()

	def _emit_complexTreeInvokeMenu(self):
		self.signal_complexTreeInvokeMenu.emit()


################### UNDO y REDO EN EL MENU DE EDIT!!!
