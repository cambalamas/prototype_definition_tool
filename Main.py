#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, i18n
from datetime import datetime
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from VIEW import VIEW
from MODEL import MODEL
from PRESENTER import PRESENTER
from PresetValues import pv

## @brief      Esto redefinira el EventHandler por defecto.
## @param      type     Info, Debug, Warning, Critial, Fatal.
## @param      context  Informacion de donde se recibio el mensaje.
## @param      msg      Informacion emitida. (Nuestra o del sistema)
## @return     None
def logger(type, context, msg):
	path    = QDir().mkpath("Logs")
	logFile = QFile("Logs/{}.log".format(datetime.now().date()))
	logFile.open(QIODevice.WriteOnly | QIODevice.Append)
	ts      = QTextStream(logFile) # Canal para enviar texto al log.
	fmtMsg  = '\n {}\n-----------------\n{}'.format(datetime.now().time(),msg)
	ts      << fmtMsg + '\n' # '<<' Operador propio para recibir cadenas.

#
# Punto de entrada a la aplicación.
#
if __name__ == '__main__':
	# Instancia de una aplicacion basada en Qt.
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	# Redefinimos el capturador de eventos con salida a fichero .log.
	# qInstallMessageHandler(logger)
	qDebug(pv['startMsg'])
	# Resolucion del dispositivo del usuario.
	scrRect = app.primaryScreen().availableGeometry()
	# Inicializaciones.
	M = MODEL()
	V = VIEW(scrRect)
	P = PRESENTER(V,M)
	# Conecta las señales del modelo.
	M.signal_modelUpdated.connect(P.listener_modelUpdated)
	# Conecta señales de la vista.
	V.signal_SaveProject.connect(P.listener_SaveProject)
	V.signal_NewSimple.connect(P.listener_NewSimple)
	V.signal_NewComplex.connect(P.listener_NewComplex)
	V.signal_Undo.connect(P.listener_Undo)
	V.signal_Redo.connect(P.listener_Redo)
	V.signal_HideMenu.connect(P.listener_HideMenu)
	V.signal_Minimalist.connect(P.listener_Minimalist)
	V.signal_ZoomIn.connect(P.listener_ZoomIn)
	V.signal_Zoom100.connect(P.listener_Zoom100)
	V.signal_ZoomOut.connect(P.listener_ZoomOut)
	V.signal_FullScreen.connect(P.listener_FullScreen)
	V.signal_Details.connect(P.listener_Details)
	V.signal_Center.connect(P.listener_Center)
	V.signal_Name.connect(P.listener_Name)
	V.signal_ZInc.connect(P.listener_ZInc)
	V.signal_ZDec.connect(P.listener_ZDec)
	V.signal_Active.connect(P.listener_Active)
	V.signal_Visible.connect(P.listener_Visible)
	V.signal_Delete.connect(P.listener_Delete)
	V.signal_Resize.connect(P.listener_Resize)
	V.signal_Move.connect(P.listener_Move)
	V.signal_SelectAll.connect(P.listener_SelectAll)
	V.signal_UnSelectAll.connect(P.listener_UnSelectAll)
	V.signal_SimpleMenu.connect(P.listener_SimpleMenu)
	V.signal_ComplexMenu.connect(P.listener_ComplexMenu)
	# Muestra la ventana maximizada.
	V.showMaximized()
	# Espera la señal 'QT' de Cierre.
	sys.exit(app.exec_())
