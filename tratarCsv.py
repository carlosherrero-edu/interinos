# -*- coding: utf-8 -*-
import csv

"""
Método que escribe varios registros en un fichero en formato CSV

Parámetros
----------
fichero - ruta relativa y nombre del fichero CSV de destino
cabecera - lista con los nombres de los campos, separados por comas
datos- lista de tuplas. Cada tupla es una fila de valores CSV
REtorno
-------
NO devuelve retorno
"""
def escribirEnCsv(fichero,cabecera,datos):
    with open(fichero,'w', newline='',encoding='utf-8') as csv_file:
        escritor = csv.writer(csv_file)
        #escribimos fila de cabecera
        escritor.writerow(cabecera)
        for fila in datos:
            escritor.writerow(fila)
#fin del método

"""
Método que lee secuencialmente la información de un fichero CSV

Parámetros
----------
fichero - ruta relativa y nombre del fichero CSV de destino

REtorno
-------
Lista compuesta: cada elemento es una lista de los valores de una fila del fichero
"""
def leerDatosInicio(fichero):
    with open(fichero,'r+', newline='',encoding='utf-8') as csv_file:
        lector = csv.reader(csv_file)
        #leemos secuencialmente cada fila y generamos una lista con todas las filas leídas
        return [fila for fila in lector]
#fin del método

