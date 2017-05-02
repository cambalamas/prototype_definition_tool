#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# http://stackoverflow.com/a/7631951/7901063
# - '.get(key)' es un método de búsqueda y llamada.
# - '[key]' se implementa en bytecode. (Más eficiente)

import json

pv = {

	'bgColor': '#999',
	'sceneColor':'#DDD',

	'startMsg' : 'SESSION STARTED !',
	'endMsg' : 'SESSION ENDED !\n\n\n',

	'defaultPath' 		: '~',

	'viewRectMargin'	: 0.20,
	'viewModScale'		: 1.1,
	'viewMinScale'		: 0.05,
	'viewMaxScale'		: 15.0,

	'imgModScale'		: 1.025,
	'imgMinScale'		: 0.025,
	'imgMaxScale'		: 5.025,

	'maxOpacity'		: 1.0,
	'noActiveOpacity'	: 0.3,
	'noVisibleOpacity'	: 0.0,

	'zJump'				: 1.0,
}
