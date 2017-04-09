# -*- coding: utf-8 -*-
# Identificadores de los tipos
INT = 0
FLOAT = 1
CHAR = 2
STR = 3
BOOL = 4
ERROR = -1
# El identificador 5 es para void (utilizado en métodos)

# Identificadores de las operaciones
SUMA = 10
RESTA = 11
DIV = 12
MULT = 13
MAYOR = 14
MENOR = 15
IGUALIGUAL = 16
DIFF = 17
MAYORIGUAL = 18
MENORIGUAL = 19
AND = 20
OR = 21
IGUAL = 22


# Colores
PURPLE = 30
CYAN = 31
RED = 32
GREEN = 33
YELLOW = 34
BLUE = 35
BLACK = 36



# Semantica de operadores y operandos
CUBO = [ #    id1    id2     +       -      /      *      >      <      ==     !=     >=     <=     &&     ||     =
            [ INT,   INT,   INT,    INT,   FLOAT, INT,   BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  ERROR, ERROR,  INT  ], 
            [ INT,   FLOAT, FLOAT,  FLOAT, FLOAT, FLOAT, BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  ERROR, ERROR,  ERROR], 
            [ INT,   CHAR,  ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR], 
            [ INT,   STR,   STR,    ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR], 
            [ INT,   BOOL,  ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR], 
            [ FLOAT, INT,   FLOAT,  FLOAT, FLOAT, FLOAT, BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  ERROR, ERROR,  FLOAT], 
            [ FLOAT, FLOAT, FLOAT,  FLOAT, FLOAT, FLOAT, BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  ERROR, ERROR,  FLOAT],
            [ FLOAT, CHAR,  ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR],
            [ FLOAT, STR,   STR,    ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR],
            [ FLOAT, BOOL,  ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR],
            [ CHAR,  INT,   ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR],
            [ CHAR,  FLOAT, ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR],
            [ CHAR,  CHAR,  STR,    ERROR, ERROR, ERROR, ERROR, ERROR, BOOL,  ERROR, ERROR, ERROR, ERROR, ERROR,  CHAR ],
            [ CHAR,  STR,   STR,    ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR],
            [ CHAR,  BOOL,  ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR],
            [ STR,   INT,   ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR],
            [ STR,   FLOAT, ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR],
            [ STR,   CHAR,  STR,    ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  STR  ],
            [ STR,   STR,   STR,    ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  STR  ],
            [ STR,   BOOL,  ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR],
            [ BOOL,  INT,   ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR],
            [ BOOL,  FLOAT, ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR],
            [ BOOL,  CHAR,  ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR],
            [ BOOL,  STR,   ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  ERROR],
            [ BOOL,  BOOL,  ERROR,  ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,  BOOL,  BOOL,  BOOL ] ]

###########################################################################
#   resultante
#   Encontrar el tipo del resultado de una operación
###########################################################################
def resultante (tipo1, tipo2, operador):
    ren = tipo1 * 5 + tipo2
    col = (operador - 10) + 2
    #print tipo1, tipo2, ren, col, operador
    return CUBO[ren][col]

def getTipo(tipo):
    if tipo == "int":
        return INT
    elif tipo == "float":
        return FLOAT
    elif tipo == "char":
        return CHAR
    elif tipo == "string":
        return STR
    elif tipo == "boolean":
        return BOOL
    else:
        return ERROR

# Obtener el código de la operación que se hará
def getNumTypeOperation(op):
    if op == "+":
        return SUMA
    elif op == "-":
        return RESTA
    elif op == "/":
        return DIV
    elif op == "*":
        return MULT
    elif op == ">":
        return MAYOR
    elif op == "<":
        return MENOR
    elif op == "==":
        return IGUALIGUAL
    elif op == "!=":
        return DIFF
    elif op == ">=":
        return MAYORIGUAL
    elif op == "<=":
        return MENORIGUAL
    elif op == "&&":
        return AND
    elif op == "||":
        return OR
    elif op == "=":
        return IGUAL
    else:
        return ERROR

def getStrType(op):
    if op == SUMA:
        return "+"
    elif op == RESTA:
        return "-"
    elif op == DIV:
        return "/"
    elif op == MULT:
        return "*"
    elif op == MAYOR:
        return ">"
    elif op == MENOR:
        return "<"
    elif op == IGUALIGUAL:
        return "=="
    elif op == DIFF:
        return "!="
    elif op == MAYORIGUAL:
        return ">="
    elif op == MENORIGUAL:
        return "<="
    elif op == AND:
        return "&&"
    elif op == OR:
        return "||"
    elif op == IGUAL:
        return "="
    else:
        return ERROR

#Funcion regresa un valor inicial 
def getValor(tipo):
    if tipo == "int":
        return 0
    elif tipo == "float":
        return 0.0
    elif tipo == "char":
        return ''
    elif tipo == "string":
        return ""
    elif tipo == "boolean":
        return False


