#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json


# .----------------------------------------.
# | Diccionario de valores preestablecidos |
# -------------------------------------------------------------------------- #

pv = {

	'startMsg' 			: 'SESSION STARTED !',
	'endMsg' 			: 'SESSION ENDED !\n\n\n',

	'defaultPath' 		: '~',
	'bgColor'			: '#999',
	'sceneColor'		: '#DDD',

	'moveTimer'			: 2.0, #secs
	'resizeTimer'		: 5.0, #secs

	'zJump'				: 1.0,
	'maxOpacity'		: 1.0,
	'noVisibleOpacity'	: 0.0,
	'noActiveOpacity'	: 0.3,

	'imgModScale'		: 1.025,
	'imgMinScale'		: 0.025,
	'imgMaxScale'		: 5.025,

	'viewModScale'		: 1.1,
	'viewMinScale'		: 0.05,
	'viewMaxScale'		: 15.0,
	'viewRectMargin'	: 0.70,

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
