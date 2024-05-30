# -*- coding: utf-8 -*-
from conectoresBD import *
"""
"""
def adjudicarPlaza(conexion,fichLog,fichErr,documento, especialidad, codCentro, ordenVacante):
     #método para adjudicar una vacante. Implica actualizar dos tablas, Vacante y Peticion
     try:
        ocuparVacante(conexion,documento,especialidad,codCentro,ordenVacante)
        ocuparPeticion (conexion,documento,especialidad,codCentro)
        fichLog.write("\n *** Se adjudica vacante en la Especialidad {0:s} y Centro {1:s} al Candidato {2:s}"
                    .format(especialidad, codCentro, documento))
     except Exception as error:
         fichErr.write("\n *** Se aborta la adjudicación de  vacante en la Especialidad {0:s} y Centro {1:s} al Candidato {2:s} por el siguiente error: \t{3:s}"
                      .format(especialidad, codCentro, documento, str(error)))
     
#fin del método

"""
"""
def ocuparVacante(conexion,documento,especialidad,codCentro,ordenVacante):
    #método para adjudicar una vacante y marcarla como ocupada
    try:
        cursor=abreCursor(conexion)
        consulta= '''update Vacante
                    set adjudicatario=?
                    where codCentro=? and codEspecialidad=? and orden=?'''
        cursor.execute(consulta,(documento,codCentro,especialidad,ordenVacante,))
        #si no hay errores, confirmamos
        conexion.commit()
    except:
        #si hay errores,abortamos la transacción
        conexion.rollback()
    finally:
        cierraCursor(cursor)
    

#fin del método
"""
"""
def ocuparPeticion(conexion,documento,especialidad,codCentro):
    #método para marcar una petición como adjudicada
    try:
        cursor=abreCursor(conexion)
        consulta= '''update Peticion
                    set estado=1
                    where documento=? and codCentro=? and codEspecialidad=?'''
        cursor.execute(consulta,(documento,codCentro,especialidad,))
        #si no hay errores, confirmamos
        conexion.commit()
    except:
        #si hay errores,abortamos la transacción
        conexion.rollback()
    finally:
        cierraCursor(cursor)

#fin del método

"""
"""
def liberarPlazaAdjudicada(conexion, fichLog,fichErr,plazaAdjudicada):
    #método para adjudicar una vacante. Implica actualizar dos tablas
    #estructura de plazaAdjudicada: documento-ordenPeticion-codCentro-codEspecialidad-estado
    try:
        liberarVacante(conexion,plazaAdjudicada[0])
        liberarPeticion (conexion,plazaAdjudicada[0], plazaAdjudicada[1])
        fichLog.write("\n *** Se libera la vacante que se adjudicó en  la Especialidad {0:s} y Centro {1:s} al Candidato {2:s}"
                    .format(plazaAdjudicada[3], plazaAdjudicada[2], plazaAdjudicada[0]))
    except Exception as error:
        fichErr.write("\n *** Se produjo un error al intentar liberar la vacante que se adjudicó en  la Especialidad {0:s} y Centro {1:s} al Candidato {2:s}:\t {3:s}"
                    .format(plazaAdjudicada[3], plazaAdjudicada[2], plazaAdjudicada[0], str(error)))
#fin del método liberarPlazaAdjudicada

"""
"""
def liberarVacante(conexion,documento):
    #método para marcar una vacante como no adjudicada, disponible
    try:
        cursor=abreCursor(conexion)
        consulta= '''update Vacante
                    set adjudicatario=null
                    where   adjudicatario=?'''
        cursor.execute(consulta,(documento,))
        #si no hay errores, confirmamos
        conexion.commit()
    except:
        #si hay errores,abortamos la transacción
        conexion.rollback()
    finally:
        cierraCursor(cursor)

#fin del método

"""
"""
def liberarPeticion(conexion,documento, preferencia):
    #método para marcar una vacante como no adjudicada, disponible
    try:
        cursor=abreCursor(conexion)
        consulta= '''update Peticion
                    set estado=0
                    where   documento=? and ordenPeticion=?'''
        cursor.execute(consulta,(documento,preferencia,))
        #si no hay errores, confirmamos
        conexion.commit()
    except:
        #si hay errores,abortamos la transacción
        conexion.rollback()
    finally:
        cierraCursor(cursor)

#fin del método