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
    telefono = re.sub(r'\D', '', telefono)
    return f"{telefono[:4]}-{telefono[4:]}"

def format_dni(documento):
    documento = re.sub(r'\D', '', documento)
    return f"{documento[:4]}-{documento[4:8]}-{documento[8:]}"

def insert_user(nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email, telefono, tipo, documento):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """INSERT INTO empleados (nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email, telefono, tipo, documento)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email, telefono, tipo, documento)
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

def update_user(id_empleado, nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email, telefono, tipo, documento):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """UPDATE empleados SET nombre = %s, apellido = %s, fecha_nacimiento = %s, puesto_trabajo = %s,
               fecha_contratacion = %s, sucursal = %s, email = %s, telefono = %s, tipo = %s, documento = %s
               WHERE id_empleado = %s"""
    values = (nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email, telefono, tipo, documento, id_empleado)
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

    tipo_documento_validations = {
        'Número de Identidad': r'^\d{13}$',
        'RTN': r'^\d{14}$',
        'Pasaporte': r'^E\d{7}$'
    }

    # Validación de fecha de nacimiento (mínimo 17 años)
    try:
        fecha_nacimiento_date = datetime.datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
        age = (datetime.datetime.now() - fecha_nacimiento_date).days // 365
        if age < 17:
            flash('Edad mínima 17 años.')
            return redirect(url_for('index_empleados'))
    except ValueError:
        flash('Fecha de nacimiento inválida.')
        return redirect(url_for('index_empleados'))

    # Validación de fecha de contratación (no puede ser mayor a 7 días en el pasado)
    try:
        fecha_contratacion_date = datetime.datetime.strptime(fecha_contratacion, '%Y-%m-%d')
        if (datetime.datetime.now() - fecha_contratacion_date).days > 7:
            flash('El tiempo de registro ya pasó.')
            return redirect(url_for('index_empleados'))
    except ValueError:
        flash('Fecha de contratación inválida.')
        return redirect(url_for('index_empleados'))

    # Validación de teléfono (debe comenzar con 2, 3, 7, 8 o 9 y tener 8 dígitos)
    if not re.match(r'^[23789]\d{7}$', telefono):
        flash('El número de teléfono no es válido. Debe empezar con 2, 3, 7, 8 o 9 y tener 8 dígitos.')
        return redirect(url_for('index_empleados'))
    telefono = format_telefono(telefono)

    if not all([nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email, telefono, tipo, documento]):
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('index_empleados'))

    for input_value in [nombre, apellido, puesto_trabajo, email, tipo]:
        if len(input_value) < 3:
            flash(f"{input_value} debe tener al menos 3 caracteres.")
            return redirect(url_for('index_empleados'))
        if len(input_value) > 20:
            flash(f"{input_value} debe tener menos de 20 caracteres.")
            return redirect(url_for('index_empleados'))
        if re.search(r'\d', input_value):
            flash(f"{input_value} no debe contener números.")
            return redirect(url_for('index_empleados'))
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', input_value):
            flash(f"{input_value} no debe contener caracteres especiales.")
            return redirect(url_for('index_empleados'))

    # Validación del documento
    if tipo not in tipo_documento_validations:
        flash('Tipo de documento no válido.')
        return redirect(url_for('index_empleados'))
    
    document_pattern = tipo_documento_validations[tipo]
    if not re.match(document_pattern, documento):
        flash('Documento no válido.')
        return redirect(url_for('index_empleados'))

    if tipo == 'Número de Identidad':
        documento = format_dni(documento)

    success = insert_user(nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email, telefono, tipo, documento)
    if success:
        flash('Empleado añadido con éxito.')
    else:
        flash('Error al añadir el empleado.')
    return redirect(url_for('index_empleados'))

@app_empleados.route('/edit/<int:id_empleado>', methods=['GET', 'POST'])
def edit_empleados(id_empleado):
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

        tipo_documento_validations = {
            'Número de Identidad': r'^\d{13}$',
            'RTN': r'^\d{14}$',
            'Pasaporte': r'^E\d{7}$'
        }

        # Validación de fecha de nacimiento (mínimo 17 años)
        try:
            fecha_nacimiento_date = datetime.datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
            age = (datetime.datetime.now() - fecha_nacimiento_date).days // 365
            if age < 18:
                flash('Edad mínima 18 años.')
                return redirect(url_for('edit_empleados', id_empleado=id_empleado))
        except ValueError:
            flash('Fecha de nacimiento inválida.')
            return redirect(url_for('edit_empleados', id_empleado=id_empleado))

        # Validación de fecha de contratación (no puede ser mayor a 7 días en el pasado)
        try:
            fecha_contratacion_date = datetime.datetime.strptime(fecha_contratacion, '%Y-%m-%d')
            if (datetime.datetime.now() - fecha_contratacion_date).days > 7:
                flash('El tiempo de registro ya pasó.')
                return redirect(url_for('edit_empleados', id_empleado=id_empleado))
        except ValueError:
            flash('Fecha de contratación inválida.')
            return redirect(url_for('edit_empleados', id_empleado=id_empleado))

        # Validación de teléfono (debe comenzar con 2, 3, 7, 8 o 9 y tener 8 dígitos)
        if not re.match(r'^[23789]\d{7}$', telefono):
            flash('El número de teléfono no es válido. Debe empezar con 2, 3, 7, 8 o 9 y tener 8 dígitos.')
            return redirect(url_for('edit_empleados', id_empleado=id_empleado))
        telefono = format_telefono(telefono)

        if not all([nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email, telefono, tipo, documento]):
            flash('Todos los campos son obligatorios.')
            return redirect(url_for('edit_empleados', id_empleado=id_empleado))

        for input_value in [nombre, apellido, puesto_trabajo, email, tipo]:
            if len(input_value) < 3:
                flash(f"{input_value} debe tener al menos 3 caracteres.")
                return redirect(url_for('edit_empleados', id_empleado=id_empleado))
            if len(input_value) > 20:
                flash(f"{input_value} debe tener menos de 20 caracteres.")
                return redirect(url_for('edit_empleados', id_empleado=id_empleado))
            if re.search(r'\d', input_value):
                flash(f"{input_value} no debe contener números.")
                return redirect(url_for('edit_empleados', id_empleado=id_empleado))
            if re.search(r'[!@#$%^&*(),.?":{}|<>]', input_value):
                flash(f"{input_value} no debe contener caracteres especiales.")
                return redirect(url_for('edit_empleados', id_empleado=id_empleado))

        if tipo not in tipo_documento_validations:
            flash('Tipo de documento no válido.')
            return redirect(url_for('edit_empleados', id_empleado=id_empleado))
        
        document_pattern = tipo_documento_validations[tipo]
        if not re.match(document_pattern, documento):
            flash('Documento no válido.')
            return redirect(url_for('edit_empleados', id_empleado=id_empleado))

        if tipo == 'Número de Identidad':
            documento = format_dni(documento)

        success = update_user(id_empleado, nombre, apellido, fecha_nacimiento, puesto_trabajo, fecha_contratacion, sucursal, email, telefono, tipo, documento)
        if success:
            flash('Empleado actualizado con éxito.')
        else:
            flash('Error al actualizar el empleado.')
        return redirect(url_for('empleados'))

    empleado = get_empleados_by_id(id_empleado)
    if empleado is None:
        flash('Empleado no encontrado.')
        return redirect(url_for('empleados'))

    sucursales = get_sucursales()
    return render_template('edit_empleados.html', empleado=empleado, sucursales=sucursales)

@app_empleados.route('/delete/<int:id_empleado>', methods=['POST'])
def eliminar_empleados(id_empleado):
    success = delete_user(id_empleado)
    if success:
        flash('Empleado eliminado con éxito.')
    else:
        flash('Error al eliminar el empleado.')
    return redirect(url_for('empleados'))

if __name__ == '__main__':
    app_empleados.run(debug=True,port=5003)
