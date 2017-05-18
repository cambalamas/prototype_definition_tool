#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from xml.dom import minidom
from lxml import etree as ET
from xml.etree import cElementTree

# Convierte XML plano a XML indentado.
def prettify(node):
    raw = cElementTree.tostring(node, 'utf-8')
    parsed = minidom.parseString(raw)
    return parsed.toprettyxml(indent="    ")

# Espera un nodo xml para cargarlo en un componente simple.
# def xml2simple(simple, node):
#     subNode         = node.Visual_Appearance.Enumeration
#     simple.name     = node.get('Name')
#     simple.visible  = node.get('Visible')
#     simple.active   = node.get('Active')
#     simple.img      = subNode.File
#     simple.sizeType = subNode.Size.get('Type')
#     simple.sizeX    = int(subNode.Size.ValueX)
#     simple.sizeY    = int(subNode.Size.ValueY)
#     simple.posType  = subNode.Position.Relative.tag
#     simple.posX     = int(subNode.Position.Relative.Coordinate.Px)
#     simple.posY     = int(subNode.Position.Relative.Coordinate.Py)

# Espera un componente simple para generar su arbol xml.
def simple2xml(simple):
    _sizeType = 'fixed'
    _posType = 'Relative'

    sc = ET.Element(
        'Simple_Component',
            {
                'Name'    : simple.getName(),
                'Active'  : str(simple.getActive()),
                'Visible' : str(simple.getVisible()),
            }
        )

    va = ET.SubElement( sc, 'Visual_Appearance' )
    enum = ET.SubElement( va, 'Enumeration' )

    file = ET.SubElement(enum, 'File')
    file.text = simple.getPath()

    size = ET.SubElement(enum, 'Size', {'Type':_sizeType})
    sizeX = ET.SubElement(size, 'ValueX')
    sizeX.text = str(simple.getSizeX())
    sizeY = ET.SubElement(size, 'ValueY')
    sizeY.text = str(simple.getSizeY())

    position = ET.SubElement(enum, 'Position')
    posType = ET.SubElement(position, _posType)
    cords = ET.SubElement(_posType, 'Coordinate')
    cordX = ET.SubElement(cords, 'Px')
    cordX.text = str(simple.getPosX())
    cordY = ET.SubElement(cords, 'Py')
    cordY.text = str(simple.getPosY())
    cordY = ET.SubElement(cords, 'Pz')
    cordY.text = str(simple.getPosZ())

    return sc
