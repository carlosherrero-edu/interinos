import csv

def escribirEnCsv(fichero,cabecera,datos):
    with open(fichero,'w', newline='') as csv_file:
        escritor = csv.writer(csv_file)
        #escribimos fila de cabecera
        escritor.writerow(cabecera)
        for fila in datos:
            escritor.writerow(fila)
#fin del método

