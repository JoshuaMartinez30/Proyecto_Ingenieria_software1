from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

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
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def insert_user(nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    query = "INSERT INTO inventario (nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo) VALUES (%s, %s, %s, %s, %s)"
    values = (nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo)
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

def get_inventario():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM inventario"
    try:
        cursor.execute(query)
        inventario = cursor.fetchall()
        return inventario
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
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
        print(f"The error '{e}' occurred")
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
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def search_users(search_query):
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM inventario WHERE nombre_del_producto LIKE %s OR descripcion LIKE %s OR cantidad_en_stock LIKE %s OR stock_minimo LIKE %s OR stock_maximo LIKE %s"
    values = (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
    try:
        cursor.execute(query, values)
        inventario = cursor.fetchall()
        return inventario
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

@app_inventario.route('/')
def index_inventario():
    return render_template('index_inventario.html')

@app_inventario.route('/inventario')
def inventario():
    search_query = request.args.get('search')
    if search_query:
        inventario = search_users(search_query)
    else:
        inventario = get_inventario()
    return render_template('inventario.html', inventario=inventario, search_query=search_query)

@app_inventario.route('/submit', methods=['POST'])
def submit():
    nombre_del_producto = request.form['nombre_del_producto']
    descripcion = request.form['descripcion']
    cantidad_en_stock = request.form['cantidad_en_stock']
    stock_minimo = request.form['stock_minimo']
    stock_maximo = request.form['stock_maximo']

    if not nombre_del_producto or not descripcion or not cantidad_en_stock or not stock_minimo or not stock_maximo:
        flash('All fields are required!')
        return redirect(url_for('index_inventario'))

    if insert_user(nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo):
        flash('Product inserted successfully!')
    else:
        flash('An error occurred while inserting the product.')
    
    return redirect(url_for('index_inventario'))

@app_inventario.route('/edit_inventario/<int:id_inventario>', methods=['GET', 'POST'])
def edit_inventario(id_inventario):
    if request.method == 'POST':
        nombre_del_producto = request.form['nombre_del_producto']
        descripcion = request.form['descripcion']
        cantidad_en_stock = request.form['cantidad_en_stock']
        stock_minimo = request.form['stock_minimo']
        stock_maximo = request.form['stock_maximo']

        if not nombre_del_producto or not descripcion or not cantidad_en_stock or not stock_minimo or not stock_maximo:
            flash('All fields are required!')
            return redirect(url_for('edit_inventario', id_inventario=id_inventario))

        if update_user(id_inventario, nombre_del_producto, descripcion, cantidad_en_stock, stock_minimo, stock_maximo):
            flash('Product updated successfully!')
        else:
            flash('An error occurred while updating the product.')
        
        return redirect(url_for('inventario'))

    inventario = get_inventario_by_id(id_inventario)
    if inventario is None:
        flash('Product not found!')
        return redirect(url_for('inventario'))
    return render_template('edit_inventario.html', inventario=inventario)

@app_inventario.route('/eliminar_inventario/<int:id_inventario>', methods=['GET', 'POST'])
def eliminar_inventario(id_inventario):
    if request.method == 'POST':
        if delete_user(id_inventario):
            flash('Product deleted successfully!')
        else:
            flash('An error occurred while deleting the product.')
        return redirect(url_for('inventario'))

    inventario = get_inventario_by_id(id_inventario)
    if inventario is None:
        flash('Product not found!')
        return redirect(url_for('inventario'))
    return render_template('eliminar_inventario.html', inventario=inventario)

if __name__ == '__main__':
    app_inventario.run(debug=True, port=5001)
