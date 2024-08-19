from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app_devoluciones = Flask(__name__)
app_devoluciones.secret_key = 'your_secret_key'  # Cambia 'your_secret_key' por una clave secreta segura

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
            print("Conexión a la base de datos MySQL exitosa.")
    except Error as e:
        print(f"Error '{e}' ocurrió")
    return connection

def insert_devolucion(id_pedido, id_detalle, fecha_devolucion, motivo, cantidad_devuelta):
    connection = create_connection()
    if connection is None:
        print("Error: No se pudo conectar a la base de datos.")
        return False
    
    cursor = connection.cursor()
    query = """INSERT INTO devoluciones_ventas (id_pedido, id_detalle, fecha_devolucion, motivo, cantidad_devuelta) VALUES (%s, %s, %s, %s, %s)"""
    values = (id_pedido, id_detalle, fecha_devolucion, motivo, cantidad_devuelta)
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Devolución insertada exitosamente.")
        return True
    except Error as e:
        print(f"Error al insertar la devolución: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


def get_devoluciones(page, per_page, search_query=None):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    if search_query:
        query = """
            SELECT d.id_devolucion, d.id_pedido, dt.id_detalle, p.nombre AS nombre_producto, 
                   d.fecha_devolucion, d.motivo, d.cantidad_devuelta
            FROM devoluciones_ventas d
            JOIN detalle_de_compra_cliente dt ON d.id_detalle = dt.id_detalle
            JOIN producto p ON dt.id_producto = p.id_producto
            WHERE d.id_devolucion LIKE %s OR d.id_pedido LIKE %s
            LIMIT %s OFFSET %s
        """
        values = (f'%{search_query}%', f'%{search_query}%', per_page, offset)
    else:
        query = """
            SELECT d.id_devolucion, d.id_pedido, dt.id_detalle, p.nombre AS nombre_producto, 
                   d.fecha_devolucion, d.motivo, d.cantidad_devuelta
            FROM devoluciones_ventas d
            JOIN detalle_de_compra_cliente dt ON d.id_detalle = dt.id_detalle
            JOIN producto p ON dt.id_producto = p.id_producto
            LIMIT %s OFFSET %s
        """
        values = (per_page, offset)

    try:
        cursor.execute(query, values)
        devoluciones = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_count = cursor.fetchone()[0]
        return devoluciones, total_count
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()


def get_pedidos():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_pedido, fecha_pedido FROM pedido_de_compra_cliente"  # Cambiar el nombre de la tabla aquí
    try:
        cursor.execute(query)
        pedidos = cursor.fetchall()
        return pedidos
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return []
    finally:
        cursor.close()
        connection.close()

def get_detalles_by_pedido(id_pedido):
    connection = create_connection()
    if connection is None:
        return []
    
    cursor = connection.cursor()
    query = """
        SELECT dt.id_detalle, dt.id_producto, dt.cantidad, dt.precio_unitario 
        FROM detalle_de_compra_cliente dt 
        WHERE dt.id_pedido = %s
    """
    try:
        cursor.execute(query, (id_pedido,))
        detalles = cursor.fetchall()
        print(f"Detalles for ID {id_pedido}: {detalles}")  # Debug line
        return detalles
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return []
    finally:
        cursor.close()
        connection.close()


def update_devolucion(id_devolucion, id_pedido, id_detalle, fecha_devolucion, motivo, cantidad_devuelta):
    connection = create_connection()
    if connection is None:
        print("Error: No se pudo conectar a la base de datos.")
        return False
    
    cursor = connection.cursor()
    query = """
    UPDATE devoluciones_ventas
    SET id_pedido = %s,
        id_detalle = %s,
        fecha_devolucion = %s,
        motivo = %s,
        cantidad_devuelta = %s
    WHERE id_devolucion = %s
    """
    try:
        cursor.execute(query, (id_pedido, id_detalle, fecha_devolucion, motivo, cantidad_devuelta, id_devolucion))
        connection.commit()
        print("Devolución actualizada exitosamente.")
        return True
    except Error as e:
        print(f"Error al actualizar la devolución: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_devolucion(id_devolucion):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM devoluciones_ventas WHERE id_devolucion = %s"
    try:
        cursor.execute(query, (id_devolucion,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def get_devolucion_by_id(id_devolucion):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM devoluciones_ventas WHERE id_devolucion = %s"
    try:
        cursor.execute(query, (id_devolucion,))
        devolucion = cursor.fetchone()
        return devolucion
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return None
    finally:
        cursor.close()
        connection.close()
    
def get_producto_by_id(id_producto):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM producto WHERE id_producto = %s"
    try:
        cursor.execute(query, (id_producto,))
        producto = cursor.fetchone()
        return producto  # Asegúrate de que aquí estás retornando el producto completo
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

@app_devoluciones.route('/detalles/<int:id_pedido>')
def detalles(id_pedido):
    detalles = get_detalles_by_pedido(id_pedido)

    # Obtener los nombres de los productos
    productos_nombres = {}
    for detalle in detalles:
        id_producto = detalle[1]  # Suponiendo que el segundo elemento es el ID del producto
        producto = get_producto_by_id(id_producto)
        if producto:
            productos_nombres[id_producto] = producto[1]  # Suponiendo que el nombre del producto es el segundo elemento en la tupla

    return jsonify([{'id_detalle': detalle[0], 'nombre_producto': productos_nombres.get(detalle[1], 'Desconocido'), 'cantidad': detalle[2]} for detalle in detalles])

@app_devoluciones.route('/')
def index_devoluciones_ventas():
    pedidos = get_pedidos()  # Your logic to fetch pedidos
    page = request.args.get('page', 1, type=int)  # Get the page number
    return render_template('index_devoluciones_ventas.html', pedidos=pedidos, page=page)

@app_devoluciones.route('/submit', methods=['POST'])
def submit():
    id_pedido = request.form.get('id_pedido')
    id_detalle = request.form.get('id_detalle')
    fecha_devolucion = request.form.get('fecha_devolucion')  # Asegúrate de que este campo esté en el formulario
    motivo = request.form.get('motivo')
    cantidad_devuelta = request.form.get('cantidad_devuelta')

    if not id_pedido or not id_detalle or not fecha_devolucion or not motivo or not cantidad_devuelta:
        flash('¡Todos los campos obligatorios deben ser completados!')
        return redirect(url_for('index_devoluciones'))

    if insert_devolucion(id_pedido, id_detalle, fecha_devolucion, motivo, cantidad_devuelta):
        flash('Devolución agregada exitosamente!')
    else:
        flash('Error al agregar la devolución.')

    return redirect(url_for('devoluciones'))  # Redirigir a la lista de devoluciones


@app_devoluciones.route('/devoluciones')
def devoluciones_ventas():
    search_query = request.args.get('search_query', '')
    search_criteria = request.args.get('search_criteria', 'id_devolucion')  # Default value
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    devoluciones, total_count = get_devoluciones(page, per_page, search_query)

    total_pages = (total_count // per_page) + (1 if total_count % per_page > 0 else 0)

    return render_template(
        'devoluciones_ventas.html',
        devoluciones=devoluciones,
        page=page,
        total_pages=total_pages,
        search_query=search_query,
        search_criteria=search_criteria,  # Ensure this is also passed
        per_page=per_page  # Pass per_page to the template
    )


@app_devoluciones.route('/edit_devolucion_ventas/<int:id_devolucion>', methods=['GET', 'POST'])
def edit_devolucion_ventas(id_devolucion):
    if request.method == 'POST':
        id_pedido = request.form.get('id_pedido')
        id_detalle = request.form.get('id_detalle')
        fecha_devolucion = request.form.get('fecha_devolucion')
        motivo = request.form.get('motivo')
        cantidad_devuelta = request.form.get('cantidad_devuelta')

        # Validación de los campos obligatorios
        if not id_pedido or not id_detalle or not fecha_devolucion or not motivo or not cantidad_devuelta:
            flash('¡Todos los campos obligatorios deben ser completados!')
            # Redirige a la página de edición correcta
            return redirect(url_for('edit_devoluciones_ventas', id_devolucion=id_devolucion))

        # Actualización de la devolución
        if update_devolucion(id_devolucion, id_pedido, id_detalle, fecha_devolucion, motivo, cantidad_devuelta):
            flash('Devolución actualizada exitosamente!')
        else:
            flash('Error al actualizar la devolución.')

        # Redirige a la lista de devoluciones de ventas
        return redirect(url_for('devoluciones_ventas'))

    # Obtener la devolución y la lista de pedidos para el método GET
    devolucion = get_devolucion_by_id(id_devolucion)
    pedidos = get_pedidos()  # Obtener la lista de pedidos
    return render_template('edit_devoluciones_ventas.html', devolucion=devolucion, pedidos=pedidos)

@app_devoluciones.route('/eliminar_devolucion/<int:id_devolucion>', methods=['GET', 'POST'])
def eliminar_devolucion(id_devolucion):
    if request.method == 'POST':
        if delete_devolucion(id_devolucion):  # Assuming you have a delete_devolucion function
            flash('¡Devolución eliminada exitosamente!')
        else:
            flash('Ocurrió un error al eliminar la devolución.')
        return redirect(url_for('devoluciones'))  # Assuming 'devolucion' is the endpoint for your devolución list

    devolucion = get_devolucion_by_id(id_devolucion)  # Assuming you have a get_devolucion_by_id function
    if devolucion is None:
        flash('¡Devolución no encontrada!')
        return redirect(url_for('devoluciones'))

    return render_template('eliminar_devolucion_ventas.html', devolucion=devolucion)


if __name__ == '__main__':
    app_devoluciones.run(debug=True)
