import sqlite3 as sql

def conectar(datos_conn):
    try:
        
        conn = sql.connect(datos_conn)
        return conn
    except Exception:
        return None
#fin de la función de conexión
    
def desconectar(conn):
    try:
        conn.close()
    except:
        print('No se pudo cerrar la conexión')
# fin de la función de desconexión

def abreCursor(conn):
    try:
        cursor=conn.cursor()
        return cursor
    except:
        return None
#fin de la función de apertura de cursor


def cierraCursor(cursor):
    try:
        cursor.close()
    except:
        print('No se pudo cerrar el cursor')
#fin de la función de cierre del cursor

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


def contarVacantesEspecialidad(conexion,especialidad):
    #método para contar cuántas vacantes hay aún libres en una especialidad dada
    try:
        
        cursor=abreCursor(conexion)
        consulta= '''select count(*) from Vacante 
                        where codEspecialidad=? and adjudicatario is null'''
        cursor.execute(consulta,(especialidad,))
        vacantes=cursor.fetchone()[0]
        cierraCursor(cursor)
        return vacantes
        
    except:
        return None
    #fin del método

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

def adjudicarPlaza(conexion,documento, especialidad, codCentro, ordenVacante):
     #método para adjudicar una vacante. Implica actualizar dos tablas
     ocuparVacante(conexion,documento,especialidad,codCentro,ordenVacante)
     ocuparPeticion (conexion,documento,especialidad,codCentro)
    
    #fin del método

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


def liberarPlazaAdjudicada(conexion,plazaAdjudicada):
    #método para adjudicar una vacante. Implica actualizar dos tablas
    #estructura de plazaAdjudicada: documento-ordenPeticion-codCentro-codEspecialidad-estado
     liberarVacante(conexion,plazaAdjudicada[0])
     liberarPeticion (conexion,plazaAdjudicada[0], plazaAdjudicada[1])


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
    








