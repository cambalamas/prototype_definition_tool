#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import copy
from collections import deque

from PyQt5.QtCore import *

from PresetValues import pv

## @brief      Clase que se encarga de la gestion de datos y persistencia.
class MODEL( QObject ):

	# Señal para solicitar actualizacion de la vista.
	signal_modelUpdated = pyqtSignal()

	## @brief      Emisor de la señal de actualizacion.
	## @param      self  Este modelo.
	## @return     None
	def emit_modelUpdated(self):
			self.signal_modelUpdated.emit()

	## @brief      Cosntructor del Modelo.
	## @param      self  Este modelo.
	def __init__(self):
		super().__init__()
		# Componente complejo principal.
		# Sobre este componente se define toda la interfaz
		# y es el que pasaremos luego al Experto de XML para guardar.
		self._interface = str()
		# Cola doble de items en la escena principal.
		# Se usa deque en lugar de queue.Queue porque
		# sera necesario iterar, para construir la escena.
		self._scene = deque()
		# Cola doble de items para una escena secundaria.
		# Como la edicion de un componente complejo.
		self._tempScene = deque()
		# Pila con los estados anteriores de la interfaz.
		self._undo = deque(maxlen=pv['historyLimit'])
		# Pila con los estados posteriores de la interfaz.
		self._redo = deque(maxlen=pv['historyLimit'])


	## @brief      Propieda de lectura del componente interfaz.
	## @param      self  Este modelo.
	## @return     COMPLEX.ComplexComponent
	@property
	def interface(self):
		return self._interface

	## @brief      Propiedad de lectura de la pila de items.
	## @param      self  Este modelo.
	## @return     collections.deque
	@property
	def scene(self):
		return self._scene

	## @brief      Propiedad de escritura de la pila de items.
	## @param      self   Este modelo.
	## @param      scene  La escena a escribir.
	## @return     None
	@scene.setter
	def scene(self,scene):
		self._scene = scene
		# self.emit_modelUpdated() # Recursion infinita.

	## @brief      Propiedad de lectura de la pila para escenas temporales.
	## @param      self  Este modelo.
	## @return     collections.deque
	@property
	def tempScene(self):
		return self._tempScene

	## @brief      Propiedad de escritura de la pila para escenas temporales.
	## @param      self       Este modelo.
	## @param      tempScene  La escena a escribir.
	## @return     None
	@tempScene.setter
	def tempScene(self,tempScene):
		self._tempScene = tempScene

	## @brief      Agrega un componente a la pila.
	## @param      self       Este modelo.
	## @param      component  El componente a agregar.
	## @return     None
	def newComponent(self,component):
		self._scene.append(component)
		self.emit_modelUpdated()

	## @brief      Elimina un componente de la pila.
	## @param      self       Este modelo.
	## @param      component  Lista de componentes a borrar.
	## @return     None
	def delComponent(self,components):
		for component in components:
			self._scene.remove(component)
		self.emit_modelUpdated()

	## @brief      Obtiene un componente en base a un ID dado.
	## @param      self  Este modelo.
	## @param      id    El identificador a buscar.
	## @return     Un componente de la escena.
	def getComponentById(self,id):
		for component in self._scene:
			if component.id == id:
				return component

	## @brief      Devuelve una copia de la escena actual.
	## @param      self  Este modelo.
	## @return     Lista de componentes.
	def copyScene(self):
		return [copy(x) for x in self._scene]


	## @brief      Guarda el estado actual en la pila de deshacer.
	## @param      self  Este modelo.
	## @return     None
	def saveState(self):
		self._undo.append(self.copyScene())
		self._redo.clear()

	## @brief      Operacion sobre datos al solicitar la accion deshacer.
	## @param      self  Este modelo.
	## @return     None
	def undo(self):
		if not len(self._undo) == 0:
			self._redo.append(self.copyScene())
			self._scene = self._undo.pop()
			self.emit_modelUpdated()

	## @brief      Operacion sobre datos al solicitar la accion rehacer.
	## @param      self  Este modelo.
	## @return     None
	def redo(self):
		if not len(self._redo) == 0:
			self._undo.append(self.copyScene())
			self._scene = self._redo.pop()
			self.emit_modelUpdated()
