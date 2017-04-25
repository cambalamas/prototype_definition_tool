#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, i18n
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal

# Ruta de los iconos.
icoPath = os.path.join(os.path.dirname(__file__),'Icons')

# Genera un QIcon a partir del nombre de la imagen.
def icon(name):
	return QIcon(os.path.join(icoPath,name))

def configWindow(window):
	# Icono del dock.
	window.setWindowIcon(icon('logo.png'))
	# Titulo de la ventana.
	window.setWindowTitle('Herramienta de definicion de prototipos.')



#
# --- // Acciones de la barra de menus.
#

def saveProjectAction(menu,emitter):
	act = menu.addAction('Guardar proyecto')
	act.setShortcut('Ctrl+S')
	act.setIcon(icon('save.png'))
	act.setStatusTip('Guarda el estado del proyecto.')
	act.triggered.connect(emitter)
	return act

def newCompSimpleAction(menu,emitter):
	act = menu.addAction('Nuevo Componente(s) simple(s)')
	act.setShortcut('Ctrl+I')
	act.setStatusTip('Crea un componente simple en base a una imagen.')
	act.triggered.connect(emitter)
	return act

def newCompComplexAction(menu,emitter):
	act = menu.addAction('Nuevo Componente complejo')
	act.setShortcut('Ctrl+Shift+I')
	act.setStatusTip('Crea un componente complejo en base a varias imgs.')
	act.triggered.connect(emitter)
	return act

def closeAction(menu,emitter):
	act = menu.addAction('Salir (!)')
	act.setShortcut(QKeySequence.Close)
	act.setStatusTip('Cierra la aplicacion...')
	act.triggered.connect(emitter)
	return act

def zoomInAction(menu,emitter):
	act = menu.addAction('Zoom +')
	act.setShortcut('Ctrl++')
	act.setStatusTip('Incrementa el zoom de la escena.')
	act.triggered.connect(emitter)
	return act

def zoomOutAction(menu,emitter):
	act = menu.addAction('Zoom -')
	act.setShortcut('Ctrl+-')
	act.setStatusTip('Decrementa el zoom de la escena.')
	act.triggered.connect(emitter)
	return act

def zoom100Action(menu,emitter):
	act = menu.addAction('Zoom 100%')
	act.setShortcut('Ctrl+0')
	act.setStatusTip('Restablece el zoom de la escena.')
	act.triggered.connect(emitter)
	return act

def fullScreenAction(menu,emitter):
	act = menu.addAction('Pantalla completa')
	act.setCheckable(True)
	act.setShortcut('F11')
	act.setStatusTip('Rota entre pantalla completa y el estado anterior.')
	act.triggered.connect(emitter)
	return act

def trEsAction(menu,emitter):
	act = menu.addAction('Traducir a Español')
	act.setCheckable(True)
	act.setStatusTip('Traduce los textos de la app a Español')
	act.triggered.connect(emitter)
	return act

def trEnAction(menu,emitter):
	act = menu.addAction('Traducir a Ingles')
	act.setCheckable(True)
	act.setStatusTip('Traduce los textos de la app a Ingles')
	act.triggered.connect(emitter)
	return act

def trFrAction(menu,emitter):
	act = menu.addAction('Traducir a Frances')
	act.setCheckable(True)
	act.setStatusTip('Traduce los textos de la app a Frances')
	act.triggered.connect(emitter)
	return act

def trDeAction(menu,emitter):
	act = menu.addAction('Traducir a Aleman')
	act.setCheckable(True)
	act.setStatusTip('Traduce los textos de la app a Aleman')
	act.triggered.connect(emitter)
	return act



#
# --- // Acciones de componente simple.
#

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


#
# --- // Acciones de la barra de herramientas.
#

# def saveproject(toolbar):
# 	act = toolbar.addAction('')
# 	act.setIcon(icon('save.png'))
# 	act.setIconText('Guardar proyecto')
# 	act.setStatusTip('Guarda el estado del proyecto.')
# 	act.triggered.connect(emmit)
# 	return act



#
# --- // Widgets.
#

def dockBar(title,widget):
	dockbar = QDockWidget(title)
	dockbar.setWidget(widget)
	# Define las areas permitidas.
	dockbar.setAllowedAreas( Qt.LeftDockWidgetArea
	                       	 | Qt.RightDockWidgetArea )
	return dockbar


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


#
# --- // Elementos necesarios por acciones del PRESENTER.
#

def ok():
	return QMessageBox.Ok

def checked():
	return Qt.Checked

def hidden():
	return Qt.UserRole

def imgDialog(parent,title,path):
	return QFileDialog.getOpenFileNames(self,title,path)

def prompt(parent,title,question):
	return QMessageBox.question( self,
							     title,
							     question,
							     QMessageBox.Ok | QMessageBox.No,
							     QMessageBox.No ) # <--- Por defecto.
