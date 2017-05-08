from lxml import etree as ET

class TriggerDA:
    def __init__( self, id, selfState, compDest, destEvent ):
        self.id    = int(id)
        self.state = int(selfState)
        self.comp  = str(compDest)
        self.event = int(destEvent)

    def __str__( self ):
        return "\n\n\t~ Id: {}\n\tState: {}\n\tComp: {}\n\tEvent: {}"\
            .format(
                self.id,
                self.state,
                self.comp,
                self.event
            )

    def toXML( self, parent ):
        ET.SubElement(
            parent,
            'Trigger_DA',
            {
                'ID'            : str(self.id),
                'SELF_STATE'    : str(self.state),
                'TO'            : self.comp,
                'Trigger_DE_ID' : str(self.event)
            }
        )
