from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re
from datetime import datetime

app_distribucion = Flask(__name__)
app_distribucion.secret_key = 'your_secret_key'

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
            print("Conexión exitosa a la base de datos MySQL")
    except Error as e:
        print(f"Error '{e}' ocurrió")
    return connection

def validate_text_field(field_value, field_name):
    if not 3 <= len(field_value) <= 20:
        return f"El campo {field_name} debe tener entre 3 y 20 caracteres."
    if re.search(r'\d', field_value):
        return f"El campo {field_name} no puede contener números."
    if re.search(r'[^a-zA-Z]', field_value):
        return f"El campo {field_name} no puede contener caracteres especiales."
    if re.search(r'(.)\1\1', field_value):
        return f"El campo {field_name} no puede contener tres letras repetidas consecutivas."
    return None

def validate_numeric_field(field_value, field_name):
    if not field_value.isdigit():
        return f"El campo {field_name} solo puede contener números."
    return None

def validate_date_field(date_value, field_name):
    try:
        date_obj = datetime.strptime(date_value, '%Y-%m-%d')
        if date_obj < datetime.now():
            return f"El campo {field_name} no puede ser una fecha anterior a la actual."
    except ValueError:
        return f"El campo {field_name} debe ser una fecha válida."
    return None

def insert_distribucion(id_almacenes_origen, id_almacenes_destino, id_producto, cantidad, fecha):
    connection = create_connection()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False
    cursor = connection.cursor()
    query = """
    INSERT INTO distribucion_almacenes (id_almacenes_origen, id_almacenes_destino, id_producto, cantidad, fecha) 
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (id_almacenes_origen, id_almacenes_destino, id_producto, cantidad, fecha)
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Inserción exitosa.")
        return True
    except Error as e:
        print(f"Error al insertar en la base de datos: {e}")  # Imprimir el error
        return False
    finally:
        cursor.close()
        connection.close()



def get_distribuciones(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = """
    SELECT SQL_CALC_FOUND_ROWS d.id_distribucion, ao.nombre AS almacen_origen, ad.nombre AS almacen_destino, 
           p.nombre AS nombre_producto, d.cantidad, d.fecha
    FROM distribucion_almacenes d
    JOIN almacenes ao ON d.id_almacenes_origen = ao.id_almacenes
    JOIN almacenes ad ON d.id_almacenes_destino = ad.id_almacenes
    JOIN producto p ON d.id_producto = p.id_producto
    LIMIT %s OFFSET %s
    """
    try:
        cursor.execute(query, (per_page, offset))
        distribuciones = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_distribuciones = cursor.fetchone()[0]
        return distribuciones, total_distribuciones
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_distribucion_by_id(id_distribucion):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM distribucion_almacenes WHERE id_distribucion = %s"
    try:
        cursor.execute(query, (id_distribucion,))
        distribucion = cursor.fetchone()
        return distribucion
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return None
    finally:
        cursor.close()
        connection.close()


def search_distribuciones(search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = """
    SELECT SQL_CALC_FOUND_ROWS d.id_distribucion, ao.nombre AS almacen_origen, ad.nombre AS almacen_destino, 
           p.nombre AS nombre_producto, d.cantidad, d.fecha
    FROM distribucion_almacenes d
    JOIN almacenes ao ON d.id_almacenes_origen = ao.id_almacenes
    JOIN almacenes ad ON d.id_almacenes_destino = ad.id_almacenes
    JOIN producto p ON d.id_producto = p.id_producto
    WHERE ao.nombre LIKE %s OR ad.nombre LIKE %s OR p.nombre LIKE %s
    LIMIT %s OFFSET %s
    """
    search_pattern = f"%{search_query}%"
    try:
        cursor.execute(query, (search_pattern, search_pattern, search_pattern, per_page, offset))
        distribuciones = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_distribuciones = cursor.fetchone()[0]
        return distribuciones, total_distribuciones
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def update_distribucion(id_distribucion, id_almacenes_origen, id_almacenes_destino, id_producto, cantidad, fecha):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    UPDATE distribucion_almacenes 
    SET id_almacenes_origen = %s, id_almacenes_destino = %s, id_producto = %s, cantidad = %s, fecha = %s 
    WHERE id_distribucion = %s
    """
    values = (id_almacenes_origen, id_almacenes_destino, id_producto, cantidad, fecha, id_distribucion)
    try:
        cursor.execute(query, values)
        connection.commit()
        return True
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_distribucion(id_distribucion):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM distribucion_almacenes WHERE id_distribucion = %s"
    try:
        cursor.execute(query, (id_distribucion,))
        connection.commit()
        return True
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()


@app_distribucion.route('/')
def index_distribucion():
    connection = create_connection()
    if connection is None:
        return render_template('index_distribucion.html', almacenes=[], productos=[])
    cursor = connection.cursor()
    
    cursor.execute("SELECT id_almacenes, nombre FROM almacenes")
    almacenes = cursor.fetchall()

    cursor.execute("SELECT id_producto, nombre FROM producto")
    productos = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('index_distribucion.html', almacenes=almacenes, productos=productos)

@app_distribucion.route('/distribuciones')
def distribuciones():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    if search_query:
        distribuciones, total_distribuciones = search_distribuciones(search_query, page, per_page)
    else:
        distribuciones, total_distribuciones = get_distribuciones(page, per_page)

    total_pages = (total_distribuciones + per_page - 1) // per_page
    return render_template('distribuciones.html', distribuciones=distribuciones, search_query=search_query, page=page, per_page=per_page, total_distribuciones=total_distribuciones, total_pages=total_pages)

@app_distribucion.route('/submit', methods=['POST'])
def submit():
    id_almacenes_origen = request.form['id_almacenes_origen']
    id_almacenes_destino = request.form['id_almacenes_destino']
    id_producto = request.form['id_producto']
    cantidad = request.form['cantidad']
    fecha = request.form['fecha']

    if not id_almacenes_origen or not id_almacenes_destino  or not id_producto or not cantidad or not fecha:
        flash('Todos los campos son requeridos!')
        return redirect(url_for('index_distribucion'))

    if insert_distribucion(id_almacenes_origen,id_almacenes_destino, id_producto, cantidad, fecha):
        flash('Distribución insertada exitosamente!')
    else:
        flash('Ocurrió un error al insertar la distribución.')

    return redirect(url_for('index_distribucion'))

@app_distribucion.route('/edit_distribucion/<int:id_distribucion>', methods=['GET', 'POST'])
def edit_distribucion(id_distribucion):
    if request.method == 'POST':
        id_almacenes_origen = request.form['id_almacenes_origen']
        id_almacenes_destino = request.form['id_almacenes_destino']
        id_producto = request.form['id_producto']
        cantidad = request.form['cantidad']
        fecha = request.form['fecha']

        if not id_almacenes_origen or not id_almacenes_destino or not id_producto or not cantidad or not fecha:
            flash('Todos los campos son requeridos!')
            return redirect(url_for('edit_distribucion', id_distribucion=id_distribucion))

        if update_distribucion(id_distribucion, id_almacenes_origen, id_almacenes_destino, id_producto, cantidad, fecha):
            flash('Distribución actualizada exitosamente!')
        else:
            flash('Ocurrió un error al actualizar la distribución.')
        
        return redirect(url_for('distribuciones'))

    distribucion = get_distribucion_by_id(id_distribucion)
    if distribucion is None:
        flash('Distribución no encontrada!')
        return redirect(url_for('distribuciones'))

    # Obtener listas de almacenes y productos
    connection = create_connection()
    if connection is None:
        return render_template('edit_distribucion.html', distribucion=distribucion, almacenes=[], productos=[])

    cursor = connection.cursor()
    cursor.execute("SELECT id_almacenes, nombre FROM almacenes")
    almacenes = cursor.fetchall()

    cursor.execute("SELECT id_producto, nombre FROM producto")
    productos = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('edit_distribucion.html', distribucion=distribucion, almacenes=almacenes, productos=productos)

@app_distribucion.route('/delete/<int:id_distribucion>', methods=['GET', 'POST'])
def eliminar_distribucion(id_distribucion):
    # Verificar si el método es POST
    if request.method == 'POST':
        if delete_distribucion(id_distribucion):
            flash('Distribución eliminada exitosamente.')
        else:
            flash('Error al eliminar la distribución.')
        return redirect(url_for('distribuciones'))

    # Si el método no es POST, verificar si la distribución existe
    distribucion = get_distribucion_by_id(id_distribucion)
    if distribucion is None:
        flash('Distribución no encontrada.')
        return redirect(url_for('distribuciones'))

    return render_template('eliminar_distribucion.html', distribucion=distribucion)

if __name__ == '__main__':
    app_distribucion.run(debug=True,port=5002)
