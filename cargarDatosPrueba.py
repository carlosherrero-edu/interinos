# -*- coding: utf-8 -*-
from accesoDatos import *
from conectoresBD import *
from constantes import constantes
from tratarCsv import *
#carga de datos de prueba

"""
"""
def vaciarTablas(conexion,fichLog, fichErr):
    #método para contar cuántas vacantes hay aún libres
    try:
        cursor=abreCursor(conexion)
       
        cursor.execute("delete from Peticion")
        cursor.execute("delete from Vacante")
        cursor.execute("delete from Lista")
        cursor.execute("delete from Candidato")
        cursor.execute("delete from Especialidad")
        cursor.execute("delete from Centro")
        conexion.commit()
        fichLog.write('\nSe han vaciado correctamente todas las tablas de la base de datos')
        
   
    except Exception as error:
        fichErr.write('Se produjo el siguiente error al vaciar las tablas: '+str(error))
        conexion.rollback()
    finally:
        cierraCursor(cursor)

#fin del método

"""
"""
def cargarEspecialidades(conexion,fichLog, fichErr):
    #método para cargar las especialidades de prueba
    try:
        listaEspecialidades=leerDatosInicio(constantes['ruta_ficheros']+'/'+constantes['ficheros_inicio'][0])
        #hacemos un slicing para omitir el primer elemento de la lista, que contiene el nombre de los campos
        listaEspecialidades.pop(0)
        
        cursor=abreCursor(conexion)
        contador=0
        for registro in listaEspecialidades:
            consulta= '''insert into Especialidad (codEspecialidad,codCuerpo, nombreEspecialidad)
                        values (?,?,?)'''
            cursor.execute(consulta,registro)
            contador+=1
        #fin del recorrido
        fichLog.write('\nSe insertaron {0:d} especialidades en la tabla Especialidad \n'.format(contador))
      
        conexion.commit()
        
    except Exception as error:
        fichErr.write('Se produjo el siguiente error al insertar en Especialidad: '+str(error))
        conexion.rollback()
    finally:
        cierraCursor(cursor)

    #fin del método

"""
"""
def cargarCentros(conexion,fichLog, fichErr):
    #método para cargar los Centros docentes de prueba
    try:
        listaCentros=leerDatosInicio(constantes['ruta_ficheros']+'/'+constantes['ficheros_inicio'][1])
        #hacemos un slicing para omitir el primer elemento de la lista, que contiene el nombre de los campos
        listaCentros.pop(0)
        cursor=abreCursor(conexion)
        contador=0
        for registro in listaCentros:
            consulta= '''insert into Centro (codCentro,nombreCentro)
                        values (?,?)'''
            cursor.execute(consulta,registro)
            contador+=1
        #fin del recorrido
        fichLog.write('\nSe insertaron {0:d} centros en la tabla Centro \n'.format(contador))
        
        conexion.commit()
        
    except Exception as error:
        fichErr.write('Se produjo el siguiente error al insertar en Centro: '+str(error))
        conexion.rollback()
    finally:
        cierraCursor(cursor)

    #fin del método

"""
"""
def cargarCandidatos(conexion,fichLog,fichErr):
    #método para cargar los candidatos/interinos de prueba
    try:
        listaCandidatos=leerDatosInicio(constantes['ruta_ficheros']+'/'+constantes['ficheros_inicio'][2])
        #hacemos un slicing para omitir el primer elemento de la lista, que contiene el nombre de los campos
        listaCandidatos.pop(0)
        cursor=abreCursor(conexion)
        contador=0
        for registro in listaCandidatos:
         
            consulta= '''insert into Candidato (documento, nombreApellidos, numSolicitud)
                        values (?,?,?)'''
            cursor.execute(consulta,registro)
            
            contador+=1
        #fin del recorrido
        fichLog.write('\nSe insertaron {0:d} candidatos en la tabla Candidato \n'.format(contador))
        
        conexion.commit()
        
    except Exception as error:
        fichErr.write('Se produjo el siguiente error al insertar en Candidato: '+str(error))
        conexion.rollback()
    finally:
        cierraCursor(cursor)

#fin del método

"""
"""
def cargarVacantes(conexion,fichLog, fichErr):
    #método para cargar las vacantes de prueba
    try:
        listaVacantes=leerDatosInicio(constantes['ruta_ficheros']+'/'+constantes['ficheros_inicio'][5])
        #hacemos un slicing para omitir el primer elemento de la lista, que contiene el nombre de los campos
        listaVacantes.pop(0)
        cursor=abreCursor(conexion)
        contador=0
        for registro in listaVacantes:
            registro.pop()   #para eliminar el último campo y que se inserte siempre un nulo
            consulta= '''insert into Vacante (codCentro,codEspecialidad,orden)
                        values (?,?,?)'''
            cursor.execute(consulta,registro)
            
            contador+=1
        #fin del recorrido
        fichLog.write('\nSe insertaron {0:d} vacantes en la tabla Vacante \n'.format(contador))
        
        conexion.commit()
        
    except Exception as error:
        fichErr.write('Se produjo el siguiente error al insertar en Vacante: '+str(error))
        conexion.rollback()
    finally:
        cierraCursor(cursor)
    #fin del método

"""
"""
def cargarBaremados(conexion,fichLog, fichErr):
    #método para cargar las relaciones de candidatos baremados por especialidad
    try:
        listaBaremados=leerDatosInicio(constantes['ruta_ficheros']+'/'+constantes['ficheros_inicio'][3])
        #hacemos un slicing para omitir el primer elemento de la lista, que contiene el nombre de los campos
        listaBaremados.pop(0)
        cursor=abreCursor(conexion)
        contador=0
        for registro in listaBaremados:
            consulta= '''insert into Lista (codEspecialidad,documento,orden)
                        values (?,?,?)'''
            cursor.execute(consulta,registro)
            
            contador+=1
        #fin del recorrido
        fichLog.write('\nSe insertaron {0:d} registros de candidaturas baremadas por especialidad en la tabla Lista \n'.format(contador))
        
        conexion.commit()
        
    except Exception as error:
        fichErr.write('Se produjo el siguiente error al insertar en Lista: '+str(error))
        conexion.rollback()
    finally:
        cierraCursor(cursor)

    #fin del método

"""
"""
def cargarPeticiones(conexion,fichLog, fichErr):
    #método para cargar las peticiones de plazas que realiza cada candidato
    try:
        listaPeticiones=leerDatosInicio(constantes['ruta_ficheros']+'/'+constantes['ficheros_inicio'][4])
        #hacemos un slicing para omitir el primer elemento de la lista, que contiene el nombre de los campos
        listaPeticiones.pop(0)
        
        cursor=abreCursor(conexion)
        contador=0
        for registro in listaPeticiones:
            consulta= '''insert into Peticion (documento,ordenPeticion,codCentro,codEspecialidad,estado)
                        values (?,?,?,?,?)'''
            cursor.execute(consulta,registro)
            
            contador+=1
        #fin del recorrido
        fichLog.write('\nSe insertaron {0:d} peticiones de vacantes en la tabla Peticion \n'.format(contador))
        
        conexion.commit()
        
    except Exception as error:
        fichErr.write('Se produjo el siguiente error al insertar en Peticion: '+str(error))
        conexion.rollback()
    finally:
        cierraCursor(cursor)

#fin del método




