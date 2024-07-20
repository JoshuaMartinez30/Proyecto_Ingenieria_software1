from flask import Flask, render_template, request, redirect, url_for, flash
import re
import mysql.connector
from mysql.connector import Error

app_impuestos = Flask(__name__)
app_impuestos.secret_key = 'your_secret_key'

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

def insert_user(nombre_producto, precio_base, tasa_impuesto, impuesto_calculado, precio_final):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    query = "INSERT INTO impuestos (nombre_producto, precio_base, tasa_impuesto, impuesto_calculado, precio_final) VALUES (%s, %s, %s, %s, %s)"
    values = (nombre_producto, precio_base, tasa_impuesto, impuesto_calculado, precio_final)
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



def get_impuestos(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM impuestos LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        impuestos = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_impuestos = cursor.fetchone()[0]
        return impuestos, total_impuestos
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()



def get_impuestos_by_id(id_impuestos):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM impuestos WHERE id_impuestos = %s"
    try:
        cursor.execute(query, (id_impuestos,))
        impuestos = cursor.fetchone()
        return impuestos
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_user(id_impuestos, nombre_producto, precio_base, tasa_impuesto, impuesto_calculado, precio_final):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE impuestos SET nombre_producto = %s, precio_base = %s, tasa_impuesto = %s, impuesto_calculado = %s, precio_final = %s WHERE id_impuestos = %s"
    values = (nombre_producto, precio_base, tasa_impuesto, impuesto_calculado, precio_final, id_impuestos)
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

def delete_user(id_impuestos):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM impuestos WHERE id_impuestos = %s"
    try:
        cursor.execute(query, (id_impuestos,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
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
    query = f"SELECT SQL_CALC_FOUND_ROWS * FROM impuestos WHERE {search_field} LIKE %s LIMIT %s OFFSET %s"
    values = (f'%{search_query}%', per_page, offset)
    try:
        cursor.execute(query, values)
        impuestos = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_impuestos = cursor.fetchone()[0]
        return impuestos, total_impuestos
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()


def validate_fields(nombre_producto, precio_base, tasa_impuesto, impuesto_calculado, precio_final):
    if not all([nombre_producto, precio_base, tasa_impuesto, impuesto_calculado, precio_final]):
        return "Todos los campos son obligatorios."
    if not (3 <= len(nombre_producto) <= 20):
        return "El nombre del producto debe tener entre 3 y 20 caracteres."
    if not re.match(r'^[A-Za-z]+$', nombre_producto):
        return "El nombre del producto no debe contener números ni signos."
    if re.search(r'(.)\1{2,}', nombre_producto):
        return "El nombre del producto no debe contener tres letras repetidas consecutivas."
    if not re.match(r'^\d+(\.\d{1,2})?$', precio_base):
        return "El precio base debe ser un número válido (puede incluir hasta dos decimales)."
    if not re.match(r'^\d+(\.\d{1,2})?$', tasa_impuesto):
        return "La tasa de impuesto debe ser un número válido (puede incluir hasta dos decimales)."
    if not re.match(r'^\d+(\.\d{1,2})?$', impuesto_calculado):
        return "El impuesto calculado debe ser un número válido (puede incluir hasta dos decimales)."
    if not re.match(r'^\d+(\.\d{1,2})?$', precio_final):
        return "El precio final debe ser un número válido (puede incluir hasta dos decimales)."
    return None

@app_impuestos.route('/')
def index_impuestos():
    return render_template('index_impuestos.html')

@app_impuestos.route('/impuestos')
def impuestos():
    search_query = request.args.get('search', '')
    search_field = request.args.get('search_field', 'nombre_producto')  # Ajusta el campo de búsqueda por defecto
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if search_query:
        impuestos, total_impuestos = search_users(search_query, search_field, page, per_page)
    else:
        impuestos, total_impuestos = get_impuestos(page, per_page)

    total_pages = (total_impuestos + per_page - 1) // per_page
    return render_template('impuestos.html', impuestos=impuestos, search_query=search_query, search_field=search_field, page=page, per_page=per_page, total_impuestos=total_impuestos, total_pages=total_pages)

@app_impuestos.route('/submit', methods=['POST'])
def submit():
    nombre_producto = request.form['nombre_producto']
    precio_base = request.form['precio_base']
    tasa_impuesto = request.form['tasa_impuesto']
    impuesto_calculado = request.form['impuesto_calculado']
    precio_final = request.form['precio_final']

    error_message = validate_fields(nombre_producto, precio_base, tasa_impuesto, impuesto_calculado, precio_final)
    if error_message:
        flash(error_message)
        return redirect(url_for('index_impuestos'))

    if insert_user(nombre_producto, precio_base, tasa_impuesto, impuesto_calculado, precio_final):
        flash('Producto insertado exitosamente.')
    else:
        flash('Ocurrió un error al insertar el producto.')
    
    return redirect(url_for('index_impuestos'))

@app_impuestos.route('/edit_impuestos/<int:id_impuestos>', methods=['GET', 'POST'])
def edit_impuestos(id_impuestos):
    if request.method == 'POST':
        nombre_producto = request.form['nombre_producto']
        precio_base = request.form['precio_base']
        tasa_impuesto = request.form['tasa_impuesto']
        impuesto_calculado = request.form['impuesto_calculado']
        precio_final = request.form['precio_final']

        error_message = validate_fields(nombre_producto, precio_base, tasa_impuesto, impuesto_calculado, precio_final)
        if error_message:
            flash(error_message)
            return redirect(url_for('edit_impuestos', id_impuestos=id_impuestos))

        if update_user(id_impuestos, nombre_producto, precio_base, tasa_impuesto, impuesto_calculado, precio_final):
            flash('Producto actualizado exitosamente.')
        else:
            flash('Ocurrió un error al actualizar el producto.')
        
        return redirect(url_for('impuestos'))

    impuestos = get_impuestos_by_id(id_impuestos)
    if impuestos is None:
        flash('Producto no encontrado.')
        return redirect(url_for('impuestos'))
    return render_template('edit_impuestos.html', impuestos=impuestos)

@app_impuestos.route('/eliminar_impuestos/<int:id_impuestos>', methods=['GET', 'POST'])
def eliminar_impuestos(id_impuestos):
    if request.method == 'POST':
        if delete_user(id_impuestos):
            flash('Producto eliminado exitosamente.')
        else:
            flash('Ocurrió un error al eliminar el producto.')
        return redirect(url_for('impuestos'))

    impuestos = get_impuestos_by_id(id_impuestos)
    if impuestos is None:
        flash('Producto no encontrado.')
        return redirect(url_for('impuestos'))
    return render_template('eliminar_impuestos.html', impuestos=impuestos)

if __name__ == '__main__':
    app_impuestos.run(debug=True, port=5013)
