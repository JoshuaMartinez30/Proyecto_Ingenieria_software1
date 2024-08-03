from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app_equipo = Flask(__name__)
app_equipo.secret_key = 'your_secret_key'

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

def insert_equipo(id_equipo, tipo, modelo, numero_serie, estado):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "INSERT INTO equipo (id_equipo, tipo, Modelo, numero_serie, estado) VALUES (%s, %s, %s, %s, %s)"
    values = (id_equipo, tipo, modelo, numero_serie, estado)
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

def get_equipos(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM equipo LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        equipos = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_equipos = cursor.fetchone()[0]
        return equipos, total_equipos
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_equipo_by_id(id_equipo):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM equipo WHERE id_equipo = %s"
    try:
        cursor.execute(query, (id_equipo,))
        equipo = cursor.fetchone()
        return equipo
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return None
    finally:
        cursor.close()
        connection.close()

def update_equipo(id_equipo, tipo, modelo, numero_serie, estado):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE equipo SET tipo = %s, Modelo = %s, numero_serie = %s, estado = %s WHERE id_equipo = %s"
    values = (tipo, modelo, numero_serie, estado, id_equipo)
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

def delete_equipo(id_equipo):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM equipo WHERE id_equipo = %s"
    try:
        cursor.execute(query, (id_equipo,))
        connection.commit()
        return True
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

@app_equipo.route('/')
def index_equipo():
    return render_template('index_equipo.html')

@app_equipo.route('/equipos')
def equipos():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    if search_query:
        equipos, total_equipos = search_equipos(search_query, page, per_page)
    else:
        equipos, total_equipos = get_equipos(page, per_page)

    total_pages = (total_equipos + per_page - 1) // per_page
    return render_template('equipos.html', equipos=equipos, search_query=search_query, page=page, per_page=per_page, total_equipos=total_equipos, total_pages=total_pages)

@app_equipo.route('/submit', methods=['POST'])
def submit():
    id_equipo = request.form['id_equipo']
    tipo = request.form['tipo']
    modelo = request.form['modelo']
    numero_serie = request.form['numero_serie']
    estado = request.form['estado']

    if not id_equipo or not tipo or not modelo or not numero_serie or not estado:
        flash('Todos los campos son requeridos!')
        return redirect(url_for('index_equipo'))

    if insert_equipo(id_equipo, tipo, modelo, numero_serie, estado):
        flash('Equipo insertado exitosamente!')
    else:
        flash('Ocurrió un error al insertar el equipo.')
    
    return redirect(url_for('index_equipo'))

@app_equipo.route('/edit_equipo/<int:id_equipo>', methods=['GET', 'POST'])
def edit_equipo(id_equipo):
    if request.method == 'POST':
        tipo = request.form['tipo']
        modelo = request.form['modelo']
        numero_serie = request.form['numero_serie']
        estado = request.form['estado']

        if not tipo or not modelo or not numero_serie or not estado:
            flash('Todos los campos son requeridos!')
            return redirect(url_for('edit_equipo', id_equipo=id_equipo))

        if update_equipo(id_equipo, tipo, modelo, numero_serie, estado):
            flash('Equipo actualizado exitosamente!')
        else:
            flash('Ocurrió un error al actualizar el equipo.')
        
        return redirect(url_for('equipos'))

    equipo = get_equipo_by_id(id_equipo)
    if equipo is None:
        flash('Equipo no encontrado!')
        return redirect(url_for('equipos'))
    return render_template('edit_equipo.html', equipo=equipo)

@app_equipo.route('/eliminar_equipo/<int:id_equipo>', methods=['GET', 'POST'])
def eliminar_equipo(id_equipo):
    if request.method == 'POST':
        if delete_equipo(id_equipo):
            flash('Equipo eliminado exitosamente!')
        else:
            flash('Ocurrió un error al eliminar el equipo.')
        return redirect(url_for('equipos'))

    equipo = get_equipo_by_id(id_equipo)
    if equipo is None:
        flash('Equipo no encontrado!')
        return redirect(url_for('equipos'))
    return render_template('eliminar_equipo.html', equipo=equipo)

def search_equipos(search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    
    query = """
    SELECT SQL_CALC_FOUND_ROWS * 
    FROM equipo 
    WHERE id_equipo LIKE %s 
       OR tipo LIKE %s 
       OR Modelo LIKE %s 
       OR numero_serie LIKE %s 
       OR estado LIKE %s
    LIMIT %s OFFSET %s
    """
    values = (
        f'%{search_query}%', 
        f'%{search_query}%', 
        f'%{search_query}%', 
        f'%{search_query}%', 
        f'%{search_query}%', 
        per_page, 
        offset
    )
    try:
        cursor.execute(query, values)
        equipos = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_equipos = cursor.fetchone()[0]
        return equipos, total_equipos
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return [], 0
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app_equipo.run(debug=True,port=5020)
