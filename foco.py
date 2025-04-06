import re
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL import *
import math as m


class foco:
  brillo = None
  luzdifusa = []
  luzambiente = []
  luzspecular = []
  posicion = []
  
  
  def getBrillo(self):
    return self.brillo

  def setBrillo(self, bri):
    self.brillo = bri
  
  def getLuzDifusa(self):
    return self.luzdifusa

  def setLuzDifusa(self, ldifusa):
    self.luzdifusa = ldifusa
  
  def getLuzAmbiente(self):
    return self.luzambiente

  def setLuzDifusa(self, lambiente):
    self.luzambiente = lambiente
  
  def getLuzSpecular(self):
    return self.luzspecular

  def setLuzSpecular(self, lspecular):
    self.luzspecular = lspecular
  
  def getPosicion(self):
    return self.posicion

  def setPosicion(self, pos):
    self.posicion = pos
  
  
  
  
  
  
  
  
  
  
  
  
