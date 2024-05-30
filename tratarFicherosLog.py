# -*- coding: utf-8 -*-
from constantes import constantes
from datetime import datetime
import accesoDatos
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
    dt=datetime.now()  #establecemos el sello de tiempo actual
    tsInicio='\nInicio del procedimiento  en {:{dfmt} {tfmt}} '.format(dt, dfmt='%d-%B-%Y', tfmt='%I:%M %p')

    fichLog.write(tsInicio)
    fichErr.write('\n')
    fichErr.write('-'*80+'\n'+'-'*80)
    fichErr.write('\nERRORES DETECTADOS DURANTE LA EJECUCIÓN\n')
    fichErr.write('-'*40)
    fichErr.write(tsInicio)

def escribirLogFinEjecucion(fichLog, fichErr, iteraciones, asignadas, libres):
    fichLog.write('\n')
    fichLog.write('-'*80)
    fichLog.write('\n'+ '**Se han completado {} iteraciones'.format(iteraciones))
    fichLog.write('\nSe han adjudicado en total {0:d} vacantes \n'.format(asignadas))
    fichLog.write('\nHan quedado desiertas {0:d} vacantes \n'.format(libres))
    dt=datetime.now()  #establecemos el sello de tiempo en que finaliza la ejecución
    tsFin='\nFin del procedimiento  en {:{dfmt} {tfmt}} '.format(dt, dfmt='%d-%B-%Y', tfmt='%I:%M %p')

    fichLog.write(tsFin)
    #fichLog.write('-'*80+'\n'+'-'*80)
    fichErr.write('\n')
    fichErr.write('-'*80)
    fichErr.write(tsFin)

def escribirInicioIteracion(fichLog,iteracion,vacantes):
    fichLog.write('\n')
    fichLog.write('-'*40)
    fichLog.write('\n'+ '**Inicio de la iteración número {}'.format(iteracion))
    fichLog.write('\n'+ '****Vacantes disponibles al comienzo:  {}'.format(vacantes))
#fin del método

def escribirFinIteracion(fichLog,iteracion,adjudicadas,mejoras,vacantes):
    fichLog.write('\n')
    fichLog.write('\nFin de la iteración número {0:d} \n'.format(iteracion))
    fichLog.write('\nSe han adjudicado {0:d} vacantes \n'.format(adjudicadas))
    fichLog.write('\nSe han producido en esta iteración {0:d} mejoras en adjudicaciones \n'.format(mejoras))
    fichLog.write("\nVacantes que no se han adjducicado: " +str(vacantes))
#fin del método


def escribirPuestosAsignados(conexion):
    puestosAdjudicados=accesoDatos.consultarPuestosAdjudicados(conexion)
    if puestosAdjudicados is not None:
        cabecera=['Código','Especialidad','Código','Centro','Documento','Adjudicatario', 'Orden Lista','Preferencia']
        tratarCsv.escribirEnCsv(constantes['ruta_resultados']+'/'+constantes['fic_asignadas'],
                                cabecera,puestosAdjudicados)
    #en caso contrario, no escribimos nada
    else:
        pass

#fin del método

def escribirPuestosDesiertos(conexion):
    puestosDesiertos=accesoDatos.consultarPuestosDesiertos(conexion)
    if puestosDesiertos is not None:
        cabecera=['Código','Especialidad','Código','Centro']
        tratarCsv.escribirEnCsv(constantes['ruta_resultados']+'/'+constantes['fic_desiertas'],
                                cabecera,puestosDesiertos)
    #en caso contrario, no escribimos nada
    else:
        pass
#fin del método



