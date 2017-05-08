from lxml import etree as ET

class StateStatus:
    def __init__( self, scName, active, visible ):
        self.scName = str(scName)
        self.active  = bool(active)
        self.visible = bool(visible)

    def __str__( self ):
        return "\n\t\t~ Name: {}\n\t\tActive: {}\n\t\tVisible: {}"\
            .format(
                self.scName,
                self.active,
                self.visible
            )

    def toXML( self, parent ):
        ET.SubElement(
            parent,
            'SC',
            {
                'Name'   : self.scName,
                'Active' : str(self.active),
                'Visible': str(self.visible)
            }
        )
