from flask import Flask, render_template, request, redirect, url_for, flash
import re
import mysql.connector
from mysql.connector import Error

app_devolucion = Flask(__name__)
app_devolucion.secret_key = 'your_secret_key'

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

def insert_devolucion(correo, nombre, estado, descripcion, fecha):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    query = "INSERT INTO devolucion (correo, nombre, estado, descripcion, fecha) VALUES (%s, %s, %s, %s, %s)"
    values = (correo, nombre, estado, descripcion, fecha)
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

def get_devolucion(limit, offset, filters=None, filter_key=None):
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    base_query = "SELECT * FROM devolucion"
    filter_query = ""
    if filters and filter_key:
        filter_query = f" WHERE {filter_key} LIKE %s"
    query = f"{base_query}{filter_query} LIMIT %s OFFSET %s"
    try:
        values = (f"%{filters}%", limit, offset) if filters and filter_key else (limit, offset)
        cursor.execute(query, values)
        devoluciones = cursor.fetchall()
        return devoluciones
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def count_devoluciones(filters=None, filter_key=None):
    connection = create_connection()
    if connection is None:
        return 0
    cursor = connection.cursor()
    base_query = "SELECT COUNT(*) FROM devolucion"
    filter_query = ""
    if filters and filter_key:
        filter_query = f" WHERE {filter_key} LIKE %s"
    query = f"{base_query}{filter_query}"
    try:
        values = (f"%{filters}%",) if filters and filter_key else ()
        cursor.execute(query, values)
        count = cursor.fetchone()[0]
        return count
    except Error as e:
        print(f"The error '{e}' occurred")
        return 0
    finally:
        cursor.close()
        connection.close()

def get_devolucion_by_id(id):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM devolucion WHERE id = %s"
    try:
        cursor.execute(query, (id,))
        devolucion = cursor.fetchone()
        return devolucion
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_devolucion(id, correo, nombre, estado, descripcion, fecha):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE devolucion SET correo = %s, nombre = %s, estado = %s, descripcion = %s, fecha = %s WHERE id = %s"
    values = (correo, nombre, estado, descripcion, fecha, id)
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

def delete_devolucion(id):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM devolucion WHERE id = %s"
    try:
        cursor.execute(query, (id,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def valid_email(email):
    if len(email) < 7 or len(email) > 18:
        return False
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return False
    return True

def valid_name(name):
    if len(name) < 3 or len(name) > 20:
        return False
    if re.search(r'\d', name):
        return False
    if re.search(r'[^a-zA-Z\s]', name):
        return False
    if re.search(r'(.)\1{2,}', name):
        return False
    return True

def valid_description(description):
    if len(description) < 10 or len(description) > 50:
        return False
    if re.search(r'\d', description):
        return False
    if re.search(r'(.)\1{2,}', description):
        return False
    return True

@app_devolucion.route('/')
def index_devolucion():
    return render_template('index_devolucion.html')

@app_devolucion.route('/devolucion')
def devolucion():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    filter_key = request.args.get('filter_key')
    filter_value = request.args.get('filter_value')

    devoluciones = get_devolucion(per_page, offset, filter_value, filter_key)
    total_devoluciones = count_devoluciones(filter_value, filter_key)

    return render_template('devolucion.html', devoluciones=devoluciones, page=page, per_page=per_page, total_devoluciones=total_devoluciones, filter_key=filter_key, filter_value=filter_value)

@app_devolucion.route('/submit', methods=['POST'])
def submit():
    correo = request.form['correo']
    nombre = request.form['nombre']
    estado = request.form['estado']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']

    if not correo or not nombre or not estado or not descripcion or not fecha:
        flash('Todos los campos son obligatorios!')
        return redirect(url_for('index_devolucion'))

    if not valid_email(correo):
        flash('Correo inválido!')
        return redirect(url_for('index_devolucion'))

    if not valid_name(nombre):
        flash('Nombre inválido!')
        return redirect(url_for('index_devolucion'))

    if not valid_description(descripcion):
        flash('Descripción inválida!')
        return redirect(url_for('index_devolucion'))

    if insert_devolucion(correo, nombre, estado, descripcion, fecha):
        flash('Devolución insertada correctamente!')
    else:
        flash('Ocurrió un error al insertar la devolución.')

    return redirect(url_for('index_devolucion'))

@app_devolucion.route('/edit_devolucion/<int:id>', methods=['GET', 'POST'])
def edit_devolucion(id):
    if request.method == 'POST':
        correo = request.form['correo']
        nombre = request.form['nombre']
        estado = request.form['estado']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']

        if not correo or not nombre or not estado or not descripcion or not fecha:
            flash('Todos los campos son obligatorios!')
            return redirect(url_for('edit_devolucion', id=id))

        if not valid_email(correo):
            flash('Correo inválido!')
            return redirect(url_for('edit_devolucion', id=id))

        if not valid_name(nombre):
            flash('Nombre inválido!')
            return redirect(url_for('edit_devolucion', id=id))

        if not valid_description(descripcion):
            flash('Descripción inválida!')
            return redirect(url_for('edit_devolucion', id=id))

        if update_devolucion(id, correo, nombre, estado, descripcion, fecha):
            flash('Devolución actualizada correctamente!')
        else:
            flash('Ocurrió un error al actualizar la devolución.')

        return redirect(url_for('devolucion'))

    devolucion = get_devolucion_by_id(id)
    if devolucion is None:
        flash('Devolución no encontrada!')
        return redirect(url_for('devolucion'))
    return render_template('edit_devolucion.html', devolucion=devolucion)

@app_devolucion.route('/eliminar_devolucion/<int:id>', methods=['GET', 'POST'])
def eliminar_devolucion(id):
    if request.method == 'POST':
        if delete_devolucion(id):
            flash('Devolución eliminada correctamente!')
        else:
            flash('Ocurrió un error al eliminar la devolución.')
        return redirect(url_for('devolucion'))

    devolucion = get_devolucion_by_id(id)
    if devolucion is None:
        flash('Devolución no encontrada!')
        return redirect(url_for('devolucion'))
    return render_template('eliminar_devolucion.html', devolucion=devolucion)

if __name__ == '__main__':
    app_devolucion.run(debug=True, port=5009)
