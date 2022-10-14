# importing element tree
# under the alias of ET
import xml.etree.ElementTree as ET
import numpy as np

# Passing the path of the
# xml document to enable the
# parsing process
tree = ET.parse('teste1.dae')

# getting the parent tag of
# the xml document
root = tree.getroot()

# printing the root (parent) tag
# of the xml document, along with
# its memory location
print(root)

i = 6   #library_geometries
j = 0

# printing the attributes of the
print(root[i][0][0][0][0].attrib)
print(root[i][0][0][0][0].text)

# normals
print("\n")
print(root[i][0][0][1][0].attrib)
print(root[i][0][0][1][0].text)

# textura
print("\n")
print(root[i][0][0][2][0].attrib)
# print(root[i][0][0][2][0].text)

# colors
print("\n")
print(root[i][0][0][3][0].attrib)
# print(root[i][0][0][3][0].text)

# Definicao dos triangulos (fases)
print("\n")
print(root[i][0][0][5][0].attrib)
# print(root[i][0][0][5][4].text)


class Triangle:
    def __init__(self):
        self.vertex

