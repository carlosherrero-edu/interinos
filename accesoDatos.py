# -*- coding: utf-8 -*-
from conectoresBD import *

"""
"""
def contarVacantesLibres(conexion):
    #método para contar cuántas vacantes hay aún libres entre todas las especialidades
    try:
        
        cursor=abreCursor(conexion)
        consulta= '''select count(*) from Vacante where adjudicatario is null'''
        cursor.execute(consulta)
        vacantes=cursor.fetchone()[0]
        cierraCursor(cursor)
        return vacantes
        
    except:
        return None
    #fin del método

"""
"""
def contarVacantesEspecialidad(conexion,especialidad):
    #método para contar cuántas vacantes hay aún libres en una especialidad dada
    try:
        
        cursor=abreCursor(conexion)
        consulta= '''select count(*) from Vacante 
                        where codEspecialidad=? and adjudicatario is null'''
        cursor.execute(consulta,(especialidad,))
        vacantes=cursor.fetchone()[0]           #sólo nos interesa el primer registro
        cierraCursor(cursor)
        return vacantes
        
    except:
        return None
    #fin del método

"""
"""
def leerListaEspecialidades(conexion):
    #método para devolver la lista de especialidades ordenadas
    try:
        cursor=abreCursor(conexion)
        consulta= '''select codEspecialidad from Especialidad order by 1'''
        cursor.execute(consulta)
        especialidades=cursor.fetchall()
        cierraCursor(cursor)
        return especialidades
    except:
        return None
    #fin del método

"""
"""
def leerListaCandidatos(conexion,especialidad):
    #método para leer la relación ordenada de candidatos por una especialidad
    try:
        cursor=abreCursor(conexion)
        consulta= '''select orden,documento from Lista
                        where codEspecialidad=?
                        order by 1'''
        cursor.execute(consulta,(especialidad,))
        listaCandidatos=cursor.fetchall()
        cierraCursor(cursor)
        return listaCandidatos
    except:
        return None
    #fin del método

"""
"""
def buscarVacanteLibre(conexion,centro,especialidad):
    #método para recuperar la primera vacante que quede libre en un centro y especialidad
    try:
        cursor=abreCursor(conexion)
        consulta= '''select orden
                        from Vacante
                        where codCentro=? and codEspecialidad=? and adjudicatario is null
                        order by orden'''
        cursor.execute(consulta,(centro,especialidad,))
        #si la hay, sólo nos interesa recuperar la primera vacante libre
        posicion=cursor.fetchone()[0]
        cierraCursor(cursor)
        return posicion
    except:
        return None
    #fin del método

"""
"""
def buscarPeticionesCandidato(conexion,candidato, especialidad):
    #recupera las peticiones ordenadas de un candidato en una especialidad
    try:
        cursor=abreCursor(conexion)
        consulta= '''select *
                        from Peticion
                        where documento=? and codEspecialidad=? 
                        order by ordenPeticion'''
        cursor.execute(consulta,(candidato,especialidad,))
        peticiones=cursor.fetchall()
        cierraCursor(cursor)
        return peticiones
    except:
        return None
    #fin del método

"""
"""
def buscarPLazaAdjudicada(conexion,candidato):
     #método para recuperar el puesto que se ha adjudicado a un candidato, si es el caso
    try:
        cursor=abreCursor(conexion)
        consulta= '''select *
                        from Peticion
                        where documento=? and estado=1'''
        cursor.execute(consulta,(candidato,))
        #si la hay, será una sola plaza
        adjudicada=cursor.fetchone()
        cierraCursor(cursor)
        return adjudicada
    except:
        return None
    #fin del método

"""
"""
def consultarPuestosAdjudicados(conexion):
    #método para recuperar una lista de todos los puestos adjudicados
    consulta='''
                SELECT e.codEspecialidad, e.nombreEspecialidad, t.codCentro, t.nombreCentro, c.documento as "Adjudicatario", 
            c.nombreApellidos, l.orden as "Posición", p.ordenPeticion as Preferencia
            from vacante v inner join candidato c on v.adjudicatario=c.documento
            inner join centro t on v.codCentro=t.codCentro
            inner join Especialidad e on v.codEspecialidad=e.codEspecialidad
            inner join Lista l on v.codEspecialidad=l.codEspecialidad and v.adjudicatario=l.documento
            inner join Peticion p on v.adjudicatario=p.documento and v.codEspecialidad=p.codEspecialidad and v.codCentro=p.codCentro
            where v.adjudicatario is not null
            order by 1,3
            '''
    try:
        cursor=abreCursor(conexion)
     
        cursor.execute(consulta)
        #recuperamos la lista de todos los puestos adjudicados
        puestos=cursor.fetchall()
        cierraCursor(cursor)
        return puestos
    except:
        return None
    #fin del método

"""
"""
def consultarPuestosDesiertos(conexion):
    #método para recuperar una lista de todos los puestos no adjudicados
    consulta='''
             SELECT v.codEspecialidad, e.nombreEspecialidad, v.codCentro, t.nombreCentro
                from vacante v inner join centro t on v.codCentro=t.codCentro
                inner join Especialidad e on v.codEspecialidad=e.codEspecialidad
                where v.adjudicatario is null
            order by 1,3
            '''
    try:
        cursor=abreCursor(conexion)
     
        cursor.execute(consulta)
        #recuperamos la lista de todos los puestos adjudicados
        puestosDesiertos=cursor.fetchall()
        cierraCursor(cursor)
        return puestosDesiertos
    except:
        return None
    #fin del método
    








