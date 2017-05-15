#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import i18n
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRectF

from SCENE import SCENE
from PresetValues import pv

iconsPath = os.path.join(os.path.dirname(__file__),'Icons')
i18n.load_path.append(os.path.join(os.path.dirname(__file__),'Translations'))

## @brief      Genera un icono a partir del nombre de la imagen.
## @param      name  Nombre de la imagen.
## @return     PyQt5.QtGui.QIcon
def icon(name):
    return QIcon(os.path.join(iconsPath,name))

## @brief      Establece el icono y el titulo.
## @param      window  Ventana a configurar.
## @return     None
def configWindow(view):
    # Icono del dock.
    view.setWindowIcon(icon('logo.png'))
    # Dialogo para solicitar idioma.
    opts = ['Español','Galego','English','Français','Deutsch']
    reply,ok = QInputDialog.getItem( view,
                                     'IDIOM',
                                     'Do you want to choose a language?',
                                     opts, editable = False )
    # Según lo seleccionado establecemos el idioma para i18n.
    if   reply == 'Español'     : i18n.set('locale', 'es')
    elif reply == 'Galego'      : i18n.set('locale', 'gl')
    elif reply == 'English'     : i18n.set('locale', 'en')
    elif reply == 'Français'    : i18n.set('locale', 'fr')
    elif reply == 'Deutsch'     : i18n.set('locale', 'de')
    else                        : i18n.set('locale', 'es')
    # Titulo de la ventana.
    view.setWindowTitle(i18n.t('E.title'))

## @brief      Presenta un dialogo para confimar la salida de la app.
## @param      view  Ventana padre.
## @return     PyQt5.QtWidgets.QMessageBox
def exitDialog(view):
    return QMessageBox.question( view,
                                 i18n.t('E.exitDialogTitle'),
                                 i18n.t('E.exitDialogQuest'),
                                 QMessageBox.Ok | QMessageBox.No,
                                 QMessageBox.No ) # <--- Por defecto.

## @brief      Dialogo para seleccionar imagenes.
## @param      parent   Ventana principal.
## @param      defPath  Ruta donde se abrira el dialogo.
## @return     PyQt5.QtWidgets.QFileDialog
def imgDialog(parent,defPath):
    title = i18n.t('E.imgDialogTitle')
    supportList = 'JPEG (*.jpg *.jpeg);;PNG (*.png);;GIF (*.gif)'
    return QFileDialog.getOpenFileNames( parent,
                                         title,
                                         defPath,
                                         supportList,
                                         'PNG (*.png)')

## @brief      Dialogo para cambiar el nombre de un componente.
## @param      parent  Ventana padre.
## @return     PyQt.QtGui.QInputDialog
def nameDialog(parent):
    newName, noCancel = QInputDialog.getText( parent,
                                              i18n.t('E.nameDialogTitle'),
                                              i18n.t('E.nameDialogQuest') )
    return newName, noCancel

## @brief      Crea los componentes de menus de la ventana principal.
## @return     PyQt5.QtWidgets.QMenuBar
## @return     PyQt5.QtWidgets.QToolBar
## @return     list<PyQt5.QtWidgets.QAction>
def mainBars():
    actions = []
    mb = QMenuBar()
    mb.setNativeMenuBar(True)
    tb = QToolBar(i18n.t('E.toolbarName'))

    mFile = mb.addMenu(i18n.t('E.fileMenu'))
    mEdit = mb.addMenu(i18n.t('E.editMenu'))
    mView = mb.addMenu(i18n.t('E.viewMenu'))
    mHelp = mb.addMenu(i18n.t('E.helpMenu'))

    act = mFile.addAction(i18n.t('E.save'))
    act.setShortcut(QKeySequence.Save)
    act.setIcon(icon('saveProject.ico'))
    act.setStatusTip(i18n.t('E.saveHint'))

    tb.addAction(act)
    mb.addSeparator()
    tb.addSeparator()
    actions.append(act)

    act = mFile.addAction(i18n.t('E.addSimple'))
    act.setShortcut('Ctrl+I')
    act.setIcon(icon('simpleComp.ico'))
    act.setStatusTip(i18n.t('E.addSimpleHint'))

    tb.addAction(act)
    actions.append(act)

    act = mFile.addAction(i18n.t('E.addComplex'))
    act.setShortcut('Ctrl+Shift+I')
    act.setIcon(icon('complexComp.ico'))
    act.setStatusTip(i18n.t('E.addComplexHint'))

    tb.addAction(act)
    tb.addSeparator()
    mb.addSeparator()
    actions.append(act)

    act = mFile.addAction(i18n.t('E.exit'))
    act.setShortcut(QKeySequence.Close)
    act.setIcon(icon('appExit.ico'))
    act.setStatusTip(i18n.t('E.exitHint'))

    actions.append(act)

    act = mEdit.addAction(i18n.t('E.selectAll'))
    act.setShortcut('Ctrl+A')
    act.setIcon(icon('selectAll.ico'))
    act.setStatusTip(i18n.t('E.selectAllHint'))

    actions.append(act)

    act = mEdit.addAction(i18n.t('E.unSelectAll'))
    act.setShortcut('Ctrl+D')
    act.setIcon(icon('unSelectAll.ico'))
    act.setStatusTip(i18n.t('E.unSelectAllHint'))

    mb.addSeparator()
    actions.append(act)

    act = mEdit.addAction(i18n.t('E.undo'))
    act.setShortcut(QKeySequence.Undo)
    act.setIcon(icon('undo.ico'))
    act.setStatusTip(i18n.t('E.undoHint'))

    tb.addAction(act)
    actions.append(act)

    act = mEdit.addAction(i18n.t('E.redo'))
    act.setShortcut(QKeySequence.Redo)
    act.setIcon(icon('redo.ico'))
    act.setStatusTip(i18n.t('E.redoHint'))

    tb.addAction(act)
    tb.addSeparator()
    actions.append(act)

    act = mView.addAction(i18n.t('E.minimal'))
    act.setShortcut('Ctrl+H')
    act.setIcon(icon('hideMenu.ico'))
    act.setStatusTip(i18n.t('E.minimalHint'))

    mb.addSeparator()
    actions.append(act)

    act = mView.addAction(i18n.t('E.zoomIn'))
    act.setShortcut(QKeySequence.ZoomIn)
    act.setIcon(icon('zoomIn.ico'))
    act.setStatusTip(i18n.t('E.zoomInHint'))

    tb.addAction(act)
    actions.append(act)

    act = mView.addAction(i18n.t('E.zoom100'))
    act.setShortcut('Ctrl+0')
    act.setIcon(icon('zoom100.ico'))
    act.setStatusTip(i18n.t('E.zoom100Hint'))

    tb.addAction(act)
    actions.append(act)

    act = mView.addAction(i18n.t('E.zoomOut'))
    act.setShortcut(QKeySequence.ZoomOut)
    act.setIcon(icon('zoomOut.ico'))
    act.setStatusTip(i18n.t('E.zoomOutHint'))

    tb.addAction(act)
    mb.addSeparator()
    actions.append(act)

    act = mView.addAction(i18n.t('E.fullScreen'))
    act.setCheckable(True)
    act.setShortcut(QKeySequence.FullScreen)
    act.setIcon(icon('fullScreen.ico'))
    act.setStatusTip(i18n.t('E.fullScreenHint'))

    tb.addAction(act)
    mb.addSeparator()
    actions.append(act)

    act = mView.addAction(i18n.t('E.centerScene'))
    act.setShortcut('Ctrl+Shift+C')
    # act.setIcon(icon('centerScene.ico'))
    act.setStatusTip(i18n.t('E.centerSceneHint'))

    actions.append(act)

    return mb, tb, actions

## @brief      Crea el menu contextual de un componente simple.
## @return     PyQt5.QtWidgets.QMenu
## @return     list<PyQt5.QtWidgets.QAction>
def simpleMenu():
    ms = QMenu()
    actions = []

    act = ms.addAction(i18n.t('E.compDetails'))
    actions.append(act)

    act = ms.addAction(i18n.t('E.compCenter')) #!!!
    actions.append(act)

    ms.addSeparator()

    act = ms.addAction(i18n.t('E.compChName'))
    actions.append(act)

    act = ms.addAction(i18n.t('E.compZInc'))
    actions.append(act)

    act = ms.addAction(i18n.t('E.compZDec'))
    actions.append(act)

    act = ms.addAction(i18n.t('E.compToggleActive'))
    actions.append(act)

    act = ms.addAction(i18n.t('E.compToggleVisible'))
    actions.append(act)

    act = ms.addAction(i18n.t('E.compDelete'))
    actions.append(act)

    return ms, actions

## @brief      Crea un area de trabajo usando QGraphicsView y QGraphicsScene.
## @return     PyQt5.QtWidgets.QGraphicsView
def workArea(screenRect):
    wArea = QGraphicsView()
    wArea.setTransformationAnchor(wArea.AnchorUnderMouse)
    wArea.setBackgroundBrush(QColor(pv['bgColor']))
    wArea.resize(screenRect.width(),screenRect.height())
    # Escena a la que se agregaran los Items con los que trabajamos.
    wAreaScene = SCENE(QRectF(screenRect),wArea)
    wAreaScene.addRect(QRectF(screenRect),Qt.black,QColor(pv['sceneColor']))
    # Asignamos la escena al area de trabajo.
    wArea.setScene(wAreaScene)

    return wArea

## @brief      Llama al cosntructor de arboles con el header de un comp simple.
## @param      emitters  Funciones a lanzar por diferentes acciones.
## @return     PyQt5.QtWidgets.QTreeView.
def simpleTreeView(*emitters):
    header = [ i18n.t('E.scHeaderName'),
               i18n.t('E.scHeaderVisible'),
               i18n.t('E.scHeaderActive'), 'Z']
    return treeView(header,*emitters)

## @brief      Llama al cosntructor de arboles con el header de un comp simple.
## @param      emitters  Funciones a lanzar por diferentes acciones.
## @return     PyQt5.QtWidgets.QTreeView
def complexTreeView(*emitters):
    header = [i18n.t('E.ccHeaderName')]
    return treeView(header,*emitters)

## @brief      Llama al cosntructor de docks para componentes simples.
## @param      widget  Panel que visualizaremos.
## @return     PyQt5.QtWidgets.QDockWidget
def simpleDockBar(widget):
    title = i18n.t('E.scTreeTitle')
    return dockBar(title,widget)

## @brief      Llama al cosntructor de docks para componentes simples.
## @param      widget  Panel que visualizaremos.
## @return     PyQt5.QtWidgets.QDockWidget
def complexDockBar(widget):
    title = i18n.t('E.ccTreeTitle')
    return dockBar(title,widget)


# -------------------------------------------------------------------------- #


## @brief      Constructor con las propiedades deseadas de una barra lateral.
## @param      title   Titulo de cabecera del widget.
## @param      widget  Panel que visualizaremos.
## @return     PyQt5.QtWidgets.QDockWidget
def dockBar(title,widget):
    dockbar = QDockWidget(title)
    dockbar.setWidget(widget)
    # dockbar.setFixedWidth(190)
    # Limitamos su anclaje a los laterales.
    dockbar.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
    return dockbar

## @brief      Constructor con las propiedades deseadas para un arbol.
## @param      header    Cabecera con las distintas columnas del arbol.
## @param      emitters  Funciones a lanzar por diferentes acciones.
## @return     PyQt5.QtWidgets.QTreeView
def treeView(header,*emitters):
    tree = QTreeView()
    model = QStandardItemModel()
    # Asigna el modelo a la vista.
    tree.setModel(model)
    # Propiedades del modelo.
    model.setHorizontalHeaderLabels(header)
    # Señal de cambio en los datos.
    model.itemChanged.connect(emitters[0])
    # Propiedades del cabecero.
    tree.header().resizeSection(0,90)
    tree.header().resizeSection(1,25)
    tree.header().resizeSection(2,25)
    tree.header().resizeSection(3,25)
    # Señal de menu contextual. (Por defecto se dispara con 'boton derecho')
    tree.customContextMenuRequested.connect(emitters[1])
    # Menu contextual solicitado por señal.
    tree.setContextMenuPolicy(Qt.CustomContextMenu)
    # Oculta las flechas de hijos.
    tree.setRootIsDecorated(False)
    # No permite expandir los hijos.
    tree.setItemsExpandable(False)
    # Iguala la altura de las filas.
    # tree.setUniformRowHeights(True)
    # Alterna colores en las filas
    tree.setAlternatingRowColors(True)
    # Dibuja el recuadro de seleccion en toda la fila.
    tree.setSelectionBehavior(QAbstractItemView.SelectRows)
    # Solo permite seleccionar un elemento a la vez.
    tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
    return tree
