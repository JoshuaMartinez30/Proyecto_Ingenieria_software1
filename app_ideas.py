import re
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app_ideas = Flask(__name__)
app_ideas.secret_key = 'your_secret_key'

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

def insert_user(id_proponente, id_evaluador, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "INSERT INTO ideas_mejora (id_proponente, id_evaluador, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (id_proponente, id_evaluador, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento)
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

def get_idea(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM ideas_mejora LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        idea = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_idea = cursor.fetchone()[0]
        return idea, total_idea
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_idea_by_id(id_mejora):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM ideas_mejora WHERE id_mejora = %s"
    try:
        cursor.execute(query, (id_mejora,))
        idea = cursor.fetchone()
        return idea
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_user(id_mejora, id_proponente, id_evaluador, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE ideas_mejora SET id_proponente = %s, id_evaluador = %s, fecha_propuesta = %s, descripcion_idea = %s, estado = %s, fecha_implementacion = %s, descripcion_implementacion = %s, fecha_evaluacion = %s, impacto = %s, indicadores_rendimiento = %s WHERE id_mejora = %s"
    values = (id_proponente, id_evaluador, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento, id_mejora)
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

def delete_user(id_mejora):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM ideas_mejora WHERE id_mejora = %s"
    try:
        cursor.execute(query, (id_mejora,))
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
    query = f"SELECT SQL_CALC_FOUND_ROWS * FROM ideas_mejora WHERE {search_field} LIKE %s LIMIT %s OFFSET %s"
    values = (f'%{search_query}%', per_page, offset)
    try:
        cursor.execute(query, values)
        idea = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_idea = cursor.fetchone()[0]
        return idea, total_idea
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

@app_ideas.route('/')
def index_ideas():
    return render_template('index_ideas.html')

@app_ideas.route('/idea')
def idea():
    search_query = request.args.get('search')
    search_field = request.args.get('field')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if search_query and search_field:
        idea, total_idea = search_users(search_query, search_field, page, per_page)
    else:
        idea, total_idea = get_idea(page, per_page)

    total_pages = (total_idea + per_page - 1) // per_page
    return render_template('ideas.html', idea=idea, search_query=search_query, search_field=search_field, page=page, per_page=per_page, total_idea=total_idea, total_pages=total_pages)

@app_ideas.route('/submit', methods=['POST'])
def submit():
    id_proponente = request.form['id_proponente']
    id_evaluador = request.form['id_evaluador']
    fecha_propuesta = request.form['fecha_propuesta']
    descripcion_idea = request.form['descripcion_idea']
    estado = request.form['estado']
    fecha_implementacion = request.form['fecha_implementacion']
    descripcion_implementacion = request.form['descripcion_implementacion']
    fecha_evaluacion = request.form['fecha_evaluacion']
    impacto = request.form['impacto']
    indicadores_rendimiento = request.form['indicadores_rendimiento']

    if not id_proponente or not id_evaluador or not fecha_propuesta or not descripcion_idea or not estado or not fecha_implementacion or not descripcion_implementacion or not fecha_evaluacion or not impacto or not indicadores_rendimiento:
        flash('All fields are required!')
        return redirect(url_for('index_ideas'))
    
    fecha_propuesta_dt = datetime.strptime(fecha_propuesta, '%Y-%m-%d')
    fecha_implementacion_dt = datetime.strptime(fecha_implementacion, '%Y-%m-%d')
    fecha_evaluacion_dt = datetime.strptime(fecha_evaluacion, '%Y-%m-%d')

    if fecha_implementacion_dt < fecha_propuesta_dt:
        flash('La fecha de implementación no puede ser antes que la fecha propuesta')
        return redirect(url_for('index_ideas'))
    
    if fecha_evaluacion_dt < fecha_propuesta_dt or fecha_evaluacion_dt < fecha_implementacion_dt:
        flash('La fecha de evaluación no puede ser antes que la fecha propuesta ni la fecha de implementación')
        return redirect(url_for('index_ideas'))

    if insert_user(id_proponente, id_evaluador, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento):
        flash('Idea inserted successfully!')
    else:
        flash('An error occurred while inserting the idea.')
    
    return redirect(url_for('index_ideas'))

@app_ideas.route('/edit_idea/<int:id_mejora>', methods=['GET', 'POST'])
def edit_idea(id_mejora):
    if request.method == 'POST':
        id_proponente = request.form['id_proponente']
        id_evaluador = request.form['id_evaluador']
        fecha_propuesta = request.form['fecha_propuesta']
        descripcion_idea = request.form['descripcion_idea']
        estado = request.form['estado']
        fecha_implementacion = request.form['fecha_implementacion']
        descripcion_implementacion = request.form['descripcion_implementacion']
        fecha_evaluacion = request.form['fecha_evaluacion']
        impacto = request.form['impacto']
        indicadores_rendimiento = request.form['indicadores_rendimiento']

        if not id_mejora or not id_proponente or not id_evaluador or not fecha_propuesta or not descripcion_idea or not estado or not fecha_implementacion or not descripcion_implementacion or not fecha_evaluacion or not impacto or not indicadores_rendimiento:
            flash('All fields are required!')
            return redirect(url_for('edit_idea', id_mejora=id_mejora))
        
        # Validación de fechas
        fecha_propuesta_dt = datetime.strptime(fecha_propuesta, '%Y-%m-%d')
        fecha_implementacion_dt = datetime.strptime(fecha_implementacion, '%Y-%m-%d')
        fecha_evaluacion_dt = datetime.strptime(fecha_evaluacion, '%Y-%m-%d')

        if fecha_implementacion_dt < fecha_propuesta_dt:
            flash('La fecha de implementación no puede ser antes que la fecha propuesta')
            return redirect(url_for('edit_idea', id_mejora=id_mejora))
        
        if fecha_evaluacion_dt < fecha_propuesta_dt or fecha_evaluacion_dt < fecha_implementacion_dt:
            flash('La fecha de evaluación no puede ser antes que la fecha propuesta ni la fecha de implementación')
            return redirect(url_for('edit_idea', id_mejora=id_mejora))

        if update_user(id_mejora, id_proponente, id_evaluador, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento):
            flash('Idea updated successfully!')
        else:
            flash('An error occurred while updating the idea.')
        
        return redirect(url_for('idea'))

    idea = get_idea_by_id(id_mejora)
    if not idea:
        flash('Idea not found!')
        return redirect(url_for('idea'))
    
    return render_template('edit_idea.html', idea=idea)

@app_ideas.route('/eliminar_idea/<int:id_mejora>')
def eliminar_idea(id_mejora):
    if delete_user(id_mejora):
        flash('Idea deleted successfully!')
    else:
        flash('An error occurred while deleting the idea.')
    return redirect(url_for('idea'))

if __name__ == '__main__':
    app_ideas.run(debug=True, port=5015)
