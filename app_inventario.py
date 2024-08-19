from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re


app_inventario = Flask(__name__)
app_inventario.secret_key = 'your_secret_key'  # Cambia 'your_secret_key' por una clave secreta segura

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

def validate_text_field(value, field_name, min_length=3, max_length=20):
    if not value or len(value) < min_length or len(value) > max_length:
        return f'{field_name} debe tener entre {min_length} y {max_length} caracteres.'
    if re.search(r'[0-9]', value):
        return f'{field_name} no debe contener números.'
    if re.search(r'[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~]', value):
        return f'{field_name} no debe contener caracteres especiales.'
    if re.search(r'(.)\1{2,}', value):
        return f'{field_name} no debe contener tres o más letras repetidas consecutivamente.'
    return None

def validate_numeric_field(value, field_name):
    if not value.isdigit():
        return f'{field_name} debe ser un número entero.'
    return None

def insert_inventario(id_producto, id_categoria, cantidad_en_stock, stock_minimo, stock_maximo):
    connection = create_connection()
    if connection is None:
        print("Error: No se pudo conectar a la base de datos.")
        return False
    cursor = connection.cursor()
    query = """INSERT INTO inventario (id_producto, id_categoria, cantidad_en_stock, stock_minimo, stock_maximo) VALUES (%s, %s, %s, %s, %s)"""
    values = (id_producto, id_categoria, cantidad_en_stock, stock_minimo, stock_maximo)
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Inventario insertado exitosamente.")
        return True
    except Error as e:
        print(f"Error al insertar el inventario: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def get_inventario(page, per_page, search_criteria=None, search_query=None):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    if search_criteria and search_query:
        query = f"""
            SELECT i.id_inventario, i.id_producto, i.id_categoria, i.cantidad_en_stock, 
                   i.stock_minimo, i.stock_maximo, 
                   p.nombre AS nombre_producto, c.nombre_categoria
            FROM inventario i
            JOIN producto p ON i.id_producto = p.id_producto
            JOIN categorias c ON i.id_categoria = c.id_categoria
            WHERE {search_criteria} LIKE %s 
            LIMIT %s OFFSET %s
        """
        values = (f'%{search_query}%', per_page, offset)
    else:
        query = """
            SELECT i.id_inventario, i.id_producto, i.id_categoria, i.cantidad_en_stock, 
                   i.stock_minimo, i.stock_maximo, 
                   p.nombre AS nombre_producto, c.nombre_categoria
            FROM inventario i
            JOIN producto p ON i.id_producto = p.id_producto
            JOIN categorias c ON i.id_categoria = c.id_categoria
            LIMIT %s OFFSET %s
        """
        values = (per_page, offset)

    try:
        cursor.execute(query, values)
        inventario = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_count = cursor.fetchone()[0]
        return inventario, total_count
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_categorias():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_categoria, nombre_categoria FROM categorias"
    try:
        cursor.execute(query)
        categorias = cursor.fetchall()
        return categorias
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def get_producto():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_producto, nombre FROM producto"
    try:
        cursor.execute(query)
        producto = cursor.fetchall()
        return producto
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def update_inventario(id_inventario, id_producto, id_categoria, cantidad_en_stock, stock_minimo, stock_maximo):
    connection = create_connection()
    if connection is None:
        print("Error: No se pudo conectar a la base de datos.")
        return False
    
    cursor = connection.cursor()
    query = """
    UPDATE inventario
    SET id_producto = %s,
        id_categoria = %s,
        cantidad_en_stock = %s,
        stock_minimo = %s,
        stock_maximo = %s
    WHERE id_inventario = %s
    """
    try:
        cursor.execute(query, (id_producto, id_categoria, cantidad_en_stock, stock_minimo, stock_maximo, id_inventario))
        connection.commit()
        print("Inventario actualizado exitosamente.")
        return True
    except Error as e:
        print(f"Error al actualizar el inventario: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_inventario(id_inventario):
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
        print(f"The error '{e}' occurred")
        return False
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
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

@app_inventario.route('/')
def index_inventario():
    categorias = get_categorias()
    productos = get_producto()
    return render_template('index_inventario.html', categorias=categorias, productos=productos)

@app_inventario.route('/submit', methods=['POST'])
def submit():
    id_producto = request.form.get('id_producto')
    id_categoria = request.form.get('id_categoria')
    cantidad_en_stock = request.form.get('cantidad_en_stock')
    stock_minimo = request.form.get('stock_minimo')
    stock_maximo = request.form.get('stock_maximo')
    
    error_message = None
    error_message = validate_text_field(id_producto, 'Producto')
    if error_message is None:
        error_message = validate_text_field(id_categoria, 'Categoría')
    if error_message is None:
        error_message = validate_numeric_field(cantidad_en_stock, 'Cantidad en Stock')
    if error_message is None:
        error_message = validate_numeric_field(stock_minimo, 'Stock Mínimo')
    if error_message is None:
        error_message = validate_numeric_field(stock_maximo, 'Stock Máximo')

    if error_message:
        flash(error_message)
        return redirect(url_for('index_inventario'))

    if insert_inventario(id_producto, id_categoria, cantidad_en_stock, stock_minimo, stock_maximo):
        flash('Inventario agregado exitosamente!')
    else:
        flash('Error al agregar el inventario.')

    return redirect(url_for('index_inventario'))

from flask import request, render_template

@app_inventario.route('/inventario')
def inventario():
    search_query = request.args.get('search_query', '')
    search_criteria = request.args.get('search_criteria', 'id_inventario')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    inventario, total_count = get_inventario(page, per_page, search_criteria, search_query)

    # Convert to list of tuples with product and category names
    inventario_con_categorias = [
        (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7])
        for item in inventario
    ]

    # Calculate total pages
    total_pages = (total_count + per_page - 1) // per_page

    return render_template('inventario.html', 
                           inventario=inventario_con_categorias, 
                           page=page, 
                           per_page=per_page, 
                           total_count=total_count, 
                           total_pages=total_pages, 
                           search_query=search_query)

@app_inventario.route('/edit_inventario/<int:id_inventario>', methods=['GET', 'POST'])
def edit_inventario(id_inventario):
    if request.method == 'POST':
        id_producto = request.form.get('id_producto')
        id_categoria = request.form.get('id_categoria')
        cantidad_en_stock = request.form.get('cantidad_en_stock')
        stock_minimo = request.form.get('stock_minimo')
        stock_maximo = request.form.get('stock_maximo')
        
        error_message = None
        error_message = validate_text_field(id_producto, 'Producto')
        if error_message is None:
            error_message = validate_text_field(id_categoria, 'Categoría')
        if error_message is None:
            error_message = validate_numeric_field(cantidad_en_stock, 'Cantidad en Stock')
        if error_message is None:
            error_message = validate_numeric_field(stock_minimo, 'Stock Mínimo')
        if error_message is None:
            error_message = validate_numeric_field(stock_maximo, 'Stock Máximo')

        if error_message:
            flash(error_message)
            return redirect(url_for('edit_inventario', id_inventario=id_inventario))

        if update_inventario(id_inventario, id_producto, id_categoria, cantidad_en_stock, stock_minimo, stock_maximo):
            flash('Inventario actualizado exitosamente!')
        else:
            flash('Error al actualizar el inventario.')

        return redirect(url_for('inventario'))

    inventario = get_inventario_by_id(id_inventario)
    if inventario is None:
        flash('Inventario no encontrado.')
        return redirect(url_for('inventario'))

    categorias = get_categorias()
    productos = get_producto()

    return render_template('edit_inventario.html', inventario=inventario, categorias=categorias, productos=productos)

@app_inventario.route('/delete_inventario/<int:id_inventario>', methods=['POST'])
def delete_inventario_route(id_inventario):
    if delete_inventario(id_inventario):
        flash('Inventario eliminado exitosamente!')
    else:
        flash('Error al eliminar el inventario.')

    return redirect(url_for('inventario'))

if __name__ == '__main__':
    app_inventario.run(debug=True,port=5001)
