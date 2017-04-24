# -*- coding: utf-8 -*-
from Parser import *
import sys, os, Scanner

if __name__ == '__main__':

    text = raw_input('Inserte el nombre del archivo: ')
    if (text):
        # Obtiene el archivo
        file = text
        try:
            f = open('programas/' + file,'r')
            data = f.read()
            f.close()
            # Si concluye la revision exitosamente
            if (parserUsh.parse(data, tracking=True) == 'Correcto'):
                print ('Lexico y sintaxis correcto');
                execfile('maquina2.py')
                print('Ejecucion terminada.')
        except EOFError:
            print(EOFError)
    else:
        print('Archivo no existe')
