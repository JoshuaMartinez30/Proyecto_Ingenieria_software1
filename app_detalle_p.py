from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error
from decimal import Decimal

app_detalle_p = Flask(__name__)
app_detalle_p.secret_key = 'your_secret_key'

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

def insert_detalle(id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    INSERT INTO detalle_de_compra_proveedor (id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total)
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
    SELECT SQL_CALC_FOUND_ROWS d.id_detalle, p.id_pedido, pr.nombre AS producto, d.cantidad, d.precio_unitario, d.subtotal, i.tasa_impuesto, d.total
    FROM detalle_de_compra_proveedor d
    JOIN pedido_de_compra_proveedor p ON d.id_pedido = p.id_pedido
    JOIN producto pr ON d.id_producto = pr.id_producto
    JOIN impuesto i ON d.id_impuesto = i.id_impuesto
    LIMIT %s OFFSET %s
    """
    try:
        cursor.execute(query, (per_page, offset))
        detalles_p = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_detalles = cursor.fetchone()[0]
        return detalles_p, total_detalles
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
    query = "SELECT * FROM detalle_de_compra_proveedor WHERE id_detalle = %s"
    try:
        cursor.execute(query, (id_detalle,))
        detalle_p = cursor.fetchone()
        return detalle_p
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
    UPDATE detalle_de_compra_proveedor
    SET id_pedido = %s, id_producto = %s, cantidad = %s, precio_unitario = %s, subtotal = %s, id_impuesto = %s, total = %s
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

def delete_detalle(id_detalle):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM detalle_de_compra_proveedor WHERE id_detalle = %s"
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

@app_detalle_p.route('/')
def index_detalle_p():
    connection = create_connection()
    if connection is None:
        return render_template('index_detalle_p.html', pedidos=[], productos=[], impuestos=[])
    cursor = connection.cursor()

    cursor.execute("SELECT id_pedido FROM pedido_de_compra_proveedor")
    pedidos = cursor.fetchall()

    cursor.execute("SELECT id_producto, nombre FROM producto")
    productos = cursor.fetchall()

    cursor.execute("SELECT id_impuesto, tasa_impuesto FROM impuesto")
    impuestos = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('index_detalle_p.html', pedidos=pedidos, productos=productos, impuestos=impuestos)

@app_detalle_p.route('/detalles_p')
def detalles_p():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    detalles_p, total_detalles = get_detalles(page, per_page)
    total_pages = (total_detalles + per_page - 1) // per_page
    return render_template('detalles_p.html', detalles_p=detalles_p, page=page, per_page=per_page, total_detalles=total_detalles, total_pages=total_pages)

@app_detalle_p.route('/submit_detalle', methods=['POST'])
def submit_detalle():
    id_pedido = request.form['id_pedido']
    id_producto = request.form['id_producto']
    cantidad = float(request.form['cantidad'])
    precio_unitario = float(request.form['precio_unitario'])
    subtotal = cantidad * precio_unitario
    id_impuesto = request.form['id_impuesto']

    # Obtener la tasa de impuesto
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT tasa_impuesto FROM impuesto WHERE id_impuesto = %s"
    cursor.execute(query, (id_impuesto,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result is None:
        flash('Impuesto no encontrado!')
        return redirect(url_for('index_detalle_p'))

    tasa_impuesto = result[0]
    tasa_impuesto = float(tasa_impuesto) if isinstance(tasa_impuesto, Decimal) else float(tasa_impuesto)
    total = (subtotal * tasa_impuesto) + subtotal

    if not id_pedido or not id_producto or not cantidad or not precio_unitario or not subtotal or not id_impuesto or not total:
        flash('Todos los campos son requeridos!')
        return redirect(url_for('index_detalle_p'))

    if insert_detalle(id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total):
        flash('detalle_p insertado exitosamente!')
    else:
        flash('Ocurrió un error al insertar el detalle_p.')
    
    return redirect(url_for('index_detalle_p'))

@app_detalle_p.route('/edit_detalle_p/<int:id_detalle>', methods=['GET', 'POST'])
def edit_detalle_p(id_detalle):
    if request.method == 'POST':
        id_pedido = request.form['id_pedido']
        id_producto = request.form['id_producto']
        cantidad = float(request.form['cantidad'])
        precio_unitario = float(request.form['precio_unitario'])
        subtotal = float(request.form['subtotal'])
        id_impuesto = request.form['id_impuesto']
        total = float(request.form['total'])

        if not id_pedido or not id_producto or not cantidad or not precio_unitario or not subtotal or not id_impuesto or not total:
            flash('Todos los campos son requeridos!')
            return redirect(url_for('edit_detalle_p', id_detalle=id_detalle))

        if update_detalle(id_detalle, id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total):
            flash('detalle_p actualizado exitosamente!')
        else:
            flash('Ocurrió un error al actualizar el detalle_p.')
        
        return redirect(url_for('detalles_p'))

    detalle_p = get_detalle_by_id(id_detalle)
    if detalle_p is None:
        flash('detalle_p no encontrado!')
        return redirect(url_for('detalles_p'))

    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT id_pedido FROM pedido_de_compra_proveedor")
    pedidos = cursor.fetchall()

    cursor.execute("SELECT id_producto, nombre FROM producto")
    productos = cursor.fetchall()

    cursor.execute("SELECT id_impuesto, tasa_impuesto FROM impuesto")
    impuestos = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('edit_detalle_p.html', detalle_p=detalle_p, pedidos=pedidos, productos=productos, impuestos=impuestos)

@app_detalle_p.route('/eliminar_detalle_p/<int:id_detalle>', methods=['GET', 'POST'])
def eliminar_detalle_p(id_detalle):
    if request.method == 'POST':
        if delete_detalle(id_detalle):
            flash('detalle_p eliminado exitosamente!')
        else:
            flash('Ocurrió un error al eliminar el detalle_p.')
        return redirect(url_for('detalles_p'))

    detalle_p = get_detalle_by_id(id_detalle)
    if detalle_p is None:
        flash('detalle_p no encontrado!')
        return redirect(url_for('detalles_p'))

    return render_template('eliminar_detalle_p.html', detalle_p=detalle_p)

@app_detalle_p.route('/get_precio/<int:id_producto>', methods=['GET'])
def get_precio(id_producto):
    connection = create_connection()
    if connection is None:
        return {"precio_unitario": 0}, 500
    cursor = connection.cursor()
    query = "SELECT original_precio FROM producto WHERE id_producto = %s"
    try:
        cursor.execute(query, (id_producto,))
        result = cursor.fetchone()
        if result:
            return {"precio_unitario": float(result[0])}, 200
        else:
            return {"precio_unitario": 0}, 404
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return {"precio_unitario": 0}, 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app_detalle_p.run(debug=True,port=5022)
