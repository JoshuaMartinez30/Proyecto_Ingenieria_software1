from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re, datetime

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

def format_telefono(telefono):
    # Remove any non-numeric characters
    telefono = re.sub(r'\D', '', telefono)
    # Format as XXXX-XXXX
    return f"{telefono[:4]}-{telefono[4:]}"

def format_dni(documento):
    # Remove any non-numeric characters
    documento = re.sub(r'\D', '', documento)
    # Format as XXXX-XXXX
    return f"{documento[:3]}-{documento[4:]}-{documento[7:]}"

def insert_user(nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email,telefono,tipo,documento):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    query = "INSERT INTO empleados (nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email,telefono,tipo,documento) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
    values = (nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email,telefono,tipo,documento)
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

def get_empleados_by_id(id_empleado):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * from empleados WHERE id_empleado = %s"
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

def get_sucursal_name(id_sucursal):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT ciudad FROM sucursales WHERE id_sucursal = %s"
    try:
        cursor.execute(query, (id_sucursal,))
        sucursal = cursor.fetchone()
        return sucursal[0] if sucursal else None
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_user(id_empleado, nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email,telefono,tipo,documento):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE empleados SET nombre = %s, apellido = %s, fecha_nacimiento = %s, puesto_trabajo = %s, fecha_contratacion = %s, sucursal = %s,  email = %s , telefono = %s , tipo =%s ,   documento = %s WHERE id_empleado = %s"
    values = (nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email,telefono,tipo,documento, id_empleado)
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
    query = "DELETE from empleados WHERE id_empleado = %s"
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

def search_users(search_criteria,search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = f"SELECT SQL_CALC_FOUND_ROWS * FROM empleados WHERE {search_criteria} LIKE %s LIMIT %s OFFSET %s"
    values = (f'%{search_query}%', per_page, offset)

    try:
        cursor.execute(query, values)
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

def get_historico_empleados(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM historicos_empleados LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        historico_empleados = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_historico_empleados = cursor.fetchone()[0]
        return historico_empleados, total_historico_empleados
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
    sucursales=get_sucursales()
    return render_template('index_empleados.html', sucursales=sucursales)


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
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha_nacimiento = request.form['fecha_nacimiento']
    puesto_trabajo = request.form['puesto_trabajo']
    fecha_contratacion = request.form['fecha_contratacion']
    sucursal = request.form['sucursal']
    email = request.form['email']
    telefono = request.form['telefono']
    tipo = request.form['tipo']
    documento = request.form['documento']

      # Validación de fecha de nacimiento (mínimo 17 años)
    try:
            fecha_nacimiento_date = datetime.datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
            age = (datetime.datetime.now() - fecha_nacimiento_date).days // 365
            if age < 17:
                flash('Edad Minima 17 años.')
                return redirect(url_for('index_empleados'))
    except ValueError:
            flash('Fecha de nacimiento invalida.')
            return redirect(url_for('index_empleados'))

        # Validación de fecha de contratación (no más de una semana atrás)
    try:
            fecha_contratacion_date = datetime.datetime.strptime(fecha_contratacion, '%Y-%m-%d')
            if (datetime.datetime.now() - fecha_contratacion_date).days > 7:
                flash('El tiempo de registro ya paso.')
                return redirect(url_for('index_empleados'))
    except ValueError:
            flash('Invalid date format for hire date.')
            return redirect(url_for('index_empleados'))
    
   

    if re.match(r'^[23789]\d{7}$', telefono):
        telefono = format_telefono(telefono)
    else:
        flash('El número de teléfono no es válido. Debe empezar con 2, 3, 7, 8 o 9 y tener 8 dígitos.')
        return redirect(url_for('index_empleados'))

    if not nombre or not apellido or not fecha_nacimiento or not puesto_trabajo or not fecha_contratacion or not sucursal or not email or not telefono or not tipo or not documento:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('index_empleados'))
    
    

    if not nombre or not apellido or not fecha_nacimiento or not puesto_trabajo or not fecha_contratacion or not sucursal  or not email or not telefono or not tipo or not documento:
        flash('All fields are required!')
        return redirect(url_for('index_empleados'))

    inputs = []
    for input_value in inputs:
        if len(input_value) < 3:
            flash(f"{input_value} must have at least 3 characters")
            return redirect(url_for('index_empleados'))
        if re.search(r'[^a-zA-Z]', input_value):
            flash(f"No special characters allowed in {input_value}")
            return redirect(url_for('index_empleados'))
        if re.search(r'([a-zA-Z])\1\1', input_value):
            flash(f"No repeated letters more than twice in {input_value}")
            return redirect(url_for('index_empleados'))
        if re.search(r'([aeiouAEIOU])\1', input_value):
            flash(f"No repeated vowels in {input_value}")
            return redirect(url_for('index_empleados'))
        if re.search(r' {2,}', input_value):
            flash(f"No more than two spaces in {input_value}")
            return redirect(url_for('index_empleados'))

    if insert_user(nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email,telefono,tipo,documento):
        flash('Product inserted successfully!')
    else:
        flash('An error occurred while inserting the product.')
    
    return redirect(url_for('index_empleados'))

@app_empleados.route('/edit_empleados/<int:id_empleado>', methods=['GET', 'POST'])
def edit_empleados(id_empleado):
    empleado = get_empleados_by_id(id_empleado)
    if empleado is None:
        flash('Employee not found!')
        return redirect(url_for('empleados'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        puesto_trabajo = request.form['puesto_trabajo']
        fecha_contratacion = request.form['fecha_contratacion']
        sucursal = request.form['sucursal']
        email = request.form['email']
        telefono = request.form['telefono']
        tipo = request.form['tipo']
        documento = request.form['documento']

        inputs = [nombre, apellido, puesto_trabajo, email, tipo, documento]

        if not all(inputs):
            flash('All fields are required!')
            return redirect(url_for('edit_empleados', id_empleado=id_empleado))

        if not re.match(r'^\d{4}-?\d{4}$', telefono):
            flash('Invalid phone number format. It should be XXXX-XXXX.')
            return redirect(url_for('edit_empleados', id_empleado=id_empleado))

        if update_user(id_empleado, nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email, telefono, tipo, documento):
            flash('Employee updated successfully!')
            return redirect(url_for('empleados'))
        else:
            flash('An error occurred while updating the employee.')

    return render_template('edit_empleados.html', empleado=empleado)


@app_empleados.route('/eliminar_empleados/<int:id_empleado>', methods=['GET', 'POST'])
def eliminar_empleados(id_empleado):
    if request.method == 'POST':
        if delete_user(id_empleado):
            flash('Employee deleted successfully!')
        else:
            flash('An error occurred while deleting the employee.')
        return redirect(url_for('empleados'))

    empleado = get_empleados_by_id(id_empleado)
    if empleado is None:
        flash('Employee not found!')
        return redirect(url_for('empleados'))

    return render_template('eliminar_empleados.html', empleado=empleado)

if __name__ == '__main__':
    app_empleados.run(debug=True,port=5003)
