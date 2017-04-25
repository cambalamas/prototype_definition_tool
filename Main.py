#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from VIEW import VIEW
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':

	# Instancia la app QT.$
	app = QApplication(sys.argv)

	# Compone la ventana y las señales ante eventos de usuario.
	view = VIEW()

	# Compone la estructura y logica de almacenameiento.

	# Muestra la ventana.
	win.showMaximized()

	# Espera la señal 'QT' de Cierre.
	sys.exit(app.exec_())
