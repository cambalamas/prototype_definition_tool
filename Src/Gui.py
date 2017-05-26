#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import i18n
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRectF

from Scene import Scene
from Viewport import Viewport
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
                                     'LANGUAGE',
                                     'Please, choose yours:',
                                     opts, editable = False )
    # Según lo seleccionado establecemos el idioma para i18n.
    if   reply == 'Español'     : i18n.set('locale', 'es')
    elif reply == 'Galego'      : i18n.set('locale', 'gl')
    elif reply == 'English'     : i18n.set('locale', 'en')
    elif reply == 'Français'    : i18n.set('locale', 'fr')
    elif reply == 'Deutsch'     : i18n.set('locale', 'de')
    else                        : i18n.set('locale', 'en')
    # Titulo de la ventana.
    view.setWindowTitle(i18n.t('E.title'))
    # Devuelve el valor del dialogo.
    return ok


## @brief      Presenta un dialogo para confimar la salida de la app.
## @param      view  Ventana padre.
## @return     PyQt5.QtWidgets.QMessageBox
def exitDialog(view):
    return QMessageBox.question( view,
                                 i18n.t('E.exitDialogTitle'),
                                 i18n.t('E.exitDialogQuest'),
                                 QMessageBox.Ok | QMessageBox.No,
                                 QMessageBox.No ) # <--- Por defecto.

## @brief      Presenta un dialogo para confimar la salida de la app.
## @param      view  Ventana padre.
## @return     PyQt5.QtWidgets.QMessageBox
def exitSaveDialog(view):
    return QMessageBox.question( view,
                                 i18n.t('E.exitDialogTitle'),
                                 i18n.t('E.saveDialogQuest'),
                                 QMessageBox.Ok | QMessageBox.No,
                                 QMessageBox.No ) # <--- Por defecto.

## @brief      Presenta un dialogo con errores de cargar un XML.
## @param      view  Ventana padre.
## @return     PyQt5.QtWidgets.QMessageBox
def loadErrorDialog(parent,msg):
    txt = ''
    if   msg == 1:
        txt = i18n.t('E.loadNotValidXML')
    elif msg == 2:
        txt = i18n.t('E.loadMissedState')
    elif msg == 3:
        txt = i18n.t('E.loadMissedImages')
    QMessageBox.about(parent, i18n.t('E.loadErrorTitle'), txt)


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

def saveDialog(parent,defPath):
    title = i18n.t('E.saveDesign')
    supportList = 'XML (*.xml)'
    return QFileDialog.getSaveFileName( parent,
                                        title,
                                        defPath,
                                        supportList,
                                        'XML (*.xml)')

def loadDialog(parent,defPath):
    title = i18n.t('E.loadDesign')
    supportList = 'XML (*.xml)'
    return QFileDialog.getOpenFileName( parent,
                                        title,
                                        defPath,
                                        supportList,
                                        'XML (*.xml)')

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
    tb.setMovable(False)

    mFile = mb.addMenu(i18n.t('E.fileMenu'))
    mEdit = mb.addMenu(i18n.t('E.editMenu'))
    mView = mb.addMenu(i18n.t('E.viewMenu'))
    mHelp = mb.addMenu(i18n.t('E.helpMenu'))

    # Archivo
    act = mFile.addAction(i18n.t('E.save'))
    act.setShortcut(QKeySequence.Save)
    act.setIcon(icon('saveProjectAs.ico'))
    act.setStatusTip(i18n.t('E.saveHint'))

    tb.addAction(act)
    actions.append(act)

    act = mFile.addAction(i18n.t('E.load'))
    act.setShortcut(QKeySequence.Open)
    act.setIcon(icon('openProject.ico'))
    act.setStatusTip(i18n.t('E.loadHint'))

    tb.addAction(act)
    mb.addSeparator()
    actions.append(act)

    act = mFile.addAction(i18n.t('E.addState'))
    act.setShortcut('Ctrl+T')
    act.setIcon(icon('newState.ico'))
    act.setStatusTip(i18n.t('E.addStateHint'))

    tb.addAction(act)
    actions.append(act)

    act = mFile.addAction(i18n.t('E.addSimple'))
    act.setShortcut('Ctrl+I')
    act.setIcon(icon('simpleComp.ico'))
    act.setStatusTip(i18n.t('E.addSimpleHint'))

    tb.addAction(act)
    tb.addSeparator()
    mb.addSeparator()
    actions.append(act)

    act = mFile.addAction(i18n.t('E.exit'))
    act.setShortcut(QKeySequence.Quit)
    act.setIcon(icon('appExit.ico'))
    act.setStatusTip(i18n.t('E.exitHint'))

    actions.append(act)

    # Editar
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
    mb.addSeparator()
    actions.append(act)

    act = mEdit.addAction(i18n.t('E.selectAll'))
    act.setShortcut('Ctrl+A')
    act.setIcon(icon('selectAll.ico'))
    act.setStatusTip(i18n.t('E.selectAllHint'))

    tb.addAction(act)
    actions.append(act)

    act = mEdit.addAction(i18n.t('E.unSelectAll'))
    act.setShortcut('Ctrl+D')
    act.setIcon(icon('unSelectAll.ico'))
    act.setStatusTip(i18n.t('E.unSelectAllHint'))

    tb.addAction(act)
    mb.addSeparator()
    actions.append(act)

    act = mEdit.addAction(i18n.t('E.duplicateComps'))
    act.setShortcut('Ctrl+Shift+D')
    act.setIcon(icon('cloneComps.ico'))
    act.setStatusTip(i18n.t('E.duplicateCompsHint'))

    tb.addAction(act)
    actions.append(act)

    act = mEdit.addAction(i18n.t('E.centerComps'))
    act.setShortcut('Ctrl+Shift+M')
    act.setIcon(icon('centerComps.ico'))
    act.setStatusTip(i18n.t('E.centerCompsHint'))

    tb.addAction(act)
    tb.addSeparator()
    mb.addSeparator()
    actions.append(act)

    # Vista

    act = mView.addAction(i18n.t('E.minimal'))
    act.setShortcut('Ctrl+H')
    act.setIcon(icon('minimalUI.ico'))
    act.setStatusTip(i18n.t('E.minimalHint'))

    tb.addAction(act)
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

    act = mView.addAction(i18n.t('E.centerScene'))
    act.setShortcut('Ctrl+Shift+C')
    act.setIcon(icon('centerScene.ico'))
    act.setStatusTip(i18n.t('E.centerSceneHint'))

    tb.addAction(act)
    actions.append(act)

    act = mView.addAction(i18n.t('E.fullScreen'))
    act.setCheckable(True)
    act.setShortcut(QKeySequence.FullScreen)
    act.setIcon(icon('fullScreen.ico'))
    act.setStatusTip(i18n.t('E.fullScreenHint'))

    tb.addAction(act)
    tb.addSeparator()
    mb.addSeparator()
    actions.append(act)

    # Ayuda
    act = mHelp.addAction(i18n.t('E.reportError'))
    act.setIcon(icon('reportError.ico'))
    act.setStatusTip(i18n.t('E.reportErrorHint'))

    tb.addAction(act)
    actions.append(act)

    act = mHelp.addAction(i18n.t('E.readTheDoc'))
    act.setIcon(icon('readTheDoc.ico'))
    act.setStatusTip(i18n.t('E.readTheDocHint'))

    tb.addAction(act)
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

    act = ms.addAction(i18n.t('E.compCenter'))
    actions.append(act)

    act = ms.addAction(i18n.t('E.compDuplicate'))
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
    ms.addSeparator()

    act = ms.addAction(i18n.t('E.compDelete'))
    actions.append(act)

    return ms, actions


## @brief      Crea el menu contextual de un componente simple.
## @return     PyQt5.QtWidgets.QMenu
## @return     list<PyQt5.QtWidgets.QAction>
def statesMenu():
    ms = QMenu()
    actions = []

    act = ms.addAction(i18n.t('E.stateClone'))
    actions.append(act)

    act = ms.addAction(i18n.t('E.stateMoveLeft'))
    actions.append(act)

    act = ms.addAction(i18n.t('E.stateMoveRight'))
    actions.append(act)
    ms.addSeparator()

    act = ms.addAction(i18n.t('E.stateDelete'))
    actions.append(act)

    return ms, actions


## @brief      Crea un area de trabajo usando QGraphicsView y QGraphicsScene.
## @return     PyQt5.QtWidgets.QGraphicsView
def workArea(screenRect):
    wArea = Viewport()
    wArea.setBackgroundBrush(QColor(pv['bgColor']))
    wArea.resize(screenRect.width(),screenRect.height())
    wArea.setTransformationAnchor(wArea.AnchorUnderMouse)
    wAreaScene = Scene(QRectF(0.0,0.0,1240.0,720.0),wArea)
    wArea.setScene(wAreaScene)

    return wArea


## @brief      Constructor con las propiedades deseadas para un arbol 'simple'.
## @param      emitters  Funciones a lanzar por diferentes acciones.
## @return     PyQt5.QtWidgets.QTreeView
def simpleTreeView(*emitters):
    tree = QTreeView()
    model = QStandardItemModel()
    # Cabeceros y propiedades de los mismos.
    modelHeader = [ i18n.t('E.scHeaderName'),
                    i18n.t('E.scHeaderVisible'),
                    i18n.t('E.scHeaderActive'), 'Z' ]
    # Asignaciones.
    tree.setModel(model)
    model.setHorizontalHeaderLabels(modelHeader)
    # Propiedades del cabecero.
    tree.header().resizeSection(0,115)
    tree.header().resizeSection(1,25)
    tree.header().resizeSection(2,25)
    tree.header().resizeSection(3,25)
    # Propiedeades
    tree.setRootIsDecorated(False) # Oculta las flechas de hijos.
    tree.setItemsExpandable(False) # No permite expandir los hijos.
    tree.setAlternatingRowColors(True) # Alterna colores en las filas.
    tree.setContextMenuPolicy(Qt.CustomContextMenu) # Menu contextual = RB.
    tree.setSelectionBehavior(QAbstractItemView.SelectRows) # Sel x fila.
    tree.setSelectionMode(QAbstractItemView.ExtendedSelection) # Sel 1 o +.
    # Señales
    model.itemChanged.connect(emitters[0])
    tree.customContextMenuRequested.connect(emitters[1])

    return tree


## @brief      Constructor con las propiedades para una lista de estados.
## @param      emitters  Funciones a lanzar por diferentes acciones.
## @return     PyQt5.QtWidgets.QTreeView
def statesTreeView(*emitters):
    tree = QTreeView()
    model = QStandardItemModel()
    # Cabecero, creacion y propiedades.
    header = QHeaderView(1,tree) # Horizontal con el arbol como padre.
    header.setDragEnabled(False) # Prohibido arrastrar items.
    header.setHighlightSections(True)
    header.setSectionResizeMode(QHeaderView.ResizeToContents) # Ajusta al item.
    # Asignaciones
    tree.setModel(model)
    tree.setHeader(header)
    # Propiedades.
    tree.setDragEnabled(False) # Prohibido arrastrar items.
    tree.setRootIsDecorated(False) # Oculta las flechas de hijos.
    tree.setItemsExpandable(False) # No permite expandir los hijos.
    tree.setContextMenuPolicy(Qt.CustomContextMenu) # Menu contextual = RB.
    tree.setSelectionBehavior(QAbstractItemView.SelectItems) # Sel x item.
    tree.setSelectionMode(QAbstractItemView.NoSelection) # Sin seleccion.
    # Señales.
    tree.customContextMenuRequested.connect(emitters[0])
    tree.pressed.connect(emitters[1])

    return tree


## @brief      Crea dock para componentes simples.
## @param      widget  Panel que visualizaremos.
## @return     PyQt5.QtWidgets.QDockWidget
def simpleDockBar(widget):
    db = QDockWidget()
    db.setWidget(widget)
    db.setFixedWidth(215)
    db.setTitleBarWidget(QWidget())
    db.setFeatures(db.DockWidgetClosable)

    return db


## @brief      Crea dock para estados.
## @param      widget  Panel que visualizaremos.
## @return     PyQt5.QtWidgets.QDockWidget
def statesDockBar(widget):
    db = QDockWidget()
    db.setWidget(widget)
    db.setFixedHeight(90)
    db.setTitleBarWidget(QWidget())
    db.setFeatures( db.DockWidgetVerticalTitleBar
                    | db.DockWidgetClosable )
    return db
