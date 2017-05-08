#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, hashlib
from os.path import basename, normpath
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PresetValues import pv

## @brief      Clase que define un componente simple.
class SimpleComponent(QGraphicsPixmapItem):

	## @brief      Constructor de componentes simples.
	## @param      self     Componente Simple.
	## @param      imgPath  La ruta de la imagen base.
	def __init__(self, imgPath):
		super().__init__()

		# Configura ciertas propiedades.
		self.oPixmap = QPixmap(imgPath)
		self.setPixmap(self.oPixmap)
		self.setFlags(self.ItemIsSelectable) # Implemnt tipica de seleccion.
		self.setCursor(QCursor(Qt.PointingHandCursor)) # Cursor = mano.
		self.setTransformationMode(Qt.SmoothTransformation) # AntiAliasing.

		# Id para localizar el elemento en una estructura de datos.
		self.__id = hashlib.sha1(os.urandom(128)).hexdigest()

		# Atributos no heredados.
		self.__active = True
		self.__visible = True
		self.__path = imgPath
		self.__name = '[S]'+basename(normpath(imgPath))[:-4]


# .------------------------------------.
# | Sobreescritura de metodos internos |
# --------------------------------------------------------------------------- #

	## @brief      Genera un diccionario con los datos del componente.
	## @param      self  Componente Simple.
	## @return     <dict>
	def readObj(self):
		data = {
			'Ruta'   	: self.__path,
			'Nombre' 	: self.__name,
			'Activo' 	: self.__active,
			'Visible'	: self.__visible,
			'SizeX'  	: self.getSizeX(),
			'SizeY'  	: self.getSizeY(),
			'PosX'	 	: self.getPosX(),
			'PosY'	 	: self.getPosY(),
			'PosZ'	 	: self.getPosZ()
		}
		return data

	## @brief      Sobrecarga del metodo __str__.
	## @param      self  Componente simple.
	## @return     Cadena que representa al objeto componente simple.
	def __str__( self ):
		toString = json.dumps(self.readObj(),indent=0)
		return toString[1:-1]


	## @brief      Sobrecarga del metodo __copy__.
	## @param      self  Componente Simple.
	## @return     SIMPLE.SimpleComponent
	def __copy__(self):
		new = type(self)(self.__path)
		new.__dict__.update(self.__dict__)
		new.setPos(self.getPosX(),self.getPosY())
		new.setScale(self.getSizeX()/self.boundingRect().width())
		new.setZValue(self.getPosZ())
		new.visibleEffect()
		return new


# .--------------------------------------.
# | Manejo de los atributos no heredados |
# --------------------------------------------------------------------------- #

	## @brief      Propiedad de lectura del id.
	## @param      self  Componente Simple.
	## @return     <str>
	@property
	def id(self):
		return self.__id

	## @brief      Propiedad de lectura del nombre.
	## @param      self  Componente Simple.
	## @return     <str>
	@property
	def name(self):
		return self.__name

	## @brief      Propiedad de escritura del nombre.
	## @param      self  Componente Simple.
	## @param      name  El nombre a escribir.
	## @return     None
	@name.setter
	def name(self,name):
		self.__name = name

	## @brief      Propiedad de lectura de la ruta de la imagen que lo define.
	## @param      self  Componente Simple.
	## @return     <str>
	@property
	def path(self):
		return self.__path

	## @brief      Propiedad de escritura de la ruta de la imagen que lo define.
	## @param      self  Componente Simple.
	## @param      path  La ruta a escribir.
	## @return     None
	@path.setter
	def path(self,path):
		self.__path = path

	## @brief      Propiedad de lectura del estado activo o inactivo.
	## @param      self  Componente Simple.
	## @return     True si lo está, False en caso contrario.
	@property
	def active(self):
		return self.__active

	## @brief      Propiedad de escritura del estado activo o inactivo.
	## @param      self    Componente Simple.
	## @param      active  El estado a escribir.
	## @return     None
	@active.setter
	def active(self,active):
		self.__active = active

	## @brief      Propiedad de lectura del estado visbile o no visible.
	## @param      self  Componente Simple.
	## @return     True si lo está, False en caso contrario.
	@property
	def visible(self):
		return self.__visible

	## @brief      Propiedad de escritura del estado visbile o no visible.
	## @param      self    Componente Simple.
	## @param      visible  El estado a escribir.
	## @return     None
	@visible.setter
	def visible(self,visible):
		self.__visible = visible


# .------------------------------------.
# | Lectura de los atributos heredados |
# --------------------------------------------------------------------------- #

	# --- .

	## @brief      Calcula el ancho en base a la imagen original y la escala.
	## @param      self  Componente Simple.
	## @return     qreal, el ancho visual del componente.
	def getSizeX(self):
		return self.boundingRect().width()  * self.scale()

	## @brief      Calcula el alto en base a la imagen original y la escala.
	## @param      self  Componente Simple.
	## @return     qreal, el alto visual del componente.
	def getSizeY(self):
		return self.boundingRect().height() * self.scale()

	## @brief      Recupera la posicion X del componente.
	## @param      self  Componente Simple.
	## @return     qreal
	def getPosX(self):
		return self.pos().x()

	## @brief      Recupera la posicion Y del componente.
	## @param      self  Componente Simple.
	## @return     qreal
	def getPosY(self):
		return self.pos().y()

	## @brief      Recupera la posicion Z del componente.
	## @param      self  Componente Simple.
	## @return     qreal
	def getPosZ(self):
		return self.zValue()

	## @brief      Obtiene la venta que contiene este componente.
	## @param      self  Componente Simple.
	## @return     PyQt5.QtWidget.QMainWindow
	def getWindow(self):
		return self.scene().parent().parent()


# .-------------------.
# | Manejo de eventos |
# --------------------------------------------------------------------------- #

	# Necesario para luego tener acceso a 'e.lastPos()'.

	## @brief      Acepta el primer clic para luego poder leer la pos anterior.
	## @param      self  Componente Simple.
	## @param      ev    Objeto con los datos del evento.
	## @return     None
	def mousePressEvent(self, ev):
		if ev.buttons() == Qt.LeftButton:
			ev.accept()

	# Mientras se manteniene clicado.

	## @brief      Controla el desplazamiento para mover el componente.
	## @param      self  Componente Simple.
	## @param      ev    Objeto con los datos del evento.
	## @return     None
	def mouseMoveEvent(self, ev):
		if self.isSelected():
			if ev.buttons() == Qt.LeftButton:
				self.getWindow().emit_Move(ev.lastPos(),ev.pos())

	## @brief      Controlar el giro de la rueda para escalar el componente.
	## @param      self  Componente Simple.
	## @param      ev    Objeto con los datos del evento.
	## @return     None
	def wheelEvent(self, ev):
		if self.isSelected():
			self.getWindow().emit_Resize(ev.delta())

	## @brief      Invoca el menu contextual relativo a este componente.
	## @param      self  Componente Simple.
	## @param      ev    Objeto con los datos del evento.
	## @return     None
	def contextMenuEvent(self, ev):
		self.setSelected(True)
		self.getWindow().emit_SimpleMenu()


# .---------------------.
# | Otros modificadores |
# --------------------------------------------------------------------------- #

	## @brief      Resta opacidad si el componente no esta activo.
	## @param      self  Componente Simple.
	## @return     None
	def activeEffect(self):
		if self.active:
			self.setOpacity(pv['maxOpacity'])
		else:
			self.setOpacity(pv['noActiveOpacity'])

	## @brief      Resta opacidad si el componente no es visible.
	## @param      self  Componente Simple.
	## @return     None
	def visibleEffect(self):
		if self.visible:
			self.activeEffect()
		else:
			self.setOpacity(pv['noVisibleOpacity'])

	# Dialogo de detalles.
	def detailsDialog(self):
		QMessageBox.information(self.getWindow(),'¡DETALLES!', self.__str__())
