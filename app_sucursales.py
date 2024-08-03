from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

app_sucursales = Flask(__name__)
app_sucursales.secret_key = 'your_secret_key'

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
    cleaned_phone = re.sub(r'[^0-9-]', '', telefono)
    parts = cleaned_phone.split('-')
    
    if len(parts) == 1:
        if len(parts[0]) == 8:
            return f"{parts[0][:4]}-{parts[0][4:]}"
        return cleaned_phone
    
    elif len(parts) == 2:
        if len(parts[0]) == 4 and len(parts[1]) == 4:
            return f"{parts[0]}-{parts[1]}"
    
    return cleaned_phone

def insert_sucursal(ciudad, telefono):
    connection = create_connection()
    if connection is None:
        return "error", None

    cursor = connection.cursor()
    errors = []

    formatted_telefono = format_telefono(telefono)

    query = "SELECT COUNT(*) FROM sucursales WHERE telefono = %s"
    cursor.execute(query, (formatted_telefono,))
    if cursor.fetchone()[0] > 0:
        errors.append("telefono_exists")

    query = "SELECT COUNT(*) FROM sucursales WHERE ciudad = %s"
    cursor.execute(query, (ciudad,))
    if cursor.fetchone()[0] > 0:
        errors.append("ciudad_exists")

    if errors:
        cursor.close()
        connection.close()
        return "error", errors

    query = "INSERT INTO sucursales (ciudad, telefono) VALUES (%s, %s)"
    values = (ciudad, formatted_telefono)
    try:
        cursor.execute(query, values)
        connection.commit()
        return "success", None
    except Error as e:
        print(f"The error '{e}' occurred")
        return "error", ["database_error"]
    finally:
        cursor.close()
        connection.close()

def update_sucursal(id_sucursal, ciudad, telefono):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    formatted_telefono = format_telefono(telefono)
    query = """UPDATE sucursales SET ciudad = %s, telefono = %s WHERE id_sucursal = %s"""
    values = (ciudad, formatted_telefono, id_sucursal)
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

def delete_sucursal(id_sucursal):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM sucursales WHERE id_sucursal = %s"
    try:
        cursor.execute(query, (id_sucursal,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def get_sucursales(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS id_sucursal, ciudad, telefono FROM sucursales LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        sucursales = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_sucursales = cursor.fetchone()[0]
        return sucursales, total_sucursales
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def search_sucursales(search_criteria, search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = f"SELECT SQL_CALC_FOUND_ROWS * FROM sucursales WHERE {search_criteria} LIKE %s LIMIT %s OFFSET %s"
    values = (f'%{search_query}%', per_page, offset)
    try:
        cursor.execute(query, values)
        sucursales = cursor.fetchall()
        cursor.execute(f"SELECT FOUND_ROWS()")
        total_count = cursor.fetchone()[0]
        return sucursales, total_count
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_sucursal_by_id(id_sucursal):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT id_sucursal, ciudad, telefono FROM sucursales WHERE id_sucursal = %s"
    cursor.execute(query, (id_sucursal,))
    sucursal = cursor.fetchone()
    cursor.close()
    connection.close()
    return sucursal

VALID_CIUDAD_REGEX = re.compile(r'^[a-zA-Z\s]+$')  # Only letters and spaces
VALID_TELEFONO_REGEX = re.compile(r'^\d{4}-\d{4}$|^\d{8}$')  # Allows 1234-5678 or 12345678

@app_sucursales.route('/')
def index_sucursales():
    return render_template('index_sucursales.html')

@app_sucursales.route('/sucursales')
def sucursales():
    search_criteria = request.args.get('search_criteria', 'ciudad')
    search_query = request.args.get('search_query', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))

    if search_query:
        sucursales, total_count = search_sucursales(search_criteria, search_query, page, per_page)
    else:
        sucursales, total_count = get_sucursales(page, per_page)
    
    total_pages = (total_count + per_page - 1) // per_page

    return render_template('sucursales.html', sucursales=sucursales, search_criteria=search_criteria, search_query=search_query, page=page, total_pages=total_pages, per_page=per_page)

@app_sucursales.route('/submit', methods=['POST'])
def submit():
    ciudad = request.form.get('ciudad')
    telefono = request.form.get('telefono')

    errors = []

    if not ciudad or not telefono:
        errors.append('¡Todos los campos obligatorios deben ser completados!')
    else:
        if not VALID_CIUDAD_REGEX.match(ciudad):
            errors.append('La ciudad contiene caracteres no permitidos. Solo se permiten letras y espacios.')

        if not VALID_TELEFONO_REGEX.match(telefono):
            errors.append('El teléfono contiene caracteres no permitidos. Solo se permiten números y un guión en el formato xxxx-xxxx.')

    if not errors:
        result, db_errors = insert_sucursal(ciudad, telefono)
        if result == "success":
            flash('¡Sucursal ingresada exitosamente!')
        elif db_errors:
            for db_error in db_errors:
                if db_error == "telefono_exists":
                    errors.append('El teléfono ya está registrado en otra sucursal. Por favor, ingrese uno nuevo.')
                elif db_error == "ciudad_exists":
                    errors.append('La ciudad ya está registrada en otra sucursal. Por favor, ingrese una nueva.')
                elif db_error == "database_error":
                    errors.append('Ocurrió un error al ingresar la sucursal. Por favor, intente nuevamente.')
        else:
            errors.append('Ocurrió un error al ingresar la sucursal. Por favor, intente nuevamente.')

    for error in errors:
        flash(error)
    return redirect(url_for('index_sucursales'))

@app_sucursales.route('/edit_sucursal/<int:id_sucursal>', methods=['GET', 'POST'])
def edit_sucursal(id_sucursal):
    if request.method == 'POST':
        ciudad = request.form.get('ciudad')
        telefono = request.form.get('telefono')

        errors = []

        if not ciudad or not telefono:
            errors.append('¡Todos los campos obligatorios deben ser completados!')
        else:
            if not VALID_CIUDAD_REGEX.match(ciudad):
                errors.append('La ciudad contiene caracteres no permitidos. Solo se permiten letras y espacios.')

            if not VALID_TELEFONO_REGEX.match(telefono):
                errors.append('El teléfono contiene caracteres no permitidos. Solo se permiten números y un guión en el formato xxxx-xxxx.')

        if not errors:
            if update_sucursal(id_sucursal, ciudad, telefono):
                flash('¡Sucursal actualizada exitosamente!')
                return redirect(url_for('sucursales'))
            else:
                flash('Ocurrió un error al actualizar la sucursal. Por favor, intente nuevamente.')
        else:
            for error in errors:
                flash(error)

    sucursal = get_sucursal_by_id(id_sucursal)
    return render_template('edit_sucursales.html', sucursal=sucursal)


@app_sucursales.route('/eliminar_sucursales/<int:id_sucursal>', methods=['GET', 'POST'])
def eliminar_sucursal(id_sucursal):
    if request.method == 'POST':
        if delete_sucursal(id_sucursal):
            flash('¡Sucursal eliminada exitosamente!')
            return redirect(url_for('sucursales'))
        else:
            flash('Ocurrió un error al eliminar la sucursal. Por favor, intente nuevamente.')
            return redirect(url_for('sucursales'))

    sucursal = get_sucursal_by_id(id_sucursal)
    if sucursal is None:
        flash('Sucursal no encontrada.')
        return redirect(url_for('sucursales'))

    return render_template('eliminar_sucursales.html', sucursal=sucursal)

if __name__ == '__main__':
    app_sucursales.run(debug=True, port=5008)
