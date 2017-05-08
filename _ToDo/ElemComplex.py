from lxml import etree as ET

from sc import *
from complex.State import *
from complex.StateStatus import *
from complex.DelegateEvent import *
from complex.DelegateAction import *
from complex.StateDialogEvent import *
from complex.StateDialogEventPrecond import *

class Complex( object ):
    def __init__( self ):
        self.name    = str()
        self.compos  = [] # Nombres de SC
        self.states  = [] # Objs States.
        self.events  = [] # Objs TriggerDE.
        self.actions = [] # Objs TriggerDA.

    def __str__( self ):
        return "\nName: {}\n\n!Comps...{}\n\n!States...{}\
            \n\n!Events...{}\n\n!Actions...{}\n"\
            .format(
                self.name,
                self.strComps(),
                self.strStates(),
                self.strEvents(),
                self.strActions()
            )
    def strComps( self ):
        out = str()
        for e in self.compos:
            out += "\n\t"+e.__str__()
        return out
    def strStates( self ):
        out = str()
        for e in self.states:
            out += e.__str__()
        return out
    def strEvents( self ):
        out = str()
        for e in self.events:
            out += e.__str__()
        return out
    def strActions( self ):
        out = str()
        for e in self.actions:
            out += e.__str__()
        return out

    # Adiciones en bloque a las listas.
    def addComps( self, *elems ):
        for e in elems:
            self.compos.append( e )
    def addState( self, *elems ):
        for e in elems:
            self.states.append( e )
    def addEvent( self, *elems ):
        for e in elems:
            self.events.append( e )
    def addAction( self, *elems ):
        for e in elems:
            self.actions.append( e )

    # Borrado en bloque de las listas.
    def rmComp( self, *elems ):
        for e in elems:
            self.compos.remove( e )
    def rmState( self, *elems ):
        for e in elems:
            self.states.remove( e )
    def rmEvent( self, *elems ):
        for e in elems:
            self.events.remove( e )
    def rmAction( self, *elems ):
        for e in elems:
            self.actions.remove( e )

    # Carga recursiva de XML.
    def fromXML( self, node ):
        self.name = node.get('Name')
        if hasattr(node.Composition, 'SC'):
            for e in node.Composition.SC:
                self.compos.append(e.text)
        if hasattr(node.Composition, 'CC'):
            for e in node.Composition.CC:
                self.compos.append(e.text)
        for e in node.CC_States.CC_State:
            state = State(e.get('ID'), e.get('Active'), e.get('Visible'))
            for x in node.CC_States.CC_State.Status.SC:
                inside = StateStatus(
                    x.get('Name'),
                    x.get('Active'),
                    x.get('Visible')
                )
                state.status.append(inside)
            for x in node.CC_States.CC_State.Dialog_State.Self_Evt:
                selfEvent = StateDialogEvent(
                    x.get('ID'),
                    x.get('Event'),
                    x.get('Component'),
                    x.get('Ini_State'),
                    x.get('End_State'),
                )
                if hasattr(node.CC_States.CC_State.Dialog_State.Self_Evt, 'Pre_Cond'):
                    for x in node.CC_States.CC_State.Dialog_State.Self_Evt.Pre_Cond:
                        precondition = StateDialogEventPrecond(
                            x.get('Component'),
                            x.get('State')
                        )
                    selfEvent.addPreconds(precondition)
                state.dialogs.append(selfEvent)

            self.states.append(state)

        for e in node.External_Events.Delegate_Actions.Trigger_DA:
            inside = TriggerDA(
                e.get('ID'),
                e.get('SELF_STATE'),
                e.get('TO'),
                e.get('Trigger_DE_ID')
            )
            self.actions.append(inside)
        for e in node.External_Events.Delegate_Events.Trigger_DE:
            inside = TriggerDE(
                e.get('ID'),
                e.get('Component'),
                e.get('Ini_State'),
                e.get('End_State')
            )
            self.events.append(inside)

    # Conversion recursiva a XML.
    def toXML( self ):
        cc          = ET.Element('Complex_Component', {'Name':self.name})
        composition = ET.SubElement( cc, 'Composition' )
        states      = ET.SubElement( cc, 'CC_States' )
        externals   = ET.SubElement( cc, 'External_Events' )
        actions     = ET.SubElement( externals, 'Delegate_Actions' )
        events      = ET.SubElement( externals, 'Delegate_Events' )
        for e in self.compos:
            SC      = ET.SubElement(composition, 'SC')
            SC.text = e.__str__()
        for e in self.states:
            e.toXML(states)
        for e in self.actions:
            e.toXML(actions)
        for e in self.events:
            e.toXML(events)
        return cc
