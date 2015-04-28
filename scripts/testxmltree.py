from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree



root= Element('Person')
tree = ElementTree(root)
name = Element('name')
root.append(name)
name.text = 'Julie'

print(etree.tostring(root))



