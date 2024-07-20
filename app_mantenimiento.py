from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

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
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def insert_user(id_equipo, fecha_mantenimiento, tipo_mantenimiento, id_tecnico, id_supervisor, detalles, estado_equipo):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    query = "INSERT INTO mantenimiento_equipos (id_equipo, fecha_mantenimiento, tipo_mantenimiento, id_tecnico, id_supervisor, detalles, estado_equipo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (id_equipo, fecha_mantenimiento, tipo_mantenimiento, id_tecnico, id_supervisor, detalles, estado_equipo)
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


def get_mantenimiento(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM mantenimiento_equipos LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        mantenimiento = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_mantenimiento = cursor.fetchone()[0]
        return mantenimiento, total_mantenimiento
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_mantenimiento_by_id(id_mantenimiento):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * from mantenimiento_equipos WHERE id_mantenimiento = %s"
    try:
        cursor.execute(query, (id_mantenimiento,))
        mantenimiento = cursor.fetchone()
        return mantenimiento
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_user(id_mantenimiento, id_equipo, fecha_mantenimiento, tipo_mantenimiento, id_tecnico, id_supervisor, detalles, estado_equipo):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE mantenimiento_equipos SET id_equipo = %s, fecha_mantenimiento = %s, tipo_mantenimiento = %s, id_tecnico = %s, id_supervisor = %s, detalles = %s, estado_equipo = %s WHERE id_mantenimiento = %s"
    values = (id_equipo, fecha_mantenimiento, tipo_mantenimiento, id_tecnico, id_supervisor, detalles, estado_equipo, id_mantenimiento)
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

def delete_user(id_mantenimiento):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE from mantenimiento_equipos WHERE id_mantenimiento = %s"
    try:
        cursor.execute(query, (id_mantenimiento,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def search_users(search_query, search_field, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = f"SELECT SQL_CALC_FOUND_ROWS * FROM mantenimiento_equipos WHERE {search_field} LIKE %s LIMIT %s OFFSET %s"
    values = (f'%{search_query}%', per_page, offset)

    try:
        cursor.execute(query, values)
        mantenimiento = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_mantenimiento = cursor.fetchone()[0]
        return mantenimiento, total_mantenimiento
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()



@app_mantenimiento.route('/')
def index_mantenimiento():
    return render_template('index_mantenimiento.html')


@app_mantenimiento.route('/mantenimiento')
def mantenimiento():
    search_query = request.args.get('search', '')
    search_field = request.args.get('search_field', 'id_mantenimiento')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if search_query:
        mantenimiento, total_mantenimiento = search_users(search_query, search_field, page, per_page)
    else:
        mantenimiento, total_mantenimiento = get_mantenimiento(page, per_page)

    total_pages = (total_mantenimiento + per_page - 1) // per_page
    return render_template('mantenimiento.html', mantenimiento=mantenimiento, search_query=search_query, search_field=search_field, page=page, per_page=per_page, total_mantenimiento=total_mantenimiento, total_pages=total_pages)

@app_mantenimiento.route('/submit', methods=['POST'])
def submit():
    id_equipo = request.form['id_equipo']
    fecha_mantenimiento = request.form['fecha_mantenimiento']
    tipo_mantenimiento = request.form['tipo_mantenimiento']
    id_tecnico = request.form['id_tecnico']
    id_supervisor = request.form['id_supervisor']
    detalles = request.form['detalles']
    estado_equipo = request.form['estado_equipo']

    if not id_equipo or not fecha_mantenimiento or not tipo_mantenimiento or not id_tecnico or not id_supervisor or not detalles or not estado_equipo:
        flash('All fields are required!')
        return redirect(url_for('index_mantenimiento'))

    inputs = [tipo_mantenimiento, detalles, estado_equipo]
    for input_value in inputs:
        if len(input_value) < 3:
            flash(f"{input_value} must have at least 3 characters")
            return redirect(url_for('index_mantenimiento'))
        if re.search(r'[^a-zA-Z]', input_value):
            flash(f"No special characters allowed in {input_value}")
            return redirect(url_for('index_mantenimiento'))
        if re.search(r'([a-zA-Z])\1\1', input_value):
            flash(f"No repeated letters more than twice in {input_value}")
            return redirect(url_for('index_mantenimiento'))
        if re.search(r'([aeiouAEIOU])\1', input_value):
            flash(f"No repeated vowels in {input_value}")
            return redirect(url_for('index_mantenimiento'))
        if re.search(r' {2,}', input_value):
            flash(f"No more than two spaces in {input_value}")
            return redirect(url_for('index_mantenimiento'))

    if insert_user(id_equipo, fecha_mantenimiento, tipo_mantenimiento, id_tecnico, id_supervisor, detalles, estado_equipo):
        flash('Product inserted successfully!')
    else:
        flash('An error occurred while inserting the product.')
    
    return redirect(url_for('index_mantenimiento'))

@app_mantenimiento.route('/edit_mantenimiento/<int:id_mantenimiento>', methods=['GET', 'POST'])
def edit_mantenimiento(id_mantenimiento):
    if request.method == 'POST':
        id_equipo = request.form['id_equipo']
        fecha_mantenimiento = request.form['fecha_mantenimiento']
        tipo_mantenimiento = request.form['tipo_mantenimiento']
        id_tecnico = request.form['id_tecnico']
        id_supervisor = request.form['id_supervisor']
        detalles = request.form['detalles']
        estado_equipo = request.form['estado_equipo']

        if not id_mantenimiento or not id_equipo or not fecha_mantenimiento or not tipo_mantenimiento or not id_tecnico or not id_supervisor or not detalles or not estado_equipo:
            flash('All fields are required!')
            return redirect(url_for('edit_mantenimiento', id_mantenimiento=id_mantenimiento))

        inputs = [tipo_mantenimiento, detalles, estado_equipo]
        for input_value in inputs:
            if len(input_value) < 3:
                flash(f"{input_value} must have at least 3 characters")
                return redirect(url_for('edit_mantenimiento', id_mantenimiento=id_mantenimiento))
            if re.search(r'[^a-zA-Z0-9 ]', input_value):
                flash(f"No special characters allowed in {input_value}")
                return redirect(url_for('edit_mantenimiento', id_mantenimiento=id_mantenimiento))
            if re.search(r'([a-zA-Z])\1\1', input_value):
                flash(f"No repeated letters more than twice in {input_value}")
                return redirect(url_for('edit_mantenimiento', id_mantenimiento=id_mantenimiento))
            if re.search(r'([aeiouAEIOU])\1', input_value):
                flash(f"No repeated vowels in {input_value}")
                return redirect(url_for('edit_mantenimiento', id_mantenimiento=id_mantenimiento))
            if re.search(r' {2,}', input_value):
                flash(f"No more than two spaces in {input_value}")
                return redirect(url_for('edit_mantenimiento', id_mantenimiento=id_mantenimiento))

        if update_user(id_mantenimiento, id_equipo, fecha_mantenimiento, tipo_mantenimiento, id_tecnico, id_supervisor, detalles, estado_equipo):
            flash('Product updated successfully!')
        else:
            flash('An error occurred while updating the product.')
        
        return redirect(url_for('mantenimiento'))

    mantenimiento = get_mantenimiento_by_id(id_mantenimiento)
    if mantenimiento is None:
        flash('Product not found!')
        return redirect(url_for('mantenimiento'))
    return render_template('edit_mantenimiento.html', mantenimiento=mantenimiento)

@app_mantenimiento.route('/eliminar_mantenimiento/<int:id_mantenimiento>')
def eliminar_mantenimiento(id_mantenimiento):
    if delete_user(id_mantenimiento):
        flash('Product deleted successfully!')
    else:
        flash('An error occurred while deleting the product.')
    return redirect(url_for('mantenimiento'))

if __name__ == '__main__':
    app_mantenimiento.run(debug=True,port=5016)
