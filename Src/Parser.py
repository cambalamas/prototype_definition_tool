#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from collections import deque

from PyQt5.QtCore import *
from xml.dom import minidom
from xml.etree import cElementTree
from lxml import etree, objectify
from lxml.etree import Element, SubElement

from State import State
from SimpleComponent import SimpleComponent



# Convierte XML plano a XML indentado.
def prettify(node):
    raw = cElementTree.tostring(node, 'utf-8')
    parsed = minidom.parseString(raw)
    return parsed.toprettyxml(indent="    ")


## @brief      Genera fichero XML con la definicion de estados y componentes.
## @param      simple  Parser
## @return     None
def save(statesList, fileName):
    tfBool = lambda x : 't' if x is True else 'f'

    # Genera cadena XML.
    root = Element('DGAIUINT')
    composition = SubElement(root, 'Composicion')
    states = SubElement(root, 'Estados')
    transitions = SubElement(root, 'Transiciones')

    for s in statesList:
        state = SubElement(states, 'Estado')
        num = SubElement(state, 'Numero')
        num.text = str(statesList.index(s) + 1)
        desc = SubElement(state, 'Descripcion')

        for sc in s.scene:
            enum = SubElement( desc, 'Enumeracion',
                               { 'Activo'  : tfBool(sc.active),
                                 'Visible' : tfBool(sc.visible) } )
            name = SubElement(enum, 'Nombre')
            name.text = sc.name
            file = SubElement(enum, 'Fichero')
            file.text = sc.path
            position = SubElement(enum, 'Posicion')
            posType = SubElement(position, 'Relativa')
            cords = SubElement(posType, 'Coordenada')
            cordX = SubElement(cords, 'Px')
            cordX.text = str(sc.getPosX())
            cordY = SubElement(cords, 'Py')
            cordY.text = str(sc.getPosY())
            cordZ = SubElement(cords, 'Pz')
            cordZ.text = str(sc.getPosZ())
            size = SubElement(enum, 'Tamano', {'Tipo':'fijo'})
            sizeX = SubElement(size, 'Valorx')
            sizeX.text = str(sc.getSizeX())
            sizeY = SubElement(size, 'Valory')
            sizeY.text = str(sc.getSizeY())

    # Genera fichero XML.
    QDir().mkpath(os.path.split(fileName)[0]) # Verifica directorio.
    saveFile = QFile(fileName)# Crear fichero de guardado.
    saveFile.open(QIODevice.WriteOnly) # Sobreescritura.
    ts = QTextStream(saveFile) # Canal para enviar texto al log.
    ts << prettify(root) # Escribe el XML en el archivo.
    saveFile.close()



## @brief      Genera la definicion de estados y componentes desde fichero XML.
## @param      simple  Parser
## @return     None
def load(filePath):

    # VERIFICAR XML CONTRA EL DTD

    toRet = deque()
    rawFile = objectify.parse(filePath)
    oneLine = etree.tostring(rawFile)
    rootNode = objectify.fromstring(oneLine)
    tfBool = lambda x : True if x is 't' else False

    # Estados
    for stateNode in rootNode.Estados.Estado:
        state = State()
        if str(stateNode.Numero).isdigit():
            stateNum = stateNode.Numero
        else:
            return False, toRet
        stateScene = deque()

        # Enumeraciones
        if hasattr(stateNode.Descripcion, 'Enumeracion'):
            for compNode in stateNode.Descripcion.Enumeracion:
                if os.path.isfile(str(compNode.Fichero)):
                    comp = SimpleComponent(str(compNode.Fichero))
                else:
                    return False, toRet

                comp.name = str(compNode.Nombre)
                comp.visible = tfBool(compNode.get('Visible'))
                comp.active = tfBool(compNode.get('Activo'))

                posX = compNode.Posicion.Relativa.Coordenada.Px
                posY = compNode.Posicion.Relativa.Coordenada.Py
                posZ = compNode.Posicion.Relativa.Coordenada.Pz
                width  = compNode.Tamano.Valorx
                height = compNode.Tamano.Valory

                for data in [posX, posY, posZ, width, height]:
                    data = str(data)
                    if re.match("\d+\.\d*", data) or data.isdigit():
                        data = float(data)
                    else:
                        data = 0.0

                comp.setPos(posX, posY)
                comp.setZValue(posZ)
                comp.setScale( width * comp.scale()
                               / comp.boundingRect().width() ) #revisar

                stateScene.append(comp)

        state.scene = stateScene
        toRet.append(state)

    return True, toRet
