#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import deque

## @brief      Clase que define un componente complejo.
class Complex(QGraphicsPixmapItem):

# .-------------.
# | Constructor |
# --------------------------------------------------------------------------- #

    ## @brief      Constructor de componentes complejos.
    ## @param      self  Componente Complejo.
    def __init__(self,*comps):
		super().__init__()

		# Configura ciertas propiedades.
		self.setFlags(self.ItemIsSelectable) # Implemnt tipica de seleccion.
		self.setCursor(QCursor(Qt.PointingHandCursor)) # Cursor = mano.
		self.setTransformationMode(Qt.SmoothTransformation) # AntiAliasing.

    	# Atributos no heredados.
        self.__name    = str()
        self.__compos  = [] # Nombres de SC
        self.__states  = [] # Objs States.
        self.__events  = [] # Objs TriggerDE.
        self.__actions = [] # Objs TriggerDA.


# .------------------------------------.
# | Sobreescritura de metodos internos |
# --------------------------------------------------------------------------- #

	## @brief      Genera un diccionario con los datos del componente.
	## @param      self  Componente Complejo
	## @return     <dict>
	def readObj(self):
		data = {
			# ...
		}
		return data

	## @brief      Sobrecarga del metodo __str__.
	## @param      self  Componente complejo.
	## @return     Cadena que representa al objeto componente complejor.
	def __str__( self ):
		toString = json.dumps(self.readObj(),indent=0)
		return toString[1:-1]


	## @brief      Sobrecarga del metodo __copy__.
	## @param      self  Componente Complejo.
	## @return     SIMPLE.SimpleComponent
	def __copy__(self):
		new = type(self)(self.__path)
		new.__dict__.update(self.__dict__)
		new.setPos(self.getPosX(),self.getPosY())
		new.setScale(self.getSizeX()/self.boundingRect().width())
		new.setZValue(self.getPosZ())
		new.visibleEffect()
		return new


# .------------.
# | SUB CLASES |
# --------------------------------------------------------------------------- #

# Cc/Estado
class State:
    def __init__( self, id, active, visible ):
        self.id      = int(id)
        self.active  = bool(active)
        self.visible = bool(visible)
        self.status  = [] # Objs StateStatus.
        self.dialogs = [] # Objs StateDialogEvent.

# Cc/Estado/Status
class StateStatus:
    def __init__( self, scName, active, visible ):
        self.scName = str(scName)
        self.active  = bool(active)
        self.visible = bool(visible)

# Cc/Estado/Dialog (Self-Events)
class StateDialogEvent:
    def __init__( self, id, event, comp, ini, end ):
        self.id       = int(id)
        self.event    = str(event) # User action that trigger the status swap.
        self.comp     = str(comp)
        self.ini      = int(ini) # swap from this state...
        self.end      = int(end) # to this other state.
        self.preconds = [] # Objs StateDialogEventPrecond.

# Cc/Estado/Dialog/Precond (Conditions for Self-Events)
class StateDialogEventPrecond:
    def __init__( self, comp, state):
        self.comp  = str(comp)
        self.state = int(state)

# Cc/Estado/DelegatedAction
class TriggerDA:
    def __init__( self, id, selfState, compDest, destEvent ):
        self.id    = int(id)
        self.state = int(selfState)
        self.comp  = str(compDest)
        self.event = int(destEvent)

# Cc/Estado/DelegatedEvent
class TriggerDE:
    def __init__( self, id, comp, ini, end ):
        self.id   = int(id)
        self.comp = str(comp)
        self.ini  = int(ini)
        self.end  = int(end)
