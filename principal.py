# -*- coding: utf-8 -*-
from constantes import constantes
from metodosAdjudicacion import *
import cargarDatosPrueba
import tratarFicherosLog

"""
Método para la carga de los datos de inicio en la base de datos

"""
def cargarDatosInicio(conexion,fichLog, fichErr):
    #ejecutamos el método para vaciar las tablas
    cargarDatosPrueba.vaciarTablas(conexion,fichLog, fichErr)

    #a continuación ejecutamos los métodos para ir poblando cada tabla con los datos de prueba
    cargarDatosPrueba.cargarEspecialidades(conexion,fichLog, fichErr)
    cargarDatosPrueba.cargarCentros(conexion,fichLog, fichErr)
    cargarDatosPrueba.cargarCandidatos(conexion,fichLog, fichErr)
    cargarDatosPrueba.cargarBaremados(conexion,fichLog, fichErr)
    cargarDatosPrueba.cargarPeticiones(conexion,fichLog, fichErr)
    cargarDatosPrueba.cargarVacantes(conexion,fichLog, fichErr)


#inicialización y apertura de la base de datos
conexion=conectar(constantes['ruta_db']+'/'+constantes['nombre_db'])
#inicialización y apertura del fichero de log
fichLog=tratarFicherosLog.abrirFicheroLog()
#inicialización y apertura del fichero de errores
fichErr=tratarFicherosLog.abrirFicheroErrores()
tratarFicherosLog.escribirLogInicioEjecucion (fichLog, fichErr)
#carga de las tablas con los datos de los ficheros CSV 
cargarDatosInicio(conexion,fichLog, fichErr)
  
#inicialización de variables para la primera iteración
numIteraciones=0
vacantesIniciales=vacantesLibres=contarVacantesLibres(conexion)
vacantesAsignadas=0
hayMejoras=True
listaEspecialidades=leerListaEspecialidades(conexion)    

while(vacantesLibres>0 and hayMejoras):
    numIteraciones+=1
    tratarFicherosLog.escribirInicioIteracion(fichLog,numIteraciones,vacantesLibres)

    #primero cambiamos la variable hayMejoras
    hayMejoras=False
    #procedimiento de recorrido por especialidades para adjudicar vacantes
    adjudicacionesIteracion, numMejoras= recorrerEspecialidades(conexion,fichLog,fichErr,listaEspecialidades)
    vacantesAsignadas+=(adjudicacionesIteracion-numMejoras)
    #hay que verificar si siguen quedando vacantes libres
    vacantesLibres=contarVacantesLibres(conexion)
    tratarFicherosLog.escribirFinIteracion(fichLog,numIteraciones,adjudicacionesIteracion, numMejoras,vacantesLibres)

    if numMejoras>0:
        hayMejoras=True  #lo que obliga a una repetición del bucle
#fin del bucle while principal

#escribir los ficheros de vacantes asignadas y vacantes desiertas
tratarFicherosLog.escribirPuestosAsignados(conexion)
tratarFicherosLog.escribirPuestosDesiertos(conexion)

tratarFicherosLog.escribirLogFinEjecucion(fichLog, fichErr, numIteraciones,vacantesAsignadas, vacantesIniciales-vacantesAsignadas)


#cerramos la conexión y el fichero de log y de errores
fichLog.close()
fichErr.close()
desconectar(conexion)
print('\n'+"*"*80)
print("\n\t\t *Vacantes iniciales :  {0:d}".format(vacantesIniciales))
print("\n\t\t *Vacantes adjudicadas :  {0:d}".format(vacantesAsignadas))
print("\n\t\t *Número de iteraciones :  {0:d}".format(numIteraciones))
tecla=input("\n\t\t * Pulse cualquier tecla para finalizar ___")
print("***Finalización del programa. Compruebe los ficheros de salida y de errores***")
      
