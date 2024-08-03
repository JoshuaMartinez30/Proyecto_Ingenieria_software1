from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app_almacenes = Flask(__name__)
app_almacenes.secret_key = 'your_secret_key'

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

def insert_almacen(nombre, direccion):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "INSERT INTO almacenes (nombre, direccion) VALUES (%s, %s)"
    values = (nombre, direccion)
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

def get_almacenes(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM almacenes LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        almacenes = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_almacenes = cursor.fetchone()[0]
        return almacenes, total_almacenes
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_almacen_by_id(id_almacen):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM almacenes WHERE id_almacenes = %s"
    try:
        cursor.execute(query, (id_almacen,))
        almacen = cursor.fetchone()
        return almacen
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return None
    finally:
        cursor.close()
        connection.close()

def update_almacen(id_almacen, nombre, direccion):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE almacenes SET nombre = %s, direccion = %s WHERE id_almacenes = %s"
    values = (nombre, direccion, id_almacen)
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

def delete_almacen(id_almacen):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM almacenes WHERE id_almacenes = %s"
    try:
        cursor.execute(query, (id_almacen,))
        connection.commit()
        return True
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

def get_historico_almacenes(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM historicos_almacenes LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        historico_almacenes = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_historico_almacenes = cursor.fetchone()[0]
        return historico_almacenes, total_historico_almacenes
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

@app_almacenes.route('/historico_almacenes')
def historico_almacenes():
    page = request.args.get('page', 1, type=int)
    per_page = int(request.args.get('per_page', 10))
    historicos, total_historicos = get_historico_almacenes(page, per_page)

    total_pages = (total_historicos + per_page - 1) // per_page
    return render_template('historico_almacenes.html', historicos=historicos, page=page, per_page=per_page, total_historicos=total_historicos, total_pages=total_pages)


@app_almacenes.route('/')
def index_almacenes():
    return render_template('index_almacenes.html')

@app_almacenes.route('/almacenes')
def almacenes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    almacenes, total_almacenes = get_almacenes(page, per_page)
    total_pages = (total_almacenes + per_page - 1) // per_page
    return render_template('almacenes.html', almacenes=almacenes, page=page, per_page=per_page, total_almacenes=total_almacenes, total_pages=total_pages)

@app_almacenes.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['nombre']
    direccion = request.form['direccion']

    if not nombre or not direccion:
        flash('Todos los campos son requeridos!')
        return redirect(url_for('index_almacenes'))

    if insert_almacen(nombre, direccion):
        flash('Almacén insertado exitosamente!')
    else:
        flash('Ocurrió un error al insertar el almacén.')
    
    return redirect(url_for('index_almacenes'))

@app_almacenes.route('/edit_almacen/<int:id_almacen>', methods=['GET', 'POST'])
def edit_almacen(id_almacen):
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']

        if not nombre or not direccion:
            flash('Todos los campos son requeridos!')
            return redirect(url_for('edit_almacen', id_almacen=id_almacen))

        if update_almacen(id_almacen, nombre, direccion):
            flash('Almacén actualizado exitosamente!')
        else:
            flash('Ocurrió un error al actualizar el almacén.')
        
        return redirect(url_for('almacenes'))

    almacen = get_almacen_by_id(id_almacen)
    if almacen is None:
        flash('Almacén no encontrado!')
        return redirect(url_for('almacenes'))
    return render_template('edit_almacen.html', almacen=almacen)

@app_almacenes.route('/eliminar_almacen/<int:id_almacen>', methods=['GET', 'POST'])
def eliminar_almacen(id_almacen):
    if request.method == 'POST':
        if delete_almacen(id_almacen):
            flash('Almacén eliminado exitosamente!')
        else:
            flash('Ocurrió un error al eliminar el almacén.')
        return redirect(url_for('almacenes'))

    almacen = get_almacen_by_id(id_almacen)
    if almacen is None:
        flash('Almacén no encontrado!')
        return redirect(url_for('almacenes'))
    return render_template('eliminar_almacen.html', almacen=almacen)

if __name__ == "__main__":
    app_almacenes.run(debug=True, port=5018)
