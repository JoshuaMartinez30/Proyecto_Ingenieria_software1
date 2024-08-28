from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app_detalles_compra = Flask(__name__)
app_detalles_compra.secret_key = 'your_secret_key'

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="qEeKLgpIkdarsoNT",
            database="proyecto_is1"
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos MySQL")
    except Error as e:
        print(f"Error '{e}' ocurrió")
    return connection

def insert_detalle(id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    INSERT INTO detalle_de_compra_cliente
    (id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total)
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


def get_detalles(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = """
    SELECT SQL_CALC_FOUND_ROWS d.id_detalle, p.id_pedido, pr.nombre AS nombre_producto,
           d.cantidad, d.precio_unitario, d.subtotal, i.tasa_impuesto, d.total
    FROM detalle_de_compra_cliente d
    JOIN pedido_de_compra_cliente p ON d.id_pedido = p.id_pedido
    JOIN producto pr ON d.id_producto = pr.id_producto
    JOIN impuesto i ON d.id_impuesto = i.id_impuesto
    LIMIT %s OFFSET %s
    """
    try:
        cursor.execute(query, (per_page, offset))
        detalles = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_detalles = cursor.fetchone()[0]
        return detalles, total_detalles
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_detalle_by_id(id_detalle):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = """
    SELECT d.id_detalle, d.id_pedido, d.id_producto, d.cantidad, d.precio_unitario, 
           d.subtotal, d.id_impuesto, d.total
    FROM detalle_de_compra_cliente d
    WHERE d.id_detalle = %s
    """
    try:
        cursor.execute(query, (id_detalle,))
        detalle = cursor.fetchone()
        return detalle
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return None
    finally:
        cursor.close()
        connection.close()

def update_detalle(id_detalle, id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    UPDATE detalle_de_compra_cliente
    SET id_pedido = %s, id_producto = %s, cantidad = %s, precio_unitario = %s, 
        subtotal = %s, id_impuesto = %s, total = %s
    WHERE id_detalle = %s
    """
    values = (id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total, id_detalle)
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

# Cambié el nombre de esta función a remove_detalle para evitar conflictos
def remove_detalle(id_detalle):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM detalle_de_compra_cliente WHERE id_detalle = %s"
    try:
        cursor.execute(query, (id_detalle,))
        connection.commit()
        return True
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

@app_detalles_compra.route('/get_stock/<int:id_producto>', methods=['GET'])
def get_stock(id_producto):
    connection = create_connection()
    if connection is None:
        return {'stock': 'N/A'}, 500
    
    cursor = connection.cursor()
    query = """
    SELECT cantidad_en_stock
    FROM inventario
    WHERE id_producto = %s
    """
    cursor.execute(query, (id_producto,))
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if result:
        return {'stock': result[0]}, 200
    else:
        return {'stock': 'N/A'}, 404

@app_detalles_compra.route('/index_detalle')
def index_detalles():
    connection = create_connection()
    if connection is None:
        return render_template('index_detalles.html', pedidos=[], productos=[], impuestos=[])

    cursor = connection.cursor()

    cursor.execute("SELECT id_pedido FROM pedido_de_compra_cliente")
    pedidos = cursor.fetchall()

    cursor.execute("SELECT id_producto, nombre, original_precio FROM producto")
    productos = cursor.fetchall()

    cursor.execute("SELECT id_impuesto, tasa_impuesto FROM impuesto")
    impuestos = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('index_detalles.html', pedidos=pedidos, productos=productos, impuestos=impuestos)

@app_detalles_compra.route('/detalles_compra')
def detalles_compra():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    detalles, total_detalles = get_detalles(page, per_page)
    total_pages = (total_detalles + per_page - 1) // per_page
    return render_template('detalles_compra.html', detalles=detalles, page=page, per_page=per_page, total_detalles=total_detalles, total_pages=total_pages)

@app_detalles_compra.route('/submit_detalle', methods=['POST'])
def submit_detalle():
    id_pedido = request.form.get('id_pedido')
    id_producto = request.form.get('id_producto')
    cantidad = request.form.get('cantidad')
    precio_unitario = request.form.get('precio_unitario')
    subtotal = request.form.get('subtotal')
    id_impuesto = request.form.get('id_impuesto')
    total = request.form.get('total')

    # Imprime los datos recibidos para depuración
    print("Datos del formulario:")
    print("id_pedido:", id_pedido)
    print("id_producto:", id_producto)
    print("cantidad:", cantidad)
    print("precio_unitario:", precio_unitario)
    print("subtotal:", subtotal)
    print("id_impuesto:", id_impuesto)
    print("total:", total)

    if not id_pedido or not id_producto or not cantidad or not precio_unitario or not id_impuesto:
        flash('Todos los campos son requeridos!')
        return redirect(url_for('index_detalles'))

    if insert_detalle(id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total):
        flash('Detalle insertado exitosamente!')
    else:
        flash('Ocurrió un error al insertar el detalle.')
    
    return redirect(url_for('index_detalles'))

@app_detalles_compra.route('/edit_detalle/<int:id_detalle>', methods=['GET', 'POST'])
def edit_detalle(id_detalle):
    if request.method == 'POST':
        id_pedido = request.form['id_pedido']
        id_producto = request.form['id_producto']
        cantidad = request.form['cantidad']
        precio_unitario = request.form['precio_unitario']
        subtotal = request.form['subtotal']
        id_impuesto = request.form['id_impuesto']
        total = request.form['total']

        if not id_pedido or not id_producto or not cantidad or not precio_unitario or not id_impuesto or not total:
            flash('Todos los campos son requeridos!')
            return redirect(url_for('edit_detalle', id_detalle=id_detalle))

        if update_detalle(id_detalle, id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total):
            flash('Detalle actualizado exitosamente!')
        else:
            flash('Ocurrió un error al actualizar el detalle.')
        
        return redirect(url_for('detalles_compra'))

    detalle = get_detalle_by_id(id_detalle)
    if detalle is None:
        flash('Detalle no encontrado!')
        return redirect(url_for('detalles_compra'))
    
    connection = create_connection()
    if connection is None:
        return render_template('edit_detalle.html', detalle=detalle, pedidos=[], productos=[], impuestos=[])

    cursor = connection.cursor()

    cursor.execute("SELECT id_pedido FROM pedido_de_compra_cliente")
    pedidos = cursor.fetchall()

    cursor.execute("SELECT id_producto, nombre, original_precio FROM producto")
    productos = cursor.fetchall()

    cursor.execute("SELECT id_impuesto, tasa_impuesto FROM impuesto")
    impuestos = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('edit_detalle.html', detalle=detalle, pedidos=pedidos, productos=productos, impuestos=impuestos)

@app_detalles_compra.route('/delete_detalle/<int:id_detalle>', methods=['POST'])
def delete_detalle(id_detalle):
    if remove_detalle(id_detalle):
        flash('Detalle eliminado exitosamente!')
    else:
        flash('Ocurrió un error al eliminar el detalle.')
    return redirect(url_for('detalles_compra'))


if __name__ == '__main__':
    app_detalles_compra.run(debug=True, port=5023)
