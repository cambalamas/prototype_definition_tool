#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, hashlib
from pprint import pprint
from os.path import basename, normpath

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from PresetValues import pv


'''
Clase que heredara de 'QGraphicsPixmapItem' y nos permitira controlar el
comportamiento del objeto ante distintos eventos.

'''
class SimpleComponent(QGraphicsPixmapItem):
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

	def __str__( self ):
		return self.__dict__

	def __copy__(self):
		new = type(self)(self._path)
		new.__dict__.update(self.__dict__)
		new.setPos(self.getPosX(),self.getPosY())
		new.setScale(self.getSizeX()/self.boundingRect().width())
		new.setZValue(self.getPosZ())
		new.setVisible(self.getVisible())
		new.activeEffect()
		return new


	# --- Recupera los atributos no heredados.

	@property
	def id(self):
		return self._id
	@property
	def name(self):
		return self._name
	@property
	def path(self):
		return self._path
	@property
	def active(self):
		return self._active

	# --- Modifica los atributos no heredados.

	@name.setter
	def name(self,name):
		self._name = name
	@path.setter
	def path(self,path):
		self._path = path
	@active.setter
	def active(self,active):
		self._active = active

	# --- Recupera los atributos del objeto heredados.

	def getVisible(self):
		return self.isVisible()
	def getSizeX(self):
		return self.boundingRect().width()  * self.scale()
	def getSizeY(self):
		return self.boundingRect().height() * self.scale()
	def getPosX(self):
		return self.pos().x()
	def getPosY(self):
		return self.pos().y()
	def getPosZ(self):
		return self.zValue()
	def getWindow(self):
		return self.scene().parent().parent()



# ----------------------------------------------------------------- #
#					   INTERACCION :: EVENTOS 						#
# ----------------------------------------------------------------- #

	'''
	Este evento controla el giro de la rueda del raton, y lo usaremos
	para manejar la escala de la imagen. Modificando asi virtualmente
	su anchura y altura.
	'''
	def wheelEvent(self, ev):
		self.getWindow().emit_Resize(ev.delta())


	# Menu contextual
	def contextMenuEvent(self, ev):
		self.setSelected(True)
		self.getWindow().emit_SimpleMenu()

	# Toggle de Visibilidad.
	def toggleVisible(self):
		self.getWindow().emit_Visible()

	# Toggle de Actividad.
	def toggleActive(self):
		self.getWindow().emit_Active()

	# Resta opacidad si el componente no esta activo.
	def activeEffect(self):
		if self.active is True:
			self.setOpacity(pv['maxOpacity'])
		else:
			self.setOpacity(pv['minOpacity'])

	# Incrementa el valor de la Z.
	def incZ(self):
		self.getWindow().emit_ZInc()

	# Decrementa el valor de la Z, nunca menor que 0.
	def decZ(self):
		self.getWindow().emit_ZDec()

	# Dialogo de detalles.
	def detailsDialog(self):
		QMessageBox.information(self.getWindow(),'¡DETALLES!', self.__str__())
