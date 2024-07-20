from flask import Flask, render_template, request, redirect, url_for, flash
import re
import mysql.connector
from mysql.connector import Error

app_transaccion = Flask(__name__)
app_transaccion.secret_key = 'your_secret_key'

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

def insert_transaccion(nombre_cliente, correo, descripcion, monto, fecha):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "INSERT INTO transaccion (nombre_cliente, correo, descripcion, monto, fecha) VALUES (%s, %s, %s, %s, %s)"
    values = (nombre_cliente, correo, descripcion, monto, fecha)
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

def get_transacciones(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM transaccion LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        transacciones = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_transacciones = cursor.fetchone()[0]
        return transacciones, total_transacciones
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_transaccion_by_id(id_transaccion):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM transaccion WHERE id_transaccion = %s"
    try:
        cursor.execute(query, (id_transaccion,))
        transaccion = cursor.fetchone()
        return transaccion
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_transaccion(id_transaccion, nombre_cliente, correo, descripcion, monto, fecha):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE transaccion SET nombre_cliente = %s, correo = %s, descripcion = %s, monto = %s, fecha = %s WHERE id_transaccion = %s"
    values = (nombre_cliente, correo, descripcion, monto, fecha, id_transaccion)
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

def delete_transaccion(id_transaccion):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM transaccion WHERE id_transaccion = %s"
    try:
        cursor.execute(query, (id_transaccion,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def search_transacciones(search_query, search_field, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = f"SELECT SQL_CALC_FOUND_ROWS * FROM transaccion WHERE {search_field} LIKE %s LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (f'%{search_query}%', per_page, offset))
        transacciones = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_transacciones = cursor.fetchone()[0]
        return transacciones, total_transacciones
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def validate_fields(nombre_cliente, correo, descripcion, monto, fecha):
    if not nombre_cliente or not correo or not descripcion or not monto or not fecha:
        return False, 'Todos los campos son obligatorios.'

    if re.search(r'(.)\1\1', nombre_cliente):
        return False, 'El nombre no puede tener la misma letra repetida 3 o más veces.'

    if not re.match(r'^[a-zA-Z]+$', nombre_cliente):
        return False, 'El nombre solo puede contener letras.'

    if not (3 <= len(nombre_cliente) <= 20):
        return False, 'El nombre debe tener entre 3 y 20 caracteres.'

    if not (7 <= len(correo) <= 20):
        return False, 'El correo debe tener entre 7 y 20 caracteres.'

    if not (8 <= len(descripcion) <= 100):
        return False, 'La descripción debe tener entre 8 y 100 caracteres.'

    if not re.match(r'^[0-9]+$', monto) or int(monto) <= 0:
        return False, 'El monto solo puede contener números positivos.'

    if any(char.isdigit() for char in descripcion):
        return False, 'La descripción no puede contener números.'

    return True, ''

@app_transaccion.route('/')
def index_transaccion():
    return render_template('index_transaccion.html')

@app_transaccion.route('/transacciones')
def transacciones():
    search_query = request.args.get('search', '')
    search_field = request.args.get('search_field', 'nombre_cliente')  # Campo de búsqueda por defecto
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if search_query:
        transacciones, total_transacciones = search_transacciones(search_query, search_field, page, per_page)
    else:
        transacciones, total_transacciones = get_transacciones(page, per_page)

    total_pages = (total_transacciones + per_page - 1) // per_page
    return render_template('transacciones.html', transacciones=transacciones, search_query=search_query, search_field=search_field, page=page, per_page=per_page, total_transacciones=total_transacciones, total_pages=total_pages)

@app_transaccion.route('/submit', methods=['POST'])
def submit():
    nombre_cliente = request.form['nombre_cliente']
    correo = request.form['correo']
    descripcion = request.form['descripcion']
    monto = request.form['monto']
    fecha = request.form['fecha']

    is_valid, message = validate_fields(nombre_cliente, correo, descripcion, monto, fecha)
    if not is_valid:
        flash(message)
        return redirect(url_for('index_transaccion'))

    if insert_transaccion(nombre_cliente, correo, descripcion, monto, fecha):
        flash('Transacción insertada exitosamente!')
    else:
        flash('Ocurrió un error al insertar la transacción.')
    
    return redirect(url_for('index_transaccion'))

@app_transaccion.route('/edit_transaccion/<int:id_transaccion>', methods=['GET', 'POST'])
def edit_transaccion(id_transaccion):
    if request.method == 'POST':
        nombre_cliente = request.form['nombre_cliente']
        correo = request.form['correo']
        descripcion = request.form['descripcion']
        monto = request.form['monto']
        fecha = request.form['fecha']

        is_valid, message = validate_fields(nombre_cliente, correo, descripcion, monto, fecha)
        if not is_valid:
            flash(message)
            return redirect(url_for('edit_transaccion', id_transaccion=id_transaccion))

        if update_transaccion(id_transaccion, nombre_cliente, correo, descripcion, monto, fecha):
            flash('Transacción actualizada exitosamente!')
        else:
            flash('Ocurrió un error al actualizar la transacción.')
        
        return redirect(url_for('transacciones'))

    transaccion = get_transaccion_by_id(id_transaccion)
    if transaccion is None:
        flash('Transacción no encontrada!')
        return redirect(url_for('transacciones'))
    return render_template('edit_transaccion.html', transaccion=transaccion)

@app_transaccion.route('/eliminar_transaccion/<int:id_transaccion>', methods=['GET', 'POST'])
def eliminar_transaccion(id_transaccion):
    if request.method == 'POST':
        if delete_transaccion(id_transaccion):
            flash('Transacción eliminada exitosamente!')
        else:
            flash('Ocurrió un error al eliminar la transacción.')
        return redirect(url_for('transacciones'))

    transaccion = get_transaccion_by_id(id_transaccion)
    if transaccion is None:
        flash('Transacción no encontrada!')
        return redirect(url_for('transacciones'))
    return render_template('eliminar_transaccion.html', transaccion=transaccion)

if __name__ == '__main__':
    app_transaccion.run(debug=True, port=5007)
