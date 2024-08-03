from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

app_transportistas = Flask(__name__)
app_transportistas.secret_key = 'your_secret_key'

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

def insert_transportista(nombre_empresa, telefono):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()

    # Asegura el formato del teléfono
    telefono = telefono.replace("-", "")  # Usa el nombre de variable correcto
    if len(telefono) == 8:
        telefono = telefono[:4] + '-' + telefono[4:]

    query = "INSERT INTO transportistas (nombre_empresa, Telefono) VALUES (%s, %s)"
    values = (nombre_empresa, telefono)
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


def get_transportista(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    query = "SELECT * FROM transportistas LIMIT %s OFFSET %s"
    
    try:
        cursor.execute(query, (per_page, offset))
        transportistas = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM transportistas")
        total_count = cursor.fetchone()[0]

        return transportistas, total_count
    except Exception as e:
        print(f"Error: {e}")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_transportista_by_id(id_transportista):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM transportistas WHERE id_transportista = %s"
    try:
        cursor.execute(query, (id_transportista,))
        transportista = cursor.fetchone()
        return transportista
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_transportista(id_transportista, nombre_empresa, Telefono):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    UPDATE transportistas
    SET nombre_empresa = %s, Telefono = %s
    WHERE id_transportista = %s
    """
    values = (nombre_empresa, Telefono, id_transportista)
    try:
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


def eliminar_transportista(id_transportista):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM transportistas WHERE id_transportista = %s"
    try:
        cursor.execute(query, (id_transportista,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def search_transportistas(search_criteria, search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    # Asegúrate de que el search_criteria esté en la lista de campos válidos
    if search_criteria not in ['nombre_empresa', 'Telefono']:
        search_criteria = 'nombre_empresa'  # Valor por defecto si el criterio de búsqueda es inválido

    if search_criteria == 'Telefono':
        # Usa REPLACE para eliminar los guiones de la base de datos durante la búsqueda
        query = f"""
        SELECT * FROM transportistas
        WHERE REPLACE(Telefono, '-', '') LIKE %s
        LIMIT %s OFFSET %s
        """
        count_query = f"""
        SELECT COUNT(*) FROM transportistas
        WHERE REPLACE(Telefono, '-', '') LIKE %s
        """
        search_query = search_query.replace('-', '')  # Elimina los guiones del query del usuario
    else:
        query = f"SELECT * FROM transportistas WHERE {search_criteria} LIKE %s LIMIT %s OFFSET %s"
        count_query = f"SELECT COUNT(*) FROM transportistas WHERE {search_criteria} LIKE %s"
    
    try:
        cursor.execute(query, (f'%{search_query}%', per_page, offset))
        transportistas = cursor.fetchall()

        cursor.execute(count_query, (f'%{search_query}%',))
        total_count = cursor.fetchone()[0]

        return transportistas, total_count
    except Exception as e:
        print(f"Error: {e}")
        return [], 0
    finally:
        cursor.close()
        connection.close()



def validate_input(field_value, field_type='text'):
    if not field_value:
        return 'El campo es obligatorio.'
    
    if field_type == 'text':
        if len(field_value) < 3 or len(field_value) > 20:
            return 'El campo debe tener entre 3 y 20 caracteres.'
        if re.search(r'\d', field_value):
            return 'El campo no debe contener números.'
        if re.search(r'(.)\1{2,}', field_value):
            return 'El campo no debe tener tres letras repetidas.'
        if re.search(r'[!?@#$%^&*()_+\-=\[\]{};\'\\:"|,.<>\/?]', field_value):
            return 'El campo no debe contener signos especiales.'
    
    elif field_type == 'telefono':
        clean_value = field_value.replace('-', '')
        if len(clean_value) != 8 or not clean_value.isdigit():
            return 'El campo Teléfono debe ser numérico y tener exactamente 8 dígitos.'
        if clean_value[0] not in '9382':
            return 'El primer número del Teléfono debe ser 9, 3, 8 o 2.'
    
    elif field_type == 'document':
        if not field_value.isdigit():
            return 'El campo Documento debe ser numérico.'
    
    return ''  # Devuelve una cadena vacía si no hay errores



@app_transportistas.route('/')
def index_transportistas():
    return render_template('index_transportistas.html')

@app_transportistas.route('/transportistas')
def transportistas():
    search_criteria = request.args.get('search_criteria')
    search_query = request.args.get('search_query')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    if search_criteria and search_query:
        transportistas, total_count = search_transportistas(search_criteria, search_query, page, per_page)
    else:
        transportistas, total_count = get_transportista(page, per_page)
    
    total_pages = (total_count + per_page - 1) // per_page

    return render_template('transportistas.html', transportistas=transportistas, search_criteria=search_criteria, search_query=search_query, page=page, total_pages=total_pages, per_page=per_page)

@app_transportistas.route('/submit', methods=['POST'])
def submit_transportista():
    nombre_empresa = request.form['nombre_empresa']
    telefono = request.form['Telefono']

    # Validaciones
    error_nombre = validate_input(nombre_empresa, 'text')
    error_telefono = validate_input(telefono, 'telefono')

    if error_nombre or error_telefono:
        flash(' '.join(filter(None, [error_nombre, error_telefono])))
        return redirect(url_for('index_transportistas'))

    # Inserta el transportista en la base de datos
    if insert_transportista(nombre_empresa, telefono):
        flash('Transportista insertado correctamente!')
    else:
        flash('Ocurrió un error al insertar el transportista.')

    return redirect(url_for('index_transportistas'))


@app_transportistas.route('/edit_transportista/<int:id_transportista>', methods=['GET', 'POST'])
def edit_transportista(id_transportista):
    if request.method == 'POST':
        nombre_empresa = request.form['nombre_empresa']
        telefono = request.form['Telefono']
        
        # Validaciones
        error_nombre = validate_input(nombre_empresa, 'text')
        error_telefono = validate_input(telefono, 'telefono')

        if error_nombre or error_telefono:
            flash(' '.join(filter(None, [error_nombre, error_telefono])))
            return redirect(url_for('edit_transportista', id_transportista=id_transportista))
        
        if update_transportista(id_transportista, nombre_empresa, telefono):
            flash('Transportista actualizado correctamente!')
        else:
            flash('Error al actualizar el transportista.')
        
        return redirect(url_for('transportistas'))

    transportista = get_transportista_by_id(id_transportista)
    if not transportista:
        flash('Transportista no encontrado.')
        return redirect(url_for('transportistas'))
    
    return render_template('edit_transportista.html', transportista=transportista)

@app_transportistas.route('/eliminar/<int:id_transportista>', methods=['POST'])
def eliminar_transportista(id_transportista):
    if eliminar_transportista(id_transportista):
        flash('Transportista eliminado correctamente!')
    else:
        flash('Error al eliminar el transportista.')
    
    return redirect(url_for('transportistas'))

if __name__ == '__main__':
    app_transportistas.run(debug=True,port=5013)
