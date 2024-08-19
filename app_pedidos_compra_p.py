import re
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from datetime import datetime


app_pedidos_compra_p = Flask(__name__)
app_pedidos_compra_p.secret_key = 'your_secret_key'

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

# Paso 1 :Para que sean seleccionables 
def get_estados():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_estado, nombre_estado FROM estado"
    try:
        cursor.execute(query)
        estados = cursor.fetchall()
        return estados
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def get_metodos():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_metodo, nombre FROM metodo_de_pago"
    try:
        cursor.execute(query)
        metodos = cursor.fetchall()
        return metodos
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def get_proveedores():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_proveedor, Nombre_del_proveedor FROM proveedores"
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

def insert_user(id_proveedor, numero_factura, fecha_pedido, fecha_entrega_estimada, fecha_entrega, id_metodo, id_estado):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
        INSERT INTO pedido_de_compra_proveedor 
        (id_proveedor,numero_factura, fecha_pedido, fecha_entrega_estimada, fecha_entrega, id_metodo, id_estado) 
        VALUES (%s, %s, %s, %s, %s, %s,%s)
    """
    values = (id_proveedor,numero_factura if numero_factura else None, fecha_pedido, fecha_entrega_estimada if fecha_entrega_estimada else None, 
              fecha_entrega if fecha_entrega else None, id_metodo, id_estado)
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




def get_pedidos_compra_p(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = """
        SELECT p.id_pedido, pr.Nombre_del_proveedor,p.numero_factura, p.fecha_pedido, p.fecha_entrega_estimada, p.fecha_entrega, mp.nombre, e.nombre_estado
        FROM pedido_de_compra_proveedor p
        JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
        JOIN metodo_de_pago mp ON p.id_metodo = mp.id_metodo
        JOIN estado e ON p.id_estado = e.id_estado
        LIMIT %s OFFSET %s
    """
    try:
        cursor.execute(query, (per_page, offset))
        pedidos_compra_p = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_pedidos_compra_p = cursor.fetchone()[0]
        return pedidos_compra_p, total_pedidos_compra_p
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()


def get_pedidos_compra_p_by_id(id_pedido):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = """
        SELECT id_pedido, id_proveedor, numero_factura, fecha_pedido, fecha_entrega_estimada, fecha_entrega, id_metodo, id_estado
        FROM pedido_de_compra_proveedor
        WHERE id_pedido = %s
    """
    try:
        cursor.execute(query, (id_pedido,))
        pedidos_compra_p = cursor.fetchone()
        return pedidos_compra_p
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()


def update_user(id_pedido, numero_factura, id_proveedor, fecha_pedido, fecha_entrega_estimada, fecha_entrega, id_metodo, id_estado):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
        UPDATE pedido_de_compra_proveedor 
        SET id_proveedor = %s, numero_factura = %s,fecha_pedido = %s, fecha_entrega_estimada = %s, fecha_entrega = %s, id_metodo = %s, id_estado = %s 
        WHERE id_pedido = %s
    """
    values = (id_proveedor,numero_factura if numero_factura else None, fecha_pedido, fecha_entrega_estimada if fecha_entrega_estimada else None, 
              fecha_entrega if fecha_entrega else None, id_metodo, id_estado, id_pedido)
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



def delete_pedido(id_pedido):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM pedido_de_compra_proveedor WHERE id_pedido = %s"
    try:
        cursor.execute(query, (id_pedido,))
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
    query = f"""
        SELECT p.id_pedido, pr.Nombre_del_proveedor,p.numero_factura, p.fecha_pedido, p.fecha_entrega, mp.nombre, e.nombre_estado
        FROM pedido_de_compra_proveedor p
        JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
        JOIN metodo_de_pago mp ON p.id_metodo = mp.id_metodo
        JOIN estado e ON p.id_estado = e.id_estado
        WHERE {search_field} LIKE %s
        LIMIT %s OFFSET %s
    """
    values = (f'%{search_query}%', per_page, offset)
    try:
        cursor.execute(query, values)
        pedidos_compra_p = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_pedidos_compra_p = cursor.fetchone()[0]
        return pedidos_compra_p, total_pedidos_compra_p
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()


def is_valid(text):
    if re.search(r'[^a-zA-Z0-9 ]', text):  # Caracteres especiales
        return False
    if re.search(r'(.)\1\1', text):  # Mismo carácter repetido más de dos veces
        return False
    if len(text) < 3:  # Longitud mínima de 3 caracteres
        return False
    if re.search(r'([aeiouAEIOU])\1', text):  # Misma vocal repetida dos veces consecutivas
        return False
    return True

#Paso 2 para que sean seleccionables
@app_pedidos_compra_p.route('/')
def index_pedidos_compra_p():
    estados = get_estados()
    metodos = get_metodos()
    proveedores= get_proveedores()

    return render_template('index_pedidos_compra_p.html', estados=estados, metodos=metodos, proveedores=proveedores)

@app_pedidos_compra_p.route('/pedidos_compra_pv')
def pedidos_compra_pv():
    search_query = request.args.get('search')
    search_field = request.args.get('field')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if search_query and search_field:
        pedidos_compra_p, total_pedidos_compra_p = search_users(search_query, search_field, page, per_page)
    else:
        pedidos_compra_p, total_pedidos_compra_p = get_pedidos_compra_p(page, per_page)

    total_pages = (total_pedidos_compra_p + per_page - 1) // per_page
    return render_template('pedidos_compra_pv.html', pedidos_compra_p=pedidos_compra_p, search_query=search_query, search_field=search_field, page=page, per_page=per_page, total_pedidos_compra_p=total_pedidos_compra_p, total_pages=total_pages)

@app_pedidos_compra_p.route('/submit', methods=['POST'])
def submit():
    id_proveedor = request.form['id_proveedor']
    numero_factura=request.form['numero_factura']
    fecha_pedido = request.form['fecha_pedido']
    fecha_entrega_estimada = request.form['fecha_entrega_estimada']
    fecha_entrega = request.form['fecha_entrega'] or None  # Set to None if empty
    id_metodo = request.form['id_metodo']
    id_estado = request.form['id_estado']
    
    if not id_proveedor or not fecha_pedido or not id_metodo or not id_estado:
        flash('All fields are required except Fecha Entrega and Fecha Entrega Estimada!')
        return redirect(url_for('index_pedidos_compra_p'))
       
    if insert_user(id_proveedor,numero_factura, fecha_pedido, fecha_entrega_estimada, fecha_entrega, id_metodo, id_estado):
        flash('Pedido inserted successfully!')
    else:
        flash('An error occurred while inserting the pedido.')
    
    return redirect(url_for('index_pedidos_compra_p'))


@app_pedidos_compra_p.route('/edit_pedidos_compra_p/<int:id_pedido>', methods=['GET', 'POST'])
def edit_pedidos_compra_p(id_pedido):
    if request.method == 'POST':
        id_proveedor = request.form['id_proveedor']
        numero_factura = request.form['numero_factura']  # Este campo no será requerido
        fecha_pedido = request.form['fecha_pedido']
        fecha_entrega_estimada = request.form['fecha_entrega_estimada']
        fecha_entrega = request.form['fecha_entrega'] or None  # Puede ser vacío
        id_metodo = request.form['id_metodo']
        id_estado = request.form['id_estado']  # Asegúrate que sea el mismo nombre que el del input oculto

        if not id_proveedor or not fecha_pedido or not id_metodo or not id_estado:
            flash('Todos los campos son obligatorios excepto "Fecha Entrega" y "Número de Factura".')
            return redirect(url_for('edit_pedidos_compra_p', id_pedido=id_pedido))

        # Asegúrate que esta función sea la correcta
        if update_user(id_pedido, numero_factura, id_proveedor, fecha_pedido, fecha_entrega_estimada, fecha_entrega, id_metodo, id_estado):
            flash('Pedido actualizado exitosamente', 'success')
            return redirect(url_for('pedidos_compra_pv'))
        else:
            flash('Ocurrió un error al actualizar el pedido.', 'danger')
            return redirect(url_for('edit_pedidos_compra_p', id_pedido=id_pedido))

    pedido = get_pedidos_compra_p_by_id(id_pedido)
    if not pedido:
        flash('Pedido no encontrado!', 'danger')
        return redirect(url_for('pedidos_compra_pv'))

    estados = get_estados()
    metodos = get_metodos()
    proveedores = get_proveedores()

    return render_template('edit_pedidos_compra_p.html', pedido=pedido, estados=estados, metodos=metodos, proveedores=proveedores)



@app_pedidos_compra_p.route('/eliminar_pedidos_compra_p/<int:id_pedido>', methods=['GET', 'POST'])
def eliminar_pedido(id_pedido):  
    if request.method == 'POST':
        if delete_pedido(id_pedido):
            flash('¡Pedido eliminado exitosamente!')
            return redirect(url_for('pedidos_compra_pv'))
        else:
            flash('Ocurrió un error al eliminar el pedido. Por favor, intente nuevamente.')
            return redirect(url_for('pedidos_compra_pv'))

    pedido = get_pedidos_compra_p_by_id(id_pedido)
    if pedido is None:
        flash('Pedido no encontrado.')
        return redirect(url_for('pedidos_compra_pv'))
    estados = get_estados()
    metodos = get_metodos()
    proveedores = get_proveedores()

    return render_template('eliminar_pedidos_compra_p.html', pedido=pedido, estados=estados, metodos=metodos, proveedores=proveedores)


    
if __name__ == '__main__':

    app_pedidos_compra_p.run(debug=True, port=5040)
