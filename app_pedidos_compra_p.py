import re
from flask import Flask, render_template, request, redirect, session, url_for, flash
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
            password="qEeKLgpIkdarsoNT",
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

def get_detalles_by_pedido_id(id_pedido):
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query ="""
    SELECT d.id_detalle, d.id_pedido, p.nombre AS nombre_producto, d.cantidad, d.precio_unitario, i.tasa_impuesto, d.subtotal, d.total
    FROM detalle_de_compra_proveedor d
    JOIN producto p ON d.id_producto = p.id_producto
    JOIN impuesto i ON d.id_impuesto = i.id_impuesto  -- Agrega este JOIN para obtener la tasa_impuesto
    WHERE d.id_pedido = %s
    """
    try:
        cursor.execute(query, (id_pedido,))
        detalles = cursor.fetchall()
        return detalles
    except Error as e:
        print(f"Error '{e}' ocurrió")
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
    query = "SELECT id_proveedor, nombre_compañia FROM proveedores"
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

def insert_user(id_proveedor, numero_factura, id_empleado, fecha_pedido, fecha_entrega_estimada, fecha_entrega, id_metodo, id_estado):
    connection = create_connection()
    if connection is None:
        print("Error: No connection to database.")
        return False
    cursor = connection.cursor()
    query = """
        INSERT INTO pedido_de_compra_proveedor 
        (id_proveedor, numero_factura, id_empleado, fecha_pedido, fecha_entrega_estimada, fecha_entrega, id_metodo, id_estado) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (id_proveedor, numero_factura if numero_factura else None, id_empleado, fecha_pedido, 
              fecha_entrega_estimada if fecha_entrega_estimada else None, fecha_entrega if fecha_entrega else None, 
              id_metodo, id_estado)
    try:
        print("Executing query:", query)
        print("With values:", values)
        cursor.execute(query, values)
        connection.commit()
        print("Insert successful.")
        return True
    except Error as e:
        print(f"Error occurred: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


def get_id_empleado():
    connection = create_connection()
    if connection is None:
        print("Error: No se pudo establecer la conexión con la base de datos.")
        return None  # En caso de fallo en la conexión, retorna None
    cursor = connection.cursor(dictionary=True)  # Usamos dictionary=True para obtener los resultados como un diccionario
    query = "SELECT * FROM empleados WHERE email = %s"

    try:
        # Obtenemos el correo del usuario logueado desde la sesión
        correo_usuario = session.get('correo')
        if not correo_usuario:
            print("Error: No hay un usuario logueado.")
            return None  # Si no hay un usuario logueado, retorna None
        
        # Ejecutamos la consulta
        cursor.execute(query, (correo_usuario,))
        empleados = cursor.fetchone()  # Obtenemos el empleado que coincide con el correo

        if empleados:
            # Guardamos el id_empleado y otros valores relevantes en la sesión
            session['id_empleado'] = empleados.get('id_empleado')
            session['nombre_empleado'] = empleados.get('nombre')
            session['apellido_empleado'] = empleados.get('apellido')
            session['id_sucursal'] = empleados.get('id_sucursal')
            
            # Depuración: Imprimir los valores almacenados
            print("Empleado encontrado y guardado en la sesión:")
            print(f"id_empleado: {session.get('id_empleado')}")
            print(f"nombre_empleado: {session.get('nombre_empleado')}")
            print(f"apellido_empleado: {session.get('apellido_empleado')}")
            print(f"id_sucursal: {session.get('id_sucursal')}")

            return empleados  # Retorna el empleado encontrado
        else:
            print("No se encontró ningún empleado con ese correo.")
            return None  # Si no se encontró ningún empleado, retorna None
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def get_pedidos_compra_p(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    # Obtener el total de registros
    count_query = """
        SELECT COUNT(*) FROM pedido_de_compra_proveedor
        JOIN proveedores pr ON pedido_de_compra_proveedor.id_proveedor = pr.id_proveedor
        JOIN metodo_de_pago mp ON pedido_de_compra_proveedor.id_metodo = mp.id_metodo
        JOIN estado e ON pedido_de_compra_proveedor.id_estado = e.id_estado
    """
    try:
        cursor.execute(count_query)
        total_pedidos_compra_p = cursor.fetchone()[0]

        # Obtener los registros para la página actual
        query = """
            SELECT p.id_pedido, pr.nombre_compañia, p.numero_factura, p.fecha_pedido, p.fecha_entrega_estimada, p.fecha_entrega, mp.nombre, e.nombre_estado, p.id_empleado
            FROM pedido_de_compra_proveedor p
            JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
            JOIN metodo_de_pago mp ON p.id_metodo = mp.id_metodo
            JOIN estado e ON p.id_estado = e.id_estado
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (per_page, offset))
        pedidos_compra_p = cursor.fetchall()
        
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
         SELECT p.id_pedido, p.id_proveedor, p.numero_factura, p.fecha_pedido, p.fecha_entrega_estimada, p.fecha_entrega, p.id_metodo, p.id_estado
        FROM pedido_de_compra_proveedor p
        JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
        WHERE id_pedido = %s
    """
    try:
        cursor.execute(query, (id_pedido,))
        pedido = cursor.fetchone()
        return pedido
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()


def update_user(id_pedido, numero_factura ,id_proveedor, fecha_pedido, fecha_entrega_estimada, fecha_entrega, id_metodo, id_estado):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
        UPDATE pedido_de_compra_proveedor 
        SET id_proveedor = %s, numero_factura = %s,fecha_pedido = %s, fecha_entrega_estimada = %s, fecha_entrega = %s, id_metodo = %s, id_estado = %s 
        WHERE id_pedido = %s
    """
    values = (id_proveedor,numero_factura ,fecha_pedido, fecha_entrega_estimada if fecha_entrega_estimada else None, 
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
        SELECT p.id_pedido, pr.nombre_compañia,p.numero_factura, p.fecha_pedido, p.fecha_entrega, mp.nombre, e.nombre_estado,p.id_empleado
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

def search_pedidos_compra_p(search_criteria, search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    
    query = f"""
        SELECT SQL_CALC_FOUND_ROWS p.id_pedido, pr.nombre_compañia, p.numero_factura, p.fecha_pedido, 
               p.fecha_entrega_estimada, p.fecha_entrega, mp.nombre, e.nombre_estado,p.id_empleado
        FROM pedido_de_compra_proveedor p
        JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
        JOIN metodo_de_pago mp ON p.id_metodo = mp.id_metodo
        JOIN estado e ON p.id_estado = e.id_estado
        WHERE {search_criteria} LIKE %s
        LIMIT %s OFFSET %s
    """
    
    values = (f'%{search_query}%', per_page, offset)
    
    try:
        cursor.execute(query, values)
        pedidos_compra_p = cursor.fetchall()
        
        cursor.execute("SELECT FOUND_ROWS()")
        total_count = cursor.fetchone()[0]
        
        return pedidos_compra_p, total_count
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

def get_usuarios(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS id_pedido, id_proveedor, numero_factura, fecha_pedido, fecha_entrega_estimada, fecha_entrega, id_metodo, id_estado FROM pedido_de_compra_proveedor LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        usuarios = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_usuarios = cursor.fetchone()[0]
        return usuarios, total_usuarios
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

#Paso 2 para que sean seleccionables
@app_pedidos_compra_p.route('/')
def index_pedidos_compra_p():
    estados = get_estados()
    metodos = get_metodos()
    proveedores= get_proveedores()
    empleados = get_id_empleado()

    return render_template('index_pedidos_compra_p.html', estados=estados, metodos=metodos, proveedores=proveedores, empleados= empleados)

@app_pedidos_compra_p.route('/pedidos_compra_pv')
def pedidos_compra_pv():
    search_criteria = request.args.get('search_criteria', 'id_pedido')
    search_query = request.args.get('search_query', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))

    if search_query:
        pedidos_compra_p, total_count = search_pedidos_compra_p(search_criteria, search_query, page, per_page)
    else:
        pedidos_compra_p, total_count = get_pedidos_compra_p(page, per_page)

    total_pages = (total_count + per_page - 1) // per_page

    return render_template('pedidos_compra_pv.html', pedidos_compra_p=pedidos_compra_p, search_criteria=search_criteria, search_query=search_query, page=page, total_pages=total_pages, per_page=per_page)

@app_pedidos_compra_p.route('/submit', methods=['POST'])
def submit():
    id_proveedor = request.form['id_proveedor']
    numero_factura=request.form['numero_factura']
    id_empleado = session.get('id_empleado')
    fecha_pedido = request.form['fecha_pedido']
    fecha_entrega_estimada = request.form['fecha_entrega_estimada']
    fecha_entrega = request.form['fecha_entrega'] or None  # Set to None if empty
    id_metodo = request.form['id_metodo']
    id_estado = request.form['id_estado']
    
    if not id_proveedor or not fecha_pedido or not id_metodo or not id_estado:
        flash('All fields are required except Fecha Entrega and Fecha Entrega Estimada!')
        return redirect(url_for('index_pedidos_compra_p'))
       
    if insert_user(id_proveedor,numero_factura,id_empleado ,fecha_pedido, fecha_entrega_estimada, fecha_entrega, id_metodo, id_estado):
        flash('Pedido inserted successfully!')
    else:
        flash('An error occurred while inserting the pedido.')
    
    return redirect(url_for('index_pedidos_compra_p'))

    

@app_pedidos_compra_p.route('/edit_pedidos_compra_p/<int:id_pedido>', methods=['GET', 'POST'])
def edit_pedidos_compra_p(id_pedido):
    if request.method == 'POST':
        id_proveedor = request.form['id_proveedor']
        numero_factura = request.form.get('numero_factura', '').strip()
        fecha_pedido = request.form['fecha_pedido']
        fecha_entrega_estimada = request.form['fecha_entrega_estimada']
        fecha_entrega = request.form['fecha_entrega'] or None
        id_metodo = request.form['id_metodo']
        id_estado = request.form['id_estado']

        # Validar campos obligatorios
        if not id_proveedor or not numero_factura or not fecha_pedido or not id_metodo or not id_estado:
            flash('Todos los campos son obligatorios excepto "Fecha Entrega".')
            return redirect(url_for('edit_pedidos_compra_p', id_pedido=id_pedido))

        # Validar el campo numero_factura
        if not numero_factura:
            flash('El número de factura es obligatorio.')
            return redirect(url_for('edit_pedidos_compra_p', id_pedido=id_pedido))

        # Llamar a la función de actualización, pasar los parámetros correctos
        if update_user(id_pedido, numero_factura, id_proveedor, fecha_pedido, fecha_entrega_estimada, fecha_entrega, id_metodo, id_estado):
            flash('Pedido actualizado exitosamente', 'success')
            return redirect(url_for('pedidos_compra_pv'))
        else:
            flash('Ocurrió un error al actualizar el pedido.')
            return redirect(url_for('edit_pedidos_compra_p', id_pedido=id_pedido))

    # Para el método GET, cargar los detalles del pedido y mostrar el formulario
    pedido = get_pedidos_compra_p_by_id(id_pedido)
    if pedido is None:
        flash('Pedido no encontrado.')
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

@app_pedidos_compra_p.route('/ver_pedido_p/<int:id_pedido>')
def ver_pedido(id_pedido):
    pedido = get_pedidos_compra_p_by_id(id_pedido)
    if pedido is None:
        flash('Pedido no encontrado!')
        return redirect(url_for('pedidos'))

    detalles = get_detalles_by_pedido_id(id_pedido)
    return render_template('ver_pedido_p.html', pedido=pedido, detalles=detalles)


    
if __name__ == '__main__':

    app_pedidos_compra_p.run(debug=True, port=5015)
