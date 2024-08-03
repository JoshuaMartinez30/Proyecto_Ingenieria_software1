from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

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

def insert_distribucion(id_almacenes, id_producto, cantidad, fecha):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "INSERT INTO distribucion_almacenes (id_almacenes, id_producto, cantidad, fecha) VALUES (%s, %s, %s, %s)"
    values = (id_almacenes, id_producto, cantidad, fecha)
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

def get_distribuciones(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = """
    SELECT SQL_CALC_FOUND_ROWS da.id_distribucion, a.nombre AS nombre_almacen, p.nombre AS nombre_producto, da.cantidad, da.fecha
    FROM distribucion_almacenes da
    JOIN almacenes a ON da.id_almacenes = a.id_almacenes
    JOIN producto p ON da.id_producto = p.id_producto
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

def update_distribucion(id_distribucion, id_almacenes, id_producto, cantidad, fecha):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE distribucion_almacenes SET id_almacenes = %s, id_producto = %s, cantidad = %s, fecha = %s WHERE id_distribucion = %s"
    values = (id_almacenes, id_producto, cantidad, fecha, id_distribucion)
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
    id_almacenes = request.form['id_almacenes']
    id_producto = request.form['id_producto']
    cantidad = request.form['cantidad']
    fecha = request.form['fecha']

    if not id_almacenes or not id_producto or not cantidad or not fecha:
        flash('Todos los campos son requeridos!')
        return redirect(url_for('index_distribucion'))

    if insert_distribucion(id_almacenes, id_producto, cantidad, fecha):
        flash('Distribución insertada exitosamente!')
    else:
        flash('Ocurrió un error al insertar la distribución.')
    
    return redirect(url_for('index_distribucion'))

@app_distribucion.route('/edit_distribucion/<int:id_distribucion>', methods=['GET', 'POST'])
def edit_distribucion(id_distribucion):
    if request.method == 'POST':
        id_almacenes = request.form['id_almacenes']
        id_producto = request.form['id_producto']
        cantidad = request.form['cantidad']
        fecha = request.form['fecha']

        if not id_almacenes or not id_producto or not cantidad or not fecha:
            flash('Todos los campos son requeridos!')
            return redirect(url_for('edit_distribucion', id_distribucion=id_distribucion))

        if update_distribucion(id_distribucion, id_almacenes, id_producto, cantidad, fecha):
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

@app_distribucion.route('/eliminar_distribucion/<int:id_distribucion>', methods=['GET', 'POST'])
def eliminar_distribucion(id_distribucion):
    if request.method == 'POST':
        if delete_distribucion(id_distribucion):
            flash('Distribución eliminada exitosamente!')
        else:
            flash('Ocurrió un error al eliminar la distribución.')
        return redirect(url_for('distribuciones'))

    distribucion = get_distribucion_by_id(id_distribucion)
    if distribucion is None:
        flash('Distribución no encontrada!')
        return redirect(url_for('distribuciones'))
    return render_template('eliminar_distribucion.html', distribucion=distribucion)

def search_distribuciones(search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    
    query = """
    SELECT SQL_CALC_FOUND_ROWS da.id_distribucion, a.nombre AS nombre_almacen, p.nombre AS nombre_producto, da.cantidad, da.fecha
    FROM distribucion_almacenes da
    JOIN almacenes a ON da.id_almacenes = a.id_almacenes
    JOIN producto p ON da.id_producto = p.id_producto
    WHERE a.nombre LIKE %s 
       OR p.nombre LIKE %s 
       OR da.cantidad LIKE %s 
       OR da.fecha LIKE %s
    LIMIT %s OFFSET %s
    """
    
    search_pattern = f'%{search_query}%'
    try:
        cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern, per_page, offset))
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

if __name__ == '__main__':
    app_distribucion.run(debug=True,port=5002)
