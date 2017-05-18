#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PresetValues import pv


## @brief      Clase que define un area de trabajo.
class Scene(QGraphicsScene):


# .-------------.
# | Constructor |
# -------------------------------------------------------------------------- #

    ## @brief      Constructuor de la escena.
    ## @param      self    Escena
    ## @param      rect    Area activa
    ## @param      parent  Padre (QGraphicsView)
    def __init__(self,rect,parent):
        super().__init__(rect,parent)
        self.isMovable = False
        # self.getWindow().setMouseTracking(True)
        self.parent().setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.parent().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__selIni = QPointF(0,0)
        self.__selPosO = QPointF(0,0)
        self.__selPosD = QPointF(0,0)
        self.__moveIni = QPointF(0,0)
        self.__selRubber = QRubberBand(QRubberBand.Rectangle, self.parent())


# .------------------------------------.
# | Lectura de los atributos heredados |
# -------------------------------------------------------------------------- #

    ## @brief      Obtiene la venta que contiene la escena.
    ## @param      self  Escena.
    ## @return     PyQt5.QtWidget.QMainWindow
    def getWindow(self):
        return self.parent().parent()


# .-----------------------.
# | Sobrecarga de eventos |
# -------------------------------------------------------------------------- #

    ## @brief      Controla el desplazamiento para mover componentes.
    ## @param      self  Escena.
    ## @param      ev    Objeto con los datos del evento.
    ## @return     None
    def keyPressEvent(self, ev):
        if ev.modifiers() == Qt.ShiftModifier:
            moveRng = pv['compShiftKeyDespl']
        else:
            moveRng = pv['compKeyDespl']
        zero = QPointF(0,0)
        if ev.key() == Qt.Key_Left:
            self.getWindow().emit_Move(zero,QPointF(-moveRng,0.0))
        if ev.key() == Qt.Key_Right:
            self.getWindow().emit_Move(zero,QPointF(moveRng,0.0))
        if ev.key() == Qt.Key_Up:
            self.getWindow().emit_Move(zero,QPointF(0.0,-moveRng))
        if ev.key() == Qt.Key_Down:
            self.getWindow().emit_Move(zero,QPointF(0.0,moveRng))

    ## @brief      Controla cuando se suelta una tecla.
    ## @param      self  Escena.
    ## @param      ev    Objeto con los datos del evento.
    ## @return     None
    def keyReleaseEvent(self, ev):
        if self.parent().cursor().shape() != Qt.ArrowCursor:
            self.getWindow().setCursor(QCursor(Qt.ArrowCursor))
        else:
            ev.ignore()

    ## @brief      Controla cuando se hace clic.
    ## @param      self  Escena.
    ## @param      ev    Objeto con los datos del evento.
    ## @return     None
    def mousePressEvent(self, ev):
        ## MB para mover la escena.
        if ev.button() == Qt.MidButton:
            self.parent().setDragMode(0)
            self.getWindow().setCursor(QCursor(Qt.SizeAllCursor))
            self.__moveIni = ev.scenePos()
        ## Shift+LB para seleccionar componentes.
        elif ev.button() == Qt.LeftButton:
            self.parent().setDragMode(2)
            self.getWindow().setCursor(QCursor(Qt.CrossCursor))
        else:
            ev.ignore()
        super(Scene,self).mousePressEvent(ev)

    ## @brief      Controla el desplazamiento del raton.
    ## @param      self  Escena.
    ## @param      ev    Objeto con los datos del evento.
    ## @return     None
    def mouseMoveEvent(self, ev):
        ## MB para mover la escena.
        if ev.buttons() == Qt.MidButton:
            posO = self.__moveIni
            posD = ev.scenePos()
            self.getWindow().emit_SceneMove(posO,posD)
        else:
            ev.ignore()
        super(Scene,self).mouseMoveEvent(ev)

    ## @brief      Controla cuando se libera el clic.
    ## @param      self  Escena.
    ## @param      ev    Objeto con los datos del evento.
    ## @return     None
    def mouseReleaseEvent(self, ev):
        ## MB para mover la escena.
        if ev.button() == Qt.MidButton:
            # Establecer el cursor normal.
            self.getWindow().setCursor(QCursor(Qt.ArrowCursor))
        ## SHIFT+LB para seleccionar componentes.
        elif ev.button() == Qt.LeftButton:
            # Establecer el cursor normal.
            self.parent().setDragMode(0)
            self.getWindow().setCursor(QCursor(Qt.ArrowCursor))
        else:
            ev.ignore()
        super(Scene,self).mouseReleaseEvent(ev)
