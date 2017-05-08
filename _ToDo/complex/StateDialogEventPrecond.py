from lxml import etree as ET

class StateDialogEventPrecond:
    def __init__( self, comp, state):
        self.comp  = str(comp)
        self.state = int(state)

    def __str__( self ):
        return "\n\t\t\t~ Comp: {}\n\t\t\tState: {}\n"\
            .format(
                self.comp,
                self.state
            )

    def toXML( self, parent ):
        ET.SubElement(
            parent,
            'Pre_Cond',
            {
                'Component' : self.comp,
                'State'     : str(self.state)
            }
        )
