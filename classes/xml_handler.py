import xml.etree.ElementTree as ET

class XmlHandler:
    @staticmethod
    def change_special_parameter(xml_file_path):
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        for param_element in root.findall(".//param[@name='Werkzeugstatus']"):
            if param_element.get('value') == 'Sonderbeschaffung':
                param_element.set('value', '5_Sonderbeschaffung')
            elif param_element.get('value') == 'FAVORIT':
                param_element.set('value', '1#_FAVORIT')
            elif param_element.get('value') == 'Freigegeben':
                param_element.set('value', '1_Freigegeben')

        tree.write(xml_file_path)