from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re
from datetime import datetime, timedelta

app_promocion = Flask(__name__)
app_promocion.secret_key = 'your_secret_key'

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

def validate_promotion(nombre, descripcion, valor, fecha_inicio, fecha_final):
    regexNoTresRepetidas = re.compile(r'(.)\1\1')
    regexNoSignos = re.compile(r'[^a-zA-Z0-9\s]')
    regexNoNumerosEnTexto = re.compile(r'\d')
    regexNoLetrasEnNumero = re.compile(r'[a-zA-Z]')
    
    if not nombre or not descripcion or not valor or not fecha_inicio or not fecha_final:
        return "Todos los campos son obligatorios."

    if regexNoTresRepetidas.search(nombre) or regexNoTresRepetidas.search(descripcion):
        return "No se permiten tres letras repetidas consecutivas."
    
    if regexNoSignos.search(nombre) or regexNoSignos.search(descripcion) or regexNoSignos.search(valor):
        return "No se permiten signos."
    
    if regexNoNumerosEnTexto.search(nombre) or regexNoNumerosEnTexto.search(descripcion):
        return "No se permiten números en campos de texto."
    
    if regexNoLetrasEnNumero.search(valor):
        return "No se permiten letras en el campo de valor."
    
    if len(nombre) < 3 or len(nombre) > 15:
        return "El nombre debe tener entre 3 y 15 caracteres."
    
    if len(descripcion) < 3 or len(descripcion) > 15:
        return "La descripción debe tener entre 3 y 15 caracteres."
    
    try:
        today = datetime.now()
        start_date = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        end_date = datetime.strptime(fecha_final, '%Y-%m-%d')

        if start_date > today + timedelta(days=30):
            return "La fecha de inicio debe ser máximo 30 días a partir de hoy."
        
        if end_date < start_date:
            return "La fecha final no puede ser antes de la fecha de inicio."
        
        if end_date < start_date + timedelta(days=7):
            return "La fecha final debe ser al menos 7 días después de la fecha de inicio."
    
    except ValueError:
        return "Formato de fecha incorrecto."
    
    return None

def insert_user(nombre, descripcion, tipo, valor, fecha_inicio, fecha_final, estado_promocion):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    query = "INSERT INTO promocion (nombre, descripcion, tipo, valor, fecha_inicio, fecha_final, estado_promocion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (nombre, descripcion, tipo, valor, fecha_inicio, fecha_final, estado_promocion)
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


def get_promocion(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM promocion LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        promocion = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_promocion = cursor.fetchone()[0]
        return promocion, total_promocion
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_promocion_by_id(id_promocion):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM promocion WHERE id_promocion = %s"
    try:
        cursor.execute(query, (id_promocion,))
        promocion = cursor.fetchone()
        return promocion
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_user(id_promocion, nombre, descripcion, tipo, valor, fecha_inicio, fecha_final, estado_promocion):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE promocion SET nombre = %s, descripcion = %s, tipo = %s, valor = %s, fecha_inicio = %s, fecha_final= %s, estado_promocion = %s WHERE id_promocion = %s"
    values = (nombre, descripcion, tipo, valor, fecha_inicio, fecha_final, estado_promocion, id_promocion)
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

def delete_user(id_promocion):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM promocion WHERE id_promocion = %s"
    try:
        cursor.execute(query, (id_promocion,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def search_users(search_query):
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM promocion WHERE nombre LIKE %s OR descripcion LIKE %s OR tipo LIKE %s OR valor LIKE %s OR fecha_inicio LIKE %s OR fecha_final LIKE %s OR estado_promocion LIKE %s"
    values = (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
    try:
        cursor.execute(query, values)
        promocion = cursor.fetchall()
        return promocion
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

@app_promocion.route('/')
def index_promocion():
    return render_template('index_promocion.html')

@app_promocion.route('/promocion')
def promocion():
    search_query = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if search_query:
        promocion, total_promocion = search_users(search_query, page, per_page)
    else:
        promocion, total_promocion = get_promocion(page, per_page)

    total_pages = (total_promocion + per_page - 1) // per_page
    return render_template('promocion.html', promocion=promocion, search_query=search_query, page=page, per_page=per_page, total_promocion=total_promocion, total_pages=total_pages)

@app_promocion.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    tipo = request.form['tipo']
    valor = request.form['valor']
    fecha_inicio = request.form['fecha_inicio']
    fecha_final = request.form['fecha_final']
    estado_promocion = request.form['estado_promocion']

    error = validate_promotion(nombre, descripcion, valor, fecha_inicio, fecha_final)
    if error:
        flash(error)
        return redirect(url_for('index_promocion'))

    if insert_user(nombre, descripcion, tipo, valor, fecha_inicio, fecha_final, estado_promocion):
        flash('Product inserted successfully!')
    else:
        flash('An error occurred while inserting the product.')
    
    return redirect(url_for('index_promocion'))

@app_promocion.route('/edit_promocion/<int:id_promocion>', methods=['GET', 'POST'])
def edit_promocion(id_promocion):
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        tipo = request.form['tipo']
        valor = request.form['valor']
        fecha_inicio = request.form['fecha_inicio']
        fecha_final = request.form['fecha_final']
        estado_promocion = request.form['estado_promocion']

        error = validate_promotion(nombre, descripcion, valor, fecha_inicio, fecha_final)
        if error:
            flash(error)
            return redirect(url_for('edit_promocion', id_promocion=id_promocion))

        if update_user(id_promocion, nombre, descripcion, tipo, valor, fecha_inicio, fecha_final, estado_promocion):
            flash('Product updated successfully!')
        else:
            flash('An error occurred while updating the product.')
        
        return redirect(url_for('promocion'))

    promocion = get_promocion_by_id(id_promocion)
    if promocion is None:
        flash('Product not found!')
        return redirect(url_for('promocion'))
    return render_template('edit_promocion.html', promocion=promocion)

@app_promocion.route('/eliminar_promocion/<int:id_promocion>', methods=['GET', 'POST'])
def eliminar_promocion(id_promocion):
    if request.method == 'POST':
        if delete_user(id_promocion):
            flash('Product deleted successfully!')
        else:
            flash('An error occurred while deleting the product.')
        return redirect(url_for('promocion'))

    promocion = get_promocion_by_id(id_promocion)
    if promocion is None:
        flash('Product not found!')
        return redirect(url_for('promocion'))
    return render_template('eliminar_promocion.html', promocion=promocion)

if __name__ == '__main__':
    app_promocion.run(debug=True, port=5014)
