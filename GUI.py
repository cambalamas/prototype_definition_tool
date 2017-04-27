#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, i18n
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *



# Ruta de los iconos.
icoPath = os.path.join(os.path.dirname(__file__),'Icons')


# Genera un QIcon a partir del nombre de la imagen.
def icon(name):
	return QIcon(os.path.join(icoPath,name))


# Establece el logo y el titulo a la ventana.
def configWindow(window):
	# Icono del dock.
	window.setWindowIcon(icon('logo.png'))
	# Titulo de la ventana.
	window.setWindowTitle(i18n.t('E.title'))

##
# DIALOGO DE ENTRADA.
##


##
# DIALOGO DE SALIDA.
##

def exitDialog(view):
	return QMessageBox.question( view,
						  		 '¡CONFIRMAR!',
						  		 '¿Seguro que quieres salir?',
						  		 QMessageBox.Ok | QMessageBox.No,
						  		 QMessageBox.No ) # <--- Por defecto.


##
# MENU CONTEXTUAL DE ARBOLES.
##

def simpleTreeViewMenu():
	return QMenu('MENU: Arbol de componentes simples')

def complexTreeViewMenu():
	return QMenu('MENU: Arbol de componentes complejos')


##
# BARRA DE MENUS.
##

def statusBar():
	return QStatusBar()

def toolBar():
	return QToolBar('HERRAMIENTAS')

def menuBar():
	menubar = QMenuBar()
	menubar.setNativeMenuBar(True)
	return menubar

def menuFile(view):
	return view.menuBar().addMenu('Archivo')

def menuView(view):
	return view.menuBar().addMenu('Vista')

def menuHelp(view):
	return view.menuBar().addMenu('Ayuda')


##
# ACCIONES BARRA DE MENUS.
##

def saveProjectAction(menu,emitter):
	act = menu.addAction(i18n.t('E.save'))
	act.setShortcut(QKeySequence.Save)
	act.setIcon(icon('saveProject.ico'))
	act.setStatusTip('Guarda el estado del proyecto.')
	act.triggered.connect(emitter)
	return act

def newCompSimpleAction(menu,emitter):
	act = menu.addAction('Nuevo Componente(s) simple(s)')
	act.setShortcut('Ctrl+I')
	act.setIcon(icon('simpleComp.ico'))
	act.setStatusTip('Crea un componente simple en base a una imagen.')
	act.triggered.connect(emitter)
	return act

def newCompComplexAction(menu,emitter):
	act = menu.addAction('Nuevo Componente complejo')
	act.setShortcut('Ctrl+Shift+I')
	act.setIcon(icon('complexComp.ico'))
	act.setStatusTip('Crea un componente complejo en base a varias imgs.')
	act.triggered.connect(emitter)
	return act

def closeAction(menu,emitter):
	act = menu.addAction('Salir (!)')
	act.setShortcut(QKeySequence.Close)
	act.setIcon(icon('appExit.ico'))
	act.setStatusTip('Cierra la aplicacion...')
	act.triggered.connect(emitter)
	return act


def hideMenuAction(menu,emitter):
	act = menu.addAction('Ocultar menu')
	act.setCheckable(True)
	act.setShortcut('Ctrl+H')
	act.setIcon(icon('hideMenu.ico'))
	act.setStatusTip('Oculta la barra de menu. (Visualizable con [ALT]')
	act.triggered.connect(emitter)
	return act

def zoomInAction(menu,emitter):
	act = menu.addAction('Zoom +')
	act.setShortcut(QKeySequence.ZoomIn)
	act.setIcon(icon('zoomIn.ico'))
	act.setStatusTip('Incrementa el zoom de la escena.')
	act.triggered.connect(emitter)
	return act

def zoom100Action(menu,emitter):
	act = menu.addAction('Zoom 100%')
	act.setShortcut('Ctrl+0')
	act.setIcon(icon('zoom100.ico'))
	act.setStatusTip('Restablece el zoom de la escena.')
	act.triggered.connect(emitter)
	return act

def zoomOutAction(menu,emitter):
	act = menu.addAction('Zoom -')
	act.setShortcut(QKeySequence.ZoomOut)
	act.setIcon(icon('zoomOut.ico'))
	act.setStatusTip('Decrementa el zoom de la escena.')
	act.triggered.connect(emitter)
	return act

def fullScreenAction(menu,emitter):
	act = menu.addAction('Pantalla completa')
	act.setCheckable(True)
	act.setShortcut(QKeySequence.FullScreen)
	act.setIcon(icon('fullScreen.ico'))
	act.setStatusTip('Rota entre pantalla completa y el estado anterior.')
	act.triggered.connect(emitter)
	return act


def trEsAction(menu,emitter):
	act = menu.addAction('Traducir a Español')
	act.setCheckable(True)
	act.setIcon(icon('trES.ico'))
	act.setStatusTip('Traduce los textos de la app a Español')
	act.triggered.connect(emitter)
	return act

def trEnAction(menu,emitter):
	act = menu.addAction('Traducir a Ingles')
	act.setCheckable(True)
	act.setIcon(icon('trEN.ico'))
	act.setStatusTip('Traduce los textos de la app a Ingles')
	act.triggered.connect(emitter)
	return act

def trFrAction(menu,emitter):
	act = menu.addAction('Traducir a Frances')
	act.setCheckable(True)
	act.setIcon(icon('trFR.ico'))
	act.setStatusTip('Traduce los textos de la app a Frances')
	act.triggered.connect(emitter)
	return act

def trDeAction(menu,emitter):
	act = menu.addAction('Traducir a Aleman')
	act.setCheckable(True)
	act.setIcon(icon('trDE.ico'))
	act.setStatusTip('Traduce los textos de la app a Aleman')
	act.triggered.connect(emitter)
	return act


##
# ACCIONES COMP SIMPLE.
##

def simpleZIncAction(menu,emitter):
	act = menu.addAction('INCREMENTA Profundidad')
	act.triggered.connect(emitter)

def simpleZDecAction(menu,emitter):
	act = menu.addAction('DECREMENTA Profundidad')
	act.triggered.connect(emitter)

def simpleToggleActiveAction(menu,emitter):
	act = menu.addAction('Rota estado: ACTIVO')
	act.setCheckable(True)
	act.triggered.connect(emitter)

def simpleToggleVisibleAction(menu,emitter):
	act = menu.addAction('Rota estado: VISIBLE')
	act.setCheckable(True)
	act.triggered.connect(emitter)

def simpleDeleteAction(menu,emitter):
	act = menu.addAction('BORRA el elemento')
	act.triggered.connect(emitter)

def simpleDetailAction(menu,emitter):
	act = menu.addAction('Informacion detallada...')
	act.triggered.connect(emitter)


##
# WIDGETS.
##

def simpleTreeView(*emitters):
	header = ['Nombre', 'Visb.', 'Act.', 'Z']
	return treeView(header,*emitters)

def complexTreeView(*emitters):
	header = ['Nombre']
	return treeView(header,*emitters)

def simpleDockBar(widget):
	title = 'COMPONENTES SIMPLES'
	return dockBar(title,widget)

def complexDockBar(widget):
	title = 'COMPONENTES COMPLEJOS'
	return dockBar(title,widget)



##
# CONSTRUCTORES DE WIDGETS.
##


""" Constructor con ciertas propiedades ya configuradas de un 'QDockWidget',
estas widgets se caracterizan por poderse anclar en cualquier borde de
la pantalla"""

def dockBar(title,widget):
	dockbar = QDockWidget(title)
	dockbar.setWidget(widget)

	# Limitamos su anclaje a los laterales.
	dockbar.setAllowedAreas( Qt.LeftDockWidgetArea
	                         | Qt.RightDockWidgetArea )
	return dockbar


""" Constructor con ciertas propiedades ya configuradas de un 'TreeView' """

def treeView(header,*emitters):
	tree = QTreeView()
	model = QStandardItemModel()

	# Asigna el modelo a la vista.
	tree.setModel(model)

	# Propiedades del modelo.
	model.setHorizontalHeaderLabels(header)
	model.itemChanged.connect(emitters[0])

	# Propiedades del cabecero.
	tree.header().resizeSection(1,44)
	tree.header().resizeSection(2,38)
	tree.header().resizeSection(3,30)

	'''Propiedades del arbol. '''

	# Señal de menu contextual.
	tree.customContextMenuRequested.connect(emitters[1])
	# Menu contextual solicitado por señal.
	tree.setContextMenuPolicy(Qt.CustomContextMenu)
	# Oculta las flechas de hijos.
	tree.setRootIsDecorated(False)
	# No permite expandir los hijos.
	tree.setItemsExpandable(False)
	# Iguala la altura de las filas.
	tree.setUniformRowHeights(True)
	# Dibuja el recuadro de seleccion en toda la fila.
	tree.setSelectionBehavior(QAbstractItemView.SelectRows)
	# Solo permite seleccionar un elemento a la vez.
	tree.setSelectionMode(QAbstractItemView.SingleSelection)

	return tree
