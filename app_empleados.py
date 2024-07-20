from flask import Flask, render_template, request, redirect, url_for, flash
import re
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

def get_empleado(page, per_page):
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

def update_user(nombre, apellido, fecha_nacimiento, puesto_de_trabajo, fecha_contratacion, sucursal, salario, email, telefono, id_empleado):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """UPDATE empleados 
               SET nombre = %s, apellido = %s, fecha_nacimiento = %s, puesto_de_trabajo = %s, fecha_contratacion = %s, sucursal = %s, salario = %s, email = %s, telefono = %s 
               WHERE id_empleado = %s"""
    values = (nombre, apellido, fecha_nacimiento, puesto_de_trabajo, fecha_contratacion, sucursal, salario, email, telefono, id_empleado)
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


def search_users(search_criteria, search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = f"SELECT * FROM empleados WHERE {search_criteria} LIKE %s LIMIT %s OFFSET %s"
    values = (f'%{search_query}%', per_page, offset)
    try:
        cursor.execute(query, values)
        empleados = cursor.fetchall()
        count_query = f"SELECT COUNT(*) FROM empleados WHERE {search_criteria} LIKE %s"
        cursor.execute(count_query, (f'%{search_query}%',))
        total_count = cursor.fetchone()[0]
        return empleados, total_count
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def validar_campo(texto, permite_numeros=False):
    if not permite_numeros:
        if any(char.isdigit() for char in texto):
            return False
    if permite_numeros:
        if any(char.isalpha() for char in texto):
            return False
    if not re.match("^[A-Za-z0-9\s]*$", texto):  # permite letras, números y espacios
        return False
    if re.search(r'(.)\1\1', texto):  # No permite tres letras iguales seguidas
        return False
    if len(texto) < 3:
        return False
    return True

@app_empleados.route('/')
def index_empleados():
    return render_template('index_empleados.html')


@app_empleados.route('/empleados')
def empleados():
    search_criteria = request.args.get('search_criteria')
    search_query = request.args.get('search_query')
    page = int(request.args.get('page', 1))
    per_page = 10

    if search_criteria and search_query:
        empleados, total_count = search_users(search_criteria, search_query, page, per_page)
    else:
        empleados, total_count = get_empleado(page, per_page)
    
    total_pages = (total_count + per_page - 1) // per_page

    return render_template('empleados.html', empleados=empleados, search_criteria=search_criteria, search_query=search_query, page=page, total_pages=total_pages)



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

    # Validaciones
    if not all([nombre, apellido, fecha_nacimiento, puesto_de_trabajo, fecha_contratacion, sucursal, salario, telefono]):
        flash('¡Todos los campos obligatorios deben ser completados!')
        return redirect(url_for('index_empleados'))

    if not (validar_campo(nombre) and validar_campo(apellido) and validar_campo(puesto_de_trabajo) and validar_campo(sucursal) and validar_campo(email, permite_numeros=False)):
        flash('Los campos no pueden contener números, signos ni letras repetidas tres veces seguidas, y deben tener al menos 3 caracteres.')
        return redirect(url_for('index_empleados'))

    if not (validar_campo(salario, permite_numeros=True) and validar_campo(telefono, permite_numeros=True)):
        flash('El salario y teléfono solo pueden contener números y deben tener al menos 3 caracteres.')
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

        # Validaciones
        if not all([nombre, apellido, fecha_nacimiento, puesto_de_trabajo, fecha_contratacion, sucursal, salario]):
            flash('¡Todos los campos obligatorios deben ser completados!')
            return redirect(url_for('edit_empleado', id_empleado=id_empleado))

        if not (validar_campo(nombre) and validar_campo(apellido) and validar_campo(puesto_de_trabajo) and validar_campo(sucursal) and validar_campo(email, permite_numeros=False)):
            flash('Los campos no pueden contener números, signos ni letras repetidas tres veces seguidas, y deben tener al menos 3 caracteres.')
            return redirect(url_for('edit_empleado', id_empleado=id_empleado))

        if not (validar_campo(salario, permite_numeros=True) and validar_campo(telefono, permite_numeros=True)):
            flash('El salario y teléfono solo pueden contener números y deben tener al menos 3 caracteres.')
            return redirect(url_for('edit_empleado', id_empleado=id_empleado))

        if update_user(nombre, apellido, fecha_nacimiento, puesto_de_trabajo, fecha_contratacion, sucursal, salario, email, telefono, id_empleado):
            flash('¡Empleado actualizado exitosamente!')
            return redirect(url_for('empleados'))
        else:
            flash('Ocurrió un error al actualizar el empleado.')
        
        return redirect(url_for('edit_empleado', id_empleado=id_empleado))

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
