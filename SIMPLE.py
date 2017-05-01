#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys,, json, hashlib
from pprint import pprint
from os.path import basename, normpath

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from PresetValues import pv

##
## @brief      Clase que define un componente simple.
##
class SimpleComponent(QGraphicsPixmapItem):

	##
	## @brief      Constructor de componentes simples.
	##
	## @param      self     El componente simple.
	## @param      imgPath  La ruta de la imagen base.
	##
	def __init__(self, imgPath):
		super().__init__()

		# Configura ciertas propiedades.
		self.setPixmap(QPixmap(imgPath))
		self.setCursor(QCursor(Qt.PointingHandCursor)) # Cursor = mano.
		self.setTransformationMode(Qt.SmoothTransformation) # AntiAliasing.
		self.setFlags(self.ItemIsSelectable|self.ItemIsMovable) # Move & Select

		# Id para localizar el elemento en una estructura de datos.
		self._id = hashlib.sha1(os.urandom(128)).hexdigest()

		# Atributos no heredados.
		self._active = True
		self._path = imgPath
		self._name = '[S]'+basename(normpath(imgPath))[:-4]

	##
	## @brief      Sobrecarga del metodo __str__.
	##
	## @param      self  El copmonente simple.
	##
	## @return     Cadena que representa al objeto componente simple.
	##
	def __str__( self ):
		return json.dumps(self.__dict__,indent=4)

	##
	## @brief      Sobrecarga del metodo __copy__.
	##
	## @param      self  El componente simple.
	##
	## @return     SIMPLE.SimpleComponent
	##
	def __copy__(self):
		new = type(self)(self._path)
		new.__dict__.update(self.__dict__)
		new.setPos(self.getPosX(),self.getPosY())
		new.setScale(self.getSizeX()/self.boundingRect().width())
		new.setZValue(self.getPosZ())
		new.setVisible(self.getVisible())
		new.activeEffect()
		return new


	# --- Manejode los atributos no heredados.

	##
	## @brief      Propiedad de lectura del id.
	##
	## @param      self  El componente simple.
	##
	## @return     <str>
	##
	@property
	def id(self):
		return self._id

	##
	## @brief      Propiedad de lectura del nombre.
	##
	## @param      self  El componente simple.
	##
	## @return     <str>
	##
	@property
	def name(self):
		return self._name

	##
	## @brief      Propiedad de escritura del nombre.
	##
	## @param      self  El componente simple.
	## @param      name  El nombre a escribir.
	##
	## @return     None
	##
	@name.setter
	def name(self,name):
		self._name = name

	##
	## @brief      Propiedad de lectura de la ruta de la imagen que lo define.
	##
	## @param      self  El componente simple.
	##
	## @return     <str>
	##
	@property
	def path(self):
		return self._path

	##
	## @brief      Propiedad de escritura de la ruta de la imagen que lo define.
	##
	## @param      self  El componente simple.
	## @param      path  La ruta a escribir.
	##
	## @return     None
	##
	@path.setter
	def path(self,path):
		self._path = path

	##
	## @brief      Propiedad de lectura del estado activo o inactivo.
	##
	## @param      self  El componente simple.
	##
	## @return     True si lo está, False en caso contrario.
	##
	@property
	def active(self):
		return self._active

	##
	## @brief      Propiedad de escritura del estado activo o inactivo.
	##
	## @param      self    El componente simple.
	## @param      active  El estado a escribir.
	##
	## @return     None
	##
	@active.setter
	def active(self,active):
		self._active = active


	# --- Lectura de los atributos heredados.

	##
	## @brief      Comprueba si el componente es visbile o no.
	##
	## @param      self  El componente simple.
	##
	## @return     True si lo es, False en caso contrario.
	##
	def getVisible(self):
		return self.isVisible()

	##
	## @brief      Calcula el ancho en base a la imagen original y la escala.
	##
	## @param      self  El componente simple.
	##
	## @return     qreal, el ancho visual del componente.
	##
	def getSizeX(self):
		return self.boundingRect().width()  * self.scale()

	##
	## @brief      Calcula el alto en base a la imagen original y la escala.
	##
	## @param      self  El componente simple.
	##
	## @return     qreal, el alto visual del componente.
	##
	def getSizeY(self):
		return self.boundingRect().height() * self.scale()

	##
	## @brief      Recupera la posicion X del componente.
	##
	## @param      self  El componente simple.
	##
	## @return     qreal
	##
	def getPosX(self):
		return self.pos().x()

	##
	## @brief      Recupera la posicion Y del componente.
	##
	## @param      self  El componente simple.
	##
	## @return     qreal
	##
	def getPosY(self):
		return self.pos().y()

	##
	## @brief      Recupera la posicion Z del componente.
	##
	## @param      self  El componente simple.
	##
	## @return     qreal
	##
	def getPosZ(self):
		return self.zValue()

	##
	## @brief      Obtiene la venta que contiene este componente.
	##
	## @param      self  El componente simple.
	##
	## @return     PyQt5.QtWidget.QMainWindow
	##
	def getWindow(self):
		return self.scene().parent().parent()


	# --- Manejo de eventos.

	##
	## @brief      Controlar el giro de la rueda para escalar el componente.
	##
	## @param      self  El componente simple.
	## @param      ev    Objeto con los datos del evento.
	##
	## @return     None
	##
	def wheelEvent(self, ev):
		self.getWindow().emit_Resize(ev.delta())

	##
	## @brief      Invoca el menu contextual relativo a este componente.
	##
	## @param      self  El componente simple.
	## @param      ev    Objeto con los datos del evento.
	##
	## @return     None
	##
	def contextMenuEvent(self, ev):
		self.setSelected(True)
		self.getWindow().emit_SimpleMenu()


	# --- Acciones emisoras.

	##
	## @brief      Emite señal para cambiar su visibilidad.
	##
	## @param      self  El componente simple.
	##
	## @return     None
	##
	def toggleVisible(self):
		# self.getWindow().emit_Visible()

	##
	## @brief      Emite señal para cambiar su estado activo.
	##
	## @param      self  El componente simple.
	##
	## @return     None
	##
	def toggleActive(self):
		self.getWindow().emit_Active()

	##
	## @brief      Resta opacidad si el componente no esta activo.
	##
	## @param      self  El componente simple.
	##
	## @return     None
	##
	def activeEffect(self):
		if self.active is True:
			self.setOpacity(pv['maxOpacity'])
		else:
			self.setOpacity(pv['minOpacity'])

	##
	## @brief      Incrementa el valor de la Z.
	##
	## @param      self  El componente simple.
	##
	## @return     None
	##
	def incZ(self):
		self.getWindow().emit_ZInc()

	##
	## @brief      Incrementa el valor de la Z.
	##
	## @param      self  El componente simple.
	##
	## @return     None
	##
	def decZ(self):
		self.getWindow().emit_ZDec()

	# Dialogo de detalles.
	def detailsDialog(self):
		QMessageBox.information(self.getWindow(),'¡DETALLES!', self.__str__())
