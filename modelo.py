import re
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL import *
import math as m

from point_face import Point3D, Face

import json
import foco as foco

class Modelo:  
    alpha=None
    beta=None

    ListaPuntos3D=[]
    ListaCaras=[]

    numCaras=None
    NumVertices=None
    
    #ESTOS 4 ELEMENTOS SE USARÁN CUANDO CADA MODELO TENGA UN MATERIAL FIJO, MIENTRAS TANTO SE USARÁ UN MENÚ
    mBrillo=None
    mLuzDifusa=[]
    mLuzAmbiente=[]
    mLuzSpecular=[]

    def __init__(self, ncaras=None, nvertices=None):
        self.NumCaras = ncaras
        self.NumVertices = nvertices
        self.inicializarParametros()
    
    def setVector4(self,v, v0, v1, v2, v3):
        v[0]=v0
        v[1]=v1
        v[2]=v2
        v[3]=v3

    def inicializarParametros(self):
        self.alpha=0
        self.beta=0

    def getNCaras(self):
        return self.numCaras

    def setNCaras(self, val):
        self.numCaras = val
    def getNVertices(self):
        return self.numVertices

    def setNVertices(self, val):
        self.numVertices = val

    def setVertices(self, val):
        self.ListaPuntos3D = val
    
    def setCaras(self, val):
        self.ListaCaras = val

    def setBrillo(self, val):
        self.mBrillo = val
        
    def getBrillo(self):
        return self.mBrillo
    
    def setLDifusa(self, val):
        self.mLuzDifusa = val
        
    def getLDifusa(self):
        return self.mLuzDifusa
    
    def setLAmbiente(self, val):
        self.mLuzAmbiente = val
        
    def getLAmbiente(self):
        return self.mLuzAmbiente
    
    def setLSpecular(self, val):
        self.mLuzSpecular = val
        
    def getLSpecular(self):
        return self.mLuzSpecular

    @staticmethod
    def load(path: str):
        """Loads a asc file as a 3D model

        Args:
            path (str): The path where the asc file can be found

        Returns:
            str: Name of the imported model
            list: List of vertices (Point3D)
            list: List of faces (Face)
        """

        num_vertices, num_faces = 0, 0
        vertices, faces = list(), list()
        name = ''

        def regex(types, regex, string):
            return [t(s) for t, s in zip(types, re.search(regex, string).groups())]

        with open(path) as file:
            for line in file:
                line = line.strip()
                if line[:5] == 'Named':
                    name = re.search('"(.*)"', line).groups()[0]
                    line = next(file)
                    _, num_vertices, _, _, num_faces = regex((str, int, str, str, int),
                                                             'Tri-mesh, Vertices:(\s+)(\d+)(\s+)Faces:(\s+)(\d+)', line)

                if line == 'Vertex list:':
                    for n in range(0, num_vertices):
                        line = next(file)

                        _, x = regex((str, float), 'X:(\s*)(-?\d*\.?\d*)', line)
                        _, y = regex((str, float), 'Y:(\s*)(-?\d*\.?\d*)', line)
                        _, z = regex((str, float), 'Z:(\s*)(-?\d*\.?\d*)', line)

                        vertices.append(Point3D(x, y, z))

                if line == 'Face list:':
                    for n in range(0, num_faces):
                        line = next(file)
                        if line.strip() == '' or 'Page' in line or 'Smoothing:' in line:
                            continue

                        _, a = regex((str, int), 'A:(\s*)(\d+)', line)
                        _, b = regex((str, int), 'B:(\s*)(\d+)', line)
                        _, c = regex((str, int), 'C:(\s*)(\d+)', line)

                        ax = vertices[a].x - vertices[b].x  # X[A] - X[B]
                        ay = vertices[a].y - vertices[b].y  # Y[A] - Y[B]
                        az = vertices[a].z - vertices[b].z  # Z[A] - Z[B]
                        bx = vertices[b].x - vertices[c].x  # X[B] - X[C]
                        by = vertices[b].y - vertices[c].y  # Y[B] - Y[C]
                        bz = vertices[b].z - vertices[c].z  # Z[B] - Z[C]

                        normal = Point3D(
                            (ay * bz) - (az * by),
                            (az * bx) - (ax * bz),
                            (ax * by) - (ay * bx))

                        l = ((normal.x ** 2) + (normal.y ** 2) + (normal.z ** 2)) ** (1 / 2)

                        normal.x /= l
                        normal.y /= l
                        normal.z /= l

                        faces.append(Face(a, b, c, normal))

        return name, vertices, faces
  
    def Draw_Model(self, iForma, scale_from_editor, zoom, iLuz, iMaterial):
    
        with open('fichero.json') as file:
            data = json.load(file)
            
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT2)
        glDisable(GL_LIGHT3)
        glDisable(GL_LIGHT4)
        glDisable(GL_LIGHT5)
        glDisable(GL_LIGHT6)
        glDisable(GL_LIGHT7)
        glEnable(GL_LIGHTING)
                
        if(iLuz == 10):
            glEnable(GL_LIGHT0)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, (data['focos'][0]['luzdifusa']))
            glLightfv(GL_LIGHT0, GL_AMBIENT, (data['focos'][0]['luzambiente']))
            glLightfv(GL_LIGHT0, GL_SPECULAR, (data['focos'][0]['luzspecular']))
            glLightfv(GL_LIGHT0, GL_POSITION, (data['focos'][0]['posicion']))
        elif(iLuz == 11):
            glEnable(GL_LIGHT1)
            glLightfv(GL_LIGHT1, GL_DIFFUSE, (data['focos'][1]['luzdifusa']))
            glLightfv(GL_LIGHT1, GL_AMBIENT, (data['focos'][1]['luzambiente']))
            glLightfv(GL_LIGHT1, GL_SPECULAR, (data['focos'][1]['luzspecular']))
            glLightfv(GL_LIGHT1, GL_POSITION, (data['focos'][1]['posicion']))
        elif(iLuz == 12):
            glEnable(GL_LIGHT2)
            glLightfv(GL_LIGHT2, GL_DIFFUSE, (data['focos'][2]['luzdifusa']))
            glLightfv(GL_LIGHT2, GL_AMBIENT, (data['focos'][2]['luzambiente']))
            glLightfv(GL_LIGHT2, GL_SPECULAR, (data['focos'][2]['luzspecular']))
            glLightfv(GL_LIGHT2, GL_POSITION, (data['focos'][2]['posicion']))
        elif(iLuz == 13):
            glEnable(GL_LIGHT3)
            glLightfv(GL_LIGHT3, GL_DIFFUSE, (data['focos'][3]['luzdifusa']))
            glLightfv(GL_LIGHT3, GL_AMBIENT, (data['focos'][3]['luzambiente']))
            glLightfv(GL_LIGHT3, GL_SPECULAR, (data['focos'][3]['luzspecular']))
            glLightfv(GL_LIGHT3, GL_POSITION, (data['focos'][3]['posicion']))
        elif(iLuz == 14):
            glEnable(GL_LIGHT4)
            glLightfv(GL_LIGHT4, GL_DIFFUSE, (data['focos'][4]['luzdifusa']))
            glLightfv(GL_LIGHT4, GL_AMBIENT, (data['focos'][4]['luzambiente']))
            glLightfv(GL_LIGHT4, GL_SPECULAR, (data['focos'][4]['luzspecular']))
            glLightfv(GL_LIGHT4, GL_POSITION, (data['focos'][4]['posicion']))
        elif(iLuz == 15):
            glEnable(GL_LIGHT5)
            glLightfv(GL_LIGHT5, GL_DIFFUSE, (data['focos'][5]['luzdifusa']))
            glLightfv(GL_LIGHT5, GL_AMBIENT, (data['focos'][5]['luzambiente']))
            glLightfv(GL_LIGHT5, GL_SPECULAR, (data['focos'][5]['luzspecular']))
            glLightfv(GL_LIGHT5, GL_POSITION, (data['focos'][5]['posicion']))
        elif(iLuz == 16):
            glEnable(GL_LIGHT6)
            glLightfv(GL_LIGHT6, GL_DIFFUSE, (data['focos'][6]['luzdifusa']))
            glLightfv(GL_LIGHT6, GL_AMBIENT, (data['focos'][6]['luzambiente']))
            glLightfv(GL_LIGHT6, GL_SPECULAR, (data['focos'][6]['luzspecular']))
            glLightfv(GL_LIGHT6, GL_POSITION, (data['focos'][6]['posicion']))
        elif(iLuz == 17):
            glEnable(GL_LIGHT7)
            glLightfv(GL_LIGHT7, GL_DIFFUSE, (data['focos'][7]['luzdifusa']))
            glLightfv(GL_LIGHT7, GL_AMBIENT, (data['focos'][7]['luzambiente']))
            glLightfv(GL_LIGHT7, GL_SPECULAR, (data['focos'][7]['luzspecular']))
            glLightfv(GL_LIGHT7, GL_POSITION, (data['focos'][7]['posicion']))
                
        
        self.mBrillo=(data['materiales'][iMaterial-18]['brillo'])
        self.mLuzDifusa=[(data['materiales'][iMaterial-18]['luzdifusa'])]
        self.mLuzAmbiente=[(data['materiales'][iMaterial-18]['luzambiente'])]
        self.mLuzSpecular=[(data['materiales'][iMaterial-18]['luzspecular'])]
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.mLuzAmbiente)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.mLuzDifusa)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.mLuzSpecular)
        glMaterialf(GL_FRONT, GL_SHININESS, self.mBrillo)
    
        for face in self.ListaCaras:
            if(iForma == 6):    #Flat
                glShadeModel(GL_FLAT)
                glBegin(GL_POLYGON)
                
                glNormal3f(face.normal.x, face.normal.y, face.normal.z)

                glVertex3f(self.ListaPuntos3D[face.a].x * scale_from_editor * zoom, self.ListaPuntos3D[face.a].y * scale_from_editor * zoom, self.ListaPuntos3D[face.a].z * scale_from_editor * zoom)
                glVertex3f(self.ListaPuntos3D[face.b].x * scale_from_editor * zoom, self.ListaPuntos3D[face.b].y * scale_from_editor * zoom, self.ListaPuntos3D[face.b].z * scale_from_editor * zoom)
                glVertex3f(self.ListaPuntos3D[face.c].x * scale_from_editor * zoom, self.ListaPuntos3D[face.c].y * scale_from_editor * zoom, self.ListaPuntos3D[face.c].z * scale_from_editor * zoom)
                
            elif(iForma == 7):  #Smooth                    
                glShadeModel(GL_SMOOTH)
                glBegin(GL_POLYGON)

		
                glNormal3f(self.ListaPuntos3D[face.a].x, self.ListaPuntos3D[face.a].y, self.ListaPuntos3D[face.a].z)
                glVertex3f(self.ListaPuntos3D[face.a].x * scale_from_editor * zoom, self.ListaPuntos3D[face.a].y * scale_from_editor * zoom, self.ListaPuntos3D[face.a].z * scale_from_editor * zoom)
                
                glNormal3f(self.ListaPuntos3D[face.b].x, self.ListaPuntos3D[face.b].y, self.ListaPuntos3D[face.b].z)
                glVertex3f(self.ListaPuntos3D[face.b].x * scale_from_editor * zoom, self.ListaPuntos3D[face.b].y * scale_from_editor * zoom, self.ListaPuntos3D[face.b].z * scale_from_editor * zoom)
                
                glNormal3f(self.ListaPuntos3D[face.c].x, self.ListaPuntos3D[face.c].y, self.ListaPuntos3D[face.c].z)
                glVertex3f(self.ListaPuntos3D[face.c].x * scale_from_editor * zoom, self.ListaPuntos3D[face.c].y * scale_from_editor * zoom, self.ListaPuntos3D[face.c].z * scale_from_editor * zoom)

                glNormal3f(self.ListaPuntos3D[face.a].x, self.ListaPuntos3D[face.a].y, self.ListaPuntos3D[face.a].z)
                glVertex3f(self.ListaPuntos3D[face.a].x * scale_from_editor * zoom, self.ListaPuntos3D[face.a].y * scale_from_editor * zoom, self.ListaPuntos3D[face.a].z * scale_from_editor * zoom)

            glEnd()
            
            
            
