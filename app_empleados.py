from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re
import datetime

app_empleados = Flask(__name__)
app_empleados.secret_key = 'your_secret_key'

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="qEeKLgpIkdarsoNT",
            database="proyecto_is1"
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def insert_user(nombre, apellido, fecha_nacimiento, id_puesto, fecha_contratacion, id_sucursal, email, telefono, tipo, documento, password):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """INSERT INTO empleados (nombre, apellido, fecha_nacimiento, id_puesto, fecha_contratacion, id_sucursal, email, telefono, tipo, documento, password)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (nombre, apellido, fecha_nacimiento, id_puesto, fecha_contratacion, id_sucursal, email, telefono, tipo, documento, password)
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Insert successful")  # Debugging line
        return True
    except Error as e:
        print(f"The error '{e}' occurred")  # Ensure this prints out any issues
        return False
    finally:
        cursor.close()
        connection.close()

def update_user(id_empleado, nombre, apellido, fecha_nacimiento, id_puesto, fecha_contratacion, id_sucursal, email, telefono, tipo, documento, password):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """UPDATE empleados SET nombre = %s, apellido = %s, fecha_nacimiento = %s, id_puesto = %s,
               fecha_contratacion = %s, id_sucursal = %s, email = %s, telefono = %s, tipo = %s, documento = %s, password = %s
               WHERE id_empleado = %s"""
    values = (nombre, apellido, fecha_nacimiento, id_puesto, fecha_contratacion, id_sucursal, email, telefono, tipo, documento, password, id_empleado)
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

def delete_user(id_empleado):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM empleados WHERE id_empleado = %s"
    try:
        cursor.execute(query, (id_empleado,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def get_empleados(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM empleados LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        empleados = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_empleados = cursor.fetchone()[0]
        return empleados, total_empleados
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def search_users(search_query, search_criteria, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = f"SELECT SQL_CALC_FOUND_ROWS * FROM empleados WHERE {search_criteria} LIKE %s LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (f"%{search_query}%", per_page, offset))
        empleados = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_empleados = cursor.fetchone()[0]
        return empleados, total_empleados
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_empleados_by_id(id_empleado):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM empleados WHERE id_empleado = %s"
    try:
        cursor.execute(query, (id_empleado,))
        empleado = cursor.fetchone()
        return empleado
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def get_sucursales():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_sucursal, ciudad FROM sucursales"
    try:
        cursor.execute(query)
        sucursales = cursor.fetchall()
        return sucursales
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def get_puestos_de_trabajo():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_puesto, puesto_trabajo FROM puesto_de_trabajo"
    try:
        cursor.execute(query)
        puestos = cursor.fetchall()
        return puestos
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()


def get_historico_empleados(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM historico_empleados LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        historicos = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_historicos = cursor.fetchone()[0]
        return historicos, total_historicos
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

@app_empleados.route('/historico_empleados')
def historico_empleados():
    page = request.args.get('page', 1, type=int)
    per_page = int(request.args.get('per_page', 10))
    historicos, total_historicos = get_historico_empleados(page, per_page)

    total_pages = (total_historicos + per_page - 1) // per_page
    return render_template('historico_empleados.html', historicos=historicos, page=page, per_page=per_page, total_historicos=total_historicos, total_pages=total_pages)

@app_empleados.route('/')
def index_empleados():
    sucursales = get_sucursales()
    puestos_de_trabajo = get_puestos_de_trabajo()  # Obtener puestos de trabajo
    return render_template('index_empleados.html', puestos_de_trabajo=puestos_de_trabajo, sucursales=sucursales)

@app_empleados.route('/empleados')
def empleados():
    search_query = request.args.get('search', '')
    search_criteria = request.args.get('search_criteria', 'id_empleado')
    page = request.args.get('page', 1, type=int)
    per_page = int(request.args.get('per_page', 5))

    if search_query:
        empleados, total_empleados = search_users(search_query, search_criteria, page, per_page)
    else:
        empleados, total_empleados = get_empleados(page, per_page)

    total_pages = (total_empleados + per_page - 1) // per_page
    return render_template('empleados.html', empleados=empleados, search_query=search_query, search_criteria=search_criteria, page=page, per_page=per_page, total_empleados=total_empleados, total_pages=total_pages)

@app_empleados.route('/submit', methods=['POST'])
def submit():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    id_puesto = request.form.get('id_puesto')
    fecha_contratacion = request.form.get('fecha_contratacion')
    id_sucursal = request.form.get('id_sucursal')  # Usando id_sucursal
    email = request.form.get('email')
    telefono = request.form.get('telefono')
    tipo = request.form.get('tipo')
    documento = request.form.get('documento')
    password = request.form.get('password')

    
    if insert_user(nombre, apellido, fecha_nacimiento, id_puesto, fecha_contratacion, id_sucursal, email, telefono, tipo, documento, password):
        flash("Empleado agregado correctamente.")
    else:
        flash("Error al agregar el empleado.")

    return redirect(url_for('empleados'))


@app_empleados.route('/edit_empleados/<int:id_empleado>', methods=['GET', 'POST'])
def edit_empleados(id_empleado):
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    id_puesto = request.form.get('id_puesto')
    fecha_contratacion = request.form.get('fecha_contratacion')
    id_sucursal = request.form.get('id_sucursal')  # Usando id_sucursal
    email = request.form.get('email')
    telefono = request.form.get('telefono')
    tipo = request.form.get('tipo')
    documento = request.form.get('documento')
    password = request.form.get('password')



    empleado = get_empleados_by_id(id_empleado)
    if not empleado:
        flash("Empleado no encontrado.")
        return redirect(url_for('empleados'))
    
    if update_user(id_empleado, nombre, apellido, fecha_nacimiento, id_puesto, fecha_contratacion, id_sucursal, email, telefono, tipo, documento, password):
        flash('Usuario actualizado exitosamente.')
    else:
        flash('Ocurrió un error al actualizar el usuario.')
    
    sucursales = get_sucursales()
    puestos_de_trabajo = get_puestos_de_trabajo()
    return render_template('edit_empleados.html', empleado=empleado, puestos_de_trabajo=puestos_de_trabajo, sucursales=sucursales)

@app_empleados.route('/eliminar_empleados/<int:id_empleado>', methods=['GET', 'POST'])
def eliminar_empleados(id_empleado):
    if request.method == 'POST':
        if delete_user(id_empleado):
            flash('¡empleados eliminada exitosamente!')
            return redirect(url_for('empleados'))
        else:
            flash('Ocurrió un error al eliminar el empleados. Por favor, intente nuevamente.')
            return redirect(url_for('empleados'))

    empleados = get_empleados_by_id(id_empleado)
    if empleados is None:
        flash('empleados no encontrada.')
        return redirect(url_for('empleados'))

    return render_template('eliminar_empleados.html', empleados=empleados)




if __name__ == '__main__':
    app_empleados.run(debug=True,port=5003)
