"""
    Definición de constantes para la aplicación, utilizando un diccionario
    Todas las rutas son relativas al directorio de ejecución del módulo principal
"""
constantes=dict()
constantes['ruta_db']='basedatos'   #carpeta donde se encuentra la base de datos
constantes['ruta_ficheros']='entradas' #carpeta donde se encuentran los ficheros csv que procesa y lee la aplicación
constantes['ruta_resultados']='resultados' #carpeta donde se encuentran los ficheros csv que devuelve y escribe la aplicación
constantes['nombre_db']='adjudicaciones.db' #nombre de la base de datos SQLite
constantes['nombre_fichero_log']='ejecuciones.txt' #nombre del fichero donde se escribe el registro de log de las ejecuciones
constantes['nombre_fichero_errores']='errrores.txt' #nombre del fichero donde se escribe el registro de errores detectados en una ejecución
constantes['fic_asignadas']='puestosAsignados.csv'  #nombre del fichero CSV donde se escribe la info de los puestos asignados
constantes['fic_desiertas']='puestosDesiertos.csv'  #nombre del fichero CSV donde se escribe la info de los puestos desiertos
constantes['ficheros_inicio']=['especialidad.csv','centro.csv','candidato.csv', 'lista.csv','peticion.csv','vacante.csv']   
        #lista con los nombres de los ficheros CSV para inicializar las tablas de las bases de datos

