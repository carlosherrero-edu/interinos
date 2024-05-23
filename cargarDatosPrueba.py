from accesoDatos import *
from constantes import constantes
#carga de datos de prueba

conexion=conectar(constantes['ruta_db']+'/'+constantes['nombre_db'])



def vaciarTablas():
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
        print('Se han vaciado con éxito todas las tablas')
   
    except:
        print('Se produjo un error al vaciar las tablas')
        conexion.rollback()
    finally:
        cierraCursor(cursor)

#fin del método


def cargarEspecialidades(listaEspecialidades):
    #método para cargar las especialidades de prueba
    try:
        
        cursor=abreCursor(conexion)
        contador=0
        for registro in listaEspecialidades:
            consulta= '''insert into Especialidad (codEspecialidad,codCuerpo, nombreEspecialidad)
                        values (?,?,?)'''
            cursor.execute(consulta,registro)
            contador+=1
        #fin del recorrido
        print("Se insertaron {0:d} especialidades".format(contador))
        conexion.commit()
        
    except:
        print('Se produjo un error al insertar Especialidades')
        conexion.rollback()
    finally:
        cierraCursor(cursor)

    #fin del método


def cargarCentros(listaCentros):
    #método para cargar las especialidades de prueba
    try:
        
        cursor=abreCursor(conexion)
        contador=0
        for registro in listaCentros:
            consulta= '''insert into Centro (codCentro,nombreCentro)
                        values (?,?)'''
            cursor.execute(consulta,registro)
            contador+=1
        #fin del recorrido
        print("Se insertaron {0:d} Centros".format(contador))
        conexion.commit()
        
    except:
        print('Se produjo un error al insertar Centros')
        conexion.rollback()
    finally:
        cierraCursor(cursor)

    #fin del método

def cargarCandidatos(listaCandidatos):
    #método para cargar las especialidades de prueba
    try:
        
        cursor=abreCursor(conexion)
        contador=0
        for registro in listaCandidatos:
            consulta= '''insert into Candidato (documento, nombreApellidos)
                        values (?,?)'''
            cursor.execute(consulta,registro)
            
            contador+=1
        #fin del recorrido
        print("Se insertaron {0:d} Candidatos".format(contador))
        conexion.commit()
        
    except:
        print('Se produjo un error al insertar Candidatos')
        conexion.rollback()
    finally:
        cierraCursor(cursor)

#fin del método


def cargarVacantes(listaVacantes):
    #método para cargar las vacantes de prueba
    try:
        
        cursor=abreCursor(conexion)
        contador=0
        for registro in listaVacantes:
            consulta= '''insert into Vacante (codCentro,codEspecialidad,orden)
                        values (?,?,?)'''
            cursor.execute(consulta,registro)
            
            contador+=1
        #fin del recorrido
        print("Se insertaron {0:d} Vacantes".format(contador))
        conexion.commit()
        
    except:
        print('Se produjo un error al insertar Vacantes')
        conexion.rollback()
    finally:
        cierraCursor(cursor)
    #fin del método


def cargarListas(listaBaremados):
    #método para cargar las vacantes de candidatos baremados por especialidad
    try:
        
        cursor=abreCursor(conexion)
        contador=0
        for registro in listaBaremados:
            consulta= '''insert into Lista (codEspecialidad,documento,orden)
                        values (?,?,?)'''
            cursor.execute(consulta,registro)
            
            contador+=1
        #fin del recorrido
        print("Se insertaron {0:d} Baremaciones".format(contador))
        conexion.commit()
        
    except:
        print('Se produjo un error al insertar Baremaciones')
        conexion.rollback()
    finally:
        cierraCursor(cursor)

    #fin del método


def cargarPeticiones(listaPeticiones):
    #método para cargar las peticiones de plazas que realiza cada candidato
    try:
        
        cursor=abreCursor(conexion)
        contador=0
        for registro in listaPeticiones:
            consulta= '''insert into Peticion (documento,ordenPeticion,codCentro,codEspecialidad,estado)
                        values (?,?,?,?,?)'''
            cursor.execute(consulta,registro)
            
            contador+=1
        #fin del recorrido
        print("Se insertaron {0:d} Peticiones".format(contador))
        conexion.commit()
        
    except:
        print('Se produjo un error al insertar Peticiones')
        conexion.rollback()
    finally:
        cierraCursor(cursor)

#fin del método

vaciarTablas()

listaEspecialidades=[ ('0590006','0590','Matemáticas'),
                        ('0590007','0590','Física y Química'),
                        ('0590019','0590','Tecnología'),
                        ('0597PRI','0597','Educación Primaria'),
                        ('0597FI','0597','Maestro Lengua Extranjera Inglés')]

listaCentros=[('60000001','IE Severo Ochoa'), ('60000003','IE El Pilar') ,
              ('60000005','IE Juan Ramón Jiménez'), ('60000007','IE Lope de Vega')]

listaCandidatos=[('11111A','Candidato 1'), ('22222B','Candidata 2'),('33333C','Candidato 3'),
                ('44444D','Candidata 4'), ('55555E','Candidato 5'),('66666F','Candidata 6'),
                ('77777G','Candidata 7')
                 ]

listaVacantes=[('60000001','0590006',1), ('60000001','0590007',1), ('60000001','0590019',1),
               ('60000003','0590006',1), ('60000003','0590007',1), 
               ('60000005','0590006',1), ('60000005','0590006',2),('60000005','0590019',1),
               ('60000005','0597PRI',1), ('60000007','0597PRI',1),
                ('60000007','0597FI',1), ('60000007','0597FI',2)
                 ]

listaBaremados=[('0590006','11111A',1),('0590006','22222B',2),('0590006','33333C',3),('0590006','44444D',4),
                ('0590007','11111A',3),('0590007','22222B',4),('0590007','33333C',1),('0590007','44444D',2),
                ('0590019','11111A',2),('0590019','22222B',3),('0590019','33333C',4),('0590019','44444D',1),
                ('0597PRI','55555E',1),('0597PRI','66666F',2),('0597PRI','77777G',3),
                ('0597FI','55555E',3),('0597FI','66666F',1),('0597FI','33333C',2),('0597FI','77777G',4)]

listaPeticiones=[ 
                #Peticiones del candidato 1
                ('11111A',1,'60000001','0590006',0),('11111A',2,'60000001','0590007',0),
                ('11111A',3,'60000001','0590019',0),('11111A',4,'60000003','0590006',0),
                ('11111A',5,'60000003','0590007',0),('11111A',6,'60000005','0590006',0),
                #Peticiones del candidato 2
                ('22222B',1,'60000001','0590006',0),('22222B',2,'60000001','0590007',0),
                ('22222B',3,'60000001','0590019',0),('22222B',4,'60000003','0590006',0),
                ('22222B',5,'60000003','0590007',0),('22222B',6,'60000005','0590006',0),
                #Peticiones del candidato 3
                ('33333C',1,'60000001','0590006',0),('33333C',2,'60000001','0590007',0),
                ('33333C',3,'60000001','0590019',0),('33333C',4,'60000003','0590006',0),
                ('33333C',5,'60000003','0590007',0),('33333C',6,'60000005','0590006',0),
                #Peticiones del candidato 4
                ('44444D',1,'60000001','0590006',0),('44444D',2,'60000001','0590007',0),
                ('44444D',3,'60000001','0590019',0),('44444D',4,'60000003','0590006',0),
                ('44444D',5,'60000003','0590007',0),('44444D',6,'60000005','0590006',0),
                #Peticiones del candidato 5
                ('55555E',1,'60000007','0597PRI',0),('55555E',2,'60000007','0597FI',0),
                ('55555E',3,'60000005','0597PRI',0),
                #Peticiones del candidato 6
                ('66666F',1,'60000007','0597PRI',0),('66666F',2,'60000007','0597FI',0),
                ('66666F',3,'60000005','0597PRI',0),
                #Peticiones del candidato 7
                ('77777G',3,'60000007','0597PRI',0),('77777G',1,'60000007','0597FI',0),
                ('77777G',2,'60000005','0597PRI',0)
]               

cargarEspecialidades(listaEspecialidades)
cargarCentros(listaCentros)
cargarCandidatos(listaCandidatos)
cargarVacantes(listaVacantes)
cargarListas(listaBaremados)
cargarPeticiones(listaPeticiones)

desconectar(conexion)




