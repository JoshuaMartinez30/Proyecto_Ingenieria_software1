from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error
from decimal import Decimal

app_detalle = Flask(__name__)
app_detalle.secret_key = 'your_secret_key'

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

def insert_detalle(id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total, id_empleado):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    INSERT INTO detalle_de_compra_cliente (id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total, id_empleado)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total, id_empleado)
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
    SELECT SQL_CALC_FOUND_ROWS d.id_detalle, p.id_pedido, pr.nombre AS producto, d.cantidad, d.precio_unitario, d.subtotal, i.tasa_impuesto, d.total, 
           CONCAT(e.nombre, ' ', e.apellido) AS empleado
    FROM detalle_de_compra_cliente d
    JOIN pedido_de_compra_cliente p ON d.id_pedido = p.id_pedido
    JOIN producto pr ON d.id_producto = pr.id_producto
    JOIN impuesto i ON d.id_impuesto = i.id_impuesto
    JOIN empleados e ON d.id_empleado = e.id_empleado
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
    SELECT d.id_detalle, p.id_pedido, pr.nombre AS producto, d.cantidad, d.precio_unitario, d.subtotal, i.tasa_impuesto, d.total, 
           CONCAT(e.nombre, ' ', e.apellido) AS empleado
    FROM detalle_de_compra_cliente d
    JOIN pedido_de_compra_cliente p ON d.id_pedido = p.id_pedido
    JOIN producto pr ON d.id_producto = pr.id_producto
    JOIN impuesto i ON d.id_impuesto = i.id_impuesto
    JOIN empleados e ON d.id_empleado = e.id_empleado
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


def update_detalle(id_detalle, id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total, id_empleado):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    UPDATE detalle_de_compra_cliente
    SET id_pedido = %s, id_producto = %s, cantidad = %s, precio_unitario = %s, subtotal = %s, id_impuesto = %s, total = %s, id_empleado = %s
    WHERE id_detalle = %s
    """
    values = (id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total, id_empleado, id_detalle)
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

@app_detalle.route('/')
def index_detalle():
    connection = create_connection()
    if connection is None:
        return render_template('index_detalle.html', pedidos=[], productos=[], impuestos=[], empleados=[], max_pedido=None)
    cursor = connection.cursor()

    cursor.execute("SELECT id_pedido FROM pedido_de_compra_cliente")
    pedidos = cursor.fetchall()

    cursor.execute("SELECT id_producto, nombre FROM producto")
    productos = cursor.fetchall()

    cursor.execute("SELECT id_impuesto, tasa_impuesto FROM impuesto")
    impuestos = cursor.fetchall()

    cursor.execute("SELECT id_empleado, nombre, apellido FROM empleados")
    empleados = cursor.fetchall()
    cursor.execute("SELECT MAX(id_pedido) FROM pedido_de_compra_cliente")
    max_pedido = cursor.fetchone()[0]
    
    cursor.close()
    connection.close()

    return render_template('index_detalle.html', pedidos=pedidos, productos=productos, impuestos=impuestos, empleados=empleados, max_pedido=max_pedido)

@app_detalle.route('/detalles')
def detalles():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    detalles, total_detalles = get_detalles(page, per_page)
    total_pages = (total_detalles + per_page - 1) // per_page
    return render_template('detalles.html', detalles=detalles, page=page, per_page=per_page, total_detalles=total_detalles, total_pages=total_pages)

@app_detalle.route('/submit_detalle', methods=['POST'])
def submit_detalle():
    id_pedido = request.form['id_pedido']
    productos = request.form.getlist('id_producto')  # Obtén la lista de productos seleccionados
    cantidades = request.form.getlist('cantidad')    # Obtén la lista de cantidades
    precios_unitarios = request.form.getlist('precio_unitario')
    id_impuesto = request.form['id_impuesto']
    id_empleado = request.form['id_empleado']

    # Obtener la tasa de impuesto
    connection = create_connection()
    cursor = connection.cursor()
    query_impuesto = "SELECT tasa_impuesto FROM impuesto WHERE id_impuesto = %s"
    cursor.execute(query_impuesto, (id_impuesto,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result is None:
        flash('Impuesto no encontrado!')
        return redirect(url_for('index_detalle'))

    tasa_impuesto = float(result[0])
    detalles_insertados = True

    for i in range(len(productos)):
        id_producto = productos[i]
        cantidad = float(cantidades[i])
        precio_unitario = float(precios_unitarios[i])
        subtotal = cantidad * precio_unitario
        total = subtotal * (1 + tasa_impuesto / 100)

        if not insert_detalle(id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total,id_empleado):
            detalles_insertados = False
            break

    if detalles_insertados:
        flash('Detalles insertados exitosamente!')
    else:
        flash('Ocurrió un error al insertar algunos detalles.')

    return redirect(url_for('index_detalle'))

@app_detalle.route('/edit_detalle/<int:id_detalle>', methods=['GET', 'POST'])
def edit_detalle(id_detalle):
    if request.method == 'POST':
        id_pedido = request.form['id_pedido']
        id_producto = request.form['id_producto']
        cantidad = float(request.form['cantidad'])
        precio_unitario = float(request.form['precio_unitario'])
        subtotal = float(request.form['subtotal'])
        id_impuesto = request.form['id_impuesto']
        total = float(request.form['total'])
        id_empleado = request.form['id_empleado']

        if not id_pedido or not id_producto or not cantidad or not precio_unitario or not subtotal or not id_impuesto or not total or not id_empleado:
            flash('Todos los campos son requeridos!')
            return redirect(url_for('edit_detalle', id_detalle=id_detalle))

        if update_detalle(id_detalle, id_pedido, id_producto, cantidad, precio_unitario, subtotal, id_impuesto, total):
            flash('Detalle actualizado exitosamente!')
        else:
            flash('Ocurrió un error al actualizar el detalle.')
        
        return redirect(url_for('detalles'))

    detalle = get_detalle_by_id(id_detalle)
    if detalle is None:
        flash('Detalle no encontrado!')
        return redirect(url_for('detalles'))

    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT id_pedido FROM pedido_de_compra_cliente")
    pedidos = cursor.fetchall()

    cursor.execute("SELECT id_producto, nombre FROM producto")
    productos = cursor.fetchall()

    cursor.execute("SELECT id_impuesto, tasa_impuesto FROM impuesto")
    impuestos = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('edit_detalle.html', detalle=detalle, pedidos=pedidos, productos=productos, impuestos=impuestos)

@app_detalle.route('/eliminar_detalle/<int:id_detalle>', methods=['GET', 'POST'])
def eliminar_detalle(id_detalle):
    if request.method == 'POST':
        if delete_detalle(id_detalle):
            flash('Detalle eliminado exitosamente!')
        else:
            flash('Ocurrió un error al eliminar el detalle.')
        return redirect(url_for('detalles'))

    detalle = get_detalle_by_id(id_detalle)
    if detalle is None:
        flash('Detalle no encontrado!')
        return redirect(url_for('detalles'))

    return render_template('eliminar_detalle.html', detalle=detalle)

@app_detalle.route('/get_precio/<int:id_producto>', methods=['GET'])
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
    app_detalle.run(debug=True, port=5023)
