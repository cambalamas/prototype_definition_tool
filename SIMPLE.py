#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, hashlib
from os.path import basename, normpath

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QGraphicsPixmapItem, QMessageBox, QMenu


'''
Clase que heredara de 'QGraphicsPixmapItem' y nos permitira controlar el
comportamiento del objeto ante distintos eventos.

'''
class SimpleComponent( QGraphicsPixmapItem ):
	def __init__(self, imgPath):
		super().__init__()
		self.setTransformationMode(Qt.SmoothTransformation) # AntiAliasing.
		self.setPixmap( QPixmap(imgPath) ) # Dialog si 'imgPath' no existe.

		# ----------------------------------------------------------------- #
		#						CLASE :: VARIABLES 							#
		# ----------------------------------------------------------------- #

		# Id para localizar el elmento en una estructura de datos.
		self.__id = hashlib.sha1(os.urandom(128)).hexdigest()

		# Estructura requerida para el XML.
		self.__name = '[S]'+basename(normpath(imgPath))[:-4]
		self.__path = imgPath
		self.__active = True
		self.__visible = self.isVisible()
		self.__sizeX = self.boundingRect().width()  * self.scale()
		self.__sizeY = self.boundingRect().height() * self.scale()
		self.__posX = self.boundingRect().x()
		self.__posY = self.boundingRect().y()
		self.__posZ = self.zValue()

		# Control del factor de escalado.
		self.__scaleMOD = 1.025
		self.__scaleMAX = 5.025
		self.__scaleMIN = 0.025


		# ----------------------------------------------------------------- #
		#					   GUI :: MENU CONTEXTUAL 						#
		# ----------------------------------------------------------------- #

		self.contextMenu = QMenu('MENU: Componente Simple')

		# ACCION: Incrementar profundidad del objeto.
		cmAct = self.contextMenu.addAction('INCREMENTA Profundidad')
		cmAct.setStatusTip('INCREMENTA Profundidad de > '+ self.getName())
		cmAct.triggered.connect(self.incZ)

		# ACCION: Decrementar profundidad del objeto.
		cmAct = self.contextMenu.addAction('DECREMENTA Profundidad')
		cmAct.setStatusTip('DECREMENTA Profundidad de > '+ self.getName())
		cmAct.triggered.connect(self.decZ)

		# Dibuja una linea horizontal.
		self.contextMenu.addSeparator()

		# ACCION: Activa / Desactiva el objeto.
		cmAct = self.contextMenu.addAction('Rota estado: ACTIVO')
		cmAct.setStatusTip('Activa / Desactiva el objeto > '+ self.getName())
		cmAct.triggered.connect(self.toggleActive)

		# ACCION: Muestra / Oculta el objeto.
		cmAct = self.contextMenu.addAction('Rota estado: VISIBLE')
		cmAct.setStatusTip('Muestra / Oculta el objeto > '+ self.getName())
		cmAct.triggered.connect(self.toggleVisible)

		# Dibuja una linea horizontal.
		self.contextMenu.addSeparator()

		# ACCION: Borra el objeto de la escena y el modelo.
		cmAct = self.contextMenu.addAction('BORRA el elemento')
		cmAct.setStatusTip('BORRA el elemento > '+ self.getName())
		cmAct.triggered.connect(self.removeItem)

		# Dibuja una linea horizontal.
		self.contextMenu.addSeparator()

		# ACCION: Dialogo con los detalles del objeto.
		cmAct = self.contextMenu.addAction('Informacion detallada...')
		cmAct.triggered.connect(self.detailsDialog)


	# ----------------------------------------------------------------- #
	#						CLASE :: 'TO STRING' 						#
	# ----------------------------------------------------------------- #

	# def __str__( self ):
	# 	retVal = '\nRUTA\t--->\t'+str(self.getPath())
	# 	retVal += '\n\nNOMBRE\t--->\t" '+self.getName()+' "'
	# 	retVal += '\n\n--------------------\n'
	# 	retVal += '\nZ\t\t--->\t'+str(self.getPosZ())
	# 	retVal += '\nACTIVO\t\t--->\t'+str(self.getActive())
	# 	retVal += '\nVISIBLE\t\t--->\t'+str(self.getVisible())
	# 	retVal += '\nY\t\t--->\t'+str(self.getPosY())
	# 	retVal += '\nX\t\t--->\t'+str(self.getPosX())
	# 	retVal += '\nALTO\t\t--->\t'+str(self.getSizeY())
	# 	retVal += '\nANCHO\t\t--->\t'+str(self.getSizeX())
	# 	return retVal

	def __copy__(self):
	  newone = type(self)(self.getPath())
	  newone.__dict__.update(self.__dict__)
	  return newone


# ----------------------------------------------------------------- #
#							CLASE :: 'GETTERS' 						#
# ----------------------------------------------------------------- #

	# Recupera los atributos del objeto que se almacenan en la estructura.
	def getID(self):
		return self.__id
	def getName(self):
		return self.__name
	def getPath(self):
		return self.__path
	def getActive(self):
		return self.__active
	def getScaleMod(self):
		return self.__scaleMOD
	def getScaleMax(self):
		return self.__scaleMAX
	def getScaleMin(self):
		return self.__scaleMIN

	# Recupera los atributos del objeto heredados del 'QGraphicsPixmapItem'
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

	# Obtiene la ventana en la que se visualiza.
	def getWindow(self):
		return self.scene().parent().parent()

	# Calcula la siguiente escala en base al factor de modificacion.
	def getNewScale(self,delta):
		# Giro de la rueda hacia adelante.
		if delta > 0:
			newScale = self.scale() * self.getScaleMod()
			if newScale < self.getScaleMax():
				return newScale
			else:
				return self.scale()
		# Giro de la rueda hacia atras.
		else:
			newScale = self.scale() / self.getScaleMod()
			if newScale > self.getScaleMin():
				return newScale
			else:
				return self.scale()


# ----------------------------------------------------------------- #
#							CLASE :: 'SETTERS' 						#
# ----------------------------------------------------------------- #

	# Reasigna el valor de los atributos del objeto que no dependen de
	# atributos herdados de 'QGraphicsPixmapItem' .
	def setName(self,newVal):
		self.__name = newVal
	def setPath(self,newVal):
		self.__path = newVal
	def setActiveState(self,newVal):
		self.__active = newVal

	# Elimina el objeto de la escena y otros contenedores.
	def removeItem(self):
		ELogic.directDelSimpleComp(self,self.getWindow())


# ----------------------------------------------------------------- #
#					   INTERACCION :: EVENTOS 						#
# ----------------------------------------------------------------- #

	# Necesario para luego tener acceso a 'e.lastPos()'.
	def mousePressEvent(self, ev):
		ev.accept()


	# Mientras se manteniene clicado.
	def mouseMoveEvent(self, ev):
		ELogic.saveState(self.getWindow())
		# Si esta pulsado el boton izquierdo del raton.
		if ev.buttons() == Qt.LeftButton:
			# Calcular nueva posicion en base al desplazamiento del cursor.
			newPos = ev.pos() - ev.lastPos()
			# Calculamos X e Y teniendo en cuenta el factor de escalado.
			x = newPos.x() * self.scale()
			y = newPos.y() * self.scale()
			# Mover en base a la posicion calculada.
			self.moveBy(x,y)


	'''
	Este evento controla el giro de la rueda del raton, y lo usaremos
	para manejar la escala de la imagen. Modificando asi virtualmente
	su anchura y altura.
	'''
	def wheelEvent(self, ev):
		ELogic.saveState(self.getWindow())
		newScale = self.getNewScale(ev.delta())
		self.setScale(newScale)



	'''
	Muestra el menu en la posicion del cursor.
	'''
	def contextMenuEvent(self, ev):
		self.contextMenu.exec(ev.screenPos())


# ----------------------------------------------------------------- #
#			   LOGICA :: FUNCIONES REQUERIDAS POR EVENTOS 			#
# ----------------------------------------------------------------- #

	'''
	Manejos de Visibilidad y Actividad.
	'''

	# Toggle de Visibilidad.
	def toggleVisible(self):
		ELogic.saveState(self.getWindow())
		toggle = not self.getVisible()
		self.setVisible(toggle)
		ELogic.updateTrees(self.getWindow())


	# Toggle de Actividad.
	def toggleActive(self):
		ELogic.saveState(self.getWindow())
		toggle = not self.getActive()
		self.setActiveState(toggle)
		# Si se desactiva, atenuamos la imagen.
		if self.getActive() is True:
			self.setOpacity(1.0)
		else:
			self.setOpacity(0.3)
		ELogic.updateTrees(self.getWindow())



	'''
	Manejos de la Z.
	'''

	# Incrementa el valor de la Z.
	def incZ(self):
		ELogic.saveState(self.getWindow())
		newZ = self.getPosZ() + 1
		self.setZValue(newZ)
		ELogic.updateTrees(self.getWindow())


	# Decrementa el valor de la Z, nunca menor que 0.
	def decZ(self):
		ELogic.saveState(self.getWindow())
		newZ = self.getPosZ() - 1
		if newZ >= 0:
			self.setZValue(newZ)
		ELogic.updateTrees(self.getWindow())



# ----------------------------------------------------------------- #
#		  GUI :: DIALOGO CON INFORMACION DETALLADA DEL OBJETO 		#
# ----------------------------------------------------------------- #

	def detailsDialog(self):
		QMessageBox.information(self.getWindow(),'¡DETALLES!', self.__str__())
