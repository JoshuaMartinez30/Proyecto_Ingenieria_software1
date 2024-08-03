from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import re
from mysql.connector import Error

app_mantenimiento = Flask(__name__)
app_mantenimiento.secret_key = 'your_secret_key'

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

def insert_mantenimiento(id_equipo, fecha, tipo, detalles, estado, documento):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "INSERT INTO mantenimiento_equipo (id_equipo, fecha, tipo, detalles, estado, documento) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (id_equipo, fecha, tipo, detalles, estado, documento)
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

def get_mantenimientos(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM mantenimiento_equipo LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        mantenimientos = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_mantenimientos = cursor.fetchone()[0]
        return mantenimientos, total_mantenimientos
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_mantenimiento_by_id(id_mantenimiento):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM mantenimiento_equipo WHERE id_mantenimiento = %s"
    try:
        cursor.execute(query, (id_mantenimiento,))
        mantenimiento = cursor.fetchone()
        return mantenimiento
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return None
    finally:
        cursor.close()
        connection.close()

def update_mantenimiento(id_mantenimiento, id_equipo, fecha, tipo, detalles, estado, documento):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE mantenimiento_equipo SET id_equipo = %s, fecha = %s, tipo = %s, detalles = %s, estado = %s, documento = %s WHERE id_mantenimiento = %s"
    values = (id_equipo, fecha, tipo, detalles, estado, documento, id_mantenimiento)
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

def delete_mantenimiento(id_mantenimiento):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM mantenimiento_equipo WHERE id_mantenimiento = %s"
    try:
        cursor.execute(query, (id_mantenimiento,))
        connection.commit()
        return True
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

def search_mantenimientos_by_field(field, value, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    query = f"""
    SELECT SQL_CALC_FOUND_ROWS * 
    FROM mantenimiento_equipo 
    WHERE {field} = %s
    LIMIT %s OFFSET %s
    """
    values = (value, per_page, offset)
    try:
        cursor.execute(query, values)
        mantenimientos = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_mantenimientos = cursor.fetchone()[0]
        return mantenimientos, total_mantenimientos
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def search_mantenimientos(search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    
    query = """
    SELECT SQL_CALC_FOUND_ROWS * 
    FROM mantenimiento_equipo 
    WHERE id_equipo LIKE %s 
       OR tipo LIKE %s 
       OR detalles LIKE %s 
       OR estado LIKE %s 
       OR fecha LIKE %s
    LIMIT %s OFFSET %s
    """
    values = (
        f'%{search_query}%', 
        f'%{search_query}%', 
        f'%{search_query}%', 
        f'%{search_query}%', 
        f'%{search_query}%', 
        per_page, 
        offset
    )
    try:
        cursor.execute(query, values)
        mantenimientos = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_mantenimientos = cursor.fetchone()[0]
        return mantenimientos, total_mantenimientos
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

@app_mantenimiento.route('/')
def index_mantenimiento():
    return render_template('index_mantenimiento.html')

@app_mantenimiento.route('/mantenimientos')
def mantenimientos():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    if search_query:
        if ':' in search_query:
            search_field, search_value = search_query.split(':', 1)
            if search_field in ["id_equipo", "tipo", "detalles", "estado", "fecha"]:
                mantenimientos, total_mantenimientos = search_mantenimientos_by_field(search_field, search_value, page, per_page)
            else:
                mantenimientos, total_mantenimientos = search_mantenimientos(search_value, page, per_page)
        else:
            mantenimientos, total_mantenimientos = search_mantenimientos(search_query, page, per_page)
    else:
        mantenimientos, total_mantenimientos = get_mantenimientos(page, per_page)

    total_pages = (total_mantenimientos + per_page - 1) // per_page
    return render_template('mantenimientos.html', mantenimientos=mantenimientos, search_query=search_query, page=page, per_page=per_page, total_mantenimientos=total_mantenimientos, total_pages=total_pages)

@app_mantenimiento.route('/submit', methods=['POST'])
def submit():
    id_equipo = request.form['id_equipo']
    fecha = request.form['fecha']
    tipo = request.form['tipo']
    detalles = request.form['detalles']
    estado = request.form['estado']
    documento = request.form['documento']

    if not id_equipo or not fecha or not tipo or not detalles or not estado or not documento:
        flash('Todos los campos son requeridos!')
        return redirect(url_for('index_mantenimiento'))

    if insert_mantenimiento(id_equipo, fecha, tipo, detalles, estado, documento):
        flash('Mantenimiento insertado exitosamente!')
    else:
        flash('Ocurrió un error al insertar el mantenimiento.')
    
    return redirect(url_for('index_mantenimiento'))

@app_mantenimiento.route('/edit_mantenimiento/<int:id_mantenimiento>', methods=['GET', 'POST'])
def edit_mantenimiento(id_mantenimiento):
    if request.method == 'POST':
        id_equipo = request.form['id_equipo']
        fecha = request.form['fecha']
        tipo = request.form['tipo']
        detalles = request.form['detalles']
        estado = request.form['estado']
        documento = request.form['documento']

        if not id_equipo or not fecha or not tipo or not detalles or not estado or not documento:
            flash('Todos los campos son requeridos!')
            return redirect(url_for('edit_mantenimiento', id_mantenimiento=id_mantenimiento))

        if update_mantenimiento(id_mantenimiento, id_equipo, fecha, tipo, detalles, estado, documento):
            flash('Mantenimiento actualizado exitosamente!')
        else:
            flash('Ocurrió un error al actualizar el mantenimiento.')
        
        return redirect(url_for('mantenimientos'))

    mantenimiento = get_mantenimiento_by_id(id_mantenimiento)
    if mantenimiento is None:
        flash('Mantenimiento no encontrado!')
        return redirect(url_for('mantenimientos'))
    return render_template('edit_mantenimiento.html', mantenimiento=mantenimiento)

@app_mantenimiento.route('/eliminar_mantenimiento/<int:id_mantenimiento>', methods=['GET', 'POST'])
def eliminar_mantenimiento(id_mantenimiento):
    if request.method == 'POST':
        if delete_mantenimiento(id_mantenimiento):
            flash('Mantenimiento eliminado exitosamente!')
        else:
            flash('Ocurrió un error al eliminar el mantenimiento.')
        return redirect(url_for('mantenimientos'))

    mantenimiento = get_mantenimiento_by_id(id_mantenimiento)
    if mantenimiento is None:
        flash('Mantenimiento no encontrado!')
        return redirect(url_for('mantenimientos'))
    return render_template('eliminar_mantenimiento.html', mantenimiento=mantenimiento)

if __name__ == "__main__":
    app_mantenimiento.run(debug=True,port=5016)
