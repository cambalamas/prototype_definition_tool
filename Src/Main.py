#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from datetime import datetime

import i18n

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Model import Model
from Parser import Parser
from Presenter import Presenter
from PresetValues import PV
from View import View


# @brief      Funcion llamada por el event handler.
# @param      type     Info, Debug, Warning, Critial, Fatal.
# @param      context  Informacion de donde se recibio el mensaje.
# @param      msg      Informacion emitida. (Nuestra o del sistema)
# @return     None
def logger(msg):
    # Fecha y hora actual.
    dt = datetime.now()
    # Crear la carpeta de Logs si no existe.
    exeFolder = os.path.split(os.path.realpath(__file__))[0]
    folder = os.path.join(exeFolder, 'Logs')
    QDir().mkpath(folder)
    # Crear fichero de log por dia
    logFile = QFile(folder+'/'+str(dt.date())+'.log')
    # Agregar entradas al final del archivo.
    logFile.open(QIODevice.WriteOnly | QIODevice.Append)
    # Canal para enviar texto al log.
    ts = QTextStream(logFile)
    # Formato desesado para el mensaje.
    fmt = '({})\t{}'.format(dt.time(), msg)
    # Enviar el mensaje formateado por el canal al fichero de log.
    ts << fmt + '\n'


# @brief      Captura los mensajes de error e información.
# @param      msgType  Gravedad del mensaje.
# @param      context  Contexto
# @param      msg      Mensaje
# @return     None
def handler(msgType, context, msg):
    if (msgType == 0
            or msgType == 1
            or msgType == 2
            or msgType == 3
            or msgType == 4):
        logger(msg)

    if msgType == 2 or msgType == 3:
        print('Something went wrong :(\nSee the logfile for more info.')


# .------------------.
# | Punto de entrada |
# -------------------------------------------------------------------------- #

if __name__ == '__main__':

    # Instancia de una aplicacion basada en Qt.
    app = QApplication(sys.argv)

    # Redefinimos el capturador de eventos con salida a fichero .log.
    qInstallMessageHandler(handler)
    qDebug(PV['startMsg'])

    # Resolucion del dispositivo del usuario.
    scrRect = app.primaryScreen().availableGeometry()

    # Inicializaciones.
    M = Model()
    V = View(scrRect)
    X = Parser(V, M)
    P = Presenter(V, M, X)

    # Conecta las señales del modelo.
    M.signal_ModelUpdated.connect(P.listener_ModelUpdated)

    # Conecta señales del menu archivo.
    V.signal_SaveProject.connect(P.listener_SaveProject)
    V.signal_LoadProject.connect(P.listener_LoadProject)
    V.signal_NewState.connect(P.listener_NewState)
    V.signal_NewSimple.connect(P.listener_NewSimple)

    # Conecta señales del menu editar.
    V.signal_SelectAll.connect(P.listener_SelectAll)
    V.signal_UnSelectAll.connect(P.listener_UnSelectAll)
    V.signal_Undo.connect(P.listener_Undo)
    V.signal_Redo.connect(P.listener_Redo)
    V.signal_Center.connect(P.listener_Center)
    V.signal_Clone.connect(P.listener_Clone)

    # Conecta señales del menu vista.
    V.signal_HideMenu.connect(P.listener_HideMenu)
    V.signal_Minimalist.connect(P.listener_Minimalist)
    V.signal_ZoomIn.connect(P.listener_ZoomIn)
    V.signal_Zoom100.connect(P.listener_Zoom100)
    V.signal_ZoomOut.connect(P.listener_ZoomOut)
    V.signal_FullScreen.connect(P.listener_FullScreen)
    V.signal_SceneCenter.connect(P.listener_SceneCenter)

    # Conecta señales del menu componente simple.
    V.signal_SimpleMenu.connect(P.listener_SimpleMenu)
    V.signal_Details.connect(P.listener_Details)
    V.signal_Name.connect(P.listener_Name)
    V.signal_ZInc.connect(P.listener_ZInc)
    V.signal_ZDec.connect(P.listener_ZDec)
    V.signal_Active.connect(P.listener_Active)
    V.signal_Visible.connect(P.listener_Visible)
    V.signal_Delete.connect(P.listener_Delete)

    # Conecta señales de 'callback' del componente simple.
    V.signal_Resize.connect(P.listener_Resize)
    V.signal_Move.connect(P.listener_Move)

    # Conecta señales de la escena.
    V.signal_SceneMove.connect(P.listener_SceneMove)
    V.signal_SelectArea.connect(P.listener_SelectArea)

    # Conecta señales del arbol de componentes.
    V.signal_ItemChanged.connect(P.listener_ItemChanged)

    # Conecta señales de menu del arbol de estados.
    V.signal_StateMoveLeft.connect(P.listener_StateMoveLeft)
    V.signal_StateMoveRight.connect(P.listener_StateMoveRight)
    V.signal_StateClone.connect(P.listener_StateClone)
    V.signal_StateDelete.connect(P.listener_StateDelete)

    # Conecta señales de 'callback' del arbol de estados.
    V.signal_StateThumbPressed.connect(P.listener_StateThumbPressed)
    V.signal_StateContextMenu.connect(P.listener_StateContextMenu)

    # Muestra la ventana maximizada.
    if V.ok:
        V.showMaximized()
        P.listener_NewState()
    else:
        sys.exit()

    # Espera la señal 'QT' de Cierre.
    sys.exit(app.exec_())
