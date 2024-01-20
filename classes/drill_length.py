import xml.etree.ElementTree as ET

class XmlHandlerStatus:

    @staticmethod

    def change_special_parameter(xml_file_path):
        tree = ET.parse(xml_file_path)
        root = tree.getroot()



        tree.write(xml_file_path)