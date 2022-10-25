# importing element tree
# under the alias of ET
from ast import For
import xml.etree.ElementTree as ET
import numpy as np
import os

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

library_geometries_index = 6
mesh_index = 0
triangles_wrapper_info_index = 5
triangles_wrapper_info_indexes_index = 4

light_power = [1000, 1000, 1000]
light_source_coord = [-1.169325, -2.531484, 3.346791] # (-1.169325, -2.531484, 3.346791) -0.3584217, 13.080434, 1.630428
light_source_rgb = [255, 255, 255]

class Triangle:
    def __init__(self, geometric_parent_name, vertex, textcoord, color):
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
        return self.areaOfTriangle(self.vertex[0], self.vertex[1], self.vertex[2])

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

    def isThereInterceptionOfAnotherObject(self, light_source_coord, another_triangle):
        nx = another_triangle.normal[0]
        ny = another_triangle.normal[1]
        nz = another_triangle.normal[2]
        ux = light_source_coord[0]        
        uy = light_source_coord[1]        
        uz = light_source_coord[2]        
        vx = self.centroid[0]        
        vy = self.centroid[1]        
        vz = self.centroid[2]
        vertex_another_triangle_1 = another_triangle.vertex[0]
        vertex_another_triangle_2 = another_triangle.vertex[1]
        vertex_another_triangle_3 = another_triangle.vertex[2]
        px = vertex_another_triangle_1[0]
        py = vertex_another_triangle_1[1]       
        pz = vertex_another_triangle_1[2]
        numerator = - nx*(ux-px) + ny*(uy-py) + nz*(uz-pz)
        denominator = nx*(vx-ux) + ny*(vy-uy) + nz*(vz-uz)

        if denominator == 0:
            return True

        alfa = numerator / denominator
        interception_plane_point = [ux+alfa*(vx-ux), uy+alfa*(vy-uy), uz+alfa*(vz-uz)]
        ipx = interception_plane_point[0]
        ipy = interception_plane_point[1]
        ipz = interception_plane_point[2]

        # https://www.geeksforgeeks.org/check-whether-a-given-point-lies-inside-a-triangle-or-not/
        area_triangle_1 = self.areaOfTriangle(vertex_another_triangle_1, vertex_another_triangle_2, interception_plane_point)
        area_triangle_2 = self.areaOfTriangle(vertex_another_triangle_2, vertex_another_triangle_3, interception_plane_point)
        area_triangle_3 = self.areaOfTriangle(vertex_another_triangle_3, vertex_another_triangle_1, interception_plane_point)

        if self.area < area_triangle_1 + area_triangle_2 + area_triangle_3:
            return False
        
        return True

    def updateRadiance(self, light_source_coord):
        self.radiance = self.calcRadiance(light_source_coord)

    def calcRadiance(self, light_source_coord):
        scalar_product = self.normal[0]*light_source_coord[0] + self.normal[1]*light_source_coord[1] + self.normal[2]*light_source_coord[2]
        normal_module = np.sqrt(self.normal[0]**2 + self.normal[1]**2 + self.normal[2]**2)
        light_source_module = np.sqrt(light_source_coord[0]**2 + light_source_coord[1]**2 + light_source_coord[2]**2)
        foreshortening = np.absolute(scalar_product / (normal_module * light_source_module))
        distance = np.sqrt((self.centroid[0] - light_source_coord[0])**2 + (self.centroid[1] - light_source_coord[1])**2 + (self.centroid[2] - light_source_coord[2])**2)
        return foreshortening / (np.pi * distance**2)

    def areaOfTriangle(self, vertex_1, vertex_2, vertex_3):
        a = np.sqrt((vertex_1[0] - vertex_2[0])**2 + (vertex_1[1] - vertex_2[1])**2 + (vertex_1[2] - vertex_2[2])**2)
        b = np.sqrt((vertex_1[0] - vertex_3[0])**2 + (vertex_1[1] - vertex_3[1])**2 + (vertex_1[2] - vertex_3[2])**2)
        c = np.sqrt((vertex_2[0] - vertex_3[0])**2 + (vertex_2[1] - vertex_3[1])**2 + (vertex_2[2] - vertex_3[2])**2)
        s = (a + b + c) / 2  # semiperimeter
        return np.sqrt(s*(s-a)*(s-b)*(s-c))

# getting vertex, normal, textcoord and color
triangles_list = []
number_of_geometrics = len(root[library_geometries_index])
geometric_index = 0
for i in range(0, number_of_geometrics):
    geometric = root[library_geometries_index][geometric_index]
    wrapper = geometric[mesh_index]
    geometric_parent_name = geometric.attrib['name']
    # print(geometric_parent_name)
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

        triangle = Triangle(geometric_parent_name, vertex, textcoord, color)
        offset += 12
        triangles_list.append(triangle)

    geometric_index += 1

# getting radiance
number_of_triangles = len(triangles_list)
for i in range(0, number_of_triangles):
    interception = False
    for j in range(0, number_of_triangles):
        if i != j:
            if triangles_list[i].isThereInterceptionOfAnotherObject(light_source_coord, triangles_list[j]) == True:
                interception = True
                break
    if interception == False:
        triangles_list[i].updateRadiance(light_source_coord)

    # print(triangles_list[i].radiance)


# replacing colors
light_power_R = light_power[0]
light_power_G = light_power[1]
light_power_B = light_power[2]
geometric_index = 0
count_triangle = 0
for i in range(0, number_of_geometrics):
    geometric = root[library_geometries_index][geometric_index]
    wrapper = geometric[mesh_index]
    color_float_array = wrapper[3][0]
    aux = color_float_array.text.split(" ")

    triangles =  wrapper[triangles_wrapper_info_index]
    indexes = triangles[triangles_wrapper_info_indexes_index].text.split(" ")
    indexes_length = len(indexes)
    offset = 0

    for j in range(0, indexes_length // 12):
        triangle = triangles_list[count_triangle]
        color_indexes = [int(indexes[offset+3]), int(indexes[offset+7]), int(indexes[offset+11])]
        B_R = 0 + triangle.rho[0] * triangle.radiance * light_power_R
        B_G = 0 + triangle.rho[1] * triangle.radiance * light_power_G
        B_B = 0 + triangle.rho[2] * triangle.radiance * light_power_B

        if B_R > 1:
            B_R = 1

        if B_G > 1:
            B_G = 1

        if B_G > 1:
            B_G = 1

        aux[color_indexes[0]*4] = B_R
        aux[color_indexes[1]*4] = B_R
        aux[color_indexes[2]*4] = B_R
        aux[color_indexes[0]*4+1] = B_G
        aux[color_indexes[1]*4+1] = B_G
        aux[color_indexes[2]*4+1] = B_G
        aux[color_indexes[0]*4+2] = B_B
        aux[color_indexes[1]*4+2] = B_B
        aux[color_indexes[2]*4+2] = B_B
        offset += 12
        count_triangle += 1

    new_text = ""
    for j in range(0, len(aux)):
        new_text += str(aux[j]) + " "
    color_float_array.text = new_text
    geometric_index += 1

modified_dae_file = ET.tostring(root).decode('utf-8').replace("ns0:", "").replace(":ns0", "").encode()
with open("teste1_modified.dae", "wb") as f:
    f.write(modified_dae_file)

