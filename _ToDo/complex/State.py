from lxml import etree as ET

class State:
    def __init__( self, id, active, visible ):
        self.id      = int(id)
        self.active  = bool(active)
        self.visible = bool(visible)
        self.status  = [] # Objs StateStatus.
        self.dialogs = [] # Objs StateDialogEvent.

    def __str__( self ):
        return "\n\n\t~ Id: {}\n\tActive: {}\n\tVisible: {}\
            \n\t----------\n\t!Status...{}\n\t!Dialogs...{}"\
            .format(
                self.id,
                self.active,
                self.visible,
                self.strStatus(),
                self.strDialogs()
            )
    def strStatus( self ):
        out = str()
        for e in self.status:
            out += e.__str__()
        return out
    def strDialogs( self ):
        out = str()
        for e in self.dialogs:
            out += e.__str__()
        return out

    def addStatus( self, *elems ):
        for e in elems:
            self.status.append( e )
    def addDialogs( self, *elems ):
        for e in elems:
            self.dialogs.append( e )

    def rmStatus( self, *elems ):
        for e in elems:
            self.status.remove( e )
    def rmDialogs( self, *elems ):
        for e in elems:
            self.dialogs.remove( e )


    def toXML( self, parent ):
        state  = ET.SubElement(
            parent,
            'CC_State',
            {
                'ID'      : str(self.id),
                'Active'  : str(self.active),
                'Visible' : str(self.visible)
            }
        )
        status  = ET.SubElement( state, 'Status' )
        dialogs = ET.SubElement( state, 'Dialog_State' )

        for e in self.status:
            e.toXML( status )

        for e in self.dialogs:
            e.toXML( dialogs )
