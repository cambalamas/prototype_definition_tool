from lxml import etree as ET

class TriggerDE:
    def __init__( self, id, comp, ini, end ):
        self.id   = int(id)
        self.comp = str(comp)
        self.ini  = int(ini)
        self.end  = int(end)

    def __str__( self ):
        return "\n\n\t~ Id: {}\n\tComp: {}\n\tIni: {}\n\tEnd: {}"\
            .format(
                self.id,
                self.comp,
                self.ini,
                self.end
            )

    def toXML( self, parent ):
        ET.SubElement(
            parent,
            'Trigger_DE',
            {
                'ID'        : str(self.id),
                'Component' : self.comp,
                'Ini_State' : str(self.ini),
                'End_State' : str(self.end)
            }
        )
