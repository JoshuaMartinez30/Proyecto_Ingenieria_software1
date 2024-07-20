from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

app_inventario = Flask(__name__)
app_inventario.secret_key = 'your_secret_key'

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

def insert_user(nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "INSERT INTO inventario (nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo) VALUES (%s, %s, %s, %s, %s)"
    values = (nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo)
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

def get_inventario(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM inventario LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        inventario = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_inventario = cursor.fetchone()[0]
        return inventario, total_inventario
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_inventario_by_id(id_inventario):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM inventario WHERE id_inventario = %s"
    try:
        cursor.execute(query, (id_inventario,))
        inventario = cursor.fetchone()
        return inventario
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return None
    finally:
        cursor.close()
        connection.close()

def update_user(id_inventario, nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE inventario SET nombre_del_producto = %s, descripcion = %s, cantidad_en_stock = %s, stock_minimo = %s, stock_maximo = %s WHERE id_inventario = %s"
    values = (nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo, id_inventario)
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

def delete_user(id_inventario):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM inventario WHERE id_inventario = %s"
    try:
        cursor.execute(query, (id_inventario,))
        connection.commit()
        return True
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

def search_users(search_query, filter_by, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    if filter_by == "nombre_del_producto":
        query = "SELECT SQL_CALC_FOUND_ROWS * FROM inventario WHERE nombre_del_producto LIKE %s LIMIT %s OFFSET %s"
        values = (f'%{search_query}%', per_page, offset)
    elif filter_by == "descripcion":
        query = "SELECT SQL_CALC_FOUND_ROWS * FROM inventario WHERE descripcion LIKE %s LIMIT %s OFFSET %s"
        values = (f'%{search_query}%', per_page, offset)
    elif filter_by == "cantidad_en_stock":
        query = "SELECT SQL_CALC_FOUND_ROWS * FROM inventario WHERE cantidad_en_stock LIKE %s LIMIT %s OFFSET %s"
        values = (f'%{search_query}%', per_page, offset)
    elif filter_by == "stock_minimo":
        query = "SELECT SQL_CALC_FOUND_ROWS * FROM inventario WHERE stock_minimo LIKE %s LIMIT %s OFFSET %s"
        values = (f'%{search_query}%', per_page, offset)
    elif filter_by == "stock_maximo":
        query = "SELECT SQL_CALC_FOUND_ROWS * FROM inventario WHERE stock_maximo LIKE %s LIMIT %s OFFSET %s"
        values = (f'%{search_query}%', per_page, offset)
    else:
        query = "SELECT SQL_CALC_FOUND_ROWS * FROM inventario WHERE nombre_del_producto LIKE %s OR descripcion LIKE %s OR cantidad_en_stock LIKE %s OR stock_minimo LIKE %s OR stock_maximo LIKE %s LIMIT %s OFFSET %s"
        values = (f'%{search_query}%',) * 5 + (per_page, offset)
    
    try:
        cursor.execute(query, values)
        inventario = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_inventario = cursor.fetchone()[0]
        return inventario, total_inventario
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

# Función para verificar si un campo contiene solo dígitos
def contiene_solo_digitos(texto):
    return texto.isdigit()

# Función para validar los campos antes de insertar o actualizar
def validar_campos(nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo):
    if not nombre_del_producto.strip() or not descripcion.strip() or not cantidad_en_stock.strip() or not stock_minimo.strip() or not stock_maximo.strip():
        return False, 'Todos los campos son requeridos.'
    
    if not contiene_solo_digitos(cantidad_en_stock) or not contiene_solo_digitos(stock_minimo) or not contiene_solo_digitos(stock_maximo):
        return False, 'Los campos de stock deben contener solo números.'

    if not descripcion.strip():
        return False, 'La descripción es requerida.'
    if len(descripcion.strip()) < 10:
        return False, 'La descripción debe tener al menos 10 caracteres.'

    if any(char.isdigit() for char in nombre_del_producto):
        return False, 'El nombre no puede contener números.'
    if any(char.isdigit() for char in descripcion):
        return False, 'La descripción no puede contener números.'

    if contiene_signos(nombre_del_producto):
        return False, 'El nombre no puede contener signos.'
    if contiene_mas_de_dos_signos(descripcion):
        return False, 'La descripción no puede contener más de dos signos repetidos seguidos.'

    # Validación de stock mínimo y máximo
    if int(stock_minimo) > int(stock_maximo):
        return False, 'El stock mínimo no puede ser mayor que el stock máximo.'

    # Validación de repetición de la misma letra tres veces consecutivas
    if contiene_repeticion_tres_letras(nombre_del_producto):
        return False, 'El nombre no puede contener la misma letra repetida tres veces consecutivas.'
    if contiene_repeticion_tres_letras(descripcion):
        return False, 'La descripción no puede contener la misma letra repetida tres veces consecutivas.'

    return True, None

# Función para verificar si un texto contiene signos
def contiene_signos(texto):
    return not bool(re.match('^[a-zA-Z0-9\s]+$', texto))

# Función para verificar si un texto contiene más de dos signos repetidos seguidos
def contiene_mas_de_dos_signos(texto):
    if len(texto) < 3:
        return False
    for i in range(len(texto) - 2):
        if not texto[i].isalnum() and texto[i] == texto[i+1] == texto[i+2]:
            return True
    return False

# Función para verificar si un texto contiene la misma letra repetida tres veces consecutivas
def contiene_repeticion_tres_letras(texto):
    return bool(re.search(r'(.)\1\1', texto))

@app_inventario.route('/')
def index_inventario():
    return render_template('index_inventario.html')

@app_inventario.route('/inventario')
def inventario():
    search_query = request.args.get('search')
    filter_by = request.args.get('filter_by', 'nombre_del_producto')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if search_query:
        inventario, total_inventario = search_users(search_query, filter_by, page, per_page)
    else:
        inventario, total_inventario = get_inventario(page, per_page)

    total_pages = (total_inventario + per_page - 1) // per_page
    return render_template('inventario.html', inventario=inventario, search_query=search_query, filter_by=filter_by, page=page, per_page=per_page, total_inventario=total_inventario, total_pages=total_pages)

@app_inventario.route('/submit', methods=['POST'])
def submit():
    nombre_del_producto = request.form['nombre_del_producto']
    descripcion = request.form['descripcion']
    cantidad_en_stock = request.form['cantidad_en_stock']
    stock_minimo = request.form['stock_minimo']
    stock_maximo = request.form['stock_maximo']

    # Validar los campos antes de proceder
    valido, mensaje_error = validar_campos(nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo)
    if not valido:
        flash(mensaje_error)
        return redirect(url_for('index_inventario'))

    if insert_user(nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo):
        flash('Producto agregado exitosamente!')
    else:
        flash('Ocurrió un error al agregar el producto.')
    return redirect(url_for('inventario'))

@app_inventario.route('/edit_inventario/<int:id_inventario>', methods=['GET', 'POST'])
def edit_inventario(id_inventario):
    if request.method == 'POST':
        nombre_del_producto = request.form['nombre_del_producto']
        descripcion = request.form['descripcion']
        cantidad_en_stock = request.form['cantidad_en_stock']
        stock_minimo = request.form['stock_minimo']
        stock_maximo = request.form['stock_maximo']

        # Validar los campos antes de proceder
        valido, mensaje_error = validar_campos(nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo)
        if not valido:
            flash(mensaje_error)
            return redirect(url_for('edit_inventario', id_inventario=id_inventario))

        if update_user(id_inventario, nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo):
            flash('Producto actualizado exitosamente!')
        else:
            flash('Ocurrió un error al actualizar el producto.')
        return redirect(url_for('inventario'))

    inventario = get_inventario_by_id(id_inventario)
    if inventario is None:
        flash('Producto no encontrado.')
        return redirect(url_for('inventario'))

    return render_template('edit_inventario.html', inventario=inventario)

@app_inventario.route('/eliminar_inventario/<int:id_inventario>')
def eliminar_inventario(id_inventario):
    if delete_user(id_inventario):
        flash('Producto eliminado exitosamente!')
    else:
        flash('Ocurrió un error al eliminar el producto.')
    return redirect(url_for('inventario'))

if __name__ == '__main__':
    app_inventario.run(debug=True, port=5001)
