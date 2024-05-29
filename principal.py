from constantes import constantes
from metodosAdjudicacion import *
from datetime import datetime
import accesoDatos
import cargarDatosPrueba
import tratarCsv



def abrirFicheroLog():
    try:
        fichLog=open(constantes['nombre_fichero_log'],'a')
        return fichLog
    except:
        print('NO ha sido posible abrir el fichero de log')
    #fin del método abrirFicheroLog

def abrirFicheroErrores():
    try:
        fichErr=open(constantes['nombre_fichero_errores'],'a')
        return fichErr
    except:
        print('NO ha sido posible abrir el fichero de errores')
    #fin del método abrirFicheroErores

def escribirLogInicioEjecucion(fichLog, fichErr):
    fichLog.write('\n')
    fichLog.write('-'*80+'\n'+'-'*80)
    fichLog.write('\nPROCEDIMIENTO DE ADJUDICACIÓN DE VACANTES DE INTERINOS\n')
    fichLog.write('-'*40)
    fichLog.write('\nInicio del procedimiento  en: '+ str(datetime.now()))
    fichErr.write('\n')
    fichErr.write('-'*80+'\n'+'-'*80)
    fichErr.write('\nERRORES DETECTADOS DURANTE LA EJECUCIÓN\n')
    fichErr.write('-'*40)
    fichErr.write('\nInicio del procedimiento  en: '+ str(datetime.now()))

def escribirLogFinEjecucion(fichLog, fichErr, iteraciones, asignadas, libres):
    fichLog.write('\n')
    fichLog.write('-'*80)
    fichLog.write('\n'+ '**Se han completado {} iteraciones'.format(iteraciones))
    fichLog.write('\nSe han adjudicado en total {0:d} vacantes \n'.format(asignadas))
    fichLog.write('\nHan quedado desiertas {0:d} vacantes \n'.format(libres))
    fichLog.write('\nFinalización del procedimiento  en: '+ str(datetime.now()))
    #fichLog.write('-'*80+'\n'+'-'*80)
    fichErr.write('\n')
    fichErr.write('-'*80)
    fichErr.write('\nFinalización del procedimiento  en: '+ str(datetime.now()))

def escribirInicioIteracion(fichLog,iteracion,vacantes):
    fichLog.write('\n')
    fichLog.write('-'*40)
    fichLog.write('\n'+ '**Inicio de la iteración número {}'.format(iteracion))
    fichLog.write('\n'+ '****Vacantes disponibles al comienzo:  {}'.format(vacantes))

def escribirFinIteracion(fichLog,iteracion,adjudicadas,mejoras,vacantes):
    fichLog.write('\n')
    fichLog.write('\nFin de la iteración número {0:d} \n'.format(iteracion))
    fichLog.write('\nSe han adjudicado {0:d} vacantes \n'.format(adjudicadas))
    fichLog.write('\nSe han producido en esta iteración {0:d} mejoras en adjudicaciones \n'.format(mejoras))
    fichLog.write("\nVacantes que no se han adjducicado: " +str(vacantes))

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


def escribirPuestosAsignados(conexion):
    puestosAdjudicados=accesoDatos.consultarPuestosAdjudicados(conexion)
    if puestosAdjudicados is not None:
        cabecera=['Código','Especialidad','Código','Centro','Documento','Adjudicatario', 'Orden Lista','Preferencia']
        tratarCsv.escribirEnCsv(constantes['ruta_ficheros']+'/'+constantes['fic_asignadas'],
                                cabecera,puestosAdjudicados)
    #en caso contrario, no escribimos nada
#fin del método

def escribirPuestosDesiertos(conexion):
    puestosDesiertos=accesoDatos.consultarPuestosDesiertos(conexion)
    if puestosDesiertos is not None:
        cabecera=['Código','Especialidad','Código','Centro']
        tratarCsv.escribirEnCsv(constantes['ruta_ficheros']+'/'+constantes['fic_desiertas'],
                                cabecera,puestosDesiertos)
    #en caso contrario, no escribimos nada
#fin del método


#inicialización y apertura de la base de datos
conexion=conectar(constantes['ruta_db']+'/'+constantes['nombre_db'])
#inicialización y apertura del fichero de log
fichLog=abrirFicheroLog()
#inicialización y apertura del fichero de errores
fichErr=abrirFicheroErrores()
escribirLogInicioEjecucion (fichLog, fichErr)
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
    escribirInicioIteracion(fichLog,numIteraciones,vacantesLibres)

    #primero cambiamos la variable hayMejoras
    hayMejoras=False
    #procedimiento de recorrido por especialidades para adjudicar vacantes
    adjudicacionesIteracion, numMejoras= recorrerEspecialidades(conexion,fichLog,fichErr,listaEspecialidades)
    vacantesAsignadas+=(adjudicacionesIteracion-numMejoras)
    #hay que verificar si siguen quedando vacantes libres
    vacantesLibres=contarVacantesLibres(conexion)
    escribirFinIteracion(fichLog,numIteraciones,adjudicacionesIteracion, numMejoras,vacantesLibres)

    if numMejoras>0:
        hayMejoras=True  #lo que obliga a una repetición del bucle
#fin del bucle while principal

#escribir los ficheros de vacantes asignadas y vacantes desiertas
escribirPuestosAsignados(conexion)
escribirPuestosDesiertos(conexion)

escribirLogFinEjecucion(fichLog, fichErr, numIteraciones,vacantesAsignadas, vacantesIniciales-vacantesAsignadas)

#cerramos la conexión y el fichero de log y de errores
fichLog.close()
fichErr.close()
desconectar(conexion)
print("***SE ha ejecutado el programa. Compruebe los ficheros de salida y de errores***")