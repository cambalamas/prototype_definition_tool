#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import copy
from collections import deque

from PyQt5.QtCore import *

from PresetValues import pv


## @brief      Clase que se encarga de la gestion de datos y persistencia.
class MODEL( QObject ):


# .---------.
# | Señales |
# -------------------------------------------------------------------------- #

	## Señal para solicitar actualizacion de la vista.
	signal_modelUpdated = pyqtSignal()


# .----------.
# | Emisores |
# -------------------------------------------------------------------------- #

	## @brief      Emisor de la señal de actualizacion.
	## @param      self  Modelo.
	## @return     None
	def emit_modelUpdated(self):
			self.signal_modelUpdated.emit()


# .-------------.
# | Constructor |
# -------------------------------------------------------------------------- #

	## @brief      Cosntructor del Modelo.
	## @param      self  Modelo.
	def __init__(self):
		super().__init__()
		## Componente complejo principal.
		## Sobre este componente se define toda la interfaz
		## y es el que pasaremos luego al Experto de XML para guardar.
		self.__interface = str()
		## Cola doble de items en la escena principal.
		## Se usa deque en lugar de queue.Queue porque
		## sera necesario iterar, para construir la escena.
		self.__scene = deque()
		## Cola doble de items para una escena secundaria.
		## Como la edicion de un componente complejo.
		self.__tempScene = deque()
		## Pila con los estados anteriores de la interfaz.
		self.__undo = deque(maxlen=pv['historyLimit'])
		## Pila con los estados posteriores de la interfaz.
		self.__redo = deque(maxlen=pv['historyLimit'])


# .-------------------------------------------.
# | Acceso 'publico' a las variables privadas |
# -------------------------------------------------------------------------- #

	## @brief      Propieda de lectura del componente interfaz.
	## @param      self  Modelo.
	## @return     COMPLEX.ComplexComponent
	@property
	def interface(self):
		return self.__interface

	## @brief      Propiedad de lectura de la pila de items.
	## @param      self  Modelo.
	## @return     collections.deque
	@property
	def scene(self):
		return self.__scene

	## @brief      Propiedad de escritura de la pila de items.
	## @param      self   Modelo.
	## @param      scene  Un iterable con la escena a escribir.
	## @return     None
	@scene.setter
	def scene(self,scene):
		self.__scene = deque(scene)
		# self.emit_modelUpdated() # Recursion infinita.

	## @brief      Propiedad de lectura de la pila para escenas temporales.
	## @param      self  Modelo.
	## @return     collections.deque
	@property
	def tempScene(self):
		return self.__tempScene

	## @brief      Propiedad de escritura de la pila para escenas temporales.
	## @param      self       Modelo.
	## @param      tempScene  La escena a escribir.
	## @return     None
	@tempScene.setter
	def tempScene(self,tempScene):
		self.__tempScene = tempScene


# .----------------------.
# | Gestion de los datos |
# -------------------------------------------------------------------------- #

	## @brief      Agrega un componente a la pila.
	## @param      self       Modelo.
	## @param      component  El componente a agregar.
	## @return     None
	def newComponent(self,component):
		self.scene.append(component)
		self.emit_modelUpdated()

	## @brief      Elimina un componente de la pila.
	## @param      self       Modelo.
	## @param      component  Lista de componentes a borrar.
	## @return     None
	def delComponent(self,components):
		for component in components:
			self.scene.remove(component)
		self.emit_modelUpdated()

	## @brief      Obtiene un componente en base a un ID dado.
	## @param      self  Modelo.
	## @param      id    El identificador a buscar.
	## @return     Un componente de la escena.
	def getComponentById(self,c_id):
		for component in self.scene:
			if component.id == c_id:
				return component


# .----------------------.
# | Gestion de historico |
# -------------------------------------------------------------------------- #

	## @brief      Guarda el estado actual en la pila de deshacer.
	## @param      self  Modelo.
	## @return     None
	def saveState(self):
		self.__undo.append(self.copyScene())
		self.__redo.clear()

	## @brief      Operacion sobre datos al solicitar la accion deshacer.
	## @param      self  Modelo.
	## @return     None
	def undo(self):
		if not len(self.__undo) == 0:
			self.__redo.append(self.copyScene())
			self.scene = self.__undo.pop()
			self.emit_modelUpdated()

	## @brief      Operacion sobre datos al solicitar la accion rehacer.
	## @param      self  Modelo.
	## @return     None
	def redo(self):
		if not len(self.__redo) == 0:
			self.__undo.append(self.copyScene())
			self.scene = self.__redo.pop()
			self.emit_modelUpdated()


# .----------------------.
# | Funciones auxiliares |
# -------------------------------------------------------------------------- #

	## @brief      Devuelve una copia de la escena actual.
	## @param      self  Modelo.
	## @return     Lista de componentes.
	def copyScene(self):
		return [copy(x) for x in self.scene]
