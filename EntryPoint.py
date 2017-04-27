#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime

import PyQt5
from PyQt5.QtCore import *

from VIEW import VIEW
from MODEL import MODEL
from PRESENTER import PRESENTER


""" Esto redefinira el EventHandler por defecto. """

def logger(type, context, msg):
	# En caso de error FATAL.
	if type == 3:
		abort()
	# Compone el mensaje.
	txt = '\n {}\n-----------------\n{}'.format(datetime.now().time(),msg)
	# Ubicacion de guardado.
	path = QDir().mkpath("Logs")
	logFile = QFile("Logs/{}.log".format(datetime.now().date()))
	# Siempre añadimos entradas despues de la ultima linea.
	logFile.open(QIODevice.WriteOnly | QIODevice.Append)
	# Graba en el archivo lo que reciba el Stream.
	ts = QTextStream(logFile)
	# Operador de adicion, propio de 'QTextStream'
	ts << txt+'\n'


""" Punto de entrada a la app. """

if __name__ == '__main__':

	# Instancia la app QT.$
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	# qInstallMessageHandler(logger)

	# Header del archivo de log.
	qDebug('SESSION STARTED !')

	# Medida de la pantalla del dispositivo.
	w = app.primaryScreen().geometry().width()
	h = app.primaryScreen().geometry().height()

	# Compone la ventana y las señales ante eventos de usuario.
	view = VIEW(w,h)
	# Compone la estructura y logica de almacenameiento.
	model = MODEL()
	# Compone la logica y tratamiento de datos.
	presenter = PRESENTER(view,model)


	##
	# CONECTA SEÑALES DE LA VISTA.
	##

	view.signal_SaveProject.connect(
		presenter.listener_SaveProject
	)

	view.signal_NewSimple.connect(
		presenter.listener_NewSimple
	)

	view.signal_NewComplex.connect(
		presenter.listener_NewComplex
	)

	view.signal_HideMenu.connect(
		presenter.listener_HideMenu
	)

	view.signal_ZoomIn.connect(
		presenter.listener_ZoomIn
	)

	view.signal_ZoomOut.connect(
		presenter.listener_ZoomOut
	)

	view.signal_Zoom100.connect(
		presenter.listener_Zoom100
	)

	view.signal_FullScreen.connect(
		presenter.listener_FullScreen
	)

	view.signal_TrEs.connect(
		presenter.listener_TrEs
	)

	view.signal_TrEn.connect(
		presenter.listener_TrEn
	)

	view.signal_TrFr.connect(
		presenter.listener_TrFr
	)

	view.signal_TrDe.connect(
		presenter.listener_TrDe
	)

	view.signal_SimpleZInc.connect(
		presenter.listener_SimpleZInc
	)

	view.signal_SimpleZDec.connect(
		presenter.listener_SimpleZDec
	)

	view.signal_SimpleActive.connect(
		presenter.listener_SimpleActive
	)

	view.signal_SimpleVisible.connect(
		presenter.listener_SimpleVisible
	)

	view.signal_SimpleDelete.connect(
		presenter.listener_SimpleDelete
	)

	view.signal_SimpleDetail.connect(
		presenter.listener_SimpleDetail
	)

	view.signal_simpleTreeItemChange.connect(
		presenter.listener_simpleTreeItemChange
	)

	view.signal_simpleTreeInvokeMenu.connect(
		presenter.listener_simpleTreeInvokeMenu
	)

	view.signal_complexTreeItemChange.connect(
		presenter.listener_complexTreeItemChange
	)

	view.signal_complexTreeInvokeMenu.connect(
		presenter.listener_complexTreeInvokeMenu
	)


	##
	# CONECTA SEÑALES DEL MODELO
	##



# --------------------------------------------------------------------------- #

	# Muestra la ventana.
	view.showMaximized()

	# Espera la señal 'QT' de Cierre.
	sys.exit(app.exec_())
