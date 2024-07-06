from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app_cliente = Flask(__name__)
app_cliente.secret_key = 'your_secret_key'

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

def insert_user( nombre, apellido, fecha_nacimiento, email,telefono,direccion,fecha_registro):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    query = "INSERT INTO cliente ( nombre, apellido, fecha_nacimiento, email,telefono,direccion,fecha_registro) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
    values =( nombre, apellido, fecha_nacimiento, email,telefono,direccion,fecha_registro)
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

def get_cliente():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM cliente"
    try:
        cursor.execute(query)
        cliente = cursor.fetchall()
        return cliente
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
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
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_user(id_cliente, nombre, apellido, fecha_nacimiento, email,telefono,direccion,fecha_registro):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE cliente SET  nombre = %s, apellido = %s, fecha_nacimiento = %s, email = %s,telefono = %s,direccion = %s,fecha_registro = %s WHERE id_cliente = %s"
    values = ( nombre, apellido, fecha_nacimiento, email,telefono,direccion,fecha_registro,id_cliente)
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
    query = "SELECT * FROM cliente WHERE id_cliente LIKE %s OR nombre LIKE %s OR apellido LIKE %s OR fecha_nacimiento LIKE %s OR email LIKE %s OR telefono LIKE %s OR direccion LIKE %s  OR fecha_registro LIKE %s"
    values = (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}', f'%{search_query}',f'%{search_query}',f'%{search_query}00')
    try:
        cursor.execute(query, values)
        cliente = cursor.fetchall()
        return cliente
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

@app_cliente.route('/')
def index_cliente():
    return render_template('index_cliente.html')

@app_cliente.route('/cliente')
def cliente():
    search_query = request.args.get('search')
    if search_query:
        cliente = search_users(search_query)
    else:
        cliente = get_cliente()
    return render_template('cliente.html', cliente=cliente, search_query=search_query)

@app_cliente.route('/submit', methods=['POST'])
def submit():
    
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha_nacimiento = request.form['fecha_nacimiento']
    email = request.form['email']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    fecha_registro = request.form['fecha_registro']

    if not  nombre or not apellido or not fecha_nacimiento or not email or not telefono or not direccion or not fecha_registro:
        flash('All fields are required!')
        return redirect(url_for('index_cliente'))

    if insert_user( nombre, apellido, fecha_nacimiento, email,telefono,direccion,fecha_registro):
        flash('Product inserted successfully!')
    else:
        flash('An error occurred while inserting the product.')
    
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

        if not id_cliente or not nombre or not apellido or not fecha_nacimiento or not email or not telefono or not direccion or not fecha_registro:
            flash('All fields are required!')
            return redirect(url_for('edit_cliente', id_cliente=id_cliente))

        if update_user(id_cliente, nombre, apellido, fecha_nacimiento, email,telefono,direccion,fecha_registro):
            flash('Product updated successfully!')
        else:
            flash('An error occurred while updating the product.')
        
        return redirect(url_for('cliente'))

    cliente = get_cliente_by_id(id_cliente)
    if cliente is None:
        flash('Product not found!')
        return redirect(url_for('cliente'))
    return render_template('edit_cliente.html', cliente=cliente)

@app_cliente.route('/eliminar_cliente/<int:id_cliente>', methods=['GET', 'POST'])
def eliminar_cliente(id_cliente):
    if request.method == 'POST':
        if delete_user(id_cliente):
            flash('Product deleted successfully!')
        else:
            flash('An error occurred while deleting the product.')
        return redirect(url_for('cliente'))

    cliente = get_cliente_by_id(id_cliente)
    if cliente is None:
        flash('Product not found!')
        return redirect(url_for('cliente'))
    return render_template('eliminar_cliente.html', cliente=cliente)

if __name__ == '__main__':
    app_cliente.run(debug=True, port=5004)
