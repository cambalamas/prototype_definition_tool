#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PresetValues import PV


# @brief      Clase que define el contenedor del area de trabajo.
class Viewport(QGraphicsView):

    # .-------------.
    # | Constructor |
    # ---------------------------------------------------------------------- #

    # @brief      Constructuor del viewport.
    # @param      self    Viewport
    def __init__(self):
        super().__init__()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # .---------.
    # | Eventos |
    # ---------------------------------------------------------------------- #

    # @brief      Controla el giro de la rueda del ratón.
    # @param      self  Viewport.
    # @param      ev    Objeto con los datos del evento.
    # @return     None
    def wheelEvent(self, ev):

        if ev.modifiers() == Qt.ControlModifier:

            # Rueda hacia adelante.
            if ev.angleDelta().y() > 0:
                self.parent().emit_ZoomIn()

            # Rueda hacia atras.
            else:
                self.parent().emit_ZoomOut()

        else:
            super(Viewport, self).wheelEvent(ev)
