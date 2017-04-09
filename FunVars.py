# -*- coding: utf-8 -*-
import Cubo as Cubo

class Pila():
	def __init__(self):
		self.lista = ["$"]
		self.size = 0

	def append(self,var):
		self.lista.append(var)
		self.size = self.size + 1

	def pop(self):
		self.size = self.size - 1
		return self.lista.pop()

	def top(self):
		return self.lista[self.size]

	def getList(self):
		return self.lista

	def getElement(self, index):
		return self.lista[index]

	def size(self):
		return self.size + 1

class Vars():
	def __init__(self, nombre, size, array, tipo):  #(self, nombre de variable, tamaño de variable, es arrray?, tipo)
		self.nombre = nombre
		self.array = array
		if array:
			self.valor = []
			for i in range(0, size):
				self.valor.append(Cubo.getValor(tipo))
		else:
			self.valor = Cubo.getValor(tipo)
		self.size = size
		self.tipo = Cubo.getTipo(tipo)
		self.direccion = -1

	def setValor(self, valor):
		self.valor = valor
	
	def setArray(self, array, size, tipo):
		self.array = array
		self.size = size
		if array:
			for i in range(0, size):
				self.valor.append(Cubo.getValor(tipo))
		else:
			self.valor = Cubo.getValor(tipo)

	def setDireccion(self, direccion):
		self.direccion = direccion
	
	def getTipo(self):
		return self.tipo

	def getNombre(self):
		return self.nombre

	def getArray(self):
		return self.array

	def getSize(self):
		return self.size

	def getDireccion(self):
		return self.direccion

class Funcion():
	def __init__(self, nombre, tipoReturn):
		self.nombre = nombre
		self.tipoReturn = tipoReturn
		self.parametros = []
		self.variables = {}
		self.cuadruploStart = -1
		self.cuadruploReturn = -1
		self.cantParam = 0

	def addParametro(self, var):
		self.parametros.append(var)
		self.cantParam = self.cantParam + 1

	def addVariable(self, var):
		self.variables[var.nombre] = var

	def getVariable(self, var):
		return (self.variables.get(var))

	def getHasVariable(self, var):
		return (self.variables.has_key(var))

	def getVariables(self):
		return self.variables

	def setCuadStart(self, cuad):
		self.cuadruploStart = cuad

	def setCuadReturn(self, cuad):
		self.cuadruploReturn = cuad

	def getParametros(self):
		return self.parametros

	def getParametro(self, pos):
		return self.parametros[pos]

	def getCantParam(self):
		return self.cantParam

	def getTipoRetorno(self):
		return self.tipoReturn

	def getCuadStart(self):
		return self.cuadruploStart

	def getCuadReturn(self):
		return self.cuadruploReturn