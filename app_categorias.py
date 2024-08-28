from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

app_categorias = Flask(__name__)
app_categorias.secret_key = 'your_secret_key'

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

def insert_categoria(nombre_categoria, descripcion):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "INSERT INTO categorias (nombre_categoria, descripcion) VALUES (%s, %s)"
    values = (nombre_categoria, descripcion)
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

def get_categorias(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    query = "SELECT * FROM categorias LIMIT %s OFFSET %s"
    
    try:
        cursor.execute(query, (per_page, offset))
        categorias = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM categorias")
        total_count = cursor.fetchone()[0]

        return categorias, total_count
    except Exception as e:
        print(f"Error: {e}")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_categoria_by_id(id_categoria):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM categorias WHERE id_categoria = %s"
    try:
        cursor.execute(query, (id_categoria,))
        categoria = cursor.fetchone()
        return categoria
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_categoria(id_categoria, nombre_categoria, Descripcion):   
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    UPDATE categorias
    SET nombre_categoria = %s, Descripcion = %s
    WHERE id_categoria = %s
    """
    values = (nombre_categoria, Descripcion, id_categoria)
    try:
        cursor.execute(query, values)
        connection.commit()
        print(f"Updated {cursor.rowcount} rows")  # Debugging line
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_categoria(id_categoria):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM categorias WHERE id_categoria = %s"
    try:
        cursor.execute(query, (id_categoria,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def search_categorias(search_criteria, search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    if search_criteria not in ['nombre_categoria', 'Descripcion']:
        search_criteria = 'nombre_categoria'

    query = f"SELECT * FROM categorias WHERE {search_criteria} LIKE %s LIMIT %s OFFSET %s"
    
    try:
        cursor.execute(query, (f'%{search_query}%', per_page, offset))
        categorias = cursor.fetchall()

        cursor.execute(f"SELECT COUNT(*) FROM categorias WHERE {search_criteria} LIKE %s", (f'%{search_query}%',))
        total_count = cursor.fetchone()[0]

        return categorias, total_count
    except Exception as e:
        print(f"Error: {e}")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def validate_input(field_value, field_type='text'):
    if not field_value:
        return "El campo no puede estar vacío."
    
    if field_type == 'text':
        if re.search(r'(.)\1{2,}', field_value):
            return "No se permiten más de tres letras seguidas."
        if re.search(r'\d', field_value):
            return "No se permiten números en este campo."
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|`~]', field_value):
            return "No se permiten símbolos en este campo."
       
    return None

@app_categorias.route('/')
def index_categorias():
    return render_template('index_categorias.html')

@app_categorias.route('/categorias')
def categorias():
    search_criteria = request.args.get('search_criteria')
    search_query = request.args.get('search_query')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    if search_criteria and search_query:
        categorias, total_count = search_categorias(search_criteria, search_query, page, per_page)
    else:
        categorias, total_count = get_categorias(page, per_page)
    
    total_pages = (total_count + per_page - 1) // per_page

    return render_template('categorias.html', categorias=categorias, search_criteria=search_criteria, search_query=search_query, page=page, total_pages=total_pages, per_page=per_page)

@app_categorias.route('/submit', methods=['POST'])
def submit_categoria():
    nombre_categoria = request.form.get('nombre_categoria')
    descripcion = request.form.get('Descripcion')

    # Validaciones
    nombre_error = validate_input(nombre_categoria)
    descripcion_error = validate_input(descripcion)

    if nombre_error or descripcion_error:
        if nombre_error:
            flash(nombre_error)
        if descripcion_error:
            flash(descripcion_error)
        return redirect(url_for('index_categorias'))

    # Inserta la categoría en la base de datos
    if insert_categoria(nombre_categoria, descripcion):
        flash('Categoría insertada correctamente!')
    else:
        flash('Ocurrió un error al insertar la categoría.')

    return redirect(url_for('index_categorias'))

@app_categorias.route('/edit_categoria/<int:id_categoria>', methods=['GET', 'POST'])
def edit_categoria(id_categoria):
    if request.method == 'POST':
        nombre_categoria = request.form.get('nombre_categoria')
        descripcion = request.form.get('Descripcion')

        # Validaciones
        nombre_error = validate_input(nombre_categoria)
        descripcion_error = validate_input(descripcion)

        if nombre_error or descripcion_error:
            if nombre_error:
                flash(nombre_error)
            if descripcion_error:
                flash(descripcion_error)
            return redirect(url_for('edit_categoria', id_categoria=id_categoria))

        if update_categoria(id_categoria, nombre_categoria, descripcion):
            flash('Categoría actualizada correctamente!')
        else:
            flash('Error al actualizar la categoría.')
        return redirect(url_for('categorias'))
    
    categoria = get_categoria_by_id(id_categoria)
    return render_template('edit_categoria.html', categoria=categoria)

@app_categorias.route('/eliminar/<int:id_categoria>', methods=['GET', 'POST'])
def eliminar_categoria(id_categoria):
    if request.method == 'POST':
        if delete_categoria(id_categoria):
            flash('Categoría eliminada exitosamente!')
        else:
            flash('Ocurrió un error al eliminar la categoría.')
        return redirect(url_for('categorias'))

    categoria = get_categoria_by_id(id_categoria)
    if categoria is None:
        flash('Categoría no encontrada!')
        return redirect(url_for('categorias'))
    
    return render_template('eliminar_categoria.html', categoria=categoria)

if __name__ == '__main__':
    app_categorias.run(debug=True, port=5009)
