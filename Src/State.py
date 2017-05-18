#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import copy
from collections import deque

from PresetValues import pv


## @brief      Clase que define los datos de un estado.
class State(object):

# .-------------.
# | Constructor |
# -------------------------------------------------------------------------- #

    ## @brief      Constructor del estado.
    ## @param      self  Estado.
    def __init__(self):
        ## Cola doble de items en la escena.
        ## Se usa deque en lugar de queue.Queue porque
        ## sera necesario iterar, para construir la escena.
        self.__scene = deque()
        ## Pila con los estados anteriores de la interfaz.
        self.__undo = deque(maxlen=pv['historyLimit'])
        ## Pila con los estados posteriores de la interfaz.
        self.__redo = deque(maxlen=pv['historyLimit'])


# .----------------------.
# | Gestion de los datos |
# -------------------------------------------------------------------------- #

    ## @brief      Agrega un componente a la pila.
    ## @param      self       Estado.
    ## @param      component  El componente a agregar.
    ## @return     None
    def newComponent(self,component):
        self.__scene.append(component)

    ## @brief      Elimina un componente de la pila.
    ## @param      self       Estado.
    ## @param      component  Lista de componentes a borrar.
    ## @return     None
    def delComponent(self,components):
        for component in components:
            self.__scene.remove(component)

    ## @brief      Obtiene un componente en base a un ID dado.
    ## @param      self  Estado.
    ## @param      id    El identificador a buscar.
    ## @return     Un componente de la escena.
    def getComponentById(self,c_id):
        for component in self.__scene:
            if component.id == c_id:
                return component


# .----------------------.
# | Gestion de historico |
# -------------------------------------------------------------------------- #

    ## @brief      Guarda el estado actual en la pila de deshacer.
    ## @param      self  Estado.
    ## @return     None
    def saveState(self):
        self.__undo.append(self.copyScene())
        self.__redo.clear()

    ## @brief      Operacion sobre datos al solicitar la accion deshacer.
    ## @param      self  Estado.
    ## @return     None
    def undo(self):
        if not len(self.__undo) == 0:
            self.__redo.append(self.copyScene())
            self.scene = self.__undo.pop()

    ## @brief      Operacion sobre datos al solicitar la accion rehacer.
    ## @param      self  Estado.
    ## @return     None
    def redo(self):
        if not len(self.__redo) == 0:
            self.__undo.append(self.copyScene())
            self.scene = self.__redo.pop()


# .----------------------.
# | Funciones auxiliares |
# -------------------------------------------------------------------------- #

    ## @brief      Devuelve una copia de la escena.
    ## @param      self  Estado.
    ## @return     collections.deque
    def copyScene(self):
        return [copy(x) for x in self.__scene]
