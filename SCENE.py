#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PresetValues import pv

class SCENE(QGraphicsScene):

    def __init__(self,rect,parent):
        super().__init__(rect,parent)
        self.isMovable = False
        # self.parent().setMouseTracking(True)
        self.parent().setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.parent().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__selRubber = QRubberBand(QRubberBand.Rectangle, self.parent())
        self.__selIni = QPointF(0,0)
        # self.__moveRubber = QRubberBand(QRubberBand.Rectangle, None)
        self.__moveIni = QPointF(0,0)

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


    ## @brief      Controla cuando se hace clic.
    ## @param      self  Escena.
    ## @param      ev    Objeto con los datos del evento.
    ## @return     None
    def mousePressEvent(self, ev):
        if ev.buttons() == Qt.LeftButton:

            ## CTRL para mover la escena.
            if ev.modifiers() == Qt.ControlModifier:
                self.__moveIni = ev.scenePos()

            ## SHIFT para seleccionar componentes.
            elif ev.modifiers() == Qt.ShiftModifier:
                self.__selIni = ev.scenePos()
                posO = self.__selIni.toPoint()
                self.__selRubber.setGeometry(QRect(posO,QSize()))
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
        if ev.buttons() == Qt.LeftButton:

            ## CTRL para mover la escena.
            if ev.modifiers() == Qt.ControlModifier:
                posO =self.__moveIni
                posD = ev.scenePos()
                self.getWindow().emit_SceneMove(posO,posD)

            ## SHIFT para seleccionar componentes.
            elif ev.modifiers() == Qt.ShiftModifier:
                posO = self.__selIni.toPoint()
                posD = ev.scenePos().toPoint()
                self.__selRubber.setGeometry(QRect(posO,posD).normalized())

            else:
                ev.ignore()
        else:
            ev.ignore()

        super(SCENE,self).mouseMoveEvent(ev)


    ## @brief      Controla cuand se libera el clic.
    ## @param      self  Escena.
    ## @param      ev    Objeto con los datos del evento.
    ## @return     None
    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.LeftButton:

            # Ocultar el area de seleccion.
            self.__selRubber.hide()

            ## SHIFT para seleccionar componentes.
            if ev.modifiers() == Qt.ShiftModifier:
                rect = self.__selRubber.geometry()
                self.getWindow().emit_SelectArea(rect)

            else:
                ev.ignore()
        else:
            ev.ignore()

        super(SCENE,self).mouseReleaseEvent(ev)
