from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re
from datetime import datetime

app_puesto_de_trabajo = Flask(__name__)
app_puesto_de_trabajo.secret_key = 'your_secret_key'  # Cambia 'your_secret_key' por una clave secreta segura

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


def validate_salary(salario):
    try:
        float(salario)  # Verifica que el salario sea un número decimal
        return None
    except ValueError:
        return "El salario debe ser un número decimal válido."

def validate_time(hora):
    try:
        datetime.strptime(hora, '%H:%M')  # Asegúrate de que la hora tenga el formato correcto
        return None
    except ValueError:
        return "La hora debe estar en el formato HH:MM."

def insert_puesto_de_trabajo(puesto_trabajo, hora_inicio, hora_fin, salario):
    connection = create_connection()
    if connection is None:
        print("Error: No se pudo conectar a la base de datos.")
        return False
    cursor = connection.cursor()
    query = """INSERT INTO puesto_de_trabajo (puesto_trabajo, hora_inicio, hora_fin, salario) 
               VALUES (%s, %s, %s, %s)"""
    values = (puesto_trabajo, hora_inicio, hora_fin, salario)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Puesto de trabajo insertado exitosamente.")
        return True
    except Error as e:
        print(f"Error al insertar el puesto de trabajo: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def get_puesto_de_trabajo(page, per_page, search_criteria=None, search_query=None):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    if search_criteria and search_query:
        query = f"""
            SELECT id_puesto, puesto_trabajo, hora_inicio, hora_fin, salario
            FROM puesto_de_trabajo
            WHERE {search_criteria} LIKE %s 
            LIMIT %s OFFSET %s
        """
        values = (f'%{search_query}%', per_page, offset)
    else:
        query = """
            SELECT id_puesto, puesto_trabajo, hora_inicio, hora_fin, salario
            FROM puesto_de_trabajo
            LIMIT %s OFFSET %s
        """
        values = (per_page, offset)

    try:
        cursor.execute(query, values)
        puesto_de_trabajo = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_count = cursor.fetchone()[0]
        return puesto_de_trabajo, total_count
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def update_puesto_de_trabajo(id_puesto, fecha, hora_inicio, hora_fin, puesto_trabajo, salario):
    connection = create_connection()
    if connection is None:
        print("Error: No se pudo conectar a la base de datos.")
        return False
    
    cursor = connection.cursor()
    query = """
    UPDATE puesto_de_trabajo
    SET hora_inicio = %s,
        hora_fin = %s,
        puesto_trabajo = %s,
        salario = %s
    WHERE id_puesto = %s
    """
    try:
        cursor.execute(query, (hora_inicio, hora_fin, puesto_trabajo, salario, id_puesto))
        connection.commit()
        print("Puesto de trabajo actualizado exitosamente.")
        return True
    except Error as e:
        print(f"Error al actualizar el puesto de trabajo: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_puesto_de_trabajo(id_puesto):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM puesto_de_trabajo WHERE id_puesto = %s"
    try:
        cursor.execute(query, (id_puesto,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def get_puesto_de_trabajo_by_id(id_puesto):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM puesto_de_trabajo WHERE id_puesto = %s"
    try:
        cursor.execute(query, (id_puesto,))
        puesto_de_trabajo = cursor.fetchone()
        return puesto_de_trabajo
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

@app_puesto_de_trabajo.route('/')
def index_puesto_de_trabajo():
    return render_template('index_puesto_de_trabajo.html')

@app_puesto_de_trabajo.route('/submit', methods=['POST'])
def submit():
    puesto_trabajo = request.form.get('puesto_trabajo')
    hora_inicio = request.form.get('hora_inicio')
    hora_fin = request.form.get('hora_fin')
    salario = request.form.get('salario')

    # Validaciones
    validation_errors = []
    
    hora_inicio_error = validate_time(hora_inicio)
    if hora_inicio_error:
        validation_errors.append(hora_inicio_error)

    hora_fin_error = validate_time(hora_fin)
    if hora_fin_error:
        validation_errors.append(hora_fin_error)


    salario_error = validate_salary(salario)
    if salario_error:
        validation_errors.append(salario_error)

    if validation_errors:
        for error in validation_errors:
            flash(error)
        return redirect(url_for('index_puesto_de_trabajo'))

    try:
        salario_decimal = float(salario)  # Asegúrate de que el salario sea un número decimal
    except ValueError:
        flash('El salario debe ser un número decimal válido.')
        return redirect(url_for('index_puesto_de_trabajo'))
    
    if insert_puesto_de_trabajo(puesto_trabajo, hora_inicio, hora_fin, salario_decimal):
        flash('Puesto de trabajo agregado exitosamente!')
    else:
        flash('Error al agregar el puesto de trabajo.')

    return redirect(url_for('index_puesto_de_trabajo'))

@app_puesto_de_trabajo.route('/puesto_de_trabajo', methods=['GET'])
def puesto_de_trabajo():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Número de registros por página
    search_criteria = request.args.get('search_criteria')
    search_query = request.args.get('search_query')
    
    puesto_de_trabajo, total_count = get_puesto_de_trabajo(page, per_page, search_criteria, search_query)
    
    # Calcular el total de páginas
    total_pages = (total_count + per_page - 1) // per_page
    
    return render_template(
        'puesto_de_trabajo.html',
        puesto_de_trabajo=puesto_de_trabajo,
        total_pages=total_pages,
        current_page=page
    )

@app_puesto_de_trabajo.route('/edit/<int:id_puesto>', methods=['GET', 'POST'])
def edit_puesto_de_trabajo(id_puesto):
    if request.method == 'POST':
        hora_inicio = request.form.get('hora_inicio')
        hora_fin = request.form.get('hora_fin')
        puesto_trabajo = request.form.get('puesto_trabajo')
        salario = request.form.get('salario')

        validation_errors = []
        
        hora_inicio_error = validate_time(hora_inicio)
        if hora_inicio_error:
            validation_errors.append(hora_inicio_error)

        hora_fin_error = validate_time(hora_fin)
        if hora_fin_error:
            validation_errors.append(hora_fin_error)

        salario_error = validate_salary(salario)
        if salario_error:
            validation_errors.append(salario_error)

        if validation_errors:
            for error in validation_errors:
                flash(error)
            return redirect(url_for('edit_puesto_de_trabajo', id_puesto=id_puesto))

        try:
            salario_decimal = float(salario)  # Asegúrate de que el salario sea un número decimal
        except ValueError:
            flash('El salario debe ser un número decimal válido.')
            return redirect(url_for('edit_puesto_de_trabajo', id_puesto=id_puesto))
        
        if update_puesto_de_trabajo(id_puesto, hora_inicio, hora_fin, puesto_trabajo, salario_decimal):
            flash('Puesto de trabajo actualizado exitosamente!')
        else:
            flash('Error al actualizar el puesto de trabajo.')
        
        return redirect(url_for('puesto_de_trabajo'))

    puesto_de_trabajo = get_puesto_de_trabajo_by_id(id_puesto)
    if puesto_de_trabajo is None:
        flash('Puesto de trabajo no encontrado.')
        return redirect(url_for('puesto_de_trabajo'))

    return render_template('edit_puesto_de_trabajo.html', puesto_de_trabajo=puesto_de_trabajo)

@app_puesto_de_trabajo.route('/delete/<int:id_puesto>', methods=['GET', 'POST'])
def delete_puesto_de_trabajo_route(id_puesto):
    # Verificar si el método es POST
    if request.method == 'POST':
        if delete_puesto_de_trabajo(id_puesto):
            flash('Puesto de trabajo eliminado exitosamente!')
        else:
            flash('Error al eliminar el puesto de trabajo.')
        return redirect(url_for('puesto_de_trabajo'))

    # Si el método no es POST, verificar si el puesto existe
    puesto_de_trabajo = get_puesto_de_trabajo_by_id(id_puesto)
    if puesto_de_trabajo is None:
        flash('Puesto de trabajo no encontrado.')
        return redirect(url_for('puesto_de_trabajo'))

    return render_template('eliminar_puesto_de_trabajo.html', puesto_de_trabajo=puesto_de_trabajo)



if __name__ == '__main__':
    app_puesto_de_trabajo.run(debug=True,port=5007)
