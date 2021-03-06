# -*- coding: utf-8 -*-
###########################################################################
#   Scanner.py
#   Análisis léxico para el lenguaje USH
#
# 
###########################################################################

# Importa la librería de léxico de PLY
import ply.lex as lex

# Contador de lineas
intline = 0

# Lista de tokens que emplea
tokens = [ 'ID',
           'LEFTSB',
           'RIGHTSB',
           'COMMA',
           'SEMICOLON',
           'COLON',
           'LEFTP',
           'RIGHTP',
           'LEFTB',
           'RIGHTB',
           'ASSIGN',
           'FLOAT_CTE',
           'INT_CTE',
           'CHAR_CTE',
           'STRING_CTE',
           'TIMES',
           'DIVISION',
           'SUM',
           'LESS',
           'EQUALS',
           'GREATEREQUAL',
           'GREATERTHAN',
           'LESSTHAN',
           'LESSEQUAL',
           'NOTEQUAL',
           'OR',
           'AND'
            
  ]

# Lista de identificadores reservados
reserved = {
    'program' : 'PROGRAM',
    'var'     : 'VAR',
    'method'  : 'METHOD',
    'int'     : 'INT',
    'char'    : 'CHAR',
    'boolean' : 'BOOLEAN',
    'float'   : 'FLOAT',
    'string'  : 'STRING',
    'void'    : 'VOID',
    'return'  : 'RETURN',
    'read'    : 'READ',
    'while'   : 'WHILE',
    'print'   : 'PRINT',
    'if'      : 'IF',
    'else'    : 'ELSE',
    'true'    : 'TRUE',
    'false'   : 'FALSE',
    'main'    : 'MAIN',
    'drawDot' : 'DRAW_DOT',
    'drawLine' : 'DRAW_LINE',
    'drawCircle' : 'DRAW_CIRCLE',
    'drawTriangle' : 'DRAW_TRIANGLE',
    'drawSquare' : 'DRAW_SQUARE',
    'drawRectangle' : 'DRAW_RECTANGLE',
    'drawQuadrilateral' : 'DRAW_QUADRITERAL',
    'red' : 'RED',
    'blue' : 'BLUE',
    'yellow' : 'YELLOW',
    'purple' : 'PURPLE',
    'green' : 'GREEN', 
    'black' : 'BLACK',
    'cyan' : 'CYAN',
    'white' : 'WHITE',
    'ForestGreen' : 'FG',
    'AntiqueWhite4' : 'AW4',
    'snow' : 'SNOW',
    'MidnightBlue' : 'MB',
    'LightYellow' : 'LY'
}

# Agregar las palabras reservadas a la lista de tokens
tokens += reserved.values()

# Expresiones regulares de los tokens
t_ignore    = ' \r\t'
t_LEFTSB = r'\['
t_RIGHTSB = r'\]'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_LEFTP = r'\('
t_RIGHTP = r'\)'
t_LEFTB = r'\{'
t_RIGHTB = r'\}'
t_ASSIGN = r'\='
t_CHAR_CTE = r'\'.\''
t_STRING_CTE = r'\"(.*?)\"'
t_TIMES = r'\*'
t_DIVISION = r'/'
t_SUM = r'\+'
t_LESS = r'\-'
t_EQUALS = r'\=\='
t_GREATEREQUAL = r'\>\='
t_GREATERTHAN = r'\>'
t_LESSTHAN = r'\<'
t_LESSEQUAL = r'\<\='
t_NOTEQUAL = r'\!\='
t_OR = r'\|\|'
t_AND = r'\&\&'
t_ignore_COMMENT = r'\#.*'

###########################################################################
#   t_FLOAT_CTE
#   Expresión regular para detectar los números con decimales
###########################################################################
def t_FLOAT_CTE(t):
    r'[-]?\d+\.\d+'
    t.value = float(t.value)
    return t

###########################################################################
#   t_INT_CTE
#   Expresión regular para identificar los números enteros
###########################################################################
def t_INT_CTE(t):
    r'[-]?\d+'
    t.value = int(t.value)
    return t

###########################################################################
#   t_ID
#   Expresión regular para identificadores
###########################################################################
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[ t.value ]
    return t

###########################################################################
#   t_newline
#   Expresión regular para contar las líneas nuevas y saltos de página
###########################################################################
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    global intline
    intline = t.lexer.lineno;

###########################################################################
#   t_error
#   Error al procesar los tokens, token no identificado entre los que
#   se enlistan arriba
###########################################################################
def t_error(t):
    print 'Illegal character ' + str(t)
    t.lexer.skip(1)

# Crear el scanner
lex.lex()
