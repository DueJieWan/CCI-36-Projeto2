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

light_source_coordinates = [1,1,1] # alterar
light_source_rgb = [255, 255, 255] 

class Triangle:
    def __init__(self, geometric_parent_name, vertex, textcoord, color, identifier):
        self.id = identifier
        self.geometric_parent_name = geometric_parent_name
        self.vertex = vertex
        self.textcoord = textcoord
        self.color = color
        self.normal = self.calcNormal()
        self.rho = self.calcRho()
        self.centroid = self.calcCentroid()
        self.area = self.calcArea()
        self.radiance = 0

    def calcRho(self):
        R = (self.color[0][0] + self.color[1][0] + self.color[2][0]) / 3
        G = (self.color[0][1] + self.color[1][1] + self.color[2][1]) / 3
        B = (self.color[0][2] + self.color[1][2] + self.color[2][2]) / 3
        A = (self.color[0][3] + self.color[1][3] + self.color[2][3]) / 3
        return [R, G, B, A]

    def calcCentroid(self):
        x = (self.vertex[0][0] + self.vertex[1][0] + self.vertex[2][0]) / 3
        y = (self.vertex[0][1] + self.vertex[1][1] + self.vertex[2][1]) / 3
        z = (self.vertex[0][2] + self.vertex[1][2] + self.vertex[2][2]) / 3
        return [x, y, z]

    def calcArea(self):
        a = np.sqrt((self.vertex[0][0] - self.vertex[1][0])**2 + (self.vertex[0][1] - self.vertex[1][1])**2 + (self.vertex[0][2] - self.vertex[1][2])**2)
        b = np.sqrt((self.vertex[0][0] - self.vertex[2][0])**2 + (self.vertex[0][1] - self.vertex[2][1])**2 + (self.vertex[0][2] - self.vertex[2][2])**2)
        c = np.sqrt((self.vertex[1][0] - self.vertex[2][0])**2 + (self.vertex[1][1] - self.vertex[2][1])**2 + (self.vertex[1][2] - self.vertex[2][2])**2)
        s = (a + b + c) / 2  # semiperimeter
        return np.sqrt(s*(s-a)*(s-b)*(s-c))

    def calcNormal(self):
        vertex_1 = self.vertex[0]
        vertex_2 = self.vertex[1]
        vertex_3 = self.vertex[2]
        v = [vertex_2[0] - vertex_1[0], vertex_2[1] - vertex_1[1], vertex_2[2] - vertex_1[2]]
        u = [vertex_3[0] - vertex_2[0], vertex_3[1] - vertex_2[1], vertex_3[2] - vertex_2[2]]
        normal_x = v[1]*u[2] - v[2]*u[1]
        normal_y = v[2]*u[0] - v[0]*u[2]
        normal_z = v[0]*u[1] - v[1]*u[0]
        return [normal_x, normal_y, normal_z]

    def updateRadiance(self, light_source_coordinates):
        scalar_product = self.normal[0]*light_source_coordinates[0] + self.normal[1]*light_source_coordinates[1] + self.normal[2]*light_source_coordinates[2]
        normal_module = np.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
        light_source_module = np.sqrt(light_source[0]**2 + light_source[1]**2 + light_source[2]**2)
        foreshortening = np.absolute(scalar_product / (normal_module * light_source_module))
        distance = np.sqrt((self.centroid[0] - light_source_coordinates[0])**2 + (self.centroid[1] - light_source_coordinates[1])**2 + (self.centroid[2] - light_source_coordinates[2])**2)
        self.radiance = foreshortening / (np.pi * distance**2)

triangles_list = []
number_of_geometrics = len(root[library_geometries_index])
geometric_index = 0
identifier = 0
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

        triangle = Triangle(geometric_parent_name, vertex, textcoord, color, identifier)
        offset += 12
        identifier += 1
        triangles_list.append(triangle)

    geometric_index += 1

print(len(triangles_list))

