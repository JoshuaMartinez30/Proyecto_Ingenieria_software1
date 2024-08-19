from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

app_almacenes = Flask(__name__)
app_almacenes.secret_key = 'your_secret_key'

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
            print("Conexión exitosa a la base de datos MySQL")
    except Error as e:
        print(f"Error '{e}' ocurrió")
    return connection

def validate_text_field(text):
    if not 3 <= len(text) <= 20:
        return False, "El campo debe tener entre 3 y 20 caracteres."
    
    if re.search(r'\d', text):
        return False, "El campo no puede contener números."

    if re.search(r'[^\w\s]', text):
        return False, "El campo no puede contener caracteres especiales."

    if re.search(r'(.)\1\1', text):
        return False, "El campo no puede contener tres letras seguidas iguales."

    return True, ""


def insert_almacen(nombre, direccion, id_sucursal):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "INSERT INTO almacenes (nombre, direccion, id_sucursal) VALUES (%s, %s, %s)"
    values = (nombre, direccion, id_sucursal)
    try:
        cursor.execute(query, values)
        connection.commit()
        return True
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

def get_sucursales():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_sucursal, Ciudad FROM sucursales"
    try:
        cursor.execute(query)
        sucursales = cursor.fetchall()
        return sucursales
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return []
    finally:
        cursor.close()
        connection.close()

def get_almacenes(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = """
        SELECT a.id_almacenes, a.nombre, a.direccion, s.Ciudad
        FROM almacenes a
        JOIN sucursales s ON a.id_sucursal = s.id_sucursal
        LIMIT %s OFFSET %s
    """
    try:
        cursor.execute(query, (per_page, offset))
        almacenes = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_almacenes = cursor.fetchone()[0]
        return almacenes, total_almacenes
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_almacen_by_id(id_almacen):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = """
        SELECT a.id_almacenes, a.nombre, a.direccion, a.id_sucursal, s.Ciudad
        FROM almacenes a
        JOIN sucursales s ON a.id_sucursal = s.id_sucursal
        WHERE a.id_almacenes = %s
    """
    try:
        cursor.execute(query, (id_almacen,))
        almacen = cursor.fetchone()
        return almacen
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return None
    finally:
        cursor.close()
        connection.close()

def update_almacen(id_almacen, nombre, direccion, id_sucursal):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE almacenes SET nombre = %s, direccion = %s, id_sucursal = %s WHERE id_almacenes = %s"
    values = (nombre, direccion, id_sucursal, id_almacen)
    try:
        cursor.execute(query, values)
        connection.commit()
        return True
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_almacen(id_almacen):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM almacenes WHERE id_almacenes = %s"
    try:
        cursor.execute(query, (id_almacen,))
        connection.commit()
        return True
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

def get_historico_almacenes(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM historicos_almacenes LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        historico_almacenes = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_historico_almacenes = cursor.fetchone()[0]
        return historico_almacenes, total_historico_almacenes
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

@app_almacenes.route('/historico_almacenes')
def historico_almacenes():
    page = request.args.get('page', 1, type=int)
    per_page = int(request.args.get('per_page', 10))
    historicos, total_historicos = get_historico_almacenes(page, per_page)

    total_pages = (total_historicos + per_page - 1) // per_page
    return render_template('historico_almacenes.html', historicos=historicos, page=page, per_page=per_page, total_historicos=total_historicos, total_pages=total_pages)


@app_almacenes.route('/')
def index_almacenes():
    sucursales = get_sucursales()  # Cargar las sucursales al inicio
    return render_template('index_almacenes.html', sucursales=sucursales)

@app_almacenes.route('/almacenes')
def almacenes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    almacenes, total_almacenes = get_almacenes(page, per_page)
    total_pages = (total_almacenes + per_page - 1) // per_page
    return render_template('almacenes.html', almacenes=almacenes, page=page, per_page=per_page, total_almacenes=total_almacenes, total_pages=total_pages)

@app_almacenes.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    id_sucursal = request.form['sucursal']

    errors = {}

    # Validaciones del campo nombre
    is_valid, error_message = validate_text_field(nombre)
    if not is_valid:
        errors['nombre_error'] = error_message

    # Validaciones del campo dirección
    if not direccion:
        errors['direccion_error'] = 'El campo dirección es obligatorio.'

    # Si hay errores, renderizar el formulario con mensajes de error
    if errors:
        sucursales = get_sucursales()  # Cargar sucursales de nuevo para el formulario
        return render_template('index_almacenes.html', errors=errors, sucursales=sucursales)

    # Si no hay errores, proceder a insertar el almacén
    if insert_almacen(nombre, direccion, id_sucursal):
        flash('Almacén insertado exitosamente!', 'success')
    else:
        flash('Ocurrió un error al insertar el almacén.', 'error')
    
    return redirect(url_for('almacenes'))

@app_almacenes.route('/edit_almacen/<int:id_almacen>', methods=['POST', 'GET'])
def edit_almacen(id_almacen):
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        id_sucursal = request.form['sucursal']

        # Validar campo 'nombre'
        is_valid, error_message = validate_text_field(nombre)
        if not is_valid:
            flash(error_message, 'error')
            return redirect(url_for('edit_almacen', id_almacen=id_almacen))

        # Actualizar almacén
        if update_almacen(id_almacen, nombre, direccion, id_sucursal):
            flash('Almacén actualizado exitosamente!', 'success')
        else:
            flash('Ocurrió un error al actualizar el almacén.', 'error')
        
        return redirect(url_for('almacenes'))
    
    # Cargar el almacén existente para la edición
    almacen = get_almacen_by_id(id_almacen)
    if almacen is None:
        flash('Almacén no encontrado.', 'error')
        return redirect(url_for('almacenes'))

    sucursales = get_sucursales()  # Obtener las sucursales para el formulario
    return render_template('edit_almacen.html', almacen=almacen, sucursales=sucursales)

@app_almacenes.route('/delete_almacen/<int:id_almacen>', methods=['POST'])
def delete_almacen(id_almacen):
    if delete_almacen(id_almacen):
        flash('Almacén eliminado exitosamente!', 'success')
    else:
        flash('Ocurrió un error al eliminar el almacén.', 'error')
    return redirect(url_for('almacenes'))

if __name__ == "__main__":
    app_almacenes.run(debug=True,port=5018)
