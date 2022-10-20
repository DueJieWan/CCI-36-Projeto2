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
# print(root)

library_geometries_index = 5
mesh_index = 0
triangles_wrapper_info_index = 5
triangles_wrapper_info_indexes_index = 4

class Triangle:
    #Classe Triangle 
    def __init__(self, geometric_parent_name, vertex, normal, textcoord, color):
        self.geometric_parent_name = geometric_parent_name
        self.vertex = vertex
        self.normal = normal
        self.textcoord = textcoord
        self.color = color
        #self.rho = self.calcRho()
        #self.centroid = self.calcCentroid()
        print(vertex)
        # print(normal)
        # print(textcoord)
        # print(color)

    def calcRho(self):
        return sum(self.color) / len(self.color)

    def calcCentroid(self):
        x = self.vertex
        
    def calcNormal(self):
        #Calcula o vetor normal de si mesmo
        pass

    def calcArea(self):
        #Calcula a area de si mesmo
        pass

    def calcFactorForm(self):

        pass


number_of_geometrics = len(root[library_geometries_index])
geometric_index = 0
for i in range(0, number_of_geometrics):
    geometric = root[library_geometries_index][geometric_index]
    wrapper = geometric[mesh_index]
    geometric_parent_name = geometric.attrib['name']
    print(geometric_parent_name)
    triangles =  wrapper[triangles_wrapper_info_index]
    indexes = triangles[triangles_wrapper_info_indexes_index].text.split(" ")
    indexes_length = len(indexes)
    offset = 0

    vertex_float_array = wrapper[0][0].text.split(" ")
    normal_float_array = wrapper[1][0].text.split(" ")
    textcoord_float_array = wrapper[2][0].text.split(" ")
    color_float_array = wrapper[3][0].text.split(" ")

    for i in range(0, indexes_length // 12):
        vertex_indexes = [int(indexes[offset]), int(indexes[offset+4]), int(indexes[offset+8])]
        normal_indexes = [int(indexes[offset+1]), int(indexes[offset+5]), int(indexes[offset+9])]
        textcoord_indexes = [int(indexes[offset+2]), int(indexes[offset+6]), int(indexes[offset+10])]
        color_indexes = [int(indexes[offset+3]), int(indexes[offset+7]), int(indexes[offset+11])]

        vertex = [
            [float(vertex_float_array[vertex_indexes[0]*3]), float(vertex_float_array[vertex_indexes[0]*3+1]), float(vertex_float_array[vertex_indexes[0]*3+2])],
            [float(vertex_float_array[vertex_indexes[1]*3]), float(vertex_float_array[vertex_indexes[1]*3+1]), float(vertex_float_array[vertex_indexes[1]*3+2])],
            [float(vertex_float_array[vertex_indexes[2]*3]), float(vertex_float_array[vertex_indexes[2]*3+1]), float(vertex_float_array[vertex_indexes[2]*3+2])]
        ]
        normal = [
            [float(normal_float_array[normal_indexes[0]*3]), float(normal_float_array[normal_indexes[0]*3+1]), float(normal_float_array[normal_indexes[0]*3+2])],
            [float(normal_float_array[normal_indexes[1]*3]), float(normal_float_array[normal_indexes[1]*3+1]), float(normal_float_array[normal_indexes[1]*3+2])],
            [float(normal_float_array[normal_indexes[2]*3]), float(normal_float_array[normal_indexes[2]*3+1]), float(normal_float_array[normal_indexes[2]*3+2])]
        ]
        textcoord = [
            [float(textcoord_float_array[textcoord_indexes[0]*2]), float(textcoord_float_array[textcoord_indexes[0]*2+1])],
            [float(textcoord_float_array[textcoord_indexes[1]*2]), float(textcoord_float_array[textcoord_indexes[1]*2+1])],
            [float(textcoord_float_array[textcoord_indexes[2]*2]), float(textcoord_float_array[textcoord_indexes[2]*2+1])]
        ]
        color = [
            [float(color_float_array[color_indexes[0]*4]), float(color_float_array[color_indexes[0]*4+1]), float(color_float_array[color_indexes[0]*4+2]), float(color_float_array[color_indexes[0]*4+3])],
            [float(color_float_array[color_indexes[1]*4]), float(color_float_array[color_indexes[1]*4+1]), float(color_float_array[color_indexes[1]*4+2]), float(color_float_array[color_indexes[1]*4+3])],
            [float(color_float_array[color_indexes[2]*4]), float(color_float_array[color_indexes[2]*4+1]), float(color_float_array[color_indexes[2]*4+2]), float(color_float_array[color_indexes[2]*4+3])]
        ]

        triangle = Triangle(geometric_parent_name, vertex, normal, textcoord, color)
        offset += 12

    geometric_index += 1


    

