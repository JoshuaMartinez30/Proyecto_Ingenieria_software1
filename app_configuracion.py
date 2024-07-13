from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

app_encuestas = Flask(__name__)
app_encuestas.secret_key = 'your_secret_key'

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="proyecto_is1"
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def insert_configuracion(nombre_de_configuracion, descripcion, estado_config):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    query = "INSERT INTO seguridad (nombre_de_configuracion, descripcion, estado_config) VALUES (%s, %s, %s)"
    values = (nombre_de_configuracion, descripcion, estado_config)
    try:
        cursor.execute(query, values)
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def get_configuraciones():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM seguridad"
    try:
        cursor.execute(query)
        configuraciones = cursor.fetchall()
        return configuraciones
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def get_configuracion_by_id(id_configuracion):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM seguridad WHERE id_configuracion = %s"
    try:
        cursor.execute(query, (id_configuracion,))
        configuracion = cursor.fetchone()
        return configuracion
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_configuracion(id_configuracion, nombre_de_configuracion, descripcion, estado_config):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    UPDATE seguridad
    SET nombre_de_configuracion = %s, descripcion = %s, estado_config = %s
    WHERE id_configuracion = %s
    """
    values = (nombre_de_configuracion, descripcion, estado_config, id_configuracion)
    try:
        cursor.execute(query, values)
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_configuracion(id_configuracion):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM seguridad WHERE id_configuracion = %s"
    try:
        cursor.execute(query, (id_configuracion,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def search_configuraciones(search_query):
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM seguridad WHERE nombre_de_configuracion LIKE %s"
    values = (f'%{search_query}%',)
    try:
        cursor.execute(query, values)
        configuraciones = cursor.fetchall()
        return configuraciones
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def validar_configuracion(nombre_de_configuracion, descripcion, estado_config):
    errores = []

    # Validar campos en blanco
    if not nombre_de_configuracion or not descripcion or not estado_config:
        errores.append("Todos los campos son requeridos.")
    
    # Validar longitud de caracteres
    if len(nombre_de_configuracion) < 3 or len(nombre_de_configuracion) > 15:
        errores.append("El nombre de la configuración debe tener entre 3 y 15 caracteres.")
    if len(descripcion) < 3 or len(descripcion) > 50:
        errores.append("La descripción debe tener entre 3 y 50 caracteres.")
    
    # Validar que no haya tres letras repetidas
    if re.search(r'(.)\1{2,}', nombre_de_configuracion):
        errores.append("El nombre de la configuración no debe tener tres letras repetidas consecutivamente.")
    if re.search(r'(.)\1{2,}', descripcion):
        errores.append("La descripción no debe tener tres letras repetidas consecutivamente.")
    
    # Validar que no haya signos
    if re.search(r'[^a-zA-Z0-9\s]', nombre_de_configuracion):
        errores.append("El nombre de la configuración no debe contener signos.")
    if re.search(r'[^a-zA-Z0-9\s]', descripcion):
        errores.append("La descripción no debe contener signos.")
    
    # Validar estado_config
    if estado_config not in ["activo", "inactivo"]:
        errores.append("El estado de la configuración debe ser 'activo' o 'inactivo'.")

    return errores

@app_encuestas.route('/')
def index_configuraciones():
    return render_template('index_configuraciones.html')

@app_encuestas.route('/configuraciones')
def configuraciones():
    search_query = request.args.get('search')
    if search_query:
        configuraciones = search_configuraciones(search_query)
    else:
        configuraciones = get_configuraciones()
    return render_template('configuraciones.html', configuraciones=configuraciones, search_query=search_query)

@app_encuestas.route('/submit', methods=['POST'])
def submit():
    nombre_de_configuracion = request.form['nombre_de_configuracion']
    descripcion = request.form['descripcion']
    estado_config = request.form['estado_config']

    errores = validar_configuracion(nombre_de_configuracion, descripcion, estado_config)
    if errores:
        for error in errores:
            flash(error)
        return redirect(url_for('index_configuraciones'))

    if insert_configuracion(nombre_de_configuracion, descripcion, estado_config):
        flash('Configuración insertada exitosamente!')
    else:
        flash('Ocurrió un error al insertar la configuración.')
    
    return redirect(url_for('index_configuraciones'))

@app_encuestas.route('/edit/<int:id_configuracion>', methods=['GET', 'POST'])
def edit_configuraciones(id_configuracion):
    if request.method == 'POST':
        nombre_de_configuracion = request.form['nombre_de_configuracion']
        descripcion = request.form['descripcion']
        estado_config = request.form['estado_config']

        errores = validar_configuracion(nombre_de_configuracion, descripcion, estado_config)
        if errores:
            for error in errores:
                flash(error)
            return redirect(url_for('edit_configuraciones', id_configuracion=id_configuracion))

        if update_configuracion(id_configuracion, nombre_de_configuracion, descripcion, estado_config):
            flash('Configuración actualizada exitosamente!')
        else:
            flash('Ocurrió un error al actualizar la configuración.')
        
        return redirect(url_for('configuraciones'))

    configuracion = get_configuracion_by_id(id_configuracion)
    if configuracion is None:
        flash('Configuración no encontrada!')
        return redirect(url_for('configuraciones'))
    return render_template('edit_configuraciones.html', configuracion=configuracion)

@app_encuestas.route('/eliminar/<int:id_configuracion>', methods=['GET', 'POST'])
def eliminar_configuraciones(id_configuracion):
    if request.method == 'POST':
        if delete_configuracion(id_configuracion):
            flash('Configuración eliminada exitosamente!')
        else:
            flash('Ocurrió un error al eliminar la configuración.')
        return redirect(url_for('configuraciones'))

    configuracion = get_configuracion_by_id(id_configuracion)
    if configuracion is None:
        flash('Configuración no encontrada!')
        return redirect(url_for('configuraciones'))
    return render_template('eliminar_configuraciones.html', configuracion=configuracion)

if __name__ == '__main__':
    app_encuestas.run(debug=True, port=5011)
