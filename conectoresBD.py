# -*- coding: utf-8 -*-
import sqlite3 as sql

"""
Método que obtiene un manejador de la conexion con la base de datos
"""
def conectar(datos_conn):
    try:
        
        conn = sql.connect(datos_conn)
        return conn
    except Exception:
        return None
#fin de la función de conexión

"""
Método que libera y cierra el manejador de conexión con la base de datos
"""
def desconectar(conn):
    try:
        conn.close()
    except:
        print('No se pudo cerrar la conexión')
# fin de la función de desconexión

"""
Método que establece y abre un cursor para manipular la base de datos
"""
def abreCursor(conn):
    try:
        cursor=conn.cursor()
        return cursor
    except:
        return None
#fin de la función de apertura de cursor

"""
Método que libera y cierra un cursor previamente abierto
"""
def cierraCursor(cursor):
    try:
        cursor.close()
    except:
        print('No se pudo cerrar el cursor')
#fin de la función de cierre del cursor