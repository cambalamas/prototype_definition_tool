#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, i18n
from lxml import etree

from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import ELogic
from Inherits.ETreeView import ETreeView

i18n.load_path.append(os.path.join(os.path.dirname(__file__),'Translations'))


class EMainWindow( QMainWindow ):
	def __init__(self):
		super().__init__()


		# ----------------------------------------------------------------- #
		#						  CONFIGURACIONES 							#
		# ----------------------------------------------------------------- #

		# Titulo de la ventana.
		self.setWindowTitle('E!')

		# Ruta de los iconos.
		self.icoPath = os.path.join(os.path.dirname(__file__),'Icons')

		# Icono que se vera etn la barra de tareas, dock, etc.
		self.setWindowIcon(QIcon( os.path.join(self.icoPath, 'logo.png') ))


		# ----------------------------------------------------------------- #
		#						 CLASE :: VARIABLES 						#
		# ----------------------------------------------------------------- #

		# Control del factor de escalado.
		self.__viewScale = 1.0
		self.__viewScaleMOD = 1.1
		self.__viewScaleMAX = 15.0
		self.__viewScaleMIN = 0.05

		# Guarda el estado anterior de la ventana.
		self.__previousWindowState = str()


		# ----------------------------------------------------------------- #
		#						GUI :: BARRA DE MENUS 						#
		# ----------------------------------------------------------------- #

		self.menubar = QMenuBar()
		self.setMenuBar(self.menubar)

		# MENU: Archivo.
		mFile = self.menubar.addMenu('Archivo')

		## Archivo - ACCION: Guardar proyecto.
		mAct = mFile.addAction('Guardar proyecto')
		mAct.setShortcut('Ctrl+S')
		mAct.setStatusTip('Guarda el estado del proyecto.')
		mAct.triggered.connect(self.saveProject)

		## Archivo - ACCION: Nuevo comp simple.
		mAct = mFile.addAction('Nuevo Componente(s) simple(s)')
		mAct.setShortcut('Ctrl+I')
		mAct.setStatusTip('Crea un componente simple en base a una imagen.')
		mAct.triggered.connect(self.newSimpleComp)

		## Archivo - ACCION: Nuevo comp complejo.
		mAct = mFile.addAction('Nuevo Componente complejo')
		mAct.setShortcut('Ctrl+Shift+I')
		mAct.setStatusTip('Crea un componente complejo en base a varias imgs.')
		# mAct.triggered.connect(self.newComplex) #TODO

		## Archivo - ACCION: Salir de la app.
		mAct = mFile.addAction('Salir (!)')
		mAct.setShortcut(QKeySequence.Close)
		mAct.setStatusTip('Cierra la aplicacion...')
		mAct.triggered.connect(self.close)

		# MENU: Vista.
		mView = self.menubar.addMenu('Vista')

		## Vista - ACCION: Aumetar zoom.
		mAct = mView.addAction('Zoom +')
		mAct.setShortcut('Ctrl++')
		mAct.setStatusTip('Incrementa el zoom de la escena.')
		mAct.triggered.connect(self.zoomIn)

		## Vista - ACCION: Disminuir zoom.
		mAct = mView.addAction('Zoom -')
		mAct.setShortcut('Ctrl+-')
		mAct.setStatusTip('Decrementa el zoom de la escena.')
		mAct.triggered.connect(self.zoomOut)

		## Vista - ACCION: Restablece el zoom.
		mAct = mView.addAction('Zoom 100%')
		mAct.setShortcut('Ctrl+0')
		mAct.setStatusTip('Restablece el zoom de la escena.')
		mAct.triggered.connect(self.zoom100)

		## Vista - ACCION: Rota entre pantalla completa y el estado anterior.
		mAct = mView.addAction('Pantalla completa')
		mAct.setCheckable(True)
		mAct.setShortcut('F11')
		mAct.setStatusTip('Rota entre pantalla completa y el estado anterior.')
		mAct.triggered.connect(self.fullScreen)

		# MENU: Ayuda.
		mHelp = self.menubar.addMenu('Ayuda')
		helpGroup = QActionGroup(mHelp)

		## Ayuda - ACCION: Traducir a Español.
		mAct = mHelp.addAction('Traducir a Español')
		mAct.setCheckable(True)
		mAct.setStatusTip('Traduce los textos de la app a Español')
		# mAct.triggered.connect(self.tr_ES)
		helpGroup.addAction(mAct)

		## Ayuda - ACCION: Traducir a Ingles.
		mAct = mHelp.addAction('Traducir a Ingles')
		mAct.setCheckable(True)
		mAct.setStatusTip('Traduce los textos de la app a Ingles')
		# mAct.triggered.connect(self.tr_ES)
		helpGroup.addAction(mAct)

		## Ayuda - ACCION: Traducir a Frances.
		mAct = mHelp.addAction('Traducir a Frances')
		mAct.setCheckable(True)
		mAct.setStatusTip('Traduce los textos de la app a Frances')
		# mAct.triggered.connect(self.tr_ES)
		helpGroup.addAction(mAct)

		## Ayuda - ACCION: Traducir a Aleman.
		mAct = mHelp.addAction('Traducir a Aleman')
		mAct.setCheckable(True)
		mAct.setStatusTip('Traduce los textos de la app a Aleman')
		# mAct.triggered.connect(self.tr_ES)
		helpGroup.addAction(mAct)


		# ----------------------------------------------------------------- #
		#					GUI :: BARRA DE HERRAMIENTAS 					#
		# ----------------------------------------------------------------- #

		self.toolbar = QToolBar('HERRAMIENTAS')
		self.addToolBar(self.toolbar)

		# ACCION: Guardar proyecto.
		tAct = self.toolbar.addAction('')
		tAct.setIcon(QIcon( os.path.join(self.icoPath, 'save.png') ))
		tAct.setIconText('Guardar proyecto')
		tAct.setStatusTip('Guarda el estado del proyecto.')
		tAct.triggered.connect(self.newSimpleComp)


		# ----------------------------------------------------------------- #
		#					  GUI :: AREA DE TRABAJO 						#
		# ----------------------------------------------------------------- #

		# QGraphicsView, otorga ventajas como Escala y Profundidad.
		self.workArea = QGraphicsView()
		self.workArea.setBackgroundBrush(Qt.gray)
		self.setCentralWidget( self.workArea )

		# Escena a la que se agregaran los Items con los que trabajamos.
		workAreaScene = QGraphicsScene(self.workArea)
		self.workArea.setScene(workAreaScene)


		# ----------------------------------------------------------------- #
		#					  GUI :: BARRA DE ESTADO 						#
		# ----------------------------------------------------------------- #

		self.statusbar = QStatusBar()
		self.setStatusBar(self.statusbar)


		# ----------------------------------------------------------------- #
		#				   GUI :: ARBOL COMPONENTES SIMPLES 				#
		# ----------------------------------------------------------------- #

		# Arbol de componentes: VISTA.
		self.simpleCompsTree = ETreeView()

		# Arbol de componentes: MODELO.
		compsModel = QStandardItemModel()

		# Asigna el modelo a la vista.
		self.simpleCompsTree.setModel(compsModel)

		# Propiedades del modelo qt para el arbol.
		simpleCompTreeHeader = ['Nombre', 'Visb.', 'Act.', 'Z']
		compsModel.setHorizontalHeaderLabels(simpleCompTreeHeader)
		compsModel.itemChanged.connect(self.simpleCompsTreeItemChanged)

		# Arbol de componentes: CABECERO.
		self.simpleCompsTree.header().resizeSection(1,44)
		self.simpleCompsTree.header().resizeSection(2,38)
		self.simpleCompsTree.header().resizeSection(3,30)


		# ----------------------------------------------------------------- #
		#					   GUI :: BARRA LATERAL 						#
		# ----------------------------------------------------------------- #

		self.dockbar = QDockWidget('INFORMACION')
		self.addDockWidget(Qt.RightDockWidgetArea, self.dockbar)

		# Define las areas permitidas.
		self.dockbar.setAllowedAreas( Qt.LeftDockWidgetArea
		                              | Qt.RightDockWidgetArea )

		# Contenedor visual.
		sideLayout = QVBoxLayout()
		# Agrega el arbol al Layout.
		sideLayout.addWidget( QLabel('COMPONENTES SIMPLES') )
		sideLayout.addWidget( self.simpleCompsTree )

		# Agrega a la dockbar el widget que contiene el layout.
		toDock = QWidget()
		toDock.setLayout(sideLayout)
		self.dockbar.setWidget(toDock)


	# ----------------------------------------------------------------- #
	#						 CLASE :: 'GETTERS' 						#
	# ----------------------------------------------------------------- #

	def getScale(self):
		return self.__viewScale
	def getScaleMod(self):
		return self.__viewScaleMOD
	def getScaleMax(self):
		return self.__viewScaleMAX
	def getScaleMin(self):
		return self.__viewScaleMIN
	def getPrevWindowState(self):
		return self.__previousWindowState


	# ----------------------------------------------------------------- #
	#						 CLASE :: 'SETTERS' 						#
	# ----------------------------------------------------------------- #

	def setScale(self, newVal):
		self.__viewScale = newVal
	def setPrevWindowState(self,newVal):
		self.__previousWindowState = newVal


	# ----------------------------------------------------------------- #
	#					  	- CONECTAR SEÑALES -						#
	# ----------------------------------------------------------------- #

	def simpleCompsTreeItemChanged(self):
		ELogic.simpleCompsTreeItemChanged(self)


	# ----------------------------------------------------------------- #
	#						INTERACCION :: EVENTOS 						#
	# ----------------------------------------------------------------- #

	'''
	Controla el cierre de la app preguntand al usuario si esta seguro.
	'''
	def closeEvent(self, ev):
		reply = QMessageBox.question( self,
									  '¡CONFIRMAR!',
									  '¿Seguro que quieres salir?',
									  QMessageBox.Ok | QMessageBox.No,
									  QMessageBox.No )
		if reply == QMessageBox.Ok:
			ev.accept()
		else:
			ev.ignore()

	'''
	Controla la presion de teclas o combinaciones.
	'''
	def keyPressEvent(self, ev):

		if ev.matches(QKeySequence.Undo):
			ELogic.getPrevState(self)

		if ev.matches(QKeySequence.Redo):
			ELogic.getNextState(self)


	# ----------------------------------------------------------------- #
	#		   INTERACCION :: FUNCIONES QUE AFECTAN AL PROYECTO			#
	# ----------------------------------------------------------------- #

	'''
	Guarda el estado del proyecto.
	'''
	def saveProject(self):
		ELogic.saveProject()


	# ----------------------------------------------------------------- #
	#					  INTERACCION :: MENU ARCHIVO					#
	# ----------------------------------------------------------------- #

	'''
	Abre un cuadro de dialogo para que el usuario seleccione las imagenes que
	quiera en cualquier formato rasterizado como BMP, JPG o el preferido, PNG.
	'''
	def newSimpleComp(self):
		# El metodo multiplataforma de obtener el 'HOME' del usuario.
		home = os.path.expanduser('~')
		# Recogemos las imagenes seleccionadas del cuadro de dialogo.
		imgPathsSet = QFileDialog.getOpenFileNames(self, 'Pick imgs!', home)
		# Pasamos las rutas recogidas al Controlador.
		ELogic.newSimpleComp(imgPathsSet,self)


	# ----------------------------------------------------------------- #
	#						INTERACCION :: MENU VISTA					#
	# ----------------------------------------------------------------- #

	'''
	Aumenta la escala de la escena.
	'''
	def zoomIn(self):
		mod = self.getScaleMod()
		# Calculamos la escala resultante de decrementar.
		inc = self.getScale() * mod

		# Si no pasamos el minimo permitido.
		if inc < self.getScaleMax():
			# Reducimos la escala en base al factor de escalado.
			self.centralWidget().scale(mod,mod)
			# Actualizamos la variable de control.
			self.setScale(inc)

		# Notificamos el zoom actual en la barra de estado.
		self.statusBar().showMessage('ZOOM: '+str(100*self.getScale())+'%')


	'''
	Disminuye la escala de la escena.
	'''
	def zoomOut(self):
		mod = self.getScaleMod()
		# Calculamos la escala resultante de decrementar.
		dec = self.getScale() / mod

		# Si no pasamos el minimo permitido.
		if dec > self.getScaleMin():
			# Reducimos la escala en base al factor de escalado.
			self.centralWidget().scale(1/mod,1/mod)
			# Actualizamos la variable de control.
			self.setScale(dec)

		# Notificamos el zoom actual en la barra de estado.
		self.statusBar().showMessage('ZOOM: '+str(100*self.getScale())+'%')


	'''
	Restaurar el nivel de Zoom al 100%
	'''
	def zoom100(self):
		scale = self.getScale()
		# Realizamos el reset en base a la escala actual.
		self.centralWidget().scale(1/scale,1/scale)
		# Actualizamos la variable de control.
		self.setScale(scale/scale)
		# Notificamos el zoom actual en la barra de estado.
		self.statusBar().showMessage('ZOOM: '+str(100)+'%')


	'''
	Sencillo -toggle- para cambiar entre la vista de pantalla completa y
	la que anteriormente establecida.
	'''
	def fullScreen(self):
		# Si esta en pantalla completa.
		if self.isFullScreen():

			# Restauro al estado antes guardado.
			if self.getPrevWindowState() == 'maximized':
				self.showMaximized()
				self.statusBar().showMessage('VENTANA: Maximizada')
			else:
				self.showNormal()
				self.statusBar().showMessage('VENTANA: Normal')

		# Si no esta en pantalla completa
		else :
			# Guardo el estado actual.
			if self.isMaximized():
				self.setPrevWindowState('maximized')
			else:
				self.setPrevWindowState('normal')

			# Cambiamos la ventana a pantalla completa.
			self.showFullScreen()
			self.statusBar().showMessage('VENTANA: Pantalla Completa')



# ----------------------------------------------------------------- #
#					  	- PUNTO DE ENTRADA -						#
# ----------------------------------------------------------------- #

if __name__ == '__main__':

	# Instancia la app QT.
	app = QApplication(sys.argv)

	# Compone la ventana y sus interaciones.
	win = EMainWindow()

	# Muestra la ventana.
	win.showMaximized()

	# Espera la señal 'QT' de Cierre.
	sys.exit(app.exec_())
