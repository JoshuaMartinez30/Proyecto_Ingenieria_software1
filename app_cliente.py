from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

app_cliente = Flask(__name__)
app_cliente.secret_key = 'tu_clave_secreta'

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
            print("Conexión a la base de datos MySQL exitosa")
    except Error as e:
        print(f"El error '{e}' ocurrió")
    return connection

def insert_user(nombre, apellido, fecha_nacimiento, email, telefono, direccion, fecha_registro):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "INSERT INTO cliente (nombre, apellido, fecha_nacimiento, email, telefono, direccion, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (nombre, apellido, fecha_nacimiento, email, telefono, direccion, fecha_registro)
    try:
        cursor.execute(query, values)
        connection.commit()
        return True
    except Error as e:
        print(f"El error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

def get_cliente(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM cliente LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        cliente = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_cliente = cursor.fetchone()[0]
        return cliente, total_cliente
    except Error as e:
        print(f"El error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_cliente_by_id(id_cliente):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM cliente WHERE id_cliente = %s"
    try:
        cursor.execute(query, (id_cliente,))
        cliente = cursor.fetchone()
        return cliente
    except Error as e:
        print(f"El error '{e}' ocurrió")
        return None
    finally:
        cursor.close()
        connection.close()

def update_user(id_cliente, nombre, apellido, fecha_nacimiento, email, telefono, direccion, fecha_registro):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE cliente SET nombre = %s, apellido = %s, fecha_nacimiento = %s, email = %s, telefono = %s, direccion = %s, fecha_registro = %s WHERE id_cliente = %s"
    values = (nombre, apellido, fecha_nacimiento, email, telefono, direccion, fecha_registro, id_cliente)
    try:
        cursor.execute(query, values)
        connection.commit()
        return True
    except Error as e:
        print(f"El error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_user(id_cliente):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM cliente WHERE id_cliente = %s"
    try:
        cursor.execute(query, (id_cliente,))
        connection.commit()
        return True
    except Error as e:
        print(f"El error '{e}' ocurrió")
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
    query = f"SELECT SQL_CALC_FOUND_ROWS * FROM cliente WHERE {search_field} LIKE %s LIMIT %s OFFSET %s"
    values = (f'%{search_query}%', per_page, offset)
    try:
        cursor.execute(query, values)
        cliente = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_cliente = cursor.fetchone()[0]
        return cliente, total_cliente
    except Error as e:
        print(f"El error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def validate_input(input_str, field_type):
    if not input_str:
        return "Este campo es obligatorio."
    if len(input_str) < 3 or len(input_str) > 20:
        return "Este campo debe tener entre 3 y 20 caracteres."
    if re.search(r'(.)\1\1', input_str):
        return "No se puede repetir tres veces un mismo carácter."
    if field_type == 'telefono':
        if not re.fullmatch(r'^\d{6,10}$', input_str):
            return "Este campo solo puede contener números y debe tener entre 6 y 10 dígitos."
    else:
        if re.fullmatch(r'[\d]+', input_str):
            return "Este campo no puede contener números."
        if re.fullmatch(r'[\W_]+', input_str):
            return "Este campo no puede contener solo signos."
    return None

def validate_email(email):
    if len(email) < 8:
        return "El correo electrónico debe tener al menos 8 caracteres."
    if '@' not in email:
        return "El correo electrónico debe contener '@'."
    return None

@app_cliente.route('/')
def index_cliente():
    return render_template('index_cliente.html')

@app_cliente.route('/cliente')
def cliente():
    search_query = request.args.get('search', '')
    search_field = request.args.get('search_field', 'nombre')  # Usa 'nombre' como valor por defecto
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if search_query:
        cliente, total_cliente = search_users(search_query, search_field, page, per_page)
    else:
        cliente, total_cliente = get_cliente(page, per_page)

    total_pages = (total_cliente + per_page - 1) // per_page
    return render_template('cliente.html', cliente=cliente, search_query=search_query, search_field=search_field, page=page, per_page=per_page, total_cliente=total_cliente, total_pages=total_pages)

@app_cliente.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha_nacimiento = request.form['fecha_nacimiento']
    email = request.form['email']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    fecha_registro = request.form['fecha_registro']

    for field, field_type in zip([nombre, apellido, direccion, telefono], ['text', 'text', 'text', 'telefono']):
        error = validate_input(field, field_type)
        if error:
            flash(f"{field_type.capitalize()}: {error}")
            return redirect(url_for('index_cliente'))

    email_error = validate_email(email)
    if email_error:
        flash(f"Email: {email_error}")
        return redirect(url_for('index_cliente'))

    if insert_user(nombre, apellido, fecha_nacimiento, email, telefono, direccion, fecha_registro):
        flash('¡Cliente insertado exitosamente!')
    else:
        flash('Ocurrió un error al insertar el cliente.')
    
    return redirect(url_for('index_cliente'))

@app_cliente.route('/edit_cliente/<int:id_cliente>', methods=['GET', 'POST'])
def edit_cliente(id_cliente):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        fecha_registro = request.form['fecha_registro']

        for field, field_type in zip([nombre, apellido, direccion, telefono], ['text', 'text', 'text', 'telefono']):
            error = validate_input(field, field_type)
            if error:
                flash(f"{field_type.capitalize()}: {error}")
                return redirect(url_for('edit_cliente', id_cliente=id_cliente))

        email_error = validate_email(email)
        if email_error:
            flash(f"Email: {email_error}")
            return redirect(url_for('edit_cliente', id_cliente=id_cliente))

        if update_user(id_cliente, nombre, apellido, fecha_nacimiento, email, telefono, direccion, fecha_registro):
            flash('¡Cliente actualizado exitosamente!')
        else:
            flash('Ocurrió un error al actualizar el cliente.')
        
        return redirect(url_for('cliente'))

    cliente = get_cliente_by_id(id_cliente)
    if cliente is None:
        flash('¡Cliente no encontrado!')
        return redirect(url_for('cliente'))
    return render_template('edit_cliente.html', cliente=cliente)

@app_cliente.route('/eliminar_cliente/<int:id_cliente>', methods=['GET', 'POST'])
def eliminar_cliente(id_cliente):
    if request.method == 'POST':
        if delete_user(id_cliente):
            flash('¡Cliente eliminado exitosamente!')
        else:
            flash('Ocurrió un error al eliminar el cliente.')
        return redirect(url_for('cliente'))

    cliente = get_cliente_by_id(id_cliente)
    if cliente is None:
        flash('¡Cliente no encontrado!')
        return redirect(url_for('cliente'))
    return render_template('eliminar_cliente.html', cliente=cliente)

if __name__ == '__main__':
    app_cliente.run(debug=True, port=5004)
