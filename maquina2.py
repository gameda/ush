# -*- coding: utf-8 -*-
import Parser
import sys
from graphics import *
from Cubo import *
from Parser import dicGlobal as Globales
from Parser import dicMain
from Parser import constantes
from Parser import diccionario_metodos
from Parser import listCuadruplos
from Parser import contTemp

dicGlobal = {}
dicMetodos = {}
varGlobales = [[],[],[],[],[]]
varMain = [[],[],[],[],[]]
temporales = []
listPos = []
listFun = []

funcMem = []
retorno = None 
Scope = 0

##########################################################################
#	memoriaGlobal()
# 	Mete al diccionario de memoria global, el tipo y el numero de variable de ese tipo
##########################################################################
def memoriaGlobal():

	contInt = 0
	contFloat = 0
	contChar = 0
	contString = 0
	contBoolean = 0

	for key in Globales:
		direc = Globales.get(key).getDireccion()
		tipo = Globales.get(key).getTipo()
		size = 1 if Globales.get(key).getSize() < 1 else Globales.get(key).getSize()
		size2 = Globales.get(key).getSize()
		if tipo == INT:
			dicGlobal[direc] = [tipo, contInt, size2]
			for i in range(0, size):
				contInt = contInt + 1
		elif tipo == FLOAT:
			dicGlobal[direc] = [tipo, contFloat, size2]
			for i in range(0, size):
				contFloat + contFloat + 1
		elif tipo == CHAR:
			dicGlobal[direc] = [tipo, contChar, size2]
			for i in range(0, size):
				contChar = contChar + 1
		elif tipo == STR:
			dicGlobal[direc] = [tipo, contString, size2]
			for i in range(0, size):
				contString = contString + 1
		elif tipo == BOOL:
			dicGlobal[direc] = [tipo, contBoolean, size2]
			for i in range(0, size):
				contBoolean = contBoolean + 1
		for i in range(0, size):
			varGlobales[tipo].append(getValor(tipo))
	
	for i in range(contTemp - 21000000):
		temporales.append(None)

	#print(temporales)
	#print(varGlobales, dicGlobal)

##########################################################################
#	memoriaGlobal()
# 	Mete al diccionario de memoria global, el tipo y el numero de variable de ese tipo
##########################################################################
def memoriaMain():

	dicFun = {}  				#Diccionario de funciones
	varFun = [[],[],[],[],[]]
	listFun.append('main')

	contInt = 0
	contFloat = 0
	contChar = 0
	contString = 0
	contBoolean = 0

	for key in dicMain:
		direc = dicMain.get(key).getDireccion()
		tipo = dicMain.get(key).getTipo()
		size = 1 if dicMain.get(key).getSize() < 1 else dicMain.get(key).getSize()
		size2 = dicMain.get(key).getSize()
		if tipo == INT:
			dicFun[direc] = [tipo, contInt, size2]
			for i in range(0, size):
				contInt = contInt + 1
		elif tipo == FLOAT:
			dicFun[direc] = [tipo, contFloat, size2]
			for i in range(0, size):
				contFloat + contFloat + 1
		elif tipo == CHAR:
			dicFun[direc] = [tipo, contChar, size2]
			for i in range(0, size):
				contChar = contChar + 1
		elif tipo == STR:
			dicFun[direc] = [tipo, contString, size2]
			for i in range(0, size):
				contString = contString + 1
		elif tipo == BOOL:
			dicFun[direc] = [tipo, contBoolean, size2]
			for i in range(0, size):
				contBoolean = contBoolean + 1
		for i in range(0, size):
			varFun[tipo].append(getValor(tipo))

	funcMem.append([dicFun, varFun]) #Guarda las funciones actuales que se estan usando el [ diccionario de variables y
									 #la lista de variables de la función ], temporalmente 
									 #funcMem = [ [ dic[direccion]=[tipo,posicion], varFun=[[valor,valor,...],[valor]..] ],  [ dic[direccion]=[tipo,posicion], varFun =[[valor,valor,...],[valor]..] ] ]
	#print(funcMem)

##########################################################################
#	memoriaFuncion( funcion )
# 	
##########################################################################

def memoriaFuncion(funcion):

	dicFun = {}  				#Diccionario de funciones
	varFun = [[],[],[],[],[]]
	func = diccionario_metodos.get(funcion) #Guarda la funcion temporalmente
	funcAct = funcion
	listFun.append(funcion)
	#Guarda los parametros como variables para ponerlos en memoria
	parametros = func.getParametros()
	for i in parametros:
		func.addVariable(i)
	variables = func.getVariables() #Guarda las variables de la funcion temporalmente 
	
	#Recorre todas las varibales de la funcion
	for v in variables:
		direccion = variables.get(v).getDireccion()
		#valor = variables.get(v).get("valor")

		# Guarda  dicFun[ direccion ] = [tipo, posicion]
		# Agrega  en VarFun = [[],[],[],[]] el valor en el la lista correspondiente 
		if variables.get(v).getTipo() == 0:
			dicFun[direccion] = [variables.get(v).getTipo(),  variables.get(v).getDireccion() - 5000000, variables.get(v).getSize()]
			#varFun[variables.get(v).get("type")].append(valor)

		elif variables.get(v).getTipo() == 1:
			dicFun[direccion] = [variables.get(v).getTipo(),  variables.get(v).getDireccion() - 6000000, variables.get(v).getSize()]

		elif variables.get(v).getTipo() == 2:
			dicFun[direccion] = [variables.get(v).getTipo(),  variables.get(v).getDireccion() - 7000000, variables.get(v).getSize()]

		elif variables.get(v).getTipo() == 3:
			dicFun[direccion] = [variables.get(v).getTipo(),  variables.get(v).getDireccion() - 8000000, variables.get(v).getSize()]

		elif variables.get(v).getTipo() == 4:
			dicFun[direccion] = [variables.get(v).getTipo(),  variables.get(v).getDireccion() - 9000000, variables.get(v).getSize()]

	#Inicializa las variables con un valor default y las guarda en la lista de variables por tipo, de funciones. 
	for k in dicFun:
		if dicFun.get(k)[0] == 0:
			varFun[dicFun.get(k)[0]].append(0)
			for i in range(0, dicFun.get(k)[2]):
				varFun[dicFun.get(k)[0]].append(0)
		elif dicFun.get(k)[0] == 1:
			varFun[dicFun.get(k)[0]].append(0.0)
			for i in range(0, dicFun.get(k)[2]):
				varFun[dicFun.get(k)[0]].append(0.0)
		elif dicFun.get(k)[0] == 2:
			varFun[dicFun.get(k)[0]].append('')
			for i in range(0, dicFun.get(k)[2]):
				varFun[dicFun.get(k)[0]].append('')
		elif dicFun.get(k)[0] == 3:
			varFun[dicFun.get(k)[0]].append("")
			for i in range(0, dicFun.get(k)[2]):
				varFun[dicFun.get(k)[0]].append("")
		elif dicFun.get(k)[0] == 4:
			varFun[dicFun.get(k)[0]].append(False)
			for i in range(0, dicFun.get(k)[2]):
				varFun[dicFun.get(k)[0]].append(False)

	'''for i in range(func.get("temporales")):
		listTemp.append(None)'''

	funcMem.append([dicFun, varFun]) #Guarda las funciones actuales que se estan usando el [ diccionario de variables y
									 #la lista de variables de la función ], temporalmente 
									 #funcMem = [ [ dic[direccion]=[tipo,posicion], varFun=[[valor,valor,...],[valor]..] ],  [ dic[direccion]=[tipo,posicion], varFun =[[valor,valor,...],[valor]..] ] ]

##########################################################################
#	scoper(direc)
# 	Vericfica de que tipo e una variable, local o global 
##########################################################################
def scopeVar(direc):
	#print (funcMem[Scope][0])

	if funcMem[Scope][0].has_key(direc): #Si existe llave , regresa 1  
		return 1

	elif dicGlobal.has_key(direc): #Si encuentra un llave en las variables globales retorna 0
		return 0
	elif (direc >= 21000000 and direc < 30000000): #Si es un temporal
		return 2
	else:
		return -1

#############################################################
#		ValorDireccion(direc)
#		Regresa el valor apartir de una dirección 
#
##############################################################
def valorDireccion(direc):
	if(isinstance(direc, list)):
		if direc[2] == 1:
			return funcMem[Scope][1][direc[0]][direc[1]]
		else:
			return varGlobales[direc[0]][direc[1]]
	var = scopeVar(direc)
	#Si var es igual a 0, es una variable global, y regresa su valor 
	if(var == 0): 
		dirGlobal = dicGlobal.get(direc)
		return varGlobales[dirGlobal[0]][dirGlobal[1]]

	#Si var es mayor a 0, es una variable de un metodo, y regresa su valor 
	elif(var == 1):
		lista = funcMem[Scope][0].get(direc)
		tipo = lista[0]
		pos = lista[1]
		return funcMem[Scope][1][tipo][pos]

	elif(21000000 <= direc and direc < 30000000):
		return temporales[direc - 21000000]

	elif(1000000 <= direc and direc < 2000000):
		return constantes[INT][direc - 1000000]

	elif(2000000 <= direc and direc < 3000000):
		return constante[FLOAT][direc - 2000000]

	elif(3000000 <= direc and direc < 4000000):
		return constantes[CHAR][direc - 3000000]

	elif(4000000 <= direc and direc < 5000000):
		return constantes[STR][direc - 4000000]
	

	return direc

def asignarTemporales(valor, direc):
	#print(direc)
	temporales[direc - 21000000] = valor
def asignarParametros(param, valor):
	pos = int(param)
	#print(pos, listFun)
	func = diccionario_metodos.get(listFun[len(listFun) - 1])
	func = func.getParametro(pos)
	direc = func.getDireccion()
	#for v in func:
		#if func.get(v).get("posicion") == pos:
		#direc = func.get(v).getDireccion()
	lista = funcMem[Scope + 1][0].get(direc)
	funcMem[Scope + 1][1][lista[0]][lista[1]] = valorDireccion(valor)

def isList(val):
	if(isinstance(val, list)):
		return valorDireccion(val)
	else:
		return val

def getCuadruplo(cuad):
	val = None if(isinstance(cuad[0], str)) else valorDireccion(cuad[0])
	return [val, valorDireccion(cuad[1]),valorDireccion(cuad[2]),valorDireccion(cuad[3])]


# Método principal
def main():
	memoriaGlobal()
	memoriaMain()


#def operacionCuadruplos(lista_cuadruplos):
if __name__ == "__main__":
	lista_cuadruplos = listCuadruplos
	main()
	ventana = GraphWin('Ush Programming Language', 800, 600)
	ventana.setCoords(0,0,812,612)
	cuadruploActual = 0

	while cuadruploActual < len(lista_cuadruplos):
		cuadruplo = lista_cuadruplos[cuadruploActual] 
		val1 = cuadruplo[0]
		val2 = cuadruplo[1]
		val3 = cuadruplo[2]
		val4 = cuadruplo[3]
		if cuadruplo[0] == '+':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			res1 = isList(res1)
			res2 = isList(res2)
			asignarTemporales(res1 + res2, val4)

		elif cuadruplo[0] == '-':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			res1 = isList(res1)
			res2 = isList(res2)
			asignarTemporales(res1 - res2, val4)

		elif cuadruplo[0] == '/':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			res1 = isList(res1)
			res2 = isList(res2)
			asignarTemporales(res1 / res2, val4)

		elif cuadruplo[0] == '*':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			res1 = isList(res1)
			res2 = isList(res2)
			asignarTemporales(res1 * res2, val4)

		elif cuadruplo[0] == '>':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			res1 = isList(res1)
			res2 = isList(res2)
			asignarTemporales(res1 > res2, val4)

		elif cuadruplo[0] == '<':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			res1 = isList(res1)
			res2 = isList(res2)
			asignarTemporales(res1 < res2, val4)

		elif cuadruplo[0] == '==':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			res1 = isList(res1)
			res2 = isList(res2)
			asignarTemporales(res1 == res2, val4)

		elif cuadruplo[0] == '!=':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			res1 = isList(res1)
			res2 = isList(res2)
			asignarTemporales(res1 != res2, val4)

		elif cuadruplo[0] == '>=':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			res1 = isList(res1)
			res2 = isList(res2)
			asignarTemporales(res1 >= res2, val4)

		elif cuadruplo[0] == '<=':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			res1 = isList(res1)
			res2 = isList(res2)
			asignarTemporales(res1 <= res2, val4)

		elif cuadruplo[0] == '&&':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			res1 = isList(res1)
			res2 = isList(res2)
			asignarTemporales(res1 and res2, val4)

		elif cuadruplo[0] == '||':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			res1 = isList(res1)
			res2 = isList(res2)
			asignarTemporales(res1 or res2, val4)

		elif cuadruplo[0] == '=':
			res1 = valorDireccion(val2)
			var = scopeVar(val4)
			res1 = isList(res1)
			#print (res1, var, dicGlobal.get(val4),funcMem[Scope][0].get(val4), valorDireccion(val4))
			if var == 0:
				lista = dicGlobal.get(val4)
				if retorno is not None:
					varGlobales[lista[0]][lista[1]] = retorno
					retorno = None
				else:
					varGlobales[lista[0]][lista[1]] = res1
			elif var == 1:
				lista = funcMem[Scope][0].get(val4)
				varsFun = funcMem[Scope][1]
				if retorno is not None:
					varsFun[lista[0]][lista[1]] = retorno
					retorno = None
				else:
					varsFun[lista[0]][lista[1]] = res1
				funcMem[Scope][1] = varsFun
			elif(isinstance(valorDireccion(val4), list)):
				direc = valorDireccion(val4)
				if(direc[2] == 1):
					funcMem[Scope][1][direc[0]][direc[1]] = res1
				else:
					#print("RES", res1, direc)
					varGlobales[direc[0]][direc[1]] = res1
			elif var == 2:
				asignarTemporales(res1, val4)
				
		elif cuadruplo[0] == 'READ':
			res1 = input()
			var = scopeVar(val4)
			#print(type(res1), getTypeLanguage(val3))
			if type(res1) is getTypeLanguage(val3):
				if var == 0:
					lista = dicGlobal.get(val4)
					varGlobales[lista[val3]][lista[1]] = res1
				elif var == 1:
					lista = funcMem[Scope][val3].get(val4)
					funcMem[Scope][1][lista[val3]][lista[1]] = res1
				if val3 == CHAR and len(res1) > 1:
					print("Type mismatch, unsopported string as char")
					ventana.close()
					sys.exit(1)
			else:
				print("Type mismatch, unsopported value")
				ventana.close()
				sys.exit(1)

		elif cuadruplo[0] == 'PRINT':
			val = valorDireccion(val4)
			if isinstance(val, list):
				val = funcMem[Scope][1][val[0]][val[1]] if val[2] == 1 else varGlobales[val[0]][val[1]]
			print val

		elif cuadruplo[0] == 'GOTOF':
			if not valorDireccion(val2):
				cuadruploActual = val4 - 1

		elif cuadruplo[0] == 'GOTO':
			cuadruploActual = val4 - 1

		elif cuadruplo[0] == 'RETURN':
			retorno = valorDireccion(val4)
			cuadruploActual = cuadruploActual

		elif cuadruplo[0] == 'ERA':
			memoriaFuncion(val4)

		elif cuadruplo[0] == 'PARAM':
			asignarParametros(val2, val4)

		elif cuadruplo[0] == 'GOSUB':
			listPos.append(cuadruploActual + 1)
			cuadruploActual = val4 - 1
			Scope = Scope + 1

		elif cuadruplo[0] == 'ENDPROC':
			Scope = Scope - 1
			if listCuadruplos[cuadruploActual - 1][0] != 'ENDPROC':
				funcMem.pop()
				listFun.pop()
				if(len(listFun) > 0):
					funcAct = listFun[len(listFun) - 1]
				if not len(listPos) == 0:
					cuadruploActual = listPos.pop() - 1
		
		#Arreglos
		elif cuadruplo[0] == 'VAL':
			size = funcMem[Scope][0].get(val2)[2] if scopeVar(val2) == 1 else dicGlobal.get(val2)[2]
			if size > 0:
				asignarTemporales(True, val4)
			else:
				print "Error variable try to access as an array"
				ventana.close()
				sys.exit(1)
		elif cuadruplo[0] == 'VER':
			size = funcMem[Scope][0].get(val2)[2] if scopeVar(val2) == 1 else dicGlobal.get(val2)[2]
			pos = valorDireccion(val3)
			#print (size, pos, val3, funcMem[Scope][0])
			if pos > -1 and pos < size:
				asignarTemporales(pos, val4)
			else:
				print "Index out of bounce"
				ventana.close()
				sys.exit(1)
		elif cuadruplo[0] == 'RES':
			lista = funcMem[Scope][0].get(val2) if scopeVar(val2) == 1 else dicGlobal.get(val2)
			valor = valorDireccion(val3)
			direc = [lista[0],lista[1] + valor, scopeVar(val2)]
			asignarTemporales(direc, val4)
		
		#Grafico
		elif cuadruplo[0] == "DOT":
			cuad = getCuadruplo(lista_cuadruplos[cuadruploActual])
			p = Point(cuad[1], cuad[2])
			p.setFill(cuad[3])
			p.draw(ventana)

		elif cuadruplo[0] == "LINE":
			cuad1 = getCuadruplo(lista_cuadruplos[cuadruploActual])
			cuad2 = getCuadruplo(lista_cuadruplos[cuadruploActual + 1])
			line = Line(Point(cuad1[1], cuad1[2]), Point(cuad2[0], cuad2[1]))
			line.setFill(cuad1[3])
			line.setWidth(cuad2[2])
			line.draw(ventana)
			cuadruploActual = cuadruploActual + 1

		elif cuadruplo[0] == "TRI":
			cuad1 = getCuadruplo(lista_cuadruplos[cuadruploActual])
			cuad2 = getCuadruplo(lista_cuadruplos[cuadruploActual + 1])
			cuad3 = getCuadruplo(lista_cuadruplos[cuadruploActual + 2])
			tri = Polygon(Point(cuad1[1], cuad1[2]), Point(cuad2[0], cuad2[1]), Point(cuad2[2], cuad2[3]))
			tri.setFill(cuad1[3])
			tri.setOutline(cuad1[3])
			tri.setWidth(cuad3[0])
			tri.draw(ventana)
			cuadruploActual = cuadruploActual + 2

		elif cuadruplo[0] == "SQUARE":
			cuad1 = getCuadruplo(lista_cuadruplos[cuadruploActual])
			cuad2 = getCuadruplo(lista_cuadruplos[cuadruploActual + 1])
			sq = Rectangle(Point(float(cuad1[1]), float(cuad1[2])), Point(float(cuad2[0] + cuad2[2]), float(cuad2[1] + cuad2[2])))
			sq.setFill(cuad1[3])
			sq.setOutline(cuad1[3])
			sq.setWidth(cuad2[3])
			sq.draw(ventana)
			cuadruploActual = cuadruploActual + 1

		elif cuadruplo[0] == "RECT":
			cuad1 = getCuadruplo(lista_cuadruplos[cuadruploActual])
			cuad2 = getCuadruplo(lista_cuadruplos[cuadruploActual + 1])
			rc = Rectangle(Point(float(cuad1[1]), float(cuad1[2])), Point(float(cuad2[0]), float(cuad2[1])))
			rc.setFill(cuad1[3])
			rc.setOutline(cuad1[3])
			rc.setWidth(cuad2[2])
			rc.draw(ventana)
			cuadruploActual = cuadruploActual + 1

		elif cuadruplo[0] == "CIR":
			cuad1 = getCuadruplo(lista_cuadruplos[cuadruploActual])
			cuad2 = getCuadruplo(lista_cuadruplos[cuadruploActual + 1])
			cir = Circle(Point(float(cuad1[1]), float(cuad1[2])), float(cuad1[3]))
			cir.setFill(cuad2[2])
			cir.setOutline(cuad2[2])
			cir.setWidth(cuad2[1])
			cir.draw(ventana)
			cuadruploActual = cuadruploActual + 1

		elif cuadruplo[0] == 'END':
			cuadruploActual = cuadruploActual
		
		cuadruploActual = cuadruploActual + 1
	
	ventana.getMouse()
	ventana.close()