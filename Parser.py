# -*- coding: utf-8 -*-
import ply.yacc as yacc
import Scanner            # Importar el analizador léxico
from FunVars import *     # Importar la clase de variables y funciones
from Cubo import *        # Importar los identificadores numéricos asignados
tokens = Scanner.tokens   # Lista de tokens
import sys

# Precedencia de los operadores
precedence = (
    ('right', 'ASSIGN'),
    ('left', 'AND', 'OR'),
    ('left', 'EQUALS', 'NOTEQUAL'),
    ('left', 'GREATERTHAN', 'GREATEREQUAL', 'LESSTHAN', 'LESSEQUAL'),
    ('left', 'SUM', 'LESS'),
    ('left', 'TIMES', 'DIVISION'),
)

# Creación de los diccionarios de tipos con sus contadores
# Variables globales
dicGlobal = {}


# Variables locales MAIN
dicMain = {}


# Variables Temporales
temporales = []
contTemp = 21000000


# Variables constantes
constantes = {}
constantes[INT] = []
constantes[FLOAT] = []
constantes[CHAR] = []
constantes[STR] = []

const_int = 1000000
const_float = 2000000
const_char = 3000000
const_str = 4000000

# Direcciones de Variables
#vars_int = 5000000 vars_float = 6000000 vars_char = 7000000 vars_string = 8000000 vars_bool = 9000000
vars_dir = [5000000, 6000000, 7000000, 8000000, 9000000]
vars_dir_global = [15000000, 16000000, 17000000, 18000000, 19000000]

# Diccionario de métodos
diccionario_metodos = {}
retornoTipo = ""        

#Lista de cuadruplos
listCuadruplos = []
contCuadruplos = 0

# Parametros
contParam = 0
funcionLlamada = ""

#Scope
scopeActual = "Global"
tipoActual = ""

#Pilas
pilaTipos = Pila()
pilaOperandos = Pila()
pilaOperadores = Pila()
pilaSaltos = Pila()
pilaRetorno = Pila()

#Funciones Especiales
color = ""

###########################################################################
#   existMetodos
#   Revisa si un identificador existe en el diccionario de métodos
###########################################################################
def existMetodos(idMet):
    if idMet in diccionario_metodos:
        return True
    return False


############################################################################
#   existVariableGlobal
#   Revisar si un identificador ya existe en las variables globales declaradas
############################################################################
def existVariableGlobal(idVar):
    return dicGlobal.has_key(idVar)
    

###########################################################################
#   varGlobalDictionary
#   Revisar en que diccionario existe un identificador, dado que ya se conoce
#   que existe en las variables globales
###########################################################################
def varGlobalDictionary(idVar):
    return dicGlobal.get(idVar).getTipo()


###########################################################################
#   addVariableGlobal
#   Añadir un identificador a los diccionarios globales de acuerdo a su tipo
###########################################################################
def addVariableGlobal(identificador, tipo, size, array):
    # Revisar si la variable ya había sido declarada con anterioridad
    global dicGlobal
    if existVariableGlobal(identificador) or existMetodos(identificador):
        print "El identificador <<" + identificador + ">> ya había sido declarado"
        sys.exit()
    else:
        var = Vars(identificador, size, array, tipo)
        var.setDireccion(vars_dir_global[var.getTipo()])
        dicGlobal[identificador] = var
        vars_dir_global[var.getTipo()] = vars_dir_global[var.getTipo()] + 1


###########################################################################
#   addVariableLocal
#   Añadir una variable local al diccionario dependiendo de su tipo, y a una
#   una lista de parámetros que será asignada al método
###########################################################################
def addVariableLocal(idVar, tipo, largo, array, scope):
    global vars_dir
    # Revisar si el nombre de la variable existe en los parámetros o en los método
    if existVariableGlobal(idVar) or existMetodos(idVar):
        print "El identificador <<" + idVar + ">> ya está en uso."
        sys.exit()
    else:
        varLoc = Vars(idVar, largo, array, tipo)
        diccionario_metodos.get(scope).addVariable(varLoc)
        tipo = diccionario_metodos.get(scope).getVariable(idVar).getTipo()
        diccionario_metodos.get(scope).getVariable(idVar).setDireccion(vars_dir[tipo])
        vars_dir[tipo] = vars_dir[tipo] + 1

###########################################################################
#   existVariableLocal
#   Busca si existe una variable en un scope local
###########################################################################
def existVariableLocal(idVar, scope):
    return diccionario_metodos.get(scope).getHasVariable(idVar)

###########################################################################
#   existVariableMain
#   Busca si existe una variable en el scope de main
###########################################################################

def addVariableMain(idVar, tipo, size, array):
    global vars_dir
    if not dicMain.has_key(idVar):
            dicMain[idVar] = Vars(idVar, size, array, tipoActual)
            tipo = dicMain[idVar].getTipo()
            dicMain[idVar].setDireccion(vars_dir[tipo])
            vars_dir[tipo] = vars_dir[tipo] + 1
    else:
        print "El identificador <<" + idVar + ">> ya está en uso."
        sys.exit()

###########################################################################
#   existVariableInParams
#   Busca si existe una variable en los parametros de un scope
###########################################################################
def existVariableInParams(idVar, scope):
    global diccionario_metodos
    params = diccionario_metodos.get(scopeActual).getParametros()
    for i in params:
        if i.getNombre() == idVar:
            return True
    return False

###########################################################################
#   cuadruplo
#  Crea cuadruplo y lo agrega a las lista de cuadruplos
###########################################################################
def cuadruplo(p1, p2, p3, p4):
    global listCuadruplos
    global contCuadruplos
    cuadruplo = [p1, p2, p3 ,p4]
    listCuadruplos.append(cuadruplo)
    contCuadruplos = contCuadruplos + 1


###########################################################################
#  operacionesBasicas
#  Crea cuadruplos de operaciones basicas cuando llega al final de
#  un nivel prioridad de derecha a izquierda
###########################################################################
def operacionesBasicas(lista):
    global pilaTipos
    global pilaOperadores
    global pilaOperandos
    global contTemp
    op = pilaOperadores.top()
    while(op in lista):
        #print pilaTipos.getList()
        #print pilaOperadores.getList()
        #print pilaOperandos.getList()
        #print op
        var2 = pilaOperandos.pop()
        var1 = pilaOperandos.pop()
        tipo2 = pilaTipos.pop()
        tipo1 = pilaTipos.pop()
        resTipo = resultante(tipo1, tipo2, op)
        if(resTipo != ERROR):
            cuadruplo(getStrType(op), var1, var2, contTemp)
            pilaOperandos.append(contTemp)
            pilaTipos.append(resTipo)
            contTemp = contTemp + 1
            pilaOperadores.pop()
            op = pilaOperadores.top()
            #print listCuadruplos
            #print "sale"
        else:
            error_semantic(p)

###########################################################################
#  asignaSalto
#  Agrega el salto del cuadruplo indicado
###########################################################################
def asignaSalto(cuad, pos):
    global listCuadruplos
    listCuadruplos[pos][3] = cuad


###########################################################################
#   p_programa
#   Regla para la especificación del programa
###########################################################################
def p_programa(p):
    'programa :  PROGRAM ID COLON globales metodos goto_main'
    cuadruplo("END", None, None, None)
    p[0] = 'Correcto'

    print "global"
    for s in dicGlobal:
        print dicGlobal.get(s).getNombre()
    print "main"
    for m in dicMain:
        print dicMain.get(m).getNombre()
    print "metodos"
    for met in diccionario_metodos:
        fun = diccionario_metodos.get(met).getVariables()
        for v in fun:
            print (v)
    print "parametros"
    for met in diccionario_metodos:
        fun = diccionario_metodos.get(met).getParametros()
        for p in fun: 
            print (p.getNombre())
    print "constantes"
    print constantes
    print pilaOperandos.getList()
    print pilaOperadores.getList()
    print pilaTipos.getList()
    pos = 0
    for i in listCuadruplos:
        print pos, i
        pos = pos + 1

###########################################################################
#   p_goto_main
#   Regla que sirve para aclarar que el primer método de la función debe
#    contener su nombre
###########################################################################
def p_goto_main(p):
    'goto_main : VOID MAIN scopemain LEFTP RIGHTP LEFTB declara_var bloque RIGHTB'

def p_scopemain(p):
    'scopemain : empty'
    global scopeActual
    global listCuadruplos
    scopeActual = "Main"
    listCuadruplos[0][3] = contCuadruplos

###########################################################################
#   p_add_globales
#   Añadir una lista de variables globales
###########################################################################
def p_globales(p):
    'globales : declara_var'
    cuadruplo('GOTO', None, None, None)
###########################################################################
#   p_declara_var
#   Revisar cuales son las variables recibidas
###########################################################################
def p_declara_var_vacio(p):
    'declara_var : empty'

def p_declara_var(p):
    'declara_var : variables'


###########################################################################
#   p_variables
#   Añadir una variable local al diccionario dependiendo de su tipo
###########################################################################
def p_variables(p):
    'variables : VAR tipo var lista_variables SEMICOLON declara_var'


    
###########################################################################
#   p_lista_variables
#   Método que revisa si existe más de una variable declarada en la lista
###########################################################################
def p_lista_variables(p):
    '''lista_variables : COMMA var lista_variables
        | empty'''
    
def p_var(p):
    '''var : ID
        | ID LEFTSB INT_CTE RIGHTSB'''
    global tipoActual
    size = 0
    array = False
    if(len(p) > 2):
        size = int(p[3])
        array = True
    if(scopeActual == "Global"):
        if not existVariableGlobal(p[1]):
            addVariableGlobal(p[1], tipoActual, size, array)
    elif(scopeActual == "Main"):
        addVariableMain(p[1], tipoActual, size, array)
    else:
        addVariableLocal(p[1], tipoActual, size, array, scopeActual)
    #print p[1], scopeActual

###########################################################################
#   p_metodos
#   Función que revisa si existen métodos
###########################################################################
def p_metodos(p):
    '''metodos : metodo metodos
        | empty'''
    
###########################################################################
#   p_metodo
#   Regla que obtiene toda la estructura de un método declarado
###########################################################################
def p_metodo(p):
    'metodo : METHOD tipo_metodo ID inicio_method LEFTP params RIGHTP LEFTB method_vars bloque RIGHTB end_method'
    global scopeActual
    global vars_dir
    vars_dir = [5000000, 6000000, 7000000, 8000000, 9000000]
    scopeActual = "Global"



###########################################################################
#   p_inicio_method
#   Regla que obtiene el cuádruplo en el que comienza el método
###########################################################################
def p_inicio_method(p):
    'inicio_method : empty'
    global scopeActual
    global diccionario_metodos
    global retornoTipo
    if not existMetodos(p[-1]):
        diccionario_metodos[p[-1]] = Funcion(p[-1], retornoTipo)
        diccionario_metodos[p[-1]].setCuadStart(contCuadruplos)
    else:
        error_method(p[-1])

    scopeActual = p[-1]

    

###########################################################################
#   p_end_method
#   Escribir el último cuádruplo del método
###########################################################################
def p_end_method(p):
    'end_method : empty'
    cuadruplo("ENDPROC", None, None, None)

###########################################################################
#   p_tipo_metodo
#   Obtener que tipo de dato retorna la función en declaración
###########################################################################
def p_tipo_metodo(p):
    '''tipo_metodo : VOID
        | tipo'''
    global retornoTipo
    if p[1] is not None:
        retornoTipo = getTipo(p[1])
    else:
        retornoTipo = getTipo(tipoActual)

###########################################################################
#   p_params
#   Parámetros que recibe el método que se está declarando
###########################################################################
def p_params(p):
    '''params : empty
            | parametro paraux'''
    
def p_paraux(p):
    '''paraux : empty
            | COMMA parametro paraux'''


###########################################################################
#   p_parametro
#   Obtener el tipo e identificador de cada parámetro
###########################################################################
def p_parametro(p):
    'parametro : tipo ID'
    global scopeActual
    global diccionario_metodos
    #print p[2], 0, False, tipoActual, scopeActual
    var = Vars(p[2], 0, False, tipoActual)
    tipo = var.getTipo()
    var.setDireccion(vars_dir[tipo])
    vars_dir[tipo] = vars_dir[tipo] + 1
    diccionario_metodos.get(scopeActual).addParametro(var)


###########################################################################
#   p_method_vars
#   Obtener las declaraciones de métodos que se realizaron para variables locales
###########################################################################
def p_method_vars(p):
    'method_vars : declara_var'    

###########################################################################
#   p_bloque
#   Lista de estatutos que puede utilizar el método
###########################################################################
def p_bloque(p):
    '''bloque : estatuto bloque
        | empty'''


###########################################################################
#   p_tipo
#   Regla para los tipos de datos
###########################################################################
def p_tipo(p):
    '''tipo : INT
        | CHAR
        | BOOLEAN
        | FLOAT
        | STRING'''
    global tipoActual
    tipoActual = p[1]


###########################################################################
#   p_estatuto
#   Tipos de estatutos que pueden utilizar los métodos
###########################################################################
def p_estatuto(p):
    '''estatuto : condicion
        | ciclo
        | return
        | lectura
        | escritura
        | llamada SEMICOLON
        | asignacion
        | dibujaPunto
        | dibujaLinea
        | dibujaCirculo
        | dibujaTriangulo
        | dibujaCuadrado
        | dibujaRectangulo
        | dibujaCuadrilatero
        '''

###########################################################################
#   p_return
#   Regla para cuando el estatuto es retorno
###########################################################################
def p_return(p):
    'return : RETURN exp SEMICOLON'
    global pilaTipos
    global pilaOperandos
    global contTemp
    var = pilaOperandos.pop()
    tipo = pilaTipos.top()
    #print (diccionario_metodos[scopeActual].getTipoRetorno(), tipo)
    if(diccionario_metodos[scopeActual].getTipoRetorno() == tipo):
        if(diccionario_metodos[scopeActual].getCuadReturn() == -1):
            diccionario_metodos[scopeActual].setCuadReturn(contTemp)
            contTemp = contTemp + 1
        cuad = diccionario_metodos[scopeActual].getCuadReturn()
        cuadruplo("=", var, None, cuad)
        cuadruplo("RETURN", None, None, cuad)
        pilaOperandos.append(contTemp)
        cuadruplo("ENDPROC", None, None, None)
    else:
        error_semantic(p)    

###########################################################################
#   p_lectura
#   Generación del cuádruplo de cuando es una lectura
###########################################################################
def p_lectura(p):
    'lectura : ID ASSIGN READ LEFTP RIGHTP SEMICOLON'
    


###########################################################################
#   p_escritura
#   Generación del cuádruplo para imprimir en pantalla
###########################################################################
def p_escritura(p):
    'escritura : PRINT LEFTP exp RIGHTP SEMICOLON'
    global pilaOperandos
    global pilaTipos
    tipo = pilaTipos.pop()
    val = pilaOperandos.pop()
    cuadruplo("PRINT",None, None, val)

###########################################################################
#   p_llamada
#   Generación del cuádruplo para realizar una llamada
###########################################################################
def p_llamada(p):
    'llamada : ID llamafun LEFTP args RIGHTP'
    global funcionLlamada
    global contParam
    global pilaOperandos
    global pilaTipos
    cuadruplo("GOSUB", None, None, diccionario_metodos[funcionLlamada].getCuadStart())
    if diccionario_metodos[funcionLlamada].getTipoRetorno() != ERROR:
        pilaTipos.append(diccionario_metodos[funcionLlamada].getTipoRetorno())
        pilaOperandos.append(diccionario_metodos[funcionLlamada].getCuadReturn())
    funcionLlamada = ""
    contParam = 0


def p_llamafun(p):
    'llamafun : empty'
    global diccionario_metodos
    global funcionLlamada
    if existMetodos(p[-1]):
        cuadruplo("ERA", None, None, p[-1])
        funcionLlamada = p[-1]
    else:
        error_method_notdeclared(p[-1])
    

###########################################################################
#   p_args
#   Argumentos que serán enviados para realizar la llamada
###########################################################################
def p_args(p):
    'args : exp param listargs'

def p_args_vacio(p):
    'args : empty'

def p_listargs(p):
    '''listargs : COMMA args
        | empty'''

def p_param(p):
    'param : empty'
    global diccionario_metodos
    global pilaTipos
    global pilaOperandos
    global contParam

    if(diccionario_metodos[funcionLlamada].getCantParam() > contParam):
        tipo = pilaTipos.pop()
        var = pilaOperandos.pop()
        if(diccionario_metodos[funcionLlamada].getParametro(contParam).getTipo() == tipo):
            cuadruplo("PARAM",contParam, None, var)
            contParam = contParam + 1
        else:
            error_types(p)
    else:
        error_params(p)


###########################################################################
#   p_asignacion
#   Regla de estatuto de asignación
###########################################################################
def p_asignacion(p):
    'asignacion : ID asign'
    global pilaTipos
    global pilaOperadores
    global pilaOperandos
    if(dicGlobal.has_key(p[1])):
        var = dicGlobal.get(p[1]).getDireccion()
        tipo = dicGlobal.get(p[1]).getTipo()
        #print( var, tipo, p[1])
    elif(dicMain.has_key(p[1])):
        var = dicMain.get(p[1]).getDireccion()
        tipo = dicMain.get(p[1]).getTipo()
    elif(diccionario_metodos.get(scopeActual).getHasVariable(p[1])):
        var = diccionario_metodos.get(scopeActual).getVariable(p[1]).getDireccion()
        tipo = diccionario_metodos.get(scopeActual).getVariable(p[1]).getTipo()
    else:
        error_variable_nodeclared(p[1])
    #print pilaTipos.getList(), p[1], tipo, pilaTipos.top()
    if(resultante(tipo, pilaTipos.top(), IGUAL) != ERROR):
        cuadruplo("=", pilaOperandos.pop(), None, var)
        pilaTipos.pop()
        pilaOperadores.pop()
    else:
        error_semantic(p)
    #if pilaOperadores[-1] == "=":
        #cuadruplo(pilaOperadores[-1],  constantes.get(FLOAT), None, pilaOperandos[-1])





def p_asignacion_array(p):
    'asignacion : ID LEFTSB exp RIGHTSB asign'
    
def p_asign(p):
    'asign : ASSIGN exp SEMICOLON'
    global pilaOperadores
    pilaOperadores.append(getNumTypeOperation(p[1]))



###########################################################################
#   p_ciclo
#   Función de la regla para cuando es un ciclo
###########################################################################
def p_ciclo(p):
    'ciclo : WHILE salto_ciclo LEFTP exp ciclo1 RIGHTP LEFTB bloque ciclo2 RIGHTB'
    

###########################################################################
#   p_salto_ciclo
#   Guardar donde el cuádruplo donde comienza la expresión
###########################################################################
def p_salto_ciclo(p):
    'salto_ciclo : empty'
    global pilaSaltos
    pilaSaltos.append(contCuadruplos)

###########################################################################
#   p_ciclo1
#   Generación del cuádruplo inicial del ciclo
###########################################################################
def p_ciclo1(p):
    'ciclo1 : empty'
    global pilaSaltos
    global pilaTipos
    global pilaOperandos
    tipo = pilaTipos.pop()
    var = pilaOperandos.pop()
    if(tipo == BOOL):
        pilaSaltos.append(contCuadruplos)
        cuadruplo("GOTOF", var, None, None)
    else:
        error_semantic(p)
   
###########################################################################
#   p_ciclo2
#   Repetir las instrucciones del ciclo
###########################################################################
def p_ciclo2(p):
    'ciclo2 : empty'
    global pilaSaltos
    pos = pilaSaltos.pop()
    asignaSalto(contCuadruplos + 1, pos)
    pos = pilaSaltos.pop()
    cuadruplo("GOTO", None, None, pos)
    

###########################################################################
#   p_condicion
#   Regla para las condicionales
###########################################################################
def p_condicion(p):
    'condicion : IF LEFTP condicion1 RIGHTP LEFTB bloque RIGHTB else'

def p_else(p):
    'else : ELSE condicion3 LEFTB bloque condicion4 RIGHTB'

def p_else_vacio(p):
    'else : empty'

###########################################################################
#   p_condicion1
#   Obtener la expresión de la condición
###########################################################################
def p_condicion1(p):
    'condicion1 : exp'
    global pilaSaltos
    global pilaTipos
    global pilaOperandos
    tipo = pilaTipos.pop()
    var = pilaOperandos.pop()
    if(tipo == BOOL):
        pilaSaltos.append(contCuadruplos)
        cuadruplo("GOTOF", var, None, None)
    else:
        error_semantic(p)

###########################################################################
#   p_condicion3
#   Generación del cuádruplo de GOTO cuando se termina de hacer la parte verdadera
###########################################################################
def p_condicion3(p):
    'condicion3 : empty'
    global pilaSaltos
    pos = pilaSaltos.pop()
    pilaSaltos.append(contCuadruplos)
    cuadruplo("GOTO", None, None, None)
    asignaSalto(contCuadruplos, pos)


###########################################################################
#   p_condicion4
#   Modificar el GOTO después de realizar la condición cuando es verdadera
###########################################################################
def p_condicion4(p):
    'condicion4 : empty'
    global pilaSaltos
    pos = pilaSaltos.pop()
    asignaSalto(contCuadruplos, pos)


###########################################################################
#   p_exp
#   Revisar el tipo de expresión que se hace, si es llamada u operación
###########################################################################
def p_exp(p):
    '''exp : llamada
        | expresion
        '''
    

###########################################################################
#   p_expresion
#   Operaciones que se pueden realizar
###########################################################################
def p_expresion(p):
    'expresion : operador1 exp1'

def p_exp1(p):
    'exp1 : empty'
    operacionesBasicas([AND, OR])
    
def p_exp1_and(p):
    'exp1 : AND saveop operador1 exp1'

def p_exp1_or(p):
    'exp1 : OR saveop operador1 exp1' 


###########################################################################
#   p_operador1
#   Operaciones de tipo comparacion booleana
###########################################################################

def p_operador1(p):
    'operador1 : operador2 exp2'

def p_exp2_vacio(p):
    'exp2 : empty'
    operacionesBasicas([IGUALIGUAL, DIFF, MENORIGUAL, MAYORIGUAL, MENOR, MAYOR])

def p_exp2_equals(p):
    'exp2 : EQUALS saveop operador2 exp2'

def p_exp2_notequals(p):
    'exp2 : NOTEQUAL saveop operador2 exp2'

def p_exp2_greatherequal(p):
    'exp2 : GREATEREQUAL saveop operador2 exp2'

def p_exp2_greatherthan(p):
    'exp2 : GREATERTHAN saveop operador2 exp2'

def p_exp2_lessthan(p):
    'exp2 : LESSTHAN saveop operador2 exp2'

def p_exp2_lessequal(p):
    'exp2 : LESSEQUAL saveop operador2 exp2'


###########################################################################
#   p_operador2
#   Operaciones de tipo termino
###########################################################################

def p_operador2(p):
    'operador2 : operador3 exp3'

def p_exp3_vacio(p):
    'exp3 : empty'
    operacionesBasicas([SUMA, RESTA])

def p_exp3_sum(p):
    'exp3 : SUM saveop operador3 exp3'


def p_exp3_less(p):
    'exp3 : LESS saveop operador3 exp3'


###########################################################################
#   p_operador3
#   Operaciones de tipo factor
###########################################################################

def p_operador3(p):
    'operador3 : operador4 exp4'

def p_exp4_empty(p):
    'exp4 : empty'
    operacionesBasicas([DIV, MULT])

def p_exp4_times(p):
    'exp4 : TIMES saveop operador4 exp4'


def p_exp4_division(p):
    'exp4 : DIVISION saveop operador4 exp4'


def p_saveop(p):
    'saveop : empty'
    global pilaOperadores
    pilaOperadores.append(getNumTypeOperation(p[-1]))

###########################################################################
#   p_operador4
#   Operaciones de tipo terminal/final
###########################################################################

def p_operador4_id(p):
    'operador4 : ID'
    global pilaOperandos
    global pilaVariables
    global pilaTipos
    global vars_dir
    global vars_dir_global
    scope = dicGlobal.has_key(p[1])
    if (scope or dicMain.has_key(p[1])):
        if scope:
            tipo = dicGlobal.get(p[1]).getTipo()
            var = dicGlobal.get(p[1]).getDireccion()
        else:
            tipo = dicMain.get(p[1]).getTipo()
            var = dicMain.get(p[1]).getDireccion()
    elif(existVariableLocal(p[1], scopeActual) or scope or existVariableInParams(p[1], scopeActual)):        
        if scope:
            tipo = dicGlobal.get(p[1]).getTipo()
            var = dicGlobal.get(p[1]).getDireccion()
        elif existVariableLocal(p[1], scopeActual):
            tipo = diccionario_metodos.get(scopeActual).getVariable(p[1]).getTipo()
            var = diccionario_metodos.get(scopeActual).getVariable(p[1]).getDireccion()
        else: 
            params = diccionario_metodos.get(scopeActual).getParametros()
            for i in params:
                if i.getNombre() == p[1]:
                    tipo = i.getTipo()
                    var = i.getDireccion()
    else:
        error_variable_nodeclared(p[1])

    pilaTipos.append(tipo)
    pilaOperandos.append(var)


def p_operador4_cons(p):
    'operador4 : constante'



def p_operador4_exp(p):
    'operador4 : LEFTP expresion RIGHTP'


###########################################################################
#   p_constante
#   Obtener constantes
###########################################################################
def p_constante_int(p):
    'constante : INT_CTE'
    global pilaTipos
    global pilaOperandos
    global const_int
    global constantes
    pilaTipos.append(INT)
    pilaOperandos.append(const_int)
    constantes.get(INT).append(int(p[1]))
    const_int = const_int + 1


def p_constante_float(p):
    'constante : FLOAT_CTE'
    global pilaTipos
    global pilaOperandos
    global const_float
    global constantes
    pilaTipos.append(FLOAT)
    pilaOperandos.append(const_float)
    constantes.get(FLOAT).append(float(p[1]))
    const_float = const_float + 1



def p_constante_char(p):
    'constante : CHAR_CTE'
    global pilaTipos
    global pilaOperandos
    global const_char
    global constantes
    pilaTipos.append(CHAR)
    var = p[1].replace('\'','')
    pilaOperandos.append(const_char)
    constantes.get(CHAR).append(var)
    const_char = const_char + 1

def p_constante_string(p):
    'constante : STRING_CTE'
    global pilaTipos
    global pilaOperandos
    global const_str
    global constantes
    pilaTipos.append(STR)
    var = p[1].replace('\"','')
    pilaOperandos.append(const_str)
    constantes.get(STR).append(var)
    const_str = const_str + 1

def p_constante_true(p):
    '''constante : TRUE
            | FALSE'''
    global pilaTipos
    global pilaOperandos
    pilaTipos.append(BOOL)
    val = True if p[1].replace('\'','') == 'true' else False
    pilaOperandos.append(val)


###########################################################################
#   Funciones de dibujo
#   
###########################################################################
def p_dibujaPunto(p): 
    'dibujaPunto : DRAW_DOT LEFTP exp COMMA exp COMMA color RIGHTP SEMICOLON'
    global pilaOperandos
    y2 = pilaOperandos.pop()
    x1 = pilaOperandos.pop()
    cuadruplo("DOT", x1, y2, color)

def p_dibujaLinea(p): 
    'dibujaLinea : DRAW_LINE LEFTP exp COMMA exp COMMA exp COMMA exp COMMA color RIGHTP SEMICOLON'
    global pilaOperandos
    w = pilaOperandos.pop()
    y2 = pilaOperandos.pop()
    x2 = pilaOperandos.pop()
    y2 = pilaOperandos.pop()
    x1 = pilaOperandos.pop()
    cuadruplo("LINE", x1, y1, color)
    cuadruplo(x2, y2, w, None)

def p_dibujaCirculo(p): 
    'dibujaCirculo : DRAW_CIRCLE LEFTP exp COMMA exp COMMA exp COMMA color RIGHTP SEMICOLON'
    global pilaOperandos
    w = pilaOperandos.pop()
    val3 = pilaOperandos.pop()
    val2 = pilaOperandos.pop()
    val1 = pilaOperandos.pop()
    cuadruplo("CIR", val1, val2, val3)
    cuadruplos(color, w, None, None)

def p_dibujaTriangulo(p): 
    'dibujaTriangulo : DRAW_TRIANGLE LEFTP exp COMMA exp COMMA exp COMMA exp COMMA exp COMMA exp COMMA color RIGHTP SEMICOLON'
    global pilaOperandos
    w = pilaOperandos.pop()
    y3 = pilaOperandos.pop()
    x3 = pilaOperandos.pop()
    y2 = pilaOperandos.pop()
    x2 = pilaOperandos.pop()
    y1 = pilaOperandos.pop()
    x1 = pilaOperandos.pop()
    cuadruplo("TRI", x1, y1, color)
    cuadruplo(x2, y2, x3, y3)
    cuadruplo(w, None, None, None)

def p_dibujaCuadrado(p): 
    'dibujaCuadrado : DRAW_SQUARE LEFTP exp COMMA exp COMMA exp COMMA exp COMMA color RIGHTP SEMICOLON'
    global pilaOperandos
    w = pilaOperandos.pop()
    l = pilaOperandos.pop()
    y1 = pilaOperandos.pop()
    x1 = pilaOperandos.pop()
    cuadruplo("SQUARE", x1, y1, color)
    cuadruplo(x1, y1, l, w)

def p_dibujaRectangulo(p): 
    'dibujaRectangulo : DRAW_RECTANGLE LEFTP exp COMMA exp COMMA exp COMMA exp COMMA color RIGHTP SEMICOLON'
    global pilaOperandos
    w = pilaOperandos.pop()
    y2 = pilaOperandos.pop()
    x2 = pilaOperandos.pop()
    y1 = pilaOperandos.pop()
    x1 = pilaOperandos.pop()
    cuadruplo("RECT", x1, y1, color)
    cuadruplo(x2, y2, w, None)
def p_dibujaCuadrilatero(p): 
    'dibujaCuadrilatero : DRAW_QUADRITERAL LEFTP exp COMMA exp COMMA exp COMMA exp COMMA exp COMMA exp COMMA exp COMMA exp COMMA exp COMMA color RIGHTP SEMICOLON'
    global pilaOperandos
    w = pilaOperandos.pop()
    y4 = pilaOperandos.pop()
    x4 = pilaOperandos.pop()
    y3 = pilaOperandos.pop()
    x3 = pilaOperandos.pop()
    y2 = pilaOperandos.pop()
    x2 = pilaOperandos.pop()
    y1 = pilaOperandos.pop()
    x1 = pilaOperandos.pop()
    cuadruplo("QUAD", x1, y1, color)
    cuadruplo(x2, y2, x3, y3)
    cuadruplo(x4, y4, w, None)
    
def p_color(p):
    '''color : RED 
        | BLUE 
        | YELLOW 
        | PURPLE 
        | GREEN 
        | BLACK 
        | CYAN 
        | WHITE'''
    global color
    color = p[1].replace('\'','')


###########################################################################
#   p_empty
#   Regla para simular vacío
###########################################################################
def p_empty(p):
    'empty :'

###########################################################################
#   p_error
#   Si existe un error de gramática en la expresión
###########################################################################
def p_error(p):
    if p:
        print("Syntax error at '%s' " % p.value)
        from Scanner import intline
        print("in line " + str(intline))
        sys.exit()
    else:
        print("Syntax error at EOF")

def error_method(var):
    print ("Method '%s' already declared" % var)
    sys.exit()

def error_method_notdeclared(meth):
    print ("Method '%s' not declared" % meth)
    sys.exit()


def error_variable_nodeclared(var):
    print ("variable '%s' not declared " % var)
    sys.exit()

def error_semantic(p): 
    print ("It is not possible realize the operation at line: %s " % p.lexer.lineno)
    sys.exit()

def error_types(p):
    print ("Type mismatch at line: %s" % p)

def error_params(p):
    print ("Error in number of parameters in line: %s" % p)

# Formar parser
# yacc.yacc(method="SLR")
parserUsh = yacc.yacc()

"""
if __name__ == '__main__':

    text = raw_input('Inserte el nombre del archivo: ')
    if (text):
        # Obtiene el archivo
        file = text
        try:
            f = open(file,'r')
            data = f.read()
            f.close()
            # Si concluye la revision exitosamente
        if (yacc.parse(data, tracking=True) == 'Correcto'):
                print ('Lexico y sintaxis correcto');
        except EOFError:
            print(EOFError)
    else:
        print('Archivo no existe')
"""