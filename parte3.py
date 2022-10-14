# importing element tree
# under the alias of ET
from ast import For
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

# colors
print("\n")
print(root[i][0][0][3][0].attrib)
# print(root[i][0][0][3][0].text)

# Definicao dos triangulos (fases)
print("\n")
print(root[i][0][0][5][0].attrib)
# print(root[i][0][0][5][4].text)

def getTriCoordAndColor(triangles, root):
    #Preencher a lista triangles com objetos Triangle
    pass


class Triangle:
    #Classe Triangle 
    def __init__(self):
        self.vertex_coord_ind
        self.vertex_color_ind
        self.vertex_coord
        self.vertex_color
        self.normal
        self.area
        self.centroid
        self.rhoCoef

    

    def calcNormal(self):
        #Calcula o vetor normal de si mesmo
        pass

    def calcArea(self):
        #Calcula a area de si mesmo
        pass

    def calcCentroid(self):
        #Calcula o centroide de si mesmo
        pass

    def calcFactorForm(self):

        pass

    


# nao fazer mais matriz


    

