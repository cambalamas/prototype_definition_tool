#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PresetValues import pv


## @brief      Clase que define un area de trabajo.
class SCENE(QGraphicsScene):


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
        self.overComp = False
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

    ## @brief      Devuelvela posicion zero real de la escena.
    ## @param      self  Escena.
    ## @return     QPoint
    def _getZero(self):
        return self.parent().mapToScene(0,0).toPoint()


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
            self.getWindow().setCursor(QCursor(Qt.SizeAllCursor))
            self.__moveIni = ev.scenePos()
        ## Shift+LB para seleccionar componentes.
        elif ev.button() == Qt.LeftButton:
            if ev.modifiers() == Qt.ShiftModifier:
                self.getWindow().setCursor(QCursor(Qt.CrossCursor))
                self.__selIni = ev.scenePos()
                self.__selPosO = self.__selIni.toPoint() - self._getZero()
                self.__selRubber.setGeometry(QRect(self.__selPosO, QSize()))
                if self.overComp is False:
                    self.__selRubber.show()
            else:
                ev.ignore()
        else:
            ev.ignore()
        super(SCENE,self).mousePressEvent(ev)

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
        ## Shift+LB para seleccionar componentes.
        elif ev.buttons() == Qt.LeftButton:
            if ev.modifiers() == Qt.ShiftModifier:
                self.__selPosO = self.__selIni.toPoint() - self._getZero()
                self.__selPosD = ev.scenePos().toPoint() - self._getZero()
                self.__selRubber.setGeometry(
                            QRect( self.__selPosO,
                                   self.__selPosD ).normalized() )
            else:
                ev.ignore()
        else:
            ev.ignore()
        super(SCENE,self).mouseMoveEvent(ev)

    ## @brief      Controla cuando se libera el clic.
    ## @param      self  Escena.
    ## @param      ev    Objeto con los datos del evento.
    ## @return     None
    def mouseReleaseEvent(self, ev):
        ## SHIFT+LB para seleccionar componentes.
        if ev.button() == Qt.LeftButton:
            # Ocultar el area de seleccion.
            self.__selRubber.hide()
            # Establecer el cursor normal.
            self.getWindow().setCursor(QCursor(Qt.ArrowCursor))
            if ev.modifiers() == Qt.ShiftModifier:
                tmpPosO = self.__selPosO + self._getZero()
                tmpPosD = self.__selPosD + self._getZero()
                rect = QRect(tmpPosO,tmpPosD)
                self.getWindow().emit_SelectArea(rect)
            else:
                ev.ignore()
        elif ev.button() == Qt.MidButton:
            # Establecer el cursor normal.
            self.getWindow().setCursor(QCursor(Qt.ArrowCursor))
        else:
            ev.ignore()
        super(SCENE,self).mouseReleaseEvent(ev)
