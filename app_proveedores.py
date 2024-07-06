from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

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

def insert_user(Nombre_del_proveedor, Contacto, Producto_Servicio, Historial_de_desempeño, id_pedido, id_marca):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    query = "INSERT INTO proveedores (Nombre_del_proveedor, Contacto, Producto_Servicio, Historial_de_desempeño, id_pedido, id_marca) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (Nombre_del_proveedor, Contacto, Producto_Servicio, Historial_de_desempeño, id_pedido, id_marca)
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
 
def get_proveedor():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM proveedores"
    try:
        cursor.execute(query)
        proveedores = cursor.fetchall()
        return proveedores
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
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

def update_user(id_proveedor, Nombre_del_proveedor, Contacto, Producto_Servicio, Historial_de_desempeño, id_pedido, id_marca):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    UPDATE proveedores
    SET Nombre_del_proveedor = %s, Contacto = %s, Producto_Servicio = %s, Historial_de_desempeño = %s, id_pedido = %s, id_marca = %s
    WHERE id_proveedor = %s
    """
    values = (Nombre_del_proveedor, Contacto, Producto_Servicio, Historial_de_desempeño, id_pedido, id_marca, id_proveedor)
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

def delete_user(id_proveedor):
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

def search_users(search_query):
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM proveedores WHERE Nombre_del_proveedor LIKE %s"
    values = (f'%{search_query}%',)
    try:
        cursor.execute(query, values)
        proveedores = cursor.fetchall()
        return proveedores
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()


@app_proveedores.route('/')
def index_proveedores():
    return render_template('index_proveedores.html')

@app_proveedores.route('/proveedores')
def proveedores():
    search_query = request.args.get('search')
    if search_query:
        proveedores = search_users(search_query)
    else:
        proveedores = get_proveedor()
    return render_template('proveedores.html', proveedores=proveedores, search_query=search_query)

@app_proveedores.route('/submit', methods=['POST'])
def submit():

    Nombre_del_proveedor = request.form['Nombre_del_proveedor']
    Contacto = request.form['Contacto']
    Producto_Servicio = request.form['Producto_Servicio']
    Historial_de_desempeño = request.form['Historial_de_desempeño']
    id_pedido = request.form['id_pedido']
    id_marca = request.form['id_marca']


    if not Nombre_del_proveedor or not Contacto or not Producto_Servicio or not Historial_de_desempeño or not id_pedido or not id_marca:
        flash('Todos los campos son necesarios')
        return redirect(url_for('index_proveedores'))

    if insert_user(Nombre_del_proveedor, Contacto, Producto_Servicio, Historial_de_desempeño, id_pedido, id_marca):
        flash('User inserted successfully!')
    else:
        flash('An error occurred while inserting the user.')
    
    return redirect(url_for('index_proveedores'))

@app_proveedores.route('/edit/<int:id_proveedor>', methods=['GET', 'POST'])
def edit_proveedores(id_proveedor):
    if request.method == 'POST':
        Nombre_del_proveedor = request.form['Nombre_del_proveedor']
        Contacto = request.form['Contacto']
        Producto_Servicio = request.form['Producto_Servicio']
        Historial_de_desempeño = request.form['Historial_de_desempeño']
        id_pedido = request.form['id_pedido']
        id_marca = request.form['id_marca']

        if not Nombre_del_proveedor or not Contacto or not Producto_Servicio or not Historial_de_desempeño or not id_pedido or not id_marca:
            flash('All fields are required!')
            return redirect(url_for('edit_proveedores', id_proveedor=id_proveedor))

        if update_user(id_proveedor, Nombre_del_proveedor, Contacto, Producto_Servicio, Historial_de_desempeño, id_pedido, id_marca):
            flash('User updated successfully!')
        else:
            flash('An error occurred while updating the user.')
        
        return redirect(url_for('proveedores'))

    proveedores = get_proveedor_by_id(id_proveedor)
    if proveedores is None:
        flash('Proveedor not found!')
        return redirect(url_for('proveedores'))
    return render_template('edit_proveedores.html', proveedores=proveedores)


@app_proveedores.route('/eliminar/<int:id_proveedor>', methods=['GET', 'POST'])
def eliminar_proveedores(id_proveedor):
    if request.method == 'POST':
        if delete_user(id_proveedor):
            flash('Product deleted successfully!')
        else:
            flash('An error occurred while deleting the product.')
        return redirect(url_for('proveedores'))

    proveedores = get_proveedor_by_id(id_proveedor)
    if proveedores is None:
        flash('Product not found!')
        return redirect(url_for('proveedor'))
    return render_template('eliminar_proveedores.html', proveedores=proveedores)

if __name__ == '__main__':
    app_proveedores.run(debug=True, port=5005)

