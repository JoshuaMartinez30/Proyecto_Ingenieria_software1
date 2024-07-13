from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

app_encuestas = Flask(__name__)
app_encuestas.secret_key = 'your_secret_key'

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

def insert_encuesta(cliente, Fecha, puntuacion, comentarios):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    query = "INSERT INTO encuestas (cliente, Fecha, puntuacion, comentarios) VALUES (%s, %s, %s, %s)"
    values = (cliente, Fecha, puntuacion, comentarios)
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

def get_encuestas():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM encuestas"
    try:
        cursor.execute(query)
        encuestas = cursor.fetchall()
        return encuestas
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def get_encuesta_by_id(id_encuesta):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM encuestas WHERE id_encuesta = %s"
    try:
        cursor.execute(query, (id_encuesta,))
        encuesta = cursor.fetchone()
        return encuesta
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_encuesta(id_encuesta, cliente, Fecha, puntuacion, comentarios):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    UPDATE encuestas
    SET cliente = %s, Fecha = %s, puntuacion = %s, comentarios = %s
    WHERE id_encuesta = %s
    """
    values = (cliente, Fecha, puntuacion, comentarios, id_encuesta)
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

def delete_encuesta(id_encuesta):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM encuestas WHERE id_encuesta = %s"
    try:
        cursor.execute(query, (id_encuesta,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def search_encuestas(search_query):
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM encuestas WHERE cliente LIKE %s"
    values = (f'%{search_query}%',)
    try:
        cursor.execute(query, values)
        encuestas = cursor.fetchall()
        return encuestas
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def validar_encuesta(cliente, Fecha, puntuacion, comentarios):
    errores = []

    # Validar campos en blanco
    if not cliente or not Fecha or not puntuacion or not comentarios:
        errores.append("Todos los campos son requeridos.")
    
    # Validar longitud de caracteres
    if len(cliente) < 3 or len(cliente) > 15:
        errores.append("El nombre del cliente debe tener entre 3 y 15 caracteres.")
    if len(comentarios) < 3 or len(comentarios) > 15:
        errores.append("Los comentarios deben tener entre 3 y 15 caracteres.")
    
    # Validar que no haya tres letras repetidas
    if re.search(r'(.)\1{2,}', cliente):
        errores.append("El nombre del cliente no debe tener tres letras repetidas consecutivamente.")
    if re.search(r'(.)\1{2,}', comentarios):
        errores.append("Los comentarios no deben tener tres letras repetidas consecutivamente.")
    
    # Validar que no haya signos
    if re.search(r'[^a-zA-Z0-9\s]', cliente):
        errores.append("El nombre del cliente no debe contener signos.")
    if re.search(r'[^a-zA-Z0-9\s]', comentarios):
        errores.append("Los comentarios no deben contener signos.")
    
    # Validar que no haya números en campos de texto y viceversa
    if re.search(r'\d', cliente):
        errores.append("El nombre del cliente no debe contener números.")
    
    # Validar fecha
    try:
        anio = int(Fecha.split("-")[0])
        if anio < 2015:
            errores.append("El año de la fecha no puede ser anterior a 2015.")
    except ValueError:
        errores.append("Formato de fecha inválido.")
    
    # Validar puntuacion
    if not puntuacion.isdigit() or int(puntuacion) < 1 or int(puntuacion) > 10:
        errores.append("La puntuación debe ser un número entre 1 y 10.")

    return errores

@app_encuestas.route('/')
def index_encuestas():
    return render_template('index_encuestas.html')

@app_encuestas.route('/encuestas')
def encuestas():
    search_query = request.args.get('search')
    if search_query:
        encuestas = search_encuestas(search_query)
    else:
        encuestas = get_encuestas()
    return render_template('encuestas.html', encuestas=encuestas, search_query=search_query)

@app_encuestas.route('/submit', methods=['POST'])
def submit():
    cliente = request.form['cliente']
    Fecha = request.form['fecha']
    puntuacion = request.form['puntuacion']
    comentarios = request.form['comentarios']

    errores = validar_encuesta(cliente, Fecha, puntuacion, comentarios)
    if errores:
        for error in errores:
            flash(error)
        return redirect(url_for('index_encuestas'))

    if insert_encuesta(cliente, Fecha, puntuacion, comentarios):
        flash('Encuesta insertada exitosamente!')
    else:
        flash('Ocurrió un error al insertar la encuesta.')
    
    return redirect(url_for('index_encuestas'))

@app_encuestas.route('/edit/<int:id_encuesta>', methods=['GET', 'POST'])
def edit_encuestas(id_encuesta):
    if request.method == 'POST':
        cliente = request.form['cliente']
        Fecha = request.form['Fecha']
        puntuacion = request.form['puntuacion']
        comentarios = request.form['comentarios']

        errores = validar_encuesta(cliente, Fecha, puntuacion, comentarios)
        if errores:
            for error in errores:
                flash(error)
            return redirect(url_for('edit_encuestas', id_encuesta=id_encuesta))

        if update_encuesta(id_encuesta, cliente, Fecha, puntuacion, comentarios):
            flash('Encuesta actualizada exitosamente!')
        else:
            flash('Ocurrió un error al actualizar la encuesta.')
        
        return redirect(url_for('encuestas'))

    encuesta = get_encuesta_by_id(id_encuesta)
    if encuesta is None:
        flash('Encuesta no encontrada!')
        return redirect(url_for('encuestas'))
    return render_template('edit_encuestas.html', encuesta=encuesta)

@app_encuestas.route('/eliminar/<int:id_encuesta>', methods=['GET', 'POST'])
def eliminar_encuestas(id_encuesta):
    if request.method == 'POST':
        if delete_encuesta(id_encuesta):
            flash('Encuesta eliminada exitosamente!')
        else:
            flash('Ocurrió un error al eliminar la encuesta.')
        return redirect(url_for('encuestas'))

    encuesta = get_encuesta_by_id(id_encuesta)
    if encuesta is None:
        flash('Encuesta no encontrada!')
        return redirect(url_for('encuestas'))
    return render_template('eliminar_encuestas.html', encuesta=encuesta)

if __name__ == '__main__':
    app_encuestas.run(debug=True, port=5010)
