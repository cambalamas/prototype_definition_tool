#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque

from PyQt5.QtCore import *

##
## @brief      Clase que se encarga de la gestion de datos y persistencia.
##
class MODEL( QObject ):

	# Señal para solicitar actualizacion de la vista.
	signal_modelUpdated = pyqtSignal()

	##
	## @brief      Emisor de la señal de actualizacion.
	##
	## @param      self  Este modelo.
	##
	## @return     None
	##
	def emit_modelUpdated(self):
		self.signal_modelUpdated.emit()

	##
	## @brief      Cosntructor del Modelo.
	##
	## @param      self  Este modelo.
	##
	def __init__(self):
		super().__init__()

		# Componente complejo principal.
		# Sobre este componente se define toda la interfaz
		# y es el que pasaremos luego al Experto de XML para guardar.
		self._interface = str()

		# Pila de items en la escena principal.
		# Se usa deque en lugar de queue.Queue porque
		# sera necesario iterar, para construir la escena.
		self._scene = deque()

		# Pila de items para una escena secundaria.
		# Como la edicion de un componente complejo.
		self._tempScene = deque()

	##
	## @brief      Propieda de lectura del componente interfaz.
	##
	## @param      self  Este modelo.
	##
	## @return     COMPLEX.ComplexComponent
	##
	@property
	def interface(self):
		return self._interface

	##
	## @brief      Propiedad de lectura de la pila de items.
	##
	## @param      self  Este modelo.
	##
	## @return     collections.deque
	##
	@property
	def scene(self):
		return self._scene

	##
	## @brief      Propiedad de escritura de la pila de items.
	##
	## @param      self   Este modelo.
	## @param      scene  La escena a escribir.
	##
	## @return     None
	##
	@scene.setter
	def scene(self,scene):
		self._scene = scene
		# self.emit_modelUpdated() # Recursion infinita.

	##
	## @brief      Propiedad de lectura de la pila para escenas temporales.
	##
	## @param      self  Este modelo.
	##
	## @return     collections.deque
	##
	@property
	def tempScene(self):
		return self._tempScene

	##
	## @brief      Propiedad de escritura de la pila para escenas temporales.
	##
	## @param      self       Este modelo.
	## @param      tempScene  La escena a escribir.
	##
	## @return     None
	##
	@tempScene.setter
	def tempScene(self,tempScene):
		self._tempScene = tempScene

	##
	## @brief      Agrega un componente a la pila.
	##
	## @param      self       Este modelo.
	## @param      component  El componente a agregar.
	##
	## @return     None
	##
	def newComponent(self,component):
		self._scene.append(component)
		self.emit_modelUpdated()

	##
	## @brief      Elimina un componente de la pila.
	##
	## @param      self       Este modelo.
	## @param      component  Lista de componentes a borrar.
	##
	## @return     None
	##
	def delComponent(self,components):
		for component in components:
			self._scene.remove(component)
		self.emit_modelUpdated()
