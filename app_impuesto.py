from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re


app_impuesto = Flask(__name__)
app_impuesto.secret_key = 'your_secret_key'

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

def insert_user(tipo_impuesto, tasa_impuesto):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "INSERT INTO impuesto (tipo_impuesto, tasa_impuesto) VALUES (%s, %s)"
    values = (tipo_impuesto, tasa_impuesto)
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

def update_user(id_impuesto, tipo_impuesto, tasa_impuesto):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE impuesto SET tipo_impuesto = %s, tasa_impuesto = %s WHERE id_impuesto = %s"
    values = (tipo_impuesto, tasa_impuesto, id_impuesto)
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

def delete_user(id_impuesto):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM impuesto WHERE id_impuesto = %s"
    try:
        cursor.execute(query, (id_impuesto,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def get_impuesto(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS id_impuesto, tipo_impuesto, tasa_impuesto FROM impuesto LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        impuesto = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_impuesto = cursor.fetchone()[0]
        return impuesto, total_impuesto
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def search_impuesto(search_criteria, search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = f"SELECT SQL_CALC_FOUND_ROWS * FROM impuesto WHERE {search_criteria} LIKE %s LIMIT %s OFFSET %s"
    values = (f'%{search_query}%', per_page, offset)
    try:
        cursor.execute(query, values)
        impuesto = cursor.fetchall()
        cursor.execute(f"SELECT FOUND_ROWS()")
        total_count = cursor.fetchone()[0]
        return impuesto, total_count
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_impuesto_by_id(id_impuesto):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT id_impuesto, tipo_impuesto, tasa_impuesto FROM impuesto WHERE id_impuesto = %s"
    cursor.execute(query, (id_impuesto,))
    impuesto = cursor.fetchone()
    cursor.close()
    connection.close()
    return impuesto

def get_historico_impuestos(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM historicos_impuestos LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        historico_impuestos = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_historico_impuestos = cursor.fetchone()[0]
        return historico_impuestos, total_historico_impuestos
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

@app_impuesto.route('/historico_impuestos')
def historico_impuestos():
    page = request.args.get('page', 1, type=int)
    per_page = int(request.args.get('per_page', 10))
    historicos, total_historicos = get_historico_impuestos(page, per_page)

    total_pages = (total_historicos + per_page - 1) // per_page
    return render_template('historico_impuestos.html', historicos=historicos, page=page, per_page=per_page, total_historicos=total_historicos, total_pages=total_pages)


@app_impuesto.route('/')
def index_impuesto():
    return render_template('index_impuesto.html')

@app_impuesto.route('/impuesto')
def impuesto():
    search_criteria = request.args.get('search_criteria')
    search_query = request.args.get('search_query', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))

    if search_query:
        impuesto, total_count = search_impuesto(search_criteria, search_query, page, per_page)
    else:
        impuesto, total_count = get_impuesto(page, per_page)
    
    total_pages = (total_count + per_page - 1) // per_page

    return render_template('impuesto.html', impuesto=impuesto, search_criteria=search_criteria, search_query=search_query, page=page, total_pages=total_pages, per_page=per_page)


@app_impuesto.route('/submit', methods=['POST'])
def submit():
    tipo_impuesto = request.form['tipo_impuesto']
    tasa_impuesto = request.form['tasa_impuesto']
    
    # Verificar si el impuesto seleccionó "Otro" y llenó el campo de texto adicional
    if tipo_impuesto == "Otro":
        tipo_impuesto = request.form['otro_tipo_impuesto']
    
    if tasa_impuesto == "Otro":
        tasa_impuesto = request.form['otro_tasa_impuesto']

    # Insertar en la base de datos
    if insert_user(tipo_impuesto, tasa_impuesto):
        flash('Impuesto ingresado exitosamente.')
    else:
        flash('Ocurrió un error al ingresar el impuesto.')
    
    return redirect(url_for('index_impuesto'))


@app_impuesto.route('/edit_impuesto/<int:id_impuesto>', methods=['GET', 'POST'])
def edit_impuesto(id_impuesto):
    if request.method == 'POST':
        tipo_impuesto = request.form['tipo_impuesto']
        tasa_impuesto = request.form['tasa_impuesto']


        if update_user(id_impuesto, tipo_impuesto, tasa_impuesto):
            flash('impuesto actualizado exitosamente.')
        else:
            flash('Ocurrió un error al actualizar el impuesto.')
        
        return redirect(url_for('impuesto'))

    impuesto = get_impuesto_by_id(id_impuesto)
    if impuesto is None:
        flash('impuesto no encontrado.')
        return redirect(url_for('impuesto'))
    return render_template('edit_impuesto.html', impuesto=impuesto)


@app_impuesto.route('/eliminar_impuesto/<int:id_impuesto>', methods=['GET', 'POST'])
def eliminar_impuesto(id_impuesto):
    if request.method == 'POST':
        if delete_user(id_impuesto):
            flash('¡impuesto eliminada exitosamente!')
            return redirect(url_for('impuesto'))
        else:
            flash('Ocurrió un error al eliminar el impuesto. Por favor, intente nuevamente.')
            return redirect(url_for('impuesto'))

    impuesto = get_impuesto_by_id(id_impuesto)
    if impuesto is None:
        flash('impuesto no encontrada.')
        return redirect(url_for('impuesto'))

    return render_template('eliminar_impuesto.html', impuesto=impuesto)

if __name__ == '__main__':
    app_impuesto.run(debug=True,port=5024)
