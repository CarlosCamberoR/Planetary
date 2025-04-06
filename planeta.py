import re
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL import *
import math as m
import modelo as modelo


class planeta:
  radio=None
  wRotAstro=None
  wRotProp=None
  tamanio=None
  nombre=None
  luna=[]
  astro=modelo.Modelo()
  
  def getAstro(self):
    return self.astro

  def setAstro(self, astro):
    self.astro = astro
      
  def getRadio(self):
    return self.radio

  def setRadio(self, radio):
    self.radio = radio
  
  def getWRotAstro(self):
    return self.wRotAstro

  def setWRotAstro(self, wRotAstro):
    self.wRotAstro = wRotAstro
  
  def getWRotProp(self):
    return self.wRotProp

  def setWRotProp(self, wRotProp):
    self.wRotProp = wRotProp
  
  def getTamanio(self):
    return self.tamanio

  def setTamanio(self, tamanio):
    self.tamanio = tamanio
  
  def getNombre(self):
    return self.nombre

  def setNombre(self, nombre):
    self.nombre = nombre
  
  def getLuna(self):
    return self.luna

  def setLuna(self, luna):
    self.luna = luna
  
  
  
  
  
  
  
