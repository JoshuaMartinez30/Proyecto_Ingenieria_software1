from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

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

def validate_promotion(nombre, valor):
    regexNoTresRepetidas = re.compile(r'(.)\1\1')
    regexNoLetrasEnNumero = re.compile(r'[a-zA-Z]')
    
    if regexNoTresRepetidas.search(nombre):
        return "No se permiten tres letras repetidas consecutivas."

    if regexNoLetrasEnNumero.search(valor):
        return "No se permiten letras en el campo de valor."

    return None

def insert_promocion(nombre, valor):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """INSERT INTO promocion (nombre, valor)
               VALUES (%s, %s)"""
    values = (nombre, valor)
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

def get_promocion(limit, offset):
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM promocion LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (limit, offset))
        promociones = cursor.fetchall()
        return promociones
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def get_promocion_count():
    connection = create_connection()
    if connection is None:
        return 0
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM promocion"
    try:
        cursor.execute(query)
        count = cursor.fetchone()[0]
        return count
    except Error as e:
        print(f"The error '{e}' occurred")
        return 0
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

def update_promocion(id_promocion, nombre, valor):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """UPDATE promocion SET nombre = %s, valor = %s 
                WHERE id_promocion = %s"""
    values = (nombre, valor, id_promocion)
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

def delete_promocion(id_promocion):
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

@app_promocion.route('/')
def index_promocion():
    return render_template('index_promocion.html')

@app_promocion.route('/promocion', methods=['GET'])
def promocion():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    promociones = get_promocion(per_page, (page-1)*per_page)
    total_promociones = get_promocion_count()

    total_pages = (total_promociones + per_page - 1) // per_page

    return render_template('promocion.html', 
                           promociones=promociones, 
                           total_pages=total_pages, 
                           current_page=page, 
                           per_page=per_page)

@app_promocion.route('/promocion/agregar', methods=['GET', 'POST'])
def agregar_promocion():
    if request.method == 'POST':
        nombre = request.form['nombre']
        valor = request.form['valor']
        
        error = validate_promotion(nombre, valor)
        if error:
            flash(error)
            return redirect(url_for('agregar_promocion'))
        
        if insert_promocion(nombre, valor):
            flash("Promoción agregada con éxito")
        else:
            flash("Error al agregar la promoción")

        return redirect(url_for('promocion'))
    return render_template('agregar_promocion.html')

@app_promocion.route('/promocion/editar/<int:id_promocion>', methods=['GET', 'POST'])
def editar_promocion(id_promocion):
    promocion = get_promocion_by_id(id_promocion)
    if not promocion:
        flash("Promoción no encontrada")
        return redirect(url_for('promocion'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()  # Elimina espacios en blanco
        valor = request.form.get('valor', '').strip()
        
        error = validate_promotion(nombre, valor)
        if error:
            flash(error)
            return redirect(url_for('editar_promocion', id_promocion=id_promocion))

        if update_promocion(id_promocion, nombre, valor):
            flash("Promoción actualizada con éxito")
        else:
            flash("Error al actualizar la promoción")

        return redirect(url_for('promocion'))

    return render_template('edit_promocion.html', promocion=promocion)

@app_promocion.route('/promocion/eliminar/<int:id_promocion>', methods=['GET', 'POST'])
def eliminar_promocion(id_promocion):
    if request.method == 'POST':
        if delete_promocion(id_promocion):
            flash('¡Promoción eliminada exitosamente!')
            return redirect(url_for('promocion'))
        else:
            flash('Ocurrió un error al eliminar la promoción. Por favor, intente nuevamente.')

    promocion = get_promocion_by_id(id_promocion)
    if promocion is None:
        flash('Promoción no encontrada.')
        return redirect(url_for('promocion'))

    return render_template('eliminar_promocion.html', promocion=promocion)

if __name__ == "__main__":
    app_promocion.run(debug=True, port=5014)
