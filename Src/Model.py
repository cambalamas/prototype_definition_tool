#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque

from PyQt5.QtCore import *

from PresetValues import pv
from State import State


# @brief      Clase que se encarga de la gestion de datos y persistencia.
class Model(QObject):

    # .---------.
    # | Señales |
    # ---------------------------------------------------------------------- #

        # Señal para solicitar actualizacion de la vista.
    signal_ModelUpdated = pyqtSignal()

# .----------.
# | Emisores |
# -------------------------------------------------------------------------- #

    # @brief      Emisor de la señal de actualizacion.
    # @param      self  Modelo.
    # @return     None
    def emit_ModelUpdated(self):
        self.signal_ModelUpdated.emit()

# .-------------.
# | Constructor |
# -------------------------------------------------------------------------- #

    # @brief      Cosntructor del Modelo.
    # @param      self  Modelo.
    def __init__(self):
        super().__init__()
        self.__states = deque()
        self.__curStatePos = 0
        self.curState = \
            lambda: self.__states[self.__curStatePos]


# .-------------------------------------------.
# | Acceso 'publico' a las variables privadas |
# -------------------------------------------------------------------------- #

    # @brief      Propiedad de lectura de la pila de items.
    # @param      self  Modelo.
    # @return     object, Scene
    @property
    def states(self):
        return self.__states

    # @brief      Propiedad de escritura de la pila de items.
    # @param      self  Modelo.
    # @return     None
    @states.setter
    def states(self, states):
        self.__states = states
        # self.curStatePos = 0 # Actualiza la posicion actual y la vista.

    # @brief      Propiedad de lectura del estado activo.
    # @param      self  Modelo.
    # @return     int
    @property
    def curStatePos(self):
        return self.__curStatePos

    # @brief      Propiedad de escritura del estado activo.
    # @param      self  Modelo.
    # @return     None
    @curStatePos.setter
    def curStatePos(self, curStatePos):
        self.__curStatePos = curStatePos
        self.emit_ModelUpdated()


# .----------------------.
# | Gestion de los datos |
# -------------------------------------------------------------------------- #

    # @brief      Crea un nuevo estado.
    # @param      self  Modelo
    # @return     None
    def createState(self):
        newState = State()
        self.states.append(newState)
        self.curStatePos = self.states.index(newState)
        self.emit_ModelUpdated()

    # @brief      Borra un estado de la lista.
    # @param      self   Modelo.
    # @param      state  El estado a borrar.
    # @return     None
    def deleteState(self, state, *autoupdate):
        self.states.remove(state)
        if not autoupdate:
            self.emit_ModelUpdated()

    # @brief      Agrega un componente a la pila del estado actual.
    # @param      self       Modelo.
    # @param      component  El componente a agregar.
    # @return     None
    def newComponent(self, component):
        self.curState().newComponent(component)
        self.emit_ModelUpdated()

    # @brief      Elimina un componente de la pila del estado actual.
    # @param      self       Modelo.
    # @param      component  Lista de componentes a borrar.
    # @return     None
    def delComponent(self, components):
        self.curState().delComponent(components)
        self.emit_ModelUpdated()

    # @brief      Obtiene un componente por ID, del estado actual.
    # @param      self  Modelo.
    # @param      id    El identificador a buscar.
    # @return     Un componente de la escena.
    def getComponentById(self, c_id):
        return self.curState().getComponentById(c_id)


# .----------------------.
# | Gestion de historico |
# -------------------------------------------------------------------------- #

    # @brief      Guarda historico del estado actual.
    # @param      self  Modelo.
    # @return     None
    def saveState(self):
        self.curState().saveState()

    # @brief      Operacion deshacer  del estado actual.
    # @param      self  Modelo.
    # @return     None
    def undo(self):
        self.curState().undo()
        self.emit_ModelUpdated()

    # @brief      Operacion rehacer del estado actual.
    # @param      self  Modelo.
    # @return     None
    def redo(self):
        self.curState().redo()
        self.emit_ModelUpdated()


# .----------------------.
# | Funciones auxiliares |
# -------------------------------------------------------------------------- #

    # @brief      Devuelve una copia de la escena del estado actual.
    # @param      self  Modelo.
    # @return     collections.deque
    def copyScene(self):
        return self.curState().copyScene()
