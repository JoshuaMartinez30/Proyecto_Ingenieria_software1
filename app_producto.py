from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app_producto = Flask(__name__)
app_producto.secret_key = 'your_secret_key'  # Cambia 'your_secret_key' por una clave secreta segura

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

def insert_producto(nombre, id_categoria, id_proveedor, original_precio, id_impuesto, id_promocion, id_garantia):
    connection = create_connection()
    if connection is None:
        print("Error: No se pudo conectar a la base de datos.")
        return False
    cursor = connection.cursor()
    query = """INSERT INTO producto (nombre, id_categoria, id_proveedor, original_precio, id_impuesto, id_promocion, id_garantia) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    values = (nombre, id_categoria, id_proveedor, original_precio, id_impuesto, id_promocion, id_garantia)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Producto insertado exitosamente.")
        return True
    except Error as e:
        print(f"Error al insertar el producto: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


def get_producto(page, per_page, search_criteria=None, search_query=None):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    if search_criteria and search_query:
        query = f"""
            SELECT p.id_producto, p.nombre, p.id_categoria, p.id_proveedor, 
                   p.original_precio, p.id_impuesto, p.id_promocion, p.id_garantia, 
                   c.nombre_categoria AS nombre_categoria, pro.Nombre_del_proveedor, i.tasa_impuesto, prom.nombre, g.duracion
            FROM producto p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            JOIN proveedores pro ON p.id_proveedor = pro.id_proveedor
            JOIN impuesto i ON p.id_impuesto = i.id_impuesto
            JOIN promocion prom ON p.id_promocion = prom.id_promocion
            JOIN garantia g ON p.id_garantia = g.id_garantia
            WHERE {search_criteria} LIKE %s 
            LIMIT %s OFFSET %s
        """
        values = (f'%{search_query}%', per_page, offset)
    else:
        query = """
            SELECT p.id_producto, p.nombre, p.id_categoria, p.id_proveedor, 
                   p.original_precio, p.id_impuesto, p.id_promocion, p.id_garantia, 
                   c.nombre_categoria AS nombre_categoria, pro.Nombre_del_proveedor, i.tasa_impuesto, prom.nombre, g.duracion
            FROM producto p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            JOIN proveedores pro ON p.id_proveedor = pro.id_proveedor
            JOIN impuesto i ON p.id_impuesto = i.id_impuesto
            JOIN promocion prom ON p.id_promocion = prom.id_promocion
            JOIN garantia g ON p.id_garantia = g.id_garantia
            LIMIT %s OFFSET %s
        """
        values = (per_page, offset)

    try:
        cursor.execute(query, values)
        producto = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_count = cursor.fetchone()[0]
        return producto, total_count
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_categorias():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_categoria, nombre_categoria FROM categorias"
    try:
        cursor.execute(query)
        documento_empleado = cursor.fetchall()
        return documento_empleado
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
        documento_empleado = cursor.fetchall()
        return documento_empleado
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def get_impuesto():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_impuesto, tasa_impuesto FROM impuesto"
    try:
        cursor.execute(query)
        documento_empleado = cursor.fetchall()
        return documento_empleado
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()


def get_promocion():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_promocion, nombre FROM promocion"
    try:
        cursor.execute(query)
        documento_empleado = cursor.fetchall()
        return documento_empleado
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def get_garantia():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_garantia, duracion FROM garantia"
    try:
        cursor.execute(query)
        documento_empleado = cursor.fetchall()
        return documento_empleado
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def update_producto(id_producto, nombre, id_categoria, id_proveedor, original_precio, id_impuesto, id_promocion, id_garantia):
    connection = create_connection()
    if connection is None:
        print("Error: No se pudo conectar a la base de datos.")
        return False
    
    cursor = connection.cursor()
    query = """
    UPDATE producto
    SET nombre = %s,
        id_categoria = %s,
        id_proveedor = %s,
        original_precio = %s,
        id_impuesto = %s,
        id_promocion = %s,
        id_garantia = %s
    WHERE id_producto = %s
    """
    try:
        cursor.execute(query, (nombre, id_categoria, id_proveedor, original_precio, id_impuesto, id_promocion, id_garantia, id_producto))
        connection.commit()
        print("Producto actualizado exitosamente.")
        return True
    except Error as e:
        print(f"Error al actualizar el Producto: {e}")
        return False
    finally:
        cursor.close()
        connection.close()



def delete_producto(id_producto):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM producto WHERE id_producto = %s"
    try:
        cursor.execute(query, (id_producto,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
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
        return producto
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def get_historico_productos(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM historicos_productos LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        historico_productos = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_historico_productos = cursor.fetchone()[0]
        return historico_productos, total_historico_productos
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

@app_producto.route('/historico_productos')
def historico_productos():
    page = request.args.get('page', 1, type=int)
    per_page = int(request.args.get('per_page', 10))
    historicos, total_historicos = get_historico_productos(page, per_page)

    total_pages = (total_historicos + per_page - 1) // per_page
    return render_template('historico_productos.html', historicos=historicos, page=page, per_page=per_page, total_historicos=total_historicos, total_pages=total_pages)


@app_producto.route('/')
def index_producto():
    categorias = get_categorias()
    proveedores = get_proveedores()
    impuesto = get_impuesto()
    promocion = get_promocion()
    garantia = get_garantia()

    return render_template('index_producto.html', categorias=categorias, proveedores=proveedores, impuesto=impuesto, promocion=promocion, garantia=garantia)

@app_producto.route('/submit', methods=['POST'])
def submit():
    nombre = request.form.get('nombre')
    id_categoria = request.form.get('id_categoria')  
    id_proveedor = request.form.get('id_proveedor')
    original_precio = request.form.get('original_precio')
    id_impuesto = request.form.get('id_impuesto')
    id_promocion = request.form.get('id_promocion')
    id_garantia = request.form.get('id_garantia')
    
    # Imprimir los datos para depuración
    print(f"nombre: {nombre}")
    print(f"id_categoria: {id_categoria}")
    print(f"id_proveedor: {id_proveedor}")
    print(f"original_precio: {original_precio}")
    print(f"id_impuesto: {id_impuesto}")
    print(f"id_promocion: {id_promocion}")
    print(f"id_garantia: {id_garantia}")
    
    try:
        original_precio_decimal = float(original_precio)  # Asegurarse de que el salario sea un número decimal
    except ValueError:
        flash('El salario debe ser un número decimal válido.')
        return redirect(url_for('index_producto'))
    
    if insert_producto(nombre, id_categoria, id_proveedor, original_precio_decimal, id_impuesto, id_promocion, id_garantia):
        flash('Producto agregado exitosamente!')
    else:
        flash('Error al agregar el Producto.')

    return redirect(url_for('index_producto'))


@app_producto.route('/producto')
def producto():
    search_query = request.args.get('search_query', '')
    search_criteria = request.args.get('search_criteria', 'id_producto')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    producto, total_count = get_producto(page, per_page, search_criteria, search_query)

    producto_con_categorias = [
        (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12])  
        for item in producto
    ]

    total_pages = (total_count // per_page) + (1 if total_count % per_page > 0 else 0)

    return render_template(
        'producto.html',
        producto=producto_con_categorias,
        page=page,
        total_pages=total_pages,
        search_query=search_query,
        search_criteria=search_criteria,
        per_page=per_page
    )

@app_producto.route('/edit_producto/<int:id_producto>', methods=['GET', 'POST'])
def edit_producto(id_producto):
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        original_precio = request.form.get('original_precio')
        id_categoria = request.form.get('id_categoria')
        id_proveedor = request.form.get('id_proveedor')
        id_impuesto = request.form.get('id_impuesto')
        id_promocion = request.form.get('id_promocion')
        id_garantia = request.form.get('id_garantia')

        if not nombre or not original_precio:
            flash('¡Todos los campos obligatorios deben ser completados!')
            return redirect(url_for('edit_producto', id_producto=id_producto))

        if update_producto(id_producto, nombre, id_categoria, id_proveedor, original_precio, id_impuesto, id_promocion, id_garantia):
            flash('Producto editado exitosamente!')
        else:
            flash('Error al editar el Producto.')

        return redirect(url_for('producto'))
    else:
        producto = get_producto_by_id(id_producto)
        categorias = get_categorias() 
        proveedores = get_proveedores()
        impuesto = get_impuesto()
        promocion = get_promocion()
        garantia = get_garantia()

        if producto:
            return render_template(
                'edit_producto.html', 
                producto=producto,
                categorias=categorias,
                proveedores=proveedores,
                impuesto=impuesto,
                promocion=promocion,
                garantia=garantia
            )
        else:
            flash('El Producto no existe.')
            return redirect(url_for('producto'))


        


@app_producto.route('/eliminar_producto/<int:id_producto>', methods=['GET', 'POST'])
def eliminar_producto(id_producto):
    if request.method == 'POST':
        if delete_producto(id_producto):
            flash('¡Producto eliminado exitosamente!')
        else:
            flash('Ocurrió un error al eliminar el Producto.')
        return redirect(url_for('producto'))

    producto = get_producto_by_id(id_producto)
    if producto is None:
        flash('¡Producto no encontrado!')
        return redirect(url_for('producto'))
    
    return render_template('eliminar_producto.html', producto=producto)


if __name__ == '__main__':
    app_producto.run(debug=True,port=5017)
