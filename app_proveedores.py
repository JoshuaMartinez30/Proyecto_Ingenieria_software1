from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

app_proveedores = Flask(__name__)
app_proveedores.secret_key = 'your_secret_key'

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

def insert_user(Nombre_del_proveedor, Producto_Servicio, Historial_de_desempeño, nombre_compañia, Telefono, Ciudad, tipo, Documento):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()

    # Validar Documento
    error_message = validate_document(Documento, tipo)
    if error_message:
        print(f"Validation error: {error_message}")
        return False

    # Asegura el formato del teléfono
    Telefono = Telefono.replace("-", "")
    if len(Telefono) == 8:
        Telefono = Telefono[:4] + '-' + Telefono[4:]
    
    query = "INSERT INTO proveedores (Nombre_del_proveedor, Producto_Servicio, Historial_de_desempeño, nombre_compañia, Telefono, Ciudad, tipo, Documento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (Nombre_del_proveedor, Producto_Servicio, Historial_de_desempeño, nombre_compañia, Telefono, Ciudad, tipo, Documento)
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

def get_proveedor(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    query = "SELECT * FROM proveedores LIMIT %s OFFSET %s"
    
    try:
        cursor.execute(query, (per_page, offset))
        proveedores = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM proveedores")
        total_count = cursor.fetchone()[0]

        return proveedores, total_count
    except Exception as e:
        print(f"Error: {e}")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_proveedor_by_id(id_proveedor):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM proveedores WHERE id_proveedor = %s"
    try:
        cursor.execute(query, (id_proveedor,))
        proveedores = cursor.fetchone()
        return proveedores
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_user(id_proveedor, Nombre_del_proveedor, Producto_Servicio, Historial_de_desempeño, nombre_compañia, Telefono, Ciudad, tipo, Documento):
    connection = create_connection()
    if connection is None:
        print("No se pudo conectar a la base de datos.")
        return False
    cursor = connection.cursor()
    query = """
    UPDATE proveedores
    SET Nombre_del_proveedor = %s, Producto_Servicio = %s, Historial_de_desempeño = %s, nombre_compañia = %s, Telefono = %s, Ciudad = %s, tipo = %s, Documento = %s
    WHERE id_proveedor = %s
    """
    values = (Nombre_del_proveedor, Producto_Servicio, Historial_de_desempeño, nombre_compañia, Telefono, Ciudad, tipo, Documento, id_proveedor)
    try:
        print(f"Ejecutando consulta: {query} con valores {values}")
        cursor.execute(query, values)
        connection.commit()
        print(f"Updated {cursor.rowcount} rows")  
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_proveedor(id_proveedor):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM proveedores WHERE id_proveedor = %s"
    try:
        cursor.execute(query, (id_proveedor,))
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

    # Normaliza el número de teléfono
    if search_criteria == 'Telefono':
        # Elimina guiones del input de búsqueda
        search_query = search_query.replace('-', '')

        # Consulta que elimina guiones del teléfono almacenado en la base de datos
        query = """
        SELECT * FROM proveedores
        WHERE REPLACE(Telefono, '-', '') LIKE %s
        LIMIT %s OFFSET %s
        """
    else:
        query = f"SELECT * FROM proveedores WHERE {search_criteria} LIKE %s LIMIT %s OFFSET %s"

    try:
        cursor.execute(query, (f'%{search_query}%', per_page, offset))
        proveedores = cursor.fetchall()

        # Obtén el total de proveedores con la misma condición
        if search_criteria == 'Telefono':
            cursor.execute("""
            SELECT COUNT(*) FROM proveedores
            WHERE REPLACE(Telefono, '-', '') LIKE %s
            """, (f'%{search_query}%',))
        else:
            cursor.execute(f"SELECT COUNT(*) FROM proveedores WHERE {search_criteria} LIKE %s", (f'%{search_query}%',))
        
        total_count = cursor.fetchone()[0]

        return proveedores, total_count
    except Exception as e:
        print(f"Error: {e}")
        return [], 0
    finally:
        cursor.close()
        connection.close()

import re

def validate_input(field_value, field_type='text', tipo=''):
    error_message = None
    if not field_value:
        error_message = 'El campo no puede estar vacío.'
    
    if field_type == 'text':
        if len(field_value) < 3 or len(field_value) > 20:
            error_message = 'El campo debe tener entre 3 y 20 caracteres.'
        elif re.search(r'\d', field_value):
            error_message = 'El campo no debe contener números.'
        elif re.search(r'(.)\1{2,}', field_value):
            error_message = 'El campo no debe contener más de tres letras seguidas.'
        elif all(char in "!?@#$%^&*()_+-=[]{};':\",.<>/?\\" for char in field_value):
            error_message = 'El campo no debe contener solo signos.'
    
    elif field_type == 'telefono':
        clean_value = field_value.replace('-', '')
        if len(clean_value) != 8 or not clean_value.isdigit():
            error_message = 'El campo Teléfono debe ser numérico y tener exactamente 8 dígitos.'
        elif clean_value[0] not in '9382':
            error_message = 'El primer número del Teléfono debe ser 9, 3, 8 o 2.'
    
    elif field_type == 'document':
        if tipo == 'RTN':
            # Validación para RTN (14 dígitos, sin guiones)
            if not (field_value.isdigit() and len(field_value) == 14):
                error_message = 'El RTN debe tener exactamente 14 dígitos.'
        elif tipo == 'Numero de Identidad':
            # Validación para Número de Identidad (13 dígitos, sin guiones)
            if not (field_value.isdigit() and len(field_value) == 13):
                error_message = 'El Número de Identidad debe tener exactamente 13 dígitos.'
        elif tipo == 'Pasaporte':
            # Validación para Pasaporte (comienza con 'E' seguido de 7 números)
            if not (field_value.startswith('E') and len(field_value) == 8 and field_value[1:].isdigit()):
                error_message = 'El Pasaporte debe comenzar con una E mayúscula seguido de 7 números.'
    
    return error_message

def validate_document(tipo, documento):
    if tipo == 'Numero de Identidad':
        return bool(re.match(r'^\d{13}$', documento))
    elif tipo == 'RTN':
        return bool(re.match(r'^\d{14}$', documento))
    elif tipo == 'Pasaporte':
        return bool(re.match(r'^E\d{7}$', documento))
    return False


def format_document(document, doc_type):
    if doc_type == 'Numero de Identidad':
        return f"{document[:4]}-{document[4:8]}-{document[8:]}"
    elif doc_type == 'RTN':
        return f"{document[:4]}-{document[4:8]}-{document[8:]}"
    return document


def format_document(document, doc_type):
    if doc_type == 'Numero de Identidad':
        return f"{document[:4]}-{document[4:8]}-{document[8:]}"
    elif doc_type == 'RTN':
        return f"{document[:4]}-{document[4:8]}-{document[8:]}"
    return document

@app_proveedores.route('/')
def index_proveedores():
    return render_template('index_proveedores.html')

@app_proveedores.route('/proveedores')
def proveedores():
    search_criteria = request.args.get('search_criteria')
    search_query = request.args.get('search_query')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))  # Obtiene el valor del parámetro 'per_page' o usa 10 por defecto

    if search_criteria and search_query:
        proveedores, total_count = search_users(search_criteria, search_query, page, per_page)
    else:
        proveedores, total_count = get_proveedor(page, per_page)
    
    total_pages = (total_count + per_page - 1) // per_page

    return render_template('proveedores.html', proveedores=proveedores, search_criteria=search_criteria, search_query=search_query, page=page, total_pages=total_pages, per_page=per_page)

@app_proveedores.route('/submit', methods=['POST'])
def submit():
    Nombre_del_proveedor = request.form['Nombre_del_proveedor']
    Producto_Servicio = request.form['Producto_Servicio']
    Historial_de_desempeño = request.form['Historial_de_desempeño']
    nombre_compañia = request.form['nombre_compañia']
    Telefono = request.form['Telefono']
    Ciudad = request.form['Ciudad']
    tipo = request.form['Tipo']
    Documento = request.form['Documento']

    # Validaciones
    errors = []
    for field, field_type in zip([Nombre_del_proveedor, Producto_Servicio, Historial_de_desempeño, nombre_compañia, Ciudad], ['text']*5):
        error_message = validate_input(field, field_type)
        if error_message:
            errors.append(error_message)
    
    # Validar teléfono
    error_message = validate_input(Telefono, 'telefono')
    if error_message:
        errors.append(error_message)

    # Validar documento según tipo
    error_message = validate_input(Documento, 'document', tipo)
    if error_message:
        errors.append(error_message)

    if errors:
        flash(' '.join(errors))
        return redirect(url_for('index_proveedores'))

    # Inserta el proveedor en la base de datos
    if insert_user(Nombre_del_proveedor, Producto_Servicio, Historial_de_desempeño, nombre_compañia, Telefono, Ciudad, tipo, Documento):
        flash('Proveedor insertado correctamente!')
    else:
        flash('Ocurrió un error al insertar el proveedor.')

    return redirect(url_for('index_proveedores'))


@app_proveedores.route('/edit/<int:id_proveedor>', methods=['GET', 'POST'])
def edit_proveedores(id_proveedor):
    if request.method == 'POST':
        Nombre_del_proveedor = request.form['Nombre_del_proveedor']
        Producto_Servicio = request.form['Producto_Servicio']
        Historial_de_desempeño = request.form['Historial_de_desempeño']
        nombre_compañia = request.form['nombre_compañia']
        Telefono = request.form['Telefono']
        Ciudad = request.form['Ciudad']
        tipo = request.form['tipo']
        Documento = request.form['Documento']

        # Validaciones
        errors = []
        for field, field_type in zip([Nombre_del_proveedor, Producto_Servicio, Historial_de_desempeño, nombre_compañia, Ciudad], ['text']*6):
            error_message = validate_input(field, field_type)
            if error_message:
                errors.append(error_message)
        
        if validate_input(Telefono, 'telefono'):
            error_message = validate_input(Telefono, 'telefono')
            if error_message:
                errors.append(error_message)

        if validate_input(Documento, 'document'):
            error_message = validate_input(Documento, 'document')
            if error_message:
                errors.append(error_message)

        if errors:
            flash(' '.join(errors))
            return redirect(url_for('edit_proveedores', id_proveedor=id_proveedor))

        if update_user(id_proveedor, Nombre_del_proveedor, Producto_Servicio, Historial_de_desempeño, nombre_compañia, Telefono, Ciudad, tipo, Documento):
            flash('Proveedor actualizado correctamente!')
        else:
            flash('Ocurrió un error al actualizar el proveedor.')
        return redirect(url_for('proveedores'))

    proveedores = get_proveedor_by_id(id_proveedor)
    return render_template('edit_proveedores.html', proveedores=proveedores)

@app_proveedores.route('/eliminar/<int:id_proveedor>', methods=['GET', 'POST'])
def eliminar_proveedores(id_proveedor):
    if request.method == 'POST':
        if delete_proveedor(id_proveedor):
            flash('Proveedor eliminado exitosamente!')
        else:
            flash('Ocurrió un error al eliminar el proveedor.')
        return redirect(url_for('proveedores'))

    proveedor = get_proveedor_by_id(id_proveedor)
    if proveedor is None:
        flash('Proveedor no encontrado!')
        return redirect(url_for('proveedores'))
    
    return render_template('eliminar_proveedores.html', proveedor=proveedor)

if __name__ == '__main__':
    app_proveedores.run(debug=True,port=5005)