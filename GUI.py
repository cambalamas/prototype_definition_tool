#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, i18n

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRectF

from PresetValues import pv

iconsPath = os.path.join(os.path.dirname(__file__),'Icons')
i18n.load_path.append(os.path.join(os.path.dirname(__file__),'Translations'))

##
## @brief      Genera un icono a partir del nombre de la imagen.
##
## @param      name  Nombre de la imagen.
##
## @return     PyQt5.QtGui.QIcon
##
def icon(name):
	return QIcon(os.path.join(iconsPath,name))

##
## @brief      Establece el icono y el titulo.
##
## @param      window  Ventana a configurar.
##
## @return     None
##
def configWindow(window):
	window.setWindowIcon(icon('logo.png'))		# Icono del dock.
	window.setWindowTitle(i18n.t('E.title'))	# Titulo de la ventana.

##
## @brief      Presenta un dialogo para confimar la salida de la app.
##
## @param      view  Ventana padre.
##
## @return     PyQt5.QtWidgets.QMessageBox
##
def exitDialog(view):
	return QMessageBox.question( view,
						  		 '¡CONFIRMAR!',
						  		 '¿Seguro que quieres salir?',
						  		 QMessageBox.Ok | QMessageBox.No,
						  		 QMessageBox.No ) # <--- Por defecto.

##
## @brief      Crea los componentes de menus de la ventana principal.
##
## @return     PyQt5.QtWidgets.QMenuBar
## @return     PyQt5.QtWidgets.QToolBar
## @return     list<PyQt5.QtWidgets.QAction>
##
def mainBars():
	mb = QMenuBar()
	mb.setNativeMenuBar(True)

	mFile = mb.addMenu('Archivo')
	mEdit = mb.addMenu('Editar')
	mView = mb.addMenu('Vista')
	mHelp = mb.addMenu('Ayuda')

	tb = QToolBar('Herramientas')

	actions = []

	act = mFile.addAction(i18n.t('E.save'))
	act.setShortcut(QKeySequence.Save)
	act.setIcon(icon('saveProject.ico'))
	act.setStatusTip('Guarda el estado del proyecto.')

	tb.addAction(act)
	mb.addSeparator()
	tb.addSeparator()
	actions.append(act)

	act = mFile.addAction('Nuevo Componente(s) simple(s)')
	act.setShortcut('Ctrl+I')
	act.setIcon(icon('simpleComp.ico'))
	act.setStatusTip('Crea un componente simple en base a una imagen.')

	tb.addAction(act)
	actions.append(act)

	act = mFile.addAction('Nuevo Componente complejo')
	act.setShortcut('Ctrl+Shift+I')
	act.setIcon(icon('complexComp.ico'))
	act.setStatusTip('Crea un componente complejo en base a varias imgs.')

	tb.addAction(act)
	tb.addSeparator()
	mb.addSeparator()
	actions.append(act)

	act = mFile.addAction('Salir (!)')
	act.setShortcut(QKeySequence.Close)
	act.setIcon(icon('appExit.ico'))
	act.setStatusTip('Cierra la aplicacion...')

	actions.append(act)

	act = mEdit.addAction('Seleccionar todos')
	act.setShortcut('Ctrl+A')
	act.setIcon(icon('selectAll.ico'))
	act.setStatusTip('Selecciona todos los elementos de la escena.')

	actions.append(act)

	act = mEdit.addAction('Deseleccionar todos')
	act.setShortcut('Ctrl+D')
	act.setIcon(icon('unSelectAll.ico'))
	act.setStatusTip('Deselecciona todos los elementos seleccionados.')

	mb.addSeparator()
	actions.append(act)

	act = mEdit.addAction('Deshacer')
	act.setShortcut(QKeySequence.Undo)
	act.setIcon(icon('undo.ico'))
	act.setStatusTip('Deshace la ultima accion ejecutada.')

	tb.addAction(act)
	actions.append(act)

	act = mEdit.addAction('Rehacer')
	act.setShortcut(QKeySequence.Redo)
	act.setIcon(icon('redo.ico'))
	act.setStatusTip('Rehace la ultima accion ejecutada.')

	tb.addAction(act)
	tb.addSeparator()
	actions.append(act)

	act = mView.addAction('Interfaz minima')
	act.setShortcut('Ctrl+H')
	act.setIcon(icon('hideMenu.ico'))
	act.setStatusTip('Oculta la barras de mView y los paneles')

	mb.addSeparator()
	actions.append(act)

	act = mView.addAction('Zoom +')
	act.setShortcut(QKeySequence.ZoomIn)
	act.setIcon(icon('zoomIn.ico'))
	act.setStatusTip('Incrementa el zoom de la escena.')

	tb.addAction(act)
	actions.append(act)

	act = mView.addAction('Zoom 100%')
	act.setShortcut('Ctrl+0')
	act.setIcon(icon('zoom100.ico'))
	act.setStatusTip('Restablece el zoom de la escena.')

	tb.addAction(act)
	actions.append(act)

	act = mView.addAction('Zoom -')
	act.setShortcut(QKeySequence.ZoomOut)
	act.setIcon(icon('zoomOut.ico'))
	act.setStatusTip('Decrementa el zoom de la escena.')

	tb.addAction(act)
	mb.addSeparator()
	actions.append(act)

	act = mView.addAction('Pantalla completa')
	act.setCheckable(True)
	act.setShortcut(QKeySequence.FullScreen)
	act.setIcon(icon('fullScreen.ico'))
	act.setStatusTip('Rota entre pantalla completa y el estado anterior.')

	tb.addAction(act)
	actions.append(act)

	act = mHelp.addAction('Traducir a Español')
	act.setCheckable(True)
	act.setIcon(icon('trES.ico'))
	act.setStatusTip('Traduce los textos de la app a Español')

	actions.append(act)

	act = mHelp.addAction('Traducir a Ingles')
	act.setCheckable(True)
	act.setIcon(icon('trEN.ico'))
	act.setStatusTip('Traduce los textos de la app a Ingles')

	actions.append(act)

	act = mHelp.addAction('Traducir a Frances')
	act.setCheckable(True)
	act.setIcon(icon('trFR.ico'))
	act.setStatusTip('Traduce los textos de la app a Frances')

	actions.append(act)

	act = mHelp.addAction('Traducir a Aleman')
	act.setCheckable(True)
	act.setIcon(icon('trDE.ico'))
	act.setStatusTip('Traduce los textos de la app a Aleman')

	actions.append(act)

	return mb, tb, actions

##
## @brief      Crea el menu contextual de un componente simple.
##
## @return     PyQt5.QtWidgets.QMenu
## @return     list<PyQt5.QtWidgets.QAction>
##
def simpleMenu():

	ms = QMenu()

	actions = []

	act = ms.addAction('Cambiar Nombre')
	actions.append(act)

	act = ms.addAction('Incrementa Profundidad')
	actions.append(act)

	act = ms.addAction('Decrementa Profundidad')
	actions.append(act)

	act = ms.addAction('Rota estado: Activo')
	act.setCheckable(True)
	actions.append(act)

	act = ms.addAction('Rota estado: Visible')
	act.setCheckable(True)
	actions.append(act)

	act = ms.addAction('Borra el elemento')
	actions.append(act)

	act = ms.addAction('Ver detalles')
	actions.append(act)

	return ms, actions

##
## @brief      Crea un area de trabajo usando QGraphicsView y QGraphicsScene.
##
## @return     PyQt5.QtWidgets.QGraphicsView
##
def workArea(screenRect):
	workArea = QGraphicsView()
	workArea.setBackgroundBrush(QColor(pv['bgColor']))
	workArea.resize(screenRect.width(),screenRect.height())

	rect   = workArea.rect()
	width  = rect.width() - rect.width()*pv['viewRectMargin']
	height = rect.height() - rect.height()*pv['viewRectMargin']
	rectF   = QRectF(0,0,width,height)

	# Escena a la que se agregaran los Items con los que trabajamos.
	workAreaScene = QGraphicsScene(rectF,workArea)
	workAreaScene.addRect(rectF,Qt.black,QColor(pv['sceneColor']))

	# Asignamos la escena al area de trabajo.
	workArea.setScene(workAreaScene)

	return workArea

##
## @brief      Llama al cosntructor de arboles con el header de un comp simple.
##
## @param      emitters  Funciones a lanzar por diferentes acciones.
##
## @return     PyQt5.QtWidgets.QTreeView.
##
def simpleTreeView(*emitters):
	header = ['Nombre', 'Visb.', 'Act.', 'Z']
	return treeView(header,*emitters)

##
## @brief      Llama al cosntructor de arboles con el header de un comp simple.
##
## @param      emitters  Funciones a lanzar por diferentes acciones.
##
## @return     PyQt5.QtWidgets.QTreeView
##
def complexTreeView(*emitters):
	header = ['Nombre']
	return treeView(header,*emitters)

##
## @brief      Llama al cosntructor de docks para componentes simples.
##
## @param      widget  Panel que visualizaremos.
##
## @return     PyQt5.QtWidgets.QDockWidget
##
def simpleDockBar(widget):
	title = 'SIMPLES'
	return dockBar(title,widget)

##
## @brief      Llama al cosntructor de docks para componentes simples.
##
## @param      widget  Panel que visualizaremos.
##
## @return     PyQt5.QtWidgets.QDockWidget
##
def complexDockBar(widget):
	title = 'COMPLEJOS'
	return dockBar(title,widget)

##
## @brief      Dialogo para seleccionar imagenes.
##
## @param      parent   Ventana principal.
## @param      defPath  Ruta donde se abrira el dialogo.
##
## @return     PyQt5.QtWidgets.QFileDialog
##
def imgDialog(parent,defPath):
	title = 'Pick imgs!'
	supportList = 'JPEG (*.jpg *.jpeg);;PNG (*.png);;GIF (*.gif)'
	return QFileDialog.getOpenFileNames( parent,
	                              		 title,
	                              		 defPath,
	                              		 supportList,
	                              		 'PNG (*.png)')


# -------------------------------------------------------------------------- #


##
## @brief      Constructor con las propiedades deseadas de una barra lateral.
##
## @param      title   Titulo de cabecera del widget.
## @param      widget  Panel que visualizaremos.
##
## @return     PyQt5.QtWidgets.QDockWidget
##
def dockBar(title,widget):
	dockbar = QDockWidget(title)
	dockbar.setWidget(widget)

	# Limitamos su anclaje a los laterales.
	# dockbar.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
	return dockbar

##
## @brief      Constructor con las propiedades deseadas para un arbol.
##
## @param      header    Cabecera con las distintas columnas del arbol.
## @param      emitters  Funciones a lanzar por diferentes acciones.
##
## @return     PyQt5.QtWidgets.QTreeView
##
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

	# Señal de menu contextual. (Por defecto se dispara con 'boton derecho')
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
	tree.setSelectionMode(QAbstractItemView.ExtendedSelection)

	return tree
