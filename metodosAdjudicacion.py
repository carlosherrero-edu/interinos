# -*- coding: utf-8 -*-
from accesoDatos import *
from escribirBD import *

"""
    Método para recorrer todas las especialidades que deben adjudicarse e ir asignando vacantes de cada especialidad
    Devuelve el número total de adjudicaciones y de mejoras en puestos que se producen durante una iteración
"""
def recorrerEspecialidades(conexion,fichLog,fichErr,listaEspecialidades):
    
    #iniciamos contador de adjudicaciones
    adjudicacionesIteracion=0
    numMejoras=0
    #vamos recorriendo las especialidades
    for registro in listaEspecialidades:
        especialidad=registro[0] #el código de especialidad es la posición 0 de la tupla
        adjudicacionesEsp, mejorasEsp=recorrerCandidatosEspecialidad(conexion,fichLog,fichErr,especialidad)
        
        fichLog.write('\n *** Se han adjudicado {0:d} vacantes en la Especialidad {1:7s} \n'
              .format(adjudicacionesEsp,especialidad))
        adjudicacionesIteracion+=adjudicacionesEsp
        numMejoras+=mejorasEsp

    #fin del bucle for sobre las especialidades
    return adjudicacionesIteracion,numMejoras

 #fin del método recorrerEspecialidades

"""
     Método que para cada especialidad, comprueba si quedan vacantes libres. 
     En caso afirmativo, recupera los candidatos de la lista de esa especialidad y examina sus peticiones
     Devuelve el número de plazas adjudicadas y posibles mejoras en esa especialidad
"""
def recorrerCandidatosEspecialidad(conexion,fichLog,fichErr,especialidad):
    
    adjudicacionesEsp=0
    mejorasEsp=0
    #comprobamos si hay vacantes libres de esta especialidad
    if (contarVacantesEspecialidad(conexion,especialidad)>0):
        #si quedan aún vacantes libres, leemos los candidatos de la especialidad
        #recuperamos la lista ordenada de candidatos de la especialidad
        listaCandidatos=leerListaCandidatos(conexion,especialidad)
       
        for candidato in listaCandidatos:
                #estructura de la tupla candidato: orden, documento
                documento=candidato[1]
                #método para estudiar las peticiones del candidato en esa especialidad
                adjudicada, mejora=estudiarPeticionesCandidato(conexion,fichLog,fichErr,documento, especialidad)
                adjudicacionesEsp+=adjudicada
                mejorasEsp+=mejora
            
            #fin del for sobre los candidatos
    #fin del condicional
    return adjudicacionesEsp, mejorasEsp

#fin método recorrerCandidatosEspecialidad


"""
    Método que recupera las peticiones realizadas por un candidato en una especialidad, según su orden de prioridad
    Valores que puede devolver:
    0-0: No se le adjudicó ninguna plaza
    1-0: Se le adjudica un puesto, pero no mejora la adjudicación anterior para el mismo candiado
    1-1: Se le adjudicón un puesto, y además ese puesto mejora la adjudicación anterior para el mismo candidato
"""
def estudiarPeticionesCandidato(conexion, fichLog,fichErr,documento,especialidad):
    
    adjudicada, mejora=0,0
    #recuperamos las peticiones de ese candidato en la especialidad          
    listaPeticiones=buscarPeticionesCandidato(conexion,documento,especialidad)
    
    #comprobamos si el candidato ha efectuado peticiones por esa especialidad
    if listaPeticiones is not None:
        #recuperamos también la plaza que ya tiene adjudicada, si es el caso. En caso contrario, el método devolverá NOne
        plazaAdjudicada=buscarPLazaAdjudicada(conexion,documento)
        #estructura de la tupla: documento, ordenPeticion,codCentro,codEspecialidad, estado
        
        #recorremos mientras no se le adjudique una plaza a ese candidato
        for peticion in listaPeticiones:
            adjudicada,mejora= analizarPeticion(conexion,fichLog,fichErr,peticion,plazaAdjudicada)
            #en el momento en que se adjudique una plaza, abandonamos el bucle
            if adjudicada !=0:
                break                  
        #fin del for sobre la lista de Peticiones
    #fin del condicional
    return adjudicada, mejora

# fin del método estudiarPeticionesCandidato

"""
Método que estudia la petición de un puesto de un candidato, determina si hay puesto vacante en el centro pedido
    Si hay puesto vacante y el candidato no había obtenido plaza, se lo adjudica
    Si ya había obtenido plaza, se lo adjudicará siempre que dicho puesto lo hubiese pedido antes que el que ya tenía
    En ese caso, se contabiliza como mejora en la adjuciación
    Valores que puede devolver:
    0-0: No se le adjudicó ninguna plaza
    1-0: Se le adjudica un puesto, pero no mejora la adjudicación anterior para el mismo candiado
    1-1: Se le adjudicón un puesto, y además ese puesto mejora la adjudicación anterior para el mismo candidato
"""
def analizarPeticion(conexion,fichLog,fichErr,peticion,plazaAdjudicada):
   
    #estructura de peticion: documento, ordenPeticion,codCentro,codEspecialidad, estado
    adjudicada, mejora=0,0
    #hay que ver si existe aún vacante en la plaza que pide
    documento=peticion[0]
    codCentro=peticion[2]
    codEspecialidad=peticion[3]
    #buscamos la primera vacante disponible en ese Centro y especialidad
    ordenVacante=buscarVacanteLibre(conexion,codCentro,codEspecialidad)
    if (ordenVacante is not None):
        #si hay vacante, hay que comprobar si mejora la plaza que pueda tener adjudicada
        if plazaAdjudicada is None:
            #no tiene adjudicada plaza, por lo que se le adjudica este puesto
            adjudicarPlaza(conexion,fichLog,fichErr,documento,codEspecialidad,codCentro,ordenVacante)
            adjudicada=1
        else:
            #tenemos que ver si esta vacante mejora su adjudicación previa
            if peticion[1]<plazaAdjudicada[1]:
                #esta nueva plaza mejora la adjudicación previa, pues el orden de prelación es menor. Por tanto:
                #1. Anulamos la adjudicación que se le realizó, liberando esa plaza
                liberarPlazaAdjudicada(conexion,fichLog,fichErr,plazaAdjudicada)
                #2. Le adjudicamos la nueva plaza, que había pedido antes de la que ya se le adjudicó
                adjudicarPlaza(conexion,fichLog,fichErr,documento,codEspecialidad,codCentro,ordenVacante)
                adjudicada=1
                 #ya hay al menos una mejora, lo que obligará a repetir el bucle
                mejora=1
 
            else:
                #si no mejora la adjudicación anterior, no hacemos nada
                pass
            #fin del condicional
        #fin del condicional
    #fin del condicoinal en cado de que no haya vacante libre
    return adjudicada, mejora
     
#fin del metodo analizarPeticion



