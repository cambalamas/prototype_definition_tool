#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json


# .----------------------------------------.
# | Diccionario de valores preestablecidos |
# -------------------------------------------------------------------------- #

pv = {

	'startMsg' 			: '\n\n\nSESSION STARTED !',
	'endMsg' 			: 'SESSION ENDED !',

	'defaultPath' 		: '~',
	'bgColor'			: '#EEE',
	'sceneColor'		: '#DDD',

	'moveTimer'			: 2.0, 		#secs
	'resizeTimer'		: 5.0, 		#secs

	'zJump'				: 1.0,
	'maxOpacity'		: 1.0,
	'noVisibleOpacity'	: 0.000,	# Invisible pero interactuable (0.001)
	'noActiveOpacity'	: 0.25,

	'imgModScale'		: 1.025,
	'imgMinScale'		: 0.025,
	'imgMaxScale'		: 200.00,

	'viewModScale'		: 1.1,
	'viewMinScale'		: 0.05, 	# Como photoshop = muy pequeño (0.0013)
	'viewMaxScale'		: 34.5,		# Como photoshop
	'viewRectMargin'	: 1.00,

	'historyLimit'		: 100,

	'compKeyDespl'      : 1.0,
	'compShiftKeyDespl' : 10.0,
}


# .------------------.
# | Metodo de acceso |
# -------------------------------------------------------------------------- #
#  http://stackoverflow.com/a/7631951/7901063
#	  - '.get(key)' es un método de búsqueda y llamada.
#	  - '[key]' se implementa en bytecode. (Más eficiente)
