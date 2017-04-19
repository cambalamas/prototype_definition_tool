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
    sizeType = 'fixed'
    posType = 'Relative'

    sc = ET.Element(
        'Simple_Component',
            {
                'Name'    : simple.name,
                'Active'  : str(simple.active),
                'Visible' : str(simple.visible),
            }
        )

    va = ET.SubElement( sc, 'Visual_Appearance' )
    enum = ET.SubElement( va, 'Enumeration' )

    file = ET.SubElement(enum, 'File')
    file.text = simple.path

    size = ET.SubElement(enum, 'Size', {'Type':sizeType})
    sizeX = ET.SubElement(size, 'ValueX')
    sizeX.text = str(simple.sizeX)
    sizeY = ET.SubElement(size, 'ValueY')
    sizeY.text = str(simple.sizeY)

    position = ET.SubElement(enum, 'Position')
    posType = ET.SubElement(position, posType)
    cords = ET.SubElement(posType, 'Coordinate')
    cordX = ET.SubElement(cords, 'Px')
    cordX.text = str(simple.posX)
    cordY = ET.SubElement(cords, 'Py')
    cordY.text = str(simple.posY)

    return sc
