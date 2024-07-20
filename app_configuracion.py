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
        return False
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

def get_configuraciones(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM seguridad LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        configuraciones = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_configuraciones = cursor.fetchone()[0]
        return configuraciones, total_configuraciones
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
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

def search_configuraciones(search_query, filter_field, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()

    offset = (page - 1) * per_page
    query = f"SELECT SQL_CALC_FOUND_ROWS * FROM seguridad WHERE {filter_field} LIKE %s LIMIT %s OFFSET %s"
    values = (f'%{search_query}%', per_page, offset)

    try:
        cursor.execute(query, values)
        configuraciones = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_configuraciones = cursor.fetchone()[0]
        return configuraciones, total_configuraciones
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def validar_configuracion(nombre_de_configuracion, descripcion, estado_config):
    errores = []
    if not nombre_de_configuracion or not descripcion or not estado_config:
        errores.append("Todos los campos son requeridos.")
    if len(nombre_de_configuracion) < 3 or len(nombre_de_configuracion) > 15:
        errores.append("El nombre de la configuración debe tener entre 3 y 15 caracteres.")
    if len(descripcion) < 3 or len(descripcion) > 50:
        errores.append("La descripción debe tener entre 3 y 50 caracteres.")
    if re.search(r'(.)\1{2,}', nombre_de_configuracion):
        errores.append("El nombre de la configuración no debe tener tres letras repetidas consecutivamente.")
    if re.search(r'(.)\1{2,}', descripcion):
        errores.append("La descripción no debe tener tres letras repetidas consecutivamente.")
    if re.search(r'[^a-zA-Z0-9\s]', nombre_de_configuracion):
        errores.append("El nombre de la configuración no debe contener signos.")
    if re.search(r'[^a-zA-Z0-9\s]', descripcion):
        errores.append("La descripción no debe contener signos.")
    if estado_config not in ["activo", "inactivo"]:
        errores.append("El estado de la configuración debe ser 'activo' o 'inactivo'.")
    return errores

@app_encuestas.route('/')
def index_configuraciones():
    return render_template('index_configuraciones.html')

@app_encuestas.route('/configuraciones')
def configuraciones():
    search_query = request.args.get('search', '')
    filter_field = request.args.get('filter', 'nombre_de_configuracion')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if search_query:
        configuraciones, total_configuraciones = search_configuraciones(search_query, filter_field, page, per_page)
    else:
        configuraciones, total_configuraciones = get_configuraciones(page, per_page)

    total_pages = (total_configuraciones + per_page - 1) // per_page
    return render_template('configuraciones.html', configuraciones=configuraciones, search_query=search_query, filter=filter_field, page=page, per_page=per_page, total_configuraciones=total_configuraciones, total_pages=total_pages)

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
