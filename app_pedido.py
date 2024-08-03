from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app_pedido = Flask(__name__)
app_pedido.secret_key = 'your_secret_key'

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

def insert_pedido(id_cliente, fecha_pedido, fecha_entrega, id_metodo, id_estado):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    INSERT INTO pedido_de_compra_cliente (id_cliente, fecha_pedido, fecha_entrega, id_metodo, id_estado)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (id_cliente, fecha_pedido, fecha_entrega, id_metodo, id_estado)
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

def get_pedidos(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = """
    SELECT SQL_CALC_FOUND_ROWS p.id_pedido, c.nombre AS nombre_cliente, p.fecha_pedido, p.fecha_entrega, m.nombre AS metodo_pago, e.nombre_estado
    FROM pedido_de_compra_cliente p
    JOIN cliente c ON p.id_cliente = c.id_cliente
    JOIN metodo_de_pago m ON p.id_metodo = m.id_metodo
    JOIN estado e ON p.id_estado = e.id_estado
    LIMIT %s OFFSET %s
    """
    try:
        cursor.execute(query, (per_page, offset))
        pedidos = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_pedidos = cursor.fetchone()[0]
        return pedidos, total_pedidos
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_pedido_by_id(id_pedido):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM pedido_de_compra_cliente WHERE id_pedido = %s"
    try:
        cursor.execute(query, (id_pedido,))
        pedido = cursor.fetchone()
        return pedido
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return None
    finally:
        cursor.close()
        connection.close()

def update_pedido(id_pedido, id_cliente, fecha_pedido, fecha_entrega, id_metodo, id_estado):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    UPDATE pedido_de_compra_cliente
    SET id_cliente = %s, fecha_pedido = %s, fecha_entrega = %s, id_metodo = %s, id_estado = %s
    WHERE id_pedido = %s
    """
    values = (id_cliente, fecha_pedido, fecha_entrega, id_metodo, id_estado, id_pedido)
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

def delete_pedido(id_pedido):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM pedido_de_compra_cliente WHERE id_pedido = %s"
    try:
        cursor.execute(query, (id_pedido,))
        connection.commit()
        return True
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

@app_pedido.route('/')
def index_pedido():
    connection = create_connection()
    if connection is None:
        return render_template('index_pedido.html', clientes=[], metodos=[], estados=[])
    cursor = connection.cursor()

    cursor.execute("SELECT id_cliente, nombre FROM cliente")
    clientes = cursor.fetchall()

    cursor.execute("SELECT id_metodo, nombre FROM metodo_de_pago")
    metodos = cursor.fetchall()

    cursor.execute("SELECT id_estado, nombre_estado FROM estado")
    estados = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('index_pedido.html', clientes=clientes, metodos=metodos, estados=estados)

@app_pedido.route('/pedidos')
def pedidos():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    if search_query:
        pedidos, total_pedidos = search_pedidos(search_query, page, per_page)
    else:
        pedidos, total_pedidos = get_pedidos(page, per_page)

    total_pages = (total_pedidos + per_page - 1) // per_page
    return render_template('pedidos.html', pedidos=pedidos, search_query=search_query, page=page, per_page=per_page, total_pedidos=total_pedidos, total_pages=total_pages)

@app_pedido.route('/submit', methods=['POST'])
def submit():
    id_cliente = request.form['id_cliente']
    fecha_pedido = request.form['fecha_pedido']
    fecha_entrega = request.form['fecha_entrega']
    id_metodo = request.form['id_metodo']
    id_estado = request.form['id_estado']

    if not id_cliente or not fecha_pedido or not fecha_entrega or not id_metodo or not id_estado:
        flash('Todos los campos son requeridos!')
        return redirect(url_for('index_pedido'))

    if insert_pedido(id_cliente, fecha_pedido, fecha_entrega, id_metodo, id_estado):
        flash('Pedido insertado exitosamente!')
    else:
        flash('Ocurrió un error al insertar el pedido.')
    
    return redirect(url_for('index_pedido'))

@app_pedido.route('/edit_pedido/<int:id_pedido>', methods=['GET', 'POST'])
def edit_pedido(id_pedido):
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        fecha_pedido = request.form['fecha_pedido']
        fecha_entrega = request.form['fecha_entrega']
        id_metodo = request.form['id_metodo']
        id_estado = request.form['id_estado']

        if not id_cliente or not fecha_pedido or not fecha_entrega or not id_metodo or not id_estado:
            flash('Todos los campos son requeridos!')
            return redirect(url_for('edit_pedido', id_pedido=id_pedido))

        if update_pedido(id_pedido, id_cliente, fecha_pedido, fecha_entrega, id_metodo, id_estado):
            flash('Pedido actualizado exitosamente!')
        else:
            flash('Ocurrió un error al actualizar el pedido.')
        
        return redirect(url_for('pedidos'))

    pedido = get_pedido_by_id(id_pedido)
    if pedido is None:
        flash('Pedido no encontrado!')
        return redirect(url_for('pedidos'))

    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT id_cliente, nombre FROM cliente")
    clientes = cursor.fetchall()

    cursor.execute("SELECT id_metodo, nombre FROM metodo_de_pago")
    metodos = cursor.fetchall()

    cursor.execute("SELECT id_estado, nombre_estado FROM estado")
    estados = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('edit_pedido.html', pedido=pedido, clientes=clientes, metodos=metodos, estados=estados)

@app_pedido.route('/eliminar_pedido/<int:id_pedido>', methods=['GET', 'POST'])
def eliminar_pedido(id_pedido):
    if request.method == 'POST':
        if delete_pedido(id_pedido):
            flash('Pedido eliminado exitosamente!')
        else:
            flash('Ocurrió un error al eliminar el pedido.')
        return redirect(url_for('pedidos'))

    pedido = get_pedido_by_id(id_pedido)
    if pedido is None:
        flash('Pedido no encontrado!')
        return redirect(url_for('pedidos'))
    return render_template('eliminar_pedido.html', pedido=pedido)

def search_pedidos(search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    
    query = """
    SELECT SQL_CALC_FOUND_ROWS p.id_pedido, c.nombre AS nombre_cliente, p.fecha_pedido, p.fecha_entrega, m.nombre AS metodo_pago, e.nombre_estado
    FROM pedido_de_compra_cliente p
    JOIN cliente c ON p.id_cliente = c.id_cliente
    JOIN metodo_de_pago m ON p.id_metodo = m.id_metodo
    JOIN estado e ON p.id_estado = e.id_estado
    WHERE c.nombre LIKE %s
    LIMIT %s OFFSET %s
    """
    try:
        cursor.execute(query, ('%' + search_query + '%', per_page, offset))
        pedidos = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_pedidos = cursor.fetchone()[0]
        return pedidos, total_pedidos
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app_pedido.run(debug=True,port=5012)
