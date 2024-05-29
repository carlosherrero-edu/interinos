import csv

def escribirEnCsv(fichero,cabecera,datos):
    with open(fichero,'w', newline='') as csv_file:
        escritor = csv.writer(csv_file)
        #escribimos fila de cabecera
        escritor.writerow(cabecera)
        for fila in datos:
            escritor.writerow(fila)
#fin del método


def leerDatosInicio(fichero):
    with open(fichero,'r+', newline='') as csv_file:
        lector = csv.reader(csv_file)
        #leemos secuencialmente cada fila y generamos una lista con todas las filas leídas
        return [fila for fila in lector]
#fin del método

