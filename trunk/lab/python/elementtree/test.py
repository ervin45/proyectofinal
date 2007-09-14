import elementtree.ElementTree as ET
tree = ET.parse("salida1.xml")
root = tree.getroot()
print root