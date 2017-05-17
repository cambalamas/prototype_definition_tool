#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import unicodedata
from pprint import pprint #temp
from threading import Timer

import i18n
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import GUI
import PARSER
import SIMPLE

from PresetValues import pv


## @brief      Clase que define la logica de negocio de la aplicacion.
class PRESENTER( object ):


# .-------------.
# | Constructor |
# -------------------------------------------------------------------------- #

    ## @brief      Constructor de el Presentador.
    ## @param      self   Presentador.
    ## @param      view   La ventana principal.
    ## @param      model  El acceso a la capa de persistencia.
    def __init__(self,view,model):
        # Ventana principal.
        self.__view = view
        # Gestion de datos y persistencia.
        self.__model = model
        # Flags para evitar drenaje de RAM.
        self.__saveFlagMove = True
        self.__saveFlagResize = True


# .----------------------------------------.
# | Acceso 'publico' la variables privadas |
# -------------------------------------------------------------------------- #

    ## @brief      Propiedad de lectura de la variable vista.
    ## @param      self  Presentador.
    ## @return     VIEW.VIEW
    @property
    def view(self):
        return self.__view

    ## @brief      Propiedad de lectura de la variable modelo.
    ## @param      self  Presentador.
    ## @return     MODEL.MODEL
    @property
    def model(self):
        return self.__model


# .--------------------------.
# | Señales del menu Archivo |
# -------------------------------------------------------------------------- #

    ## @brief      Guarda la interfaz actual en XML.
    ## @param      self  Presentador.
    ## @return     None
    def listener_SaveProject(self):
        pass # PARSER.save(self.model.interface)
        qDebug('Saving project...')


    ## @brief      Crea un nuevo componente simple.
    ## @param      self  Presentador.
    ## @return     None
    def listener_NewSimple(self):
        home = os.path.expanduser(pv['defaultPath'])
        imgPathSet = GUI.imgDialog(self.view,home) # ret: ([<path>],<formato>)
        if imgPathSet[0]:
            self.model.saveState()  # Guarda el estado previo.
            for imgPath in imgPathSet[0]:
                item = SIMPLE.SimpleComponent(imgPath) # Crea comp simpmle.
                if item is not None:
                    item.setZValue(1.0)
                    self.model.newComponent(item) # Lo agrega a la pila.
                    qDebug('Created new component from '+self._nfc(imgPath))

    ## @brief      Crea un nuevo componente complejo.
    ## @param      self  Presentador.
    ## @return     None
    def listener_NewComplex(self):
        pass


# .-------------------------.
# | Señales del menu Editar |
# -------------------------------------------------------------------------- #

    ## @brief      Establece True la propiedad 'selected' de todos los comps.
    ## @param      self  Presentador.
    ## @return     None
    def listener_SelectAll(self):
        for item in self.view.workScene.items():
            item.setSelected(True)
        qDebug('Selected all components')

    ## @brief      Establece False la propiedad 'selected' de todos los comps.
    ## @param      self  Presentador.
    ## @return     None
    def listener_UnSelectAll(self):
        for item in self._selectedItems():
            item.setSelected(False)
        qDebug('Unselected all components')

    ## @brief      Devuelve el area de trabajo a su estado anterior.
    ## @param      self  Presentador.
    ## @return     None
    def listener_Undo(self):
        self.model.undo()
        qDebug('Undone previous action')

    ## @brief      Devuelve el area de trabajo a un estado posterior.
    ## @param      self  Presentador.
    ## @return     None
    def listener_Redo(self):
        self.model.redo()
        qDebug('Redone subsequent action')


# .------------------------.
# | Señales del menu Vista |
# -------------------------------------------------------------------------- #

    ## @brief      Oculta todos las widgets.
    ## @param      self  Presentador.
    ## @return     None
    def listener_Minimalist(self):
        mtb = self.view.toolbar
        sdb = self.view.simpleDockbar
        # cdb = self.view.complexDockbar
        stb = self.view.statusBar()
        if( mtb.isVisible()
                == sdb.isVisible()
                # == cdb.isVisible()
                == stb.isVisible()
                == True):
            mtb.setVisible(False)
            sdb.setVisible(False)
            # cdb.setVisible(False)
            stb.setVisible(False)
        else:
            mtb.setVisible(True)
            sdb.setVisible(True)
            # cdb.setVisible(True)
            stb.setVisible(True)
        qDebug('Hided all interface stuff')

    ## @brief      Devuelve la escena al centro de la ventana.
    ## @param      self  Presenter
    ## @return     None
    def listener_SceneCenter(self):
        x = self.view.screenRect.x()
        y = self.view.screenRect.y()
        w = self.view.workScene.sceneRect().width()
        h = self.view.workScene.sceneRect().height()
        self.view.workScene.setSceneRect(x,y,w,h)
        qDebug('Re-Centered the scene')

    ## @brief      Oculta la barra de menus.
    ## @param      self  Presentador.
    ## @return     None
    def listener_HideMenu(self):
        menuBar = self.view.menuBar()
        if menuBar.height() is not 0:
            menuBar.setFixedHeight(0)
        else:
            menuBar.setFixedHeight(menuBar.sizeHint().height())
        qDebug('Hided the menubar')

    ## @brief      Aumenta la escala de la escena.
    ## @param      self  Presentador.
    ## @return     None
    def listener_ZoomIn(self):
        if not self.view.scale * pv['viewModScale'] > pv['viewMaxScale']:
            self.view.workArea.scale(pv['viewModScale'],pv['viewModScale'])
            qDebug('Increment viewport zoom to '
                    +self._nfc(round(self.view.scale*100,2))+'%' )
        else:
            qDebug('Trying to increment, but has reached the maximum')

    ## @brief      Restaurar el nivel de Zoom al 100%.
    ## @param      self  Presentador.
    ## @return     None
    def listener_Zoom100(self):
        self.view.workArea.scale(1/self.view.scale,1/self.view.scale)
        qDebug('Reset viewport zoom to 100%')

    ## @brief      Disminuye la escala de la escena.
    ## @param      self  Presentador.
    ## @return     None
    def listener_ZoomOut(self):
        if not self.view.scale / pv['viewModScale'] < pv['viewMinScale']:
            self.view.workArea.scale(1/pv['viewModScale'],1/pv['viewModScale'])
            qDebug( 'Decremented viewport zoom to '
                    +self._nfc(round(self.view.scale*100,2))+'%' )
        else:
            qDebug( 'Trying to decrement viewport scale, \
                    but has reached the minimun' )

    ## @brief      Rota entre pantalla completa y el estado anterior.
    ## @param      self  Presentador.
    ## @return     None
    def listener_FullScreen(self):
        if self.view.isFullScreen():
            self.view.setWindowState(self.view.prevState)
            qDebug('Window exit of FullScreen')
        else:
            self.view.prevState = self.view.windowState()
            self.view.showFullScreen()
            qDebug( 'Window enter to FullScreen, from '
                    +self._nfc(self.view.prevState) )


# .---------------------------------------.
# | Señales 'menu' de componentes simples |
# -------------------------------------------------------------------------- #

    ## @brief      Invoca el menu contextual de los componentes simples.
    ## @param      self  Presentador.
    ## @return     None
    def listener_SimpleMenu(self):
        # Comprueba si el evento se origina en el arbol.
        if self._isOver(self.view.simpleTree):
            indexes = self.view.simpleTree.selectedIndexes()
            if indexes:
                self.view.simpleMenu.exec(self.view.cursor().pos())
                self.listener_UnSelectAll()
                for index in indexes:
                    row = self.view.simpleTree.model().itemFromIndex(index)
                    if row.child(0,0) is not None:
                        id = row.child(0,0).data(0)
                        comp = self.model.getComponentById(id)
                        comp.setSelected(True)
            qDebug('Invoked context menu, over the components\' tree')
        else:
            # Ejecuta el menu contextual.
            self.view.simpleMenu.exec(self.view.cursor().pos())
            qDebug('Invoked context menu, over a component')

    ## @brief      Abre un cuadro de dialogo con el ToString del componente.
    ## @param      self  Presentador.
    ## @return     None
    def listener_Details(self):
        for item in self._selectedItems():
            item.detailsDialog()
            qDebug('Details of '+self._nfc(item.name))

    ## @brief      Centra los componentes en la escena.
    ## @param      self  Presentador.
    ## @return     None
    def listener_Center(self):
        x = self.view.workScene.sceneRect().width()/2
        y = self.view.workScene.sceneRect().height()/2
        for item in self._selectedItems():
            itemX = item.getSizeX()/2
            itemY = item.getSizeY()/2
            item.setPos(x-itemX,y-itemY)
            qDebug('Centered component '+self._nfc(item.name))

    ## @brief      Dialogo para cambiar el nombre los comps. seleccionados.
    ## @param      self  Presentador.
    ## @return     None
    def listener_Name(self):
        self.model.saveState()  # Guarda el estado previo.
        newName, noCancel = GUI.nameDialog(self.view)
        # Si se acepta el cambio de nombre.
        if noCancel:
            # Si hay seleccionados varios componentes,
            # el cambio de nombre sera secuencial.
            if len(self._selectedItems()) > 1:
                i = 0
                for item in self._selectedItems():
                    i += 1
                    item.name = str(i)+'_'+newName
                    qDebug( 'Changed name for '+self._nfc(item.imgPath)
                            +', to'+self._nfc(item.name) )
            # Si solo afecta a un componente,
            # sera el texto de la caja, sin ninugna secuencia.
            else:
                for item in self._selectedItems():
                    item.name = newName
                    qDebug( 'Changed name for '+self._nfc(item.imgPath)
                            )
            # Actualiza los datos en el arbol de componentes.
            self._updateTree()

    ## @brief      Mueve una posición al frente los componentes seleccionados.
    ## @param      self  Presentador.
    ## @return     None
    def listener_ZInc(self):
        self.model.saveState()  # Guarda el estado previo.
        for item in self._selectedItems():
            newZ = item.getPosZ() + pv['zJump']
            item.setZValue(newZ)
            qDebug( 'Incremented Z of '+self._nfc(item.name)
                    +', to'+self._nfc(newZ) )
        # Actualiza los datos en el arbol de componentes.
        self._updateTree()

    ## @brief      Mueve una posición al fondo los componentes seleccionados.
    ## @param      self  Presentador.
    ## @return     None
    def listener_ZDec(self):
        self.model.saveState()  # Guarda el estado previo.
        for item in self._selectedItems():
            newZ = item.getPosZ() - pv['zJump']
            if newZ >= 0:
                item.setZValue(newZ)
                qDebug( 'Decremented Z of '+self._nfc(item.name)
                        +', to'+self._nfc(newZ) )
            else:
                qDebug('Z has reached the minimun on '+self._nfc(item.name))
        # Actualiza los datos en el arbol de componentes.
        self._updateTree()

    ## @brief      Rota el estado Activo de los componentes seleccionados.
    ## @param      self  Presentador.
    ## @return     None
    def listener_Active(self):
        self.model.saveState()  # Guarda el estado previo.
        for item in self._selectedItems():
            toggle = not item.active
            item.active = toggle
            item.activeEffect()
            qDebug('Toggle active status of '+self._nfc(item.name))
        # Actualiza los datos en el arbol de componentes.
        self._updateTree()

    ## @brief      Rota el estado Visible de los componentes seleccionados.
    ## @param      self  Presentador.
    ## @return     None
    def listener_Visible(self):
        self.model.saveState()  # Guarda el estado previo.
        for item in self._selectedItems():
            item.visible = not item.visible
            item.visibleEffect()
            qDebug('Toggle visible status of '+self._nfc(item.name))
        # Actualiza los datos en el arbol de componentes.
        self._updateTree()

    ## @brief      Elimina por completo los componentes seleccionados.
    ## @param      self  Presentador.
    ## @return     None
    def listener_Delete(self):
        self.model.saveState()  # Guarda el estado previo.
        self.model.delComponent(self._selectedItems())
        qDebug('Deleted a batch of components')


# .-------------------------------------------.
# | Señales 'callback' de componentes simples |
# -------------------------------------------------------------------------- #

    ## @brief      Mueve los comps. seleccinados segun el despl. del cursor.
    ## @param      self  Presentador.
    ## @param      posO  Posición de origen.
    ## @param      posD  Posición de destiono.
    ## @return     None
    def listener_Move(self,posO,posD,overItem):
        # Calculo de desplazamiento.
        despl = posD - posO
        # Temporizador para el guardado de estados.
        # Para evitar drenaje de RAM.
        if self.__saveFlagMove:
            self.__saveFlagMove = False
            self.model.saveState()
            Timer(pv['moveTimer'],self._thMoveFlag).start()
        # Desplaza todos los items seleccionados.
        for item in self._selectedItems():
            x = despl.x() * overItem.scale()
            y = despl.y() * overItem.scale()
            item.moveBy(x,y)
            qDebug( 'Moved item '+self._nfc(item.name)
                    +', '+self._nfc(x)+' pos on X, '
                    +self._nfc(y)+' pos on Y' )

    ## @brief      Escala virtualmente los comps. según el giro de la rueda.
    ## @param      self   Presentador.
    ## @param      delta  Giro de la rueda (+: Adelante / -: Atrás)
    ## @return     None
    def listener_Resize(self,delta):
        # Temporizador para el guardado de estados.
        # Para evitar drenaje de RAM.
        if self.__saveFlagResize:
            self.__saveFlagResize = False
            self.model.saveState()
            Timer(pv['resizeTimer'],self._thResizeFlag).start()
        # Giro de la rueda hacia adelante.
        if delta > 0:
            # Escala todos los items seleccionados.
            for item in self._selectedItems():
                # Si no excede el maximo.
                if not item.scale() * pv['imgModScale'] > pv['imgMaxScale']:
                    item.setScale(item.scale() * pv['imgModScale'])
                    qDebug( 'Scaled component '+self._nfc(item.name)
                            +', to '+self._nfc(round(item.scale()*100,2))+'%' )
                else:
                    qDebug('Component has reached the maximun scale')
        # Giro de la rueda hacia atras.
        else:
            # Escala todos los items seleccionados.
            for item in self._selectedItems():
                # Si no excede el minimo.
                if not item.scale() / pv['imgModScale'] < pv['imgMinScale']:
                    item.setScale(item.scale() / pv['imgModScale'])
                    qDebug( 'Scaled component '+self._nfc(item.name)
                            +', to '+self._nfc(round(item.scale()*100,2))+'%' )
                else:
                    qDebug('Component has reached the minimun scale')
        # Actualiza los datos en el arbol de componentes.
        self._updateTree()


# .---------------------------------.
# | Señales 'callback' de la Escena |
# -------------------------------------------------------------------------- #

    ## @brief      Desplaza la posicion de la escena.
    ## @param      self  Presentador.
    ## @param      posO  Posicion origen.
    ## @param      posD  Posicion destino.
    ## @return     None
    def listener_SceneMove(self,posO,posD):
        # Calculo de desplazamiento.
        despl = posO - posD
        # Obtencion de la escala.
        scale = self.view.scale
        # Factor de desplazamiento con la escala aumentada.
        if scale > 1.0:
            moveFactorX = despl.x()*1.5 / scale
            moveFactorY = despl.y()*1.5 / scale
        # Factor de desplazamiento con la escala disminuida.
        else:
            moveFactorX = despl.x() * scale
            moveFactorY = despl.y() * scale
        # Nueva 'rect' de la escena.
        x = self.view.workScene.sceneRect().x() + moveFactorX
        y = self.view.workScene.sceneRect().y() + moveFactorY
        w = self.view.workScene.sceneRect().width()
        h = self.view.workScene.sceneRect().height()
        self.view.workScene.setSceneRect(x,y,w,h)
        qDebug( 'Moved scene, '+self._nfc(x)
                +' pos on X and '+self._nfc(y)+' pos on Y' )

    ## @brief      Selecciona los componentes dentro del area de seleccion.
    ## @param      self  Presentador.
    ## @param      rect  Area de seleccion.
    ## @return     None
    def listener_SelectArea(self,rect):
        for child in self._getComponents():
            if rect.contains(child.getRect()):
                child.setSelected(True)
                qDebug('Component '+self._nfc(child.name)+', selected on area')


# .------------------------------.
# | Señales 'callback' del Arbol |
# -------------------------------------------------------------------------- #

    ## @brief      Atiende la señal nativa del arbol cuando se cambia un dato.
    ## @param      self  Presentador.
    ## @param      item  Item cambiado del arbol.
    ## @return     None
    def listener_ItemChanged(self,item):
        compID = item.child(0,0).data(0)
        component = self.model.getComponentById(compID)
        # Si el dato modificado fue el nombre.
        if item.column() == 0:
            component.name = item.data(0)
            qDebug('Changed name of'+self._nfc(component.imgPath)
                   +'from components\' tree, to '+self._nfc(component.name))
        # Si el dato modificado fue la visibilidad.
        if item.column() == 1:
            if item.checkState() == 0:
                component.visible = False
            elif item.checkState() == 2:
                component.visible = True
            component.visibleEffect()
            qDebug('Changed visible status of'+self._nfc(component.name)
                   +'from components\' tree, to '+self._nfc(component.visible))
        # Si el dato modificado fue el estado activo.
        if item.column() == 2:
            if item.checkState() == 0:
                component.active = False
            elif item.checkState() == 2:
                component.active = True
            component.visibleEffect()
            qDebug('Changed active status of'+self._nfc(component.name)
                   +'from components\' tree, to '+self._nfc(component.active))
        # Si el dato modificado fue la posicion Z.
        if item.column() == 3:
            newZ = item.data(0)
            if re.match("\d+\.\d*", newZ) or newZ.isdigit():
                component.setZValue(float(newZ))
                qDebug('Changed Z value of'+self._nfc(component.name)
                       +'from components\' tree, to '
                       +self._nfc(component.zValue()))
            else:
                qDebug('Trying to chang Z value of'+self._nfc(component.name)
                       +'from components\' tree, but entered an invalid value')
        # Actualiza los datos del arbol.
        self._updateTree()


# .--------------------.
# | Señales del Modelo |
# -------------------------------------------------------------------------- #

    ## @brief      Crea la escena segun el modelo al recibir la notificación.
    ## @param      self  Presentador.
    ## @return     None
    def listener_modelUpdated(self):
        scene = self.model.copyScene()
        self.view.resetWorkScene()
        for component in scene:
            self.view.workScene.addItem(component)
        self.model.scene = scene
        qDebug('Updated VIEW by MODEL notification')
        # Actualiza los datos en el arbol de componentes.
        self._updateTree()


# .--------------------------------.
# | Logicas externas a las señales |
# -------------------------------------------------------------------------- #

    ## @brief      Convierte el valor de entrada a una cadena Unicode-NFC
    ## @param      self     Presentador.
    ## @param      inValue  Valor de entrada.
    ## @return     str
    def _nfc(self,inValue):
        inValue = str(inValue)
        nfc = unicodedata.normalize('NFC',inValue)
        return re.sub(r'[^\x00-\x7f]',r'',nfc)

    ## @brief      Resetea el flag que controla guardar estado al redimesionar.
    ## @param      self  El componente simple.
    ## @return     None
    def _thResizeFlag(self):
        self.__saveFlagResize = True

    ## @brief      Resetea el flag que controla guardar estado al mover.
    ## @param      self  El componente simple.
    ## @return     None
    def _thMoveFlag(self):
        self.__saveFlagMove = True

    ## @brief      Comprueba si el cursor se encuentra sobre un widget dado.
    ## @param      self    Presentador.
    ## @param      widget  El widget sobre el que hacer la comprobacion.
    ## @return     True si esta encima, False en caso contrario.
    def _isOver(self,widget):
        mouse = widget.mapFromGlobal(QCursor.pos())
        return widget.geometry().contains(mouse)

    ## @brief      Recupera los componentes de la escena.
    ## @param      self  Presentador.
    ## @return     list
    def _getComponents(self):
        items = self.view.workScene.items()
        for item in items:
            if type(item) == QGraphicsRectItem:
                items.remove(item)
        return items

    ## @brief      Devuelve los items seleccionados en la escena.
    ## @param      self  Presentador.
    ## @return     <list> de componentes. (Simples y Complejos)
    def _selectedItems(self):
        selectedItems = []
        for item in self.view.workScene.items():
            if item.isSelected():
                selectedItems.append(item)
        return selectedItems

    ## @brief      Actualiza los arboles de la aplicacion.
    ## @param      self  Presentador.
    ## @return     None
    def _updateTree(self):
        treeModel = self.view.simpleTree.model()
        treeModel.removeRows(0, treeModel.rowCount()) # Vacia el arbol.
        for elem in self.model.scene:
            # Guarda el ID de forma oculta.
            child0 = QStandardItem(elem.id)
            child1 = QStandardItem(elem.id)
            child2 = QStandardItem(elem.id)
            child3 = QStandardItem(elem.id)
            # Nombre del elemento.
            icon = QIcon(elem.imgPath)
            col0 = QStandardItem(icon,elem.name)
            col0.setChild(0,0,child0)
            # Estado Visible del elemento.
            col1 = QStandardItem()
            if elem.visible == True:
                col1.setCheckState(Qt.Checked)
            else:
                col1.setCheckState(Qt.Unchecked)
            col1.setCheckable(True)
            col1.setChild(0,0,child1)
            # Estado Acvtivo del elemento.
            col2 = QStandardItem()
            if elem.active == True:
                col2.setCheckState(Qt.Checked)
            else:
                col2.setCheckState(Qt.Unchecked)
            col2.setCheckable(True)
            col2.setChild(0,0,child2)
            # Posicion Z para facilitar el control de la profundidad.
            col3 = QStandardItem(str(elem.getPosZ()))
            col3.setChild(0,0,child3)
            # Compone la fila y la agregamos al arbol.
            treeModel.appendRow( [col0 , col1, col2, col3] )
            qDebug('Updated components\' tree')

    ## @brief      Muestra mensajes en la barra de estado.
    ## @param      self  Presentador.
    ## @param      text  Texto del mensaje.
    ## @return     None
    def _SbMsg(self,text):
        zoomInfo = QLabel('[{}%]'.format(self.view.scale*100))
        self.view.statusBar().addPermanentWidget(zoomInfo)
        self.view.statusBar().showMessage(str(text))

        # DEBE SER UNA SEÑAL DE LA VISTA...
