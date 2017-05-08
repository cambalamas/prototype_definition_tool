from lxml import etree as ET

class StateDialogEvent:
    def __init__( self, id, event, comp, ini, end ):
        self.id       = int(id)
        self.event    = str(event) # User action that trigger the status swap.
        self.comp     = str(comp)
        self.ini      = int(ini)
        self.end      = int(end)
        self.preconds = [] # Objs StateDialogEventPrecond.

    def __str__( self ):
        return "\n\t\t~ Id: {}\n\t\tEvent: {}\n\t\tComp: {}\
            \n\t\tIni: {}\n\t\tEnd: {}\n\t\t!Preconds...{}"\
            .format(
                self.id,
                self.event,
                self.comp,
                self.ini,
                self.end,
                self.strPreconds()
            )
    def strPreconds( self ):
        out = str()
        for e in self.preconds:
            out += e.__str__()
        return out

    def addPreconds( self, *elems ):
        for e in elems:
            self.preconds.append( e )

    def rmPreconds( self, *elems ):
        for e in elems:
            self.preconds.remove( e )

    def toXML( self, parent ):
        dialog = ET.SubElement(
            parent,
            'Self_Evt',
            {
                'ID'        : str(self.id),
                'Event'     : self.event,
                'Component' : self.comp,
                'Ini_State' : str(self.ini),
                'End_State' : str(self.end)
            }
        )
        preconds = ET.SubElement( dialog, 'Preconditions' )

        for e in self.preconds:
            e.toXML( preconds )
