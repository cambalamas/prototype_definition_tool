#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from collections import deque

from PyQt5.QtCore import *
from xml.dom import minidom
from xml.etree import cElementTree
import lxml
from lxml import etree, objectify
from lxml.etree import Element, SubElement

from State import State
from SimpleComponent import SimpleComponent


## @brief      Clase que define al experto en XML
class Parser(object):


# .-------------.
# | Constructor |
# -------------------------------------------------------------------------- #

    ## @brief      Constructor del parser.
    ## @param      self  Parser
    ## @param      view  Vista
    ## @param      model Modelo
    def __init__(self,view,model):
        self.__view = view
        self.__model = model


# .-------------------------------------------.
# | Acceso 'publico' a las variables privadas |
# -------------------------------------------------------------------------- #

    ## @brief      Propiedad de lectura de la variable vista.
    ## @param      self  Presentador.
    ## @return     View.View
    @property
    def view(self):
        return self.__view

    ## @brief      Propiedad de lectura de la variable modelo.
    ## @param      self  Presentador.
    ## @return     View.View
    @property
    def model(self):
        return self.__model


# .----------------------.
# | Funciones auxiliares |
# -------------------------------------------------------------------------- #

    ## @brief      Convierte XML plano a XML indentado.
    ## @param      self  Parser.
    ## @param      node  Nodo xml.
    ## @return     str
    def prettify(self,node):
        raw = cElementTree.tostring(node, 'utf-8')
        parsed = minidom.parseString(raw)
        return parsed.toprettyxml(indent="    ")


# .----------------------.
# | Volcado de los datos |
# -------------------------------------------------------------------------- #

    ## @brief      Genera XML con la definicion de estados y componentes.
    ## @param      self        Parser.
    ## @param      statesList  Lista de estados.
    ## @param      fileName    Nombre del archivo.
    ## @return     None
    def save(self,statesList, fileName):
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

                imgName = os.path.split(sc.path)[1]

                imgFolder = os.path.split(
                    fileName)[0] +'/'+os.path.split(fileName)[1][:-4]+'_imgs'

                QDir().mkpath(imgFolder)
                sc.pixmap().save(imgFolder+'/'+imgName,'png',100)

                file.text = os.path.basename(
                    imgFolder) +'/'+ os.path.split(sc.path)[1]


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
        xml = self.prettify(root)
        xml = xml.replace( '<?xml version="1.0" ?>',
                     '<?xml version="1.0" encoding="ISO-8859-1"?>' )
        ts << xml # Escribe el XML en el archivo.
        saveFile.close()


# .--------------------.
# | Carga de los datos |
# -------------------------------------------------------------------------- #

    ## @brief      Genera estados y componentes desde fichero XML.
    ## @param      self  Parser.
    ## @param      filePath  Archivo XML
    ## @return     None
    def load(self,filePath):

        fileFolder = os.path.split(filePath)[0]

        # Variables propias.
        toRet = 0
        tfBool = lambda x : True if x is 't' else False

        # Reseteo de vista y modelo.
        self.model.states = deque()
        treeModel = self.view.statesTree.model()
        treeModel.removeColumns(0,treeModel.columnCount())

        # Variables xml.
        try:
            rawFile = objectify.parse(filePath)
        except lxml.etree.XMLSyntaxError:
            self.view.emit_NewState()
            toRet = 1
            return toRet

        oneLine = etree.tostring(rawFile)
        rootNode = objectify.fromstring(oneLine)

        # Validacion del XML cargado.
        execFolder = os.path.dirname(os.path.realpath(__file__))
        dtd = etree.DTD(execFolder+'/xml.dtd')
        qDebug('XML validation against DTD: '+str(dtd.validate(rootNode)))
        if not dtd.validate(rootNode):
            self.view.emit_NewState()
            toRet = 1
            return toRet

        # Estados
        for stateNode in rootNode.Estados.Estado:
            if str(stateNode.Numero).isdigit():
                stateNum = int(stateNode.Numero)

                self.view.emit_NewState()
                state = self.model.curState()
                stateScene = deque()

                # Enumeraciones
                if hasattr(stateNode.Descripcion, 'Enumeracion'):
                    for compNode in stateNode.Descripcion.Enumeracion:

                        file = fileFolder+'/'+str(compNode.Fichero)

                        if os.path.isfile(file):
                            comp = SimpleComponent(file)
                        else:
                            toRet = 3
                            break

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
                        comp.setScale(width / comp.boundingRect().width())

                        stateScene.append(comp)

                state.scene = stateScene

            else:
                toRet = 2

        return toRet
