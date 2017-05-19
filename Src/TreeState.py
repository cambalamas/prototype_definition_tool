#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class TreeState(QTreeView):
    def __init__(self):
        super().__init__()
        # Propiedades.
        model = QStandardItemModel()
        header = QHeaderView(1,self)
        header.setDragEnabled(False)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setHeader(header)
        self.setModel(model)  # Asigna el modelo a la vista.
        self.setDragEnabled(False)
        self.setContextMenuPolicy(Qt.CustomContextMenu) # Menu contextual = RB.
        self.setRootIsDecorated(False) # Oculta las flechas de hijos.
        self.setItemsExpandable(False) # No permite expandir los hijos.
        self.setSelectionBehavior(QAbstractItemView.SelectItems) # Sel x item.
        self.setSelectionMode(QAbstractItemView.SingleSelection) # Sel x item.


    def getWindow(self):
        return self.parent()

    # def mousePressEvent(self):

