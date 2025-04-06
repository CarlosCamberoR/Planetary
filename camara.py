import re
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL import *
import math as m



class camara:
  
  ejex=None
  ejey=None
  ejez=None
  centrox=None
  centroy=None
  centroz=None
  upx=None
  upy=None
  upz=None
  
  
  
  def getEjex(self):
    return self.ejex

  def setEjex(self, ejeX):
    self.ejex = ejeX
  
  def getEjey(self):
    return self.ejey

  def setEjey(self, ejeY):
    self.ejey = ejeY
  
  def getEjez(self):
    return self.ejez

  def setEjez(self, ejeZ):
    self.ejez = ejeZ
  
  def getCentrox(self):
    return self.centrox

  def setCentrox(self, centroX):
    self.centrox = centroX
  
  def getCentroy(self):
    return self.centro

  def setCentroy(self, centroY):
    self.centroy = centroY
  
  def getCentroz(self):
    return self.centroz

  def setCentroz(self, centroZ):
    self.centroz = centroZ
  
  def getUpx(self):
    return self.upx

  def setUpx(self, upX):
    self.upx = upX
  
  def getUpy(self):
    return self.upy

  def setUpy(self, upY):
    self.upy = upY
  
  def getUpz(self):
    return self.upz

  def setUpz(self, upZ):
    self.upz = upZ
  
  
  
  
  
