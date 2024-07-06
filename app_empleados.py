from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app_empleados = Flask(__name__)
app_empleados.secret_key = 'your_secret_key'

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

def insert_user(nombre, apellido, fecha_nacimiento, puesto_de_trabajo, fecha_contratacion, sucursal, salario, email, telefono):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    query = """INSERT INTO empleados (nombre, apellido, fecha_nacimiento, puesto_de_trabajo, fecha_contratacion, sucursal, salario, email, telefono) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (nombre, apellido, fecha_nacimiento, puesto_de_trabajo, fecha_contratacion, sucursal, salario, email, telefono)
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

def get_empleado():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM empleados"
    try:
        cursor.execute(query)
        empleados = cursor.fetchall()
        return empleados
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def get_empleado_by_id(id_empleado):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM empleados WHERE id_empleado = %s"
    try:
        cursor.execute(query, (id_empleado,))
        empleados = cursor.fetchone()
        return empleados
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_user(nombre, apellido, fecha_nacimiento, puesto_de_trabajo, fecha_contratacion, sucursal, salario, email, telefono):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """UPDATE empleados SET nombre = %s, apellido = %s, fecha_nacimiento = %s, puesto_de_trabajo = %s, fecha_contratacion = %s, sucursal = %s, salario = %s, email = %s, telefono = %s WHERE id_empleado = %s"""
    values = (nombre, apellido, fecha_nacimiento, puesto_de_trabajo, fecha_contratacion, sucursal, salario, email, telefono)
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

def search_users(search_query):
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM empleados WHERE nombre LIKE %s OR apellido LIKE %s OR puesto_de_trabajo LIKE %s OR sucursal LIKE %s"
    values = (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
    try:
        cursor.execute(query, values)
        empleados = cursor.fetchall()
        return empleados
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

@app_empleados.route('/')
def index_empleados():
    return render_template('index_empleados.html')

@app_empleados.route('/empleados')
def empleados():
    search_query = request.args.get('search')
    if search_query:
        empleados = search_users(search_query)
    else:
        empleados = get_empleado()
    return render_template('empleados.html', empleados=empleados, search_query=search_query)


@app_empleados.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha_nacimiento = request.form['fecha_nacimiento']
    puesto_de_trabajo = request.form['puesto_de_trabajo']
    fecha_contratacion = request.form['fecha_contratacion']
    sucursal = request.form['sucursal']
    salario = request.form['salario']
    email = request.form['email']
    telefono = request.form['telefono']

    if not nombre or not apellido or not fecha_nacimiento or not puesto_de_trabajo or not fecha_contratacion or not sucursal or not salario or not telefono:
        flash('¡Todos los campos obligatorios deben ser completados!')
        return redirect(url_for('index_empleados'))

    if insert_user(nombre, apellido, fecha_nacimiento, puesto_de_trabajo, fecha_contratacion, sucursal, salario, email, telefono):
        flash('¡Empleado ingresado exitosamente!')
    else:
        flash('Ocurrió un error al ingresar el empleado.')

    return redirect(url_for('index_empleados'))

@app_empleados.route('/edit_empleado/<int:id_empleado>', methods=['GET', 'POST'])
def edit_empleado(id_empleado):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        puesto_de_trabajo = request.form['puesto_de_trabajo']
        fecha_contratacion = request.form['fecha_contratacion']
        sucursal = request.form['sucursal']
        salario = request.form['salario']
        email = request.form['email']
        telefono = request.form['telefono']

        if not nombre or not apellido or not fecha_nacimiento or not puesto_de_trabajo or not fecha_contratacion or not sucursal or not salario:
            flash('¡Todos los campos obligatorios deben ser completados!')
            return redirect(url_for('edit_empleado', id_empleado=id_empleado))  # Corregido el nombre de la función

        if update_user(id_empleado, nombre, apellido, fecha_nacimiento, puesto_de_trabajo, fecha_contratacion, sucursal, salario, email, telefono):
            flash('¡Empleado actualizado exitosamente!')
        else:
            flash('Ocurrió un error al actualizar el empleado.')
        
        return redirect(url_for('empleados'))

    empleado = get_empleado_by_id(id_empleado)
    if empleado is None:
        flash('¡Empleado no encontrado!')
        return redirect(url_for('empleados'))
    
    return render_template('edit_empleados.html', empleado=empleado)

@app_empleados.route('/eliminar_empleado/<int:id_empleado>', methods=['GET', 'POST'])
def eliminar_empleado(id_empleado):
    if request.method == 'POST':
        if delete_user(id_empleado):
            flash('¡Empleado eliminado exitosamente!')
        else:
            flash('Ocurrió un error al eliminar el empleado.')
        return redirect(url_for('empleados'))

    empleado = get_empleado_by_id(id_empleado)
    if empleado is None:
        flash('¡Empleado no encontrado!')
        return redirect(url_for('empleados'))

    return render_template('eliminar_empleados.html', empleado=empleado)


if __name__ == '__main__':
    app_empleados.run(debug=True, port=5003)