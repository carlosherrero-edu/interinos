from accesoDatos import *


def recorrerEspecialidades(conexion,listaEspecialidades):
    #iniciamos contador de adjudicaciones
    adjudicacionesIteracion=0
    numMejoras=0
    #vamos recorriendo las especialidades
    for registro in listaEspecialidades:
        especialidad=registro[0] #el código de especialidad es la posición 0 de la tupla
        adjudicacionesEsp, mejorasEsp=recorrerCandidatosEspecialidad(conexion,especialidad)
        
        print('Se han adjudicado {0:d} vacantes en la Especialidad {1:7s} \n'
              .format(adjudicacionesEsp,especialidad))
        adjudicacionesIteracion+=adjudicacionesEsp
        numMejoras+=mejorasEsp

    #fin del bucle for sobre las especialidades
    return adjudicacionesIteracion,numMejoras

 #fin del método recorrerEspecialidades

def recorrerCandidatosEspecialidad(conexion,especialidad):
    adjudicacionesEsp=0
    mejorasEsp=0
    #comprobamos si hay vacantes libres de esta especialidad
    if (contarVacantesEspecialidad(conexion,especialidad)>0):
        #si quedan aún vacantes libres, leemos los candidatos de la especialidad
        #recuperamos la lista ordenada de candidatos de la especialidad
        listaCandidatos=leerListaCandidatos(conexion,especialidad)
        print(" Especialidad :" +especialidad)
        print ("Candidatos de la especialidad:")
        print (listaCandidatos)
        for candidato in listaCandidatos:
                #estructura de la tupla candidato: orden, documento
                documento=candidato[1]
                adjudicada, mejora=estudiarPeticionesCandidato(conexion,documento, especialidad)
                adjudicacionesEsp+=adjudicada
                mejorasEsp+=mejora
            
            #fin del for sobre los candidatos
    #fin del condicional
    return adjudicacionesEsp, mejorasEsp

#fin método recorrerCandidatosEspecialidad

def estudiarPeticionesCandidato(conexion, documento,especialidad):
    adjudicada, mejora=0,0
    #recuperamos las peticiones de ese candidato en la especialidad          
    listaPeticiones=buscarPeticionesCandidato(conexion,documento,especialidad)
    print ("Peticiones del candidato {0:s} en la especialidad {1:s}".format(documento,especialidad))
    print(listaPeticiones)
    #comprobamos si el candidato ha efectuado peticiones por esa especialidad
    if listaPeticiones is not None:
        #recuperamos también la plaza que ya tiene adjudicada, si es el caso
        plazaAdjudicada=buscarPLazaAdjudicada(conexion,documento)
        if plazaAdjudicada is not None:
            print("Plaza ya adjudicada al candidato {0:s} :".format(documento))
            #estructura de la tupla: documento, ordenPeticion,codCentro,codEspecialidad, estado
            
        #recorremos mientras no se le adjudique una plaza a ese candidato
        for peticion in listaPeticiones:
            adjudicada,mejora= analizarPeticion(conexion,peticion,plazaAdjudicada)
            #en el momento en que se adjudique una plaza, abandonamos el bucle
            if adjudicada !=0:
                break                  
        #fin del for sobre la lista de Peticiones
    #fin del condicional
    return adjudicada, mejora

# fin del método estudiarPeticionesCandidato

def analizarPeticion(conexion,peticion,plazaAdjudicada):
    #estructura de peticion: documento, ordenPeticion,codCentro,codEspecialidad, estado
    adjudicada, mejora=0,0
    #hay que ver si existe aún vacante en la plaza que pide
    documento=peticion[0]
    codCentro=peticion[2]
    codEspecialidad=peticion[3]
    ordenVacante=buscarVacanteLibre(conexion,codCentro,codEspecialidad)
    if (ordenVacante is not None):
        #si hay vacante, hay que comprobar si mejora la plaza que pueda tener adjudicada
        if plazaAdjudicada is None:
            #no tiene adjudicada plaza, por lo que se le adjudica este puesto
            adjudicarPlaza(conexion,documento,codEspecialidad,codCentro,ordenVacante)
            adjudicada=1
        else:
            #tenemos que ver si esta vacante mejora su adjudicación previa
            if peticion[1]<plazaAdjudicada[1]:
                #esta nueva plaza mejora la adjudicación previa. Por tanto
                liberarPlazaAdjudicada(conexion,plazaAdjudicada)
                adjudicarPlaza(conexion,documento,codEspecialidad,codCentro,ordenVacante)
                adjudicada=1
                 #ya hay al menos una mejora, lo que obligará a repetir el bucle
                mejora=1
 
            else:
                #si no mejora la adjudicación anterior, nohacemos nada
                None
            #fin del condicional
        #fin del condicional
    #fin del condiconal en cado de que no haya vacante libre
    return adjudicada, mejora
     
#fin del metodo analizarPeticion



