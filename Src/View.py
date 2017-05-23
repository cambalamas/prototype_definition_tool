#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import Gui
from SimpleComponent import SimpleComponent as sc
from PresetValues import pv

## @brief      Clase encargada de la estructura visual de la aplicacion.
class View( QMainWindow ):


# .---------.
# | Señales |
# -------------------------------------------------------------------------- #

    # File menu
    signal_SaveProject              =   pyqtSignal()
    signal_LoadProject              =   pyqtSignal()
    signal_NewState                 =   pyqtSignal()
    signal_NewSimple                =   pyqtSignal()
    # Edit menu
    signal_SelectAll                =   pyqtSignal()
    signal_UnSelectAll              =   pyqtSignal()
    signal_Undo                     =   pyqtSignal()
    signal_Redo                     =   pyqtSignal()
    signal_Center                   =   pyqtSignal()
    signal_Clone                    =   pyqtSignal()
    # View menu
    signal_HideMenu                 =   pyqtSignal()
    signal_Minimalist               =   pyqtSignal()
    signal_ZoomIn                   =   pyqtSignal()
    signal_Zoom100                  =   pyqtSignal()
    signal_ZoomOut                  =   pyqtSignal()
    signal_FullScreen               =   pyqtSignal()
    signal_SceneCenter              =   pyqtSignal()
    # Simple menu
    signal_SimpleMenu               =   pyqtSignal()
    signal_Details                  =   pyqtSignal()
    signal_Name                     =   pyqtSignal()
    signal_ZInc                     =   pyqtSignal()
    signal_ZDec                     =   pyqtSignal()
    signal_Active                   =   pyqtSignal()
    signal_Visible                  =   pyqtSignal()
    signal_Delete                   =   pyqtSignal()
    # Simple callbacks
    signal_Resize                   =   pyqtSignal(int)
    signal_Move                     =   pyqtSignal(QPointF,QPointF,tuple)
    # Scene callbacks
    signal_SceneMove                =   pyqtSignal(QPointF,QPointF)
    signal_SelectArea               =   pyqtSignal(QRect)
    # Comps tree callbacks
    signal_ItemChanged              =   pyqtSignal(QStandardItem)
    # States menu
    signal_StateMoveLeft            =   pyqtSignal()
    signal_StateMoveRight           =   pyqtSignal()
    signal_StateClone               =   pyqtSignal()
    signal_StateDelete              =   pyqtSignal()
    # States tree callbacks
    signal_StateThumbPressed        =   pyqtSignal(QModelIndex)
    # States states tree
    signal_StateContextMenu         =   pyqtSignal()


# .----------.
# | Emisores |
# -------------------------------------------------------------------------- #

    # File menu
    def emit_SaveProject(self):
        self.signal_SaveProject.emit()
    def emit_LoadProject(self):
        self.signal_LoadProject.emit()
    def emit_NewSimple(self):
        self.signal_NewSimple.emit()
    def emit_NewState(self):
        self.signal_NewState.emit()
    # Edit menu
    def emit_SelectAll(self):
        self.signal_SelectAll.emit()
    def emit_UnSelectAll(self):
        self.signal_UnSelectAll.emit()
    def emit_Undo(self):
        self.signal_Undo.emit()
    def emit_Redo(self):
        self.signal_Redo.emit()
    def emit_Center(self):
        self.signal_Center.emit()
    def emit_Clone(self):
        self.signal_Clone.emit()
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
    # Help menu
    def emit_ReadTheDoc(self):
        url = 'https://github.com/cambalamas/prototype_definition_tool'
        QDesktopServices.openUrl(QUrl(url))
    def emit_ReportIssue(self):
        url = 'https://github.com/cambalamas/prototype_definition_tool/issues'
        QDesktopServices.openUrl(QUrl(url))
    # Simple menu
    def emit_SimpleMenu(self):
        self.signal_SimpleMenu.emit()
    def emit_Details(self):
        self.signal_Details.emit()
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
    def emit_Move(self,posO,posD,*sc):
        self.signal_Move.emit(posO,posD,sc)
    # Scene callbacks
    def emit_SceneMove(self,posO,posD):
        self.signal_SceneMove.emit(posO,posD)
    def emit_SelectArea(self,rect):
        self.signal_SelectArea.emit(rect)
    # Comps tree callbacks
    def emit_ItemChanged(self,item):
        self.signal_ItemChanged.emit(item)
    # States tree menu
    def emit_StateMoveLeft(self):
        self.signal_StateMoveLeft.emit()
    def emit_StateMoveRight(self):
        self.signal_StateMoveRight.emit()
    def emit_StateClone(self):
        self.signal_StateClone.emit()
    def emit_StateDelete(self):
        self.signal_StateDelete.emit()
    # States tree callbacks
    def emit_StateThumbPressed(self,item):
        self.signal_StateThumbPressed.emit(item)
    def emit_StateContextMenu(self):
        self.signal_StateContextMenu.emit()


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
        self.ok = Gui.configWindow(self)

        # Guarda la resolucion de la pantalla del usuario.
        self.screenRect = screenRect
        newWidth = self.screenRect.width()*pv['viewRectMargin']
        newHeight = self.screenRect.height()*pv['viewRectMargin']
        self.screenRect.setWidth(newWidth)
        self.screenRect.setHeight(newHeight)

        # Estado anterior a Pantalla Completa.
        self.__prevState = Qt.WindowStates

        # Emisores de las señales relacionadas con la aplicacion o proyecto.
        mainEmitters = [ # File
                         self.emit_SaveProject,
                         self.emit_LoadProject,
                         self.emit_NewState,
                         self.emit_NewSimple,
                         self.close,
                         # Edit
                         self.emit_Undo,
                         self.emit_Redo,
                         self.emit_SelectAll,
                         self.emit_UnSelectAll,
                         self.emit_Clone,
                         self.emit_Center,
                         # View
                         self.emit_Minimalist,
                         self.emit_ZoomIn,
                         self.emit_Zoom100,
                         self.emit_ZoomOut,
                         self.emit_SceneCenter,
                         self.emit_FullScreen,
                         # Help
                         self.emit_ReportIssue,
                         self.emit_ReadTheDoc ]

        # Construir la GUI de la barra de menus.
        # Construir la GUI de la barra de tareas.
        # Lista de acciones ejectuables por dichas barras.
        _menubar, self.__toolbar, mainActions = Gui.mainBars()
        self.setMenuBar(_menubar)
        self.addToolBar(Qt.LeftToolBarArea,self.__toolbar)
        self._connectSignals(mainActions,mainEmitters)


        # Emisores de las señales relacionadas con componentes simples.
        simpleEmitters = [ self.emit_Details,
                           self.emit_Center,
                           self.emit_Clone,
                           self.emit_Name,
                           self.emit_ZInc,
                           self.emit_ZDec,
                           self.emit_Active,
                           self.emit_Visible,
                           self.emit_Delete ]

        # Menu contextual arbol simple.
        self.__simpleMenu, simpleActions = Gui.simpleMenu()
        self._connectSignals(simpleActions,simpleEmitters)

        # Arbol de componentes simples.
        self.__simpleTree = Gui.simpleTreeView( self.emit_ItemChanged,
                                                self.emit_SimpleMenu )

        # Emisores de las señales relacionadas con estados.
        statesEmitters = [ self.emit_StateClone,
                           self.emit_StateMoveLeft,
                           self.emit_StateMoveRight,
                           self.emit_StateDelete ]

        # Menu contextual de arbol de estados.
        self.__statesMenu, statesActions = Gui.statesMenu()
        self._connectSignals(statesActions,statesEmitters)

        # Arbol de estados.
        self.__statesTree = Gui.statesTreeView( self.emit_StateContextMenu,
                                                self.emit_StateThumbPressed )

        # Barras anexas.
        self.__simpleDockbar = Gui.simpleDockBar(self.__simpleTree)
        self.addDockWidget(Qt.RightDockWidgetArea, self.__simpleDockbar)
        self.__statesDockbar = Gui.statesDockBar(self.__statesTree)
        self.addDockWidget(Qt.TopDockWidgetArea, self.__statesDockbar)

        # Area de trabajo.
        _workArea = Gui.workArea(self.screenRect)
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
    def statesTree(self):
        return self.__statesTree

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
    def statesDockbar(self):
        return self.__statesDockbar

    ## @brief      Propiedad de lectura del menu para componentes complejos.
    ## @param      self  Vista.
    ## @return     PyQt.QtWidgets.QMenu
    @property
    def statesMenu(self):
        return self.__statesMenu

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
        self.workScene.setSceneRect(x,y,w,h)


# .-----------------------.
# | Sobrecarga de eventos |
# -------------------------------------------------------------------------- #

    ## @brief      Solicita confirmación al intentar cerrar la ventana.
    ## @param      self  Vista.
    ## @param      ev    El objeto con la informacion que da este evento.
    ## @return     None
    def closeEvent(self,ev):
      reply = Gui.exitDialog(self)
      if reply == QMessageBox.Ok:
          qDebug(pv['endMsg'])
          ev.accept()
      else:
          ev.ignore()

    ## @brief      Captura cuando se pulsa una o una combiancion de teclas.
    ## @param      self  Vista.
    ## @param      ev    El objeto con la informacion que da este evento.
    ## @return     None
    def keyReleaseEvent(self,ev):
        if ev.key() == Qt.Key_Alt: # Al pulsar la tecla Alt.
            self.emit_HideMenu()   # Se Oculta/Muestra la barra de menús.
