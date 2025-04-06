import modelo as model
from OpenGL.GLUT import * 
from OpenGL.GLU import *
from OpenGL.GL import *
import math as math
import camara as camara
import planeta as planeta
import json
import time

class Mundo:

    # Distintas opciones del menu.
    opcionesMenu = {
      "FONDO_1":0,
      "FONDO_2":1,
      "FONDO_3":2,
      "DIBUJO_1":3,
      "DIBUJO_2":4,
      "DIBUJO_3":5,
      "FORMA_1":6,
      "FORMA_2":7,
      "FORMA_3":8,
      "FORMA_4":9,
      "LUZ_0":10,
      "LUZ_1":11,
      "LUZ_2":12,
      "LUZ_3":13,
      "LUZ_4":14,
      "LUZ_5":15,
      "LUZ_6":16,
      "LUZ_7":17,
      "MATERIAL_1":18,
      "MATERIAL_2":19,
      "MATERIAL_3":20,
      "MATERIAL_4":21,
      "MATERIAL_5":22,
      "MATERIAL_6":23,
      "MATERIAL_7":24,
      "MATERIAL_8":25,
      "MATERIAL_9":26,
      "MATERIAL_10":27,
      "CAMARA_1":28,
      "CAMARA_2":29,
      "CAMARA_3":30,
      "CAMARA_4":31
    }

    #Número de vistas diferentes.
    numCamaras=4
    
    
    #Definimos los distintos colores que usaremos para visualizar nuestro Sistema Planetario.
    #Negro, Verde oscuro, Azul oscuro, Blanco, Verde claro, Azul claro
    colores=[(0.00, 0.00, 0.00), (0.06, 0.25, 0.13), (0.10, 0.07, 0.33), (1.00, 1.00, 1.00), (0.12, 0.50, 0.26), (0.20, 0.14, 0.66)]
        
    with open('fichero.json') as file:
        data = json.load(file)
    
    ejex=[(data['camaras'][0]['ejex']),(data['camaras'][1]['ejex']),(data['camaras'][2]['ejex']),(data['camaras'][3]['ejex'])]
    ejey=[(data['camaras'][0]['ejey']),(data['camaras'][1]['ejey']),(data['camaras'][2]['ejey']),(data['camaras'][3]['ejey'])]
    ejez=[(data['camaras'][0]['ejez']),(data['camaras'][1]['ejez']),(data['camaras'][2]['ejez']),(data['camaras'][3]['ejez'])]
    centrox=[(data['camaras'][0]['centrox']),(data['camaras'][1]['centrox']),(data['camaras'][2]['centrox']),(data['camaras'][3]['centrox'])]
    centroy=[(data['camaras'][0]['centroy']),(data['camaras'][1]['centroy']),(data['camaras'][2]['centroy']),(data['camaras'][3]['centroy'])]
    centroz=[(data['camaras'][0]['centroz']),(data['camaras'][1]['centroz']),(data['camaras'][2]['centroz']),(data['camaras'][3]['centroz'])]
    upx=[(data['camaras'][0]['upx']),(data['camaras'][1]['upx']),(data['camaras'][2]['upx']),(data['camaras'][3]['upx'])]
    upy=[(data['camaras'][0]['upy']),(data['camaras'][1]['upy']),(data['camaras'][2]['upy']),(data['camaras'][3]['upy'])]
    upz=[(data['camaras'][0]['upz']),(data['camaras'][1]['upz']),(data['camaras'][2]['upz']),(data['camaras'][3]['upz'])]

    def __init__(self):
        #Inicializamos todo:

        #Variables de la clase
        self.width=800
        self.height=800
        self.aspect = self.width/self.height
        self.angulo = 0
        self.window=0
        self.Sol=model.Modelo()

        #Tamaño de los ejes y del alejamiento de Z.
        self.tamanio=0
        self.z0=0

        #Factor para el tamaño del modelo.
        self.escalaGeneral = 0.005

        #Rotacion de los modelos.
        self.alpha=0
        self.beta=0

        #Variables para la gestion del ratón.
        self.xold=0
        self.yold=0
        self.zoom=1.0

        #Vistas del Sistema Planetario.
        self.iFondo=0
        self.iDibujo=3
        self.iForma=6
        self.iLuz=13
        self.iMaterial=18
        self.iCamara=31
    
        self.start=time.time()


    def drawAxis(self):
        #Inicializamos
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        glClearColor(0.0, 0.0, 0.0, 0.0)
	
        #Eje X Rojo
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(self.tamanio, 0.0, 0.0)

        #Eje Y Verde
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, self.tamanio, 0.0)

        #Eje Z Azul
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, self.tamanio)

        glClearColor(0.0, 0.0, 0.0, 0.0)

        glEnd()
        glEnable(GL_LIGHTING)

    def drawModel(self,forma, escala):
        forma.Draw_Model(self.iForma, escala, self.zoom,self.iLuz,self.iMaterial)
        

    def display(self):
        
        glClearDepth(1.0)
        glClearColor(self.colores[self.getIFondo()][0], self.colores[self.getIFondo()][1], self.colores[self.getIFondo()][2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0,1.0,-1.0,1.0,1.0,20.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        gluLookAt(self.ejex[self.iCamara-28],self.ejey[self.iCamara-28],self.ejez[self.iCamara-28],
        self.centrox[self.iCamara-28],self.centroy[self.iCamara-28],self.centroz[self.iCamara-28],
        self.upx[self.iCamara-28],self.upy[self.iCamara-28],self.upz[self.iCamara-28])
        

        #Establecemos el color del Modelo.
        glColor3f(self.colores[self.getIDibujo()][0], self.colores[self.getIDibujo()][1], self.colores[self.getIDibujo()][2])
        
        with open('fichero.json') as file:
            data = json.load(file)
        
        self.iMaterial=18
        #Pintamos el modelo.
        for p in data['planetas']:
            tiempo=time.time()
            glPushMatrix()
            radio=p['radio']
            tamanio=p['tamanio']
            nombre=p['nombre']
            wRotAstro=p['wRotAstro']
            wRotProp=p['wRotProp']
            
            glDisable(GL_LIGHTING)
            glBegin(GL_LINES)
            for i in range(360):
                glVertex3d((radio/100.0)*math.cos(i*3.14*360),0,(radio/100.0)*math.sin(i*3.14*360))
            
            glEnd()
            glEnable(GL_LIGHTING)
            
            glRotatef(wRotAstro*tiempo,0.0,1.0,0.0)
            glTranslatef(radio/100.0*math.cos(wRotAstro*tiempo*3.14/360),0,radio/100.0*math.sin(wRotAstro*tiempo*3.14/360))
            
            glPushMatrix()
            glRotatef(wRotProp*tiempo,0.0,1.0,0.0)
            
            self.drawModel(self.Sol,self.escalaGeneral*tamanio)
            
            if self.iMaterial < 26:
                self.iMaterial=self.iMaterial+1
            else:
                self.iMaterial=18
            glPopMatrix()
            
            for luna in p["l"]:
                glPushMatrix()
                radiol=luna['radio']
                tamanio=luna['tamanio']
                nombre=luna['nombre']
                wRotAstro=luna['wRotAstro']
                wRotProp=luna['wRotProp']
                
                glDisable(GL_LIGHTING)
                glBegin(GL_LINES)
                for i in range(360):
                    glVertex3d((radiol/100.0)*math.cos(i*3.14*360),0,(radiol/100.0)*math.sin(i*3.14*360))
            
                glEnd()
                glEnable(GL_LIGHTING)
                
                glRotatef(wRotProp*tiempo,0.0,1.0,0.0)
                glTranslatef(((radiol)/100.0)*math.cos(wRotAstro*tiempo*3.14/360),0,((radiol)/100.0)*math.sin(wRotAstro*tiempo*3.14/360))
            
                self.drawModel(self.Sol,self.escalaGeneral*tamanio)
                glPopMatrix()
            
            glPopMatrix()
            
        glFlush()
        glutSwapBuffers()
        
    #Funcion para gestionar los movimientos del raton.
    def onMouse(self, button, state, x, y):
        if (button == 3) or (button == 4):
            if (state == GLUT_UP):
                pass
            if(button==3):
                self.zoom=self.zoom-0.1
                print("Zoom negativo...." + self.zoom)
            else:
                self.zoom=self.zoom+0.1
                print("Zoom positivo...." + self.zoom)
        else:
            #Actualizamos los valores de x, y.
            self.xold = x
            self.yold = y 

    #Funcion que actualiza la posicion de los modelos en la pantalla segun los movimientos del raton.
    def onMotion(self, x, y):
        self.alpha = (self.alpha + (y - self.yold))
        self.beta = (self.beta + (x - self.xold))
        self.xold = x
        self.yold = y
        glutPostRedisplay()

    #Funcion que gestiona las pulsaciones en el teclado.
    def keyPressed(self, key, x, y):
        if(key == 27):  #Tecla Esc
            #Cerramos la ventana y salimos
            glutDestroyWindow(self.window)
            exit(self, 0)

    def setVector4(self, v, v0, v1, v2, v3):
        v[0] = v0
        v[1] = v1
        v[2] = v2
        v[3] = v3
  
    #Funcion para activar las distintas opciones que permite el menu.
    def onMenu(self, opcion):
        if(opcion == self.opcionesMenu["FONDO_1"]):
            self.setIFondo(0)
        elif(opcion == self.opcionesMenu["FONDO_2"]):
            self.setIFondo(1)
        elif(opcion == self.opcionesMenu["FONDO_3"]):
            self.setIFondo(2)
        elif(opcion == self.opcionesMenu["DIBUJO_1"]):
            self.setIDibujo(3)
        elif(opcion == self.opcionesMenu["DIBUJO_2"]):
            self.setIDibujo(4)
        elif(opcion == self.opcionesMenu["DIBUJO_3"]):
            self.setIDibujo(5)
        elif(opcion == self.opcionesMenu["FORMA_1"]):
            self.setIForma(6)
        elif(opcion == self.opcionesMenu["FORMA_2"]):
            self.setIForma(7)
        elif(opcion == self.opcionesMenu["LUZ_0"]):
            self.setILuz(10)
        elif(opcion == self.opcionesMenu["LUZ_1"]):
            self.setILuz(11)
        elif(opcion == self.opcionesMenu["LUZ_2"]):
            self.setILuz(12)
        elif(opcion == self.opcionesMenu["LUZ_3"]):
            self.setILuz(13)
        elif(opcion == self.opcionesMenu["LUZ_4"]):
            self.setILuz(14)
        elif(opcion == self.opcionesMenu["LUZ_5"]):
            self.setILuz(15)
        elif(opcion == self.opcionesMenu["LUZ_6"]):
            self.setILuz(16)
        elif(opcion == self.opcionesMenu["LUZ_7"]):
            self.setILuz(17)
        elif(opcion == self.opcionesMenu["CAMARA_1"]):
            self.setICamara(28)
        elif(opcion == self.opcionesMenu["CAMARA_2"]):
            self.setICamara(29)
        elif(opcion == self.opcionesMenu["CAMARA_3"]):
            self.setICamara(30)
        elif(opcion == self.opcionesMenu["CAMARA_4"]):
            self.setICamara(31)
        glutPostRedisplay()
        return opcion
        


    def cargarModelo(self, nombre):
        _, vertices, caras = self.Sol.load(nombre)
        self.Sol.setNVertices(len(vertices))
        self.Sol.setNCaras(len(caras))
        self.Sol.setCaras(caras)
        self.Sol.setVertices(vertices)
        
        
    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setIFondo(self, iFondo):
        self.iFondo = iFondo

    def getIFondo(self):
        return self.iFondo

    def setIDibujo(self, iDibujo):
        self.iDibujo = iDibujo

    def getIDibujo(self):
        return self.iDibujo
    
    def setIForma(self, iForma):
        self.iForma = iForma

    def getIForma(self):
        return self.iForma
    
    def setILuz(self, iLuz):
        self.iLuz = iLuz

    def getILuz(self):
        return self.iLuz
    
    def setIMaterial(self, iMaterial):
        self.iMaterial = iMaterial

    def getIMaterial(self):
        return self.iMaterial
    
    def setICamara(self, iCamara):
        self.iCamara = iCamara

    def getICamara(self):
        return self.iCamara
        
        
        
        
