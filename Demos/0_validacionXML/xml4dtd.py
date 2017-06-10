#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import lxml
from lxml import etree, objectify

"""
Load a xml from a file and validate it against a DTD file.

@param      xmlFile  Existing xml file
@param      dtdFile  Existing dtd file

@return     xml node object, bool
"""
def xml4dtd(xmlFile, dtdFile):

    # Load DTD and check it syntax.
    try:
        dtd = etree.DTD(dtdFile)
    except lxml.etree.DTDParseError:
        print('WARNING: DTD had a bad syntax.')
        sys.exit()

    # Load XML and check it syntax
    try:
        rawFile = objectify.parse(xmlFile)
    except lxml.etree.XMLSyntaxError:
        print('WARNING: The file is empty or had a bad syntax.')
        sys.exit()

    # Objetify XML
    oneLine = etree.tostring(rawFile)
    rootNode = objectify.fromstring(oneLine)

    # Validacion del XML cargado.
    valid = dtd.validate(rootNode)
    print('XML validation = {}'.format(valid))

    # Shows the reasons why the DTD does not validate.
    if dtd.error_log.filter_from_errors():
        print('\nReasons:\n--------')
        print(dtd.error_log.filter_from_errors()[0])

    # Returns the node and her valid state.
    return rootNode, valid


# EntryPoint.
if __name__ == '__main__':
    args = sys.argv[1:]
    helpMsg = '\n[ Type python xml4dtd.py -h, for some help ! ]'

    if args[0] == '-h':
        print('python xml4dtd.py <file1>.xml <file2>.dtd')

    elif len(args) != 2:
        print('Incorrect number of parameters.'+helpMsg)

    else:
        if not args[0][-3:] == 'xml' and not args[1][-3:] == 'dtd':
            print('Bad extension of both arguments.'+helpMsg)
        elif not args[0][-3:] == 'xml' and args[1][-3:] == 'dtd':
            print('Bad extension of first argument.'+helpMsg)
        elif args[0][-3:] == 'xml' and not args[1][-3:] == 'dtd':
            print('Bad extension of second argument.'+helpMsg)
        elif not os.path.isfile(args[0]) and not os.path.isfile(args[1]):
            print('Both arguments, do not exists.'+helpMsg)
        elif not os.path.isfile(args[0]) and os.path.isfile(args[1]):
            print('First argument, do not exists.'+helpMsg)
        elif os.path.isfile(args[0]) and not os.path.isfile(args[1]):
            print('Second argument, do not exists.'+helpMsg)
        else:
            xml4dtd(args[0], args[1])
