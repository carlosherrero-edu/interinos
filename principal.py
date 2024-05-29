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
    #fin del método abrirFichero

def escribirLogInicioEjecucion(fichLog):
    fichLog.write('\n')
    fichLog.write('-'*80+'\n'+'-'*80)
    fichLog.write('\nPROCEDIMIENTO DE ADJUDICACIÓN DE VACANTES DE INTERINOS\n')
    fichLog.write('-'*40)
    fichLog.write('\nInicio del procedimiento  en: '+ str(datetime.now()))

def escribirLogFinEjecucion(fichLog, iteraciones, asignadas, libres):
    fichLog.write('\n')
    fichLog.write('-'*80)
    fichLog.write('\n'+ '**Se han completado {} iteraciones'.format(iteraciones))
    fichLog.write('\nSe han adjudicado en total {0:d} vacantes \n'.format(asignadas))
    fichLog.write('\nHan quedado desiertas {0:d} vacantes \n'.format(libres))
    fichLog.write('\nFinalización del procedimiento  en: '+ str(datetime.now()))
    fichLog.write('-'*80+'\n'+'-'*80)

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

def cargarDatosInicio(conexion,fichLog):
    #ejecutamos el método para vaciar las tablas
    cargarDatosPrueba.vaciarTablas(conexion,fichLog)

    #a continuación ejecutamos los métodos para ir poblando cada tabla con los datos de prueba
    cargarDatosPrueba.cargarEspecialidades(conexion,fichLog)
    cargarDatosPrueba.cargarCentros(conexion,fichLog)
    cargarDatosPrueba.cargarCandidatos(conexion,fichLog)
    cargarDatosPrueba.cargarBaremados(conexion,fichLog)
    cargarDatosPrueba.cargarPeticiones(conexion,fichLog)
    cargarDatosPrueba.cargarVacantes(conexion,fichLog)


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
escribirLogInicioEjecucion (fichLog)
#carga de las tablas con los datos de los ficheros CSV 
cargarDatosInicio(conexion,fichLog)
  
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
    adjudicacionesIteracion, numMejoras= recorrerEspecialidades(conexion,listaEspecialidades)
    vacantesAsignadas+=(adjudicacionesIteracion-numMejoras)
    #hay que verificar si siguen quedando vacantes libres
    vacantesLibres=contarVacantesLibres(conexion)
    escribirFinIteracion(fichLog,numIteraciones,adjudicacionesIteracion, numMejoras,vacantesLibres)

    if numMejoras>0:
        hayMejoras=True  #lo que obliga a una repetición del bucle
#fin del bucle while principal

escribirLogFinEjecucion(fichLog, numIteraciones,vacantesAsignadas, vacantesIniciales-vacantesAsignadas)
#escribir los ficheros de vacantes asignadas y vacantes desiertas
escribirPuestosAsignados(conexion)
escribirPuestosDesiertos(conexion)
#cerramos la conexión y el fichero de log
fichLog.close()
desconectar(conexion)