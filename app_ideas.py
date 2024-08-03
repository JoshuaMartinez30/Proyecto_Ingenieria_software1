from flask import Flask, render_template, request, redirect, url_for, flash
import re
import mysql.connector
from mysql.connector import Error

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

def insert_idea(documento, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    query = """INSERT INTO ideas_mejora (documento, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (documento, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento)
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

def get_ideas(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM ideas_mejora LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        ideas = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_ideas = cursor.fetchone()[0]
        return ideas, total_ideas
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

def update_idea(documento, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento, id_mejora):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """UPDATE ideas_mejora 
               SET documento = %s, fecha_propuesta = %s, descripcion_idea = %s, estado = %s, fecha_implementacion = %s, descripcion_implementacion = %s, fecha_evaluacion = %s, impacto = %s, indicadores_rendimiento = %s 
               WHERE id_mejora = %s"""
    values = (documento, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento, id_mejora)
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

def delete_idea(id_mejora):
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

def search_ideas(search_criteria, search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = f"SELECT * FROM ideas_mejora WHERE {search_criteria} LIKE %s LIMIT %s OFFSET %s"
    values = (f'%{search_query}%', per_page, offset)
    try:
        cursor.execute(query, values)
        ideas = cursor.fetchall()
        count_query = f"SELECT COUNT(*) FROM ideas_mejora WHERE {search_criteria} LIKE %s"
        cursor.execute(count_query, (f'%{search_query}%',))
        total_count = cursor.fetchone()[0]
        return ideas, total_count
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

@app_ideas.route('/')
def index_ideas():
    return render_template('index_ideas.html')

@app_ideas.route('/ideas')
def ideas():
    search_criteria = request.args.get('search_criteria')
    search_query = request.args.get('search_query')
    page = int(request.args.get('page', 1))
    per_page = 10

    if search_criteria and search_query:
        ideas, total_count = search_ideas(search_criteria, search_query, page, per_page)
    else:
        ideas, total_count = get_ideas(page, per_page)
    
    total_pages = (total_count + per_page - 1) // per_page

    return render_template('ideas.html', ideas=ideas, search_criteria=search_criteria, search_query=search_query, page=page, total_pages=total_pages)

@app_ideas.route('/submit', methods=['POST'])
def submit():
    documento = request.form['documento']
    fecha_propuesta = request.form['fecha_propuesta']
    descripcion_idea = request.form['descripcion_idea']
    estado = request.form['estado']
    fecha_implementacion = request.form['fecha_implementacion']
    descripcion_implementacion = request.form['descripcion_implementacion']
    fecha_evaluacion = request.form['fecha_evaluacion']
    impacto = request.form['impacto']
    indicadores_rendimiento = request.form['indicadores_rendimiento']

    # Validaciones
    if not all([documento, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento]):
        flash('¡Todos los campos obligatorios deben ser completados!')
        return redirect(url_for('index_ideas'))

    if insert_idea(documento, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento):
        flash('¡Idea ingresada exitosamente!')
    else:
        flash('Ocurrió un error al ingresar la idea.')

    return redirect(url_for('index_ideas'))

@app_ideas.route('/edit_idea/<int:id_mejora>', methods=['GET', 'POST'])
def edit_idea(id_mejora):
    if request.method == 'POST':
        documento = request.form['documento']
        fecha_propuesta = request.form['fecha_propuesta']
        descripcion_idea = request.form['descripcion_idea']
        estado = request.form['estado']
        fecha_implementacion = request.form['fecha_implementacion']
        descripcion_implementacion = request.form['descripcion_implementacion']
        fecha_evaluacion = request.form['fecha_evaluacion']
        impacto = request.form['impacto']
        indicadores_rendimiento = request.form['indicadores_rendimiento']

        # Validaciones
        if not all([documento, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento]):
            flash('¡Todos los campos obligatorios deben ser completados!')
            return redirect(url_for('edit_idea', id_mejora=id_mejora))

        if update_idea(documento, fecha_propuesta, descripcion_idea, estado, fecha_implementacion, descripcion_implementacion, fecha_evaluacion, impacto, indicadores_rendimiento, id_mejora):
            flash('¡Idea actualizada exitosamente!')
            return redirect(url_for('ideas'))
        else:
            flash('Ocurrió un error al actualizar la idea.')
        
        return redirect(url_for('edit_idea', id_mejora=id_mejora))

    idea = get_idea_by_id(id_mejora)
    if idea is None:
        flash('¡Idea no encontrada!')
        return redirect(url_for('ideas'))
    
    return render_template('edit_ideas.html', idea=idea)

@app_ideas.route('/eliminar_idea/<int:id_mejora>', methods=['GET', 'POST'])
def eliminar_idea(id_mejora):
    if request.method == 'POST':
        if delete_idea(id_mejora):
            flash('¡Idea eliminada exitosamente!')
        else:
            flash('Ocurrió un error al eliminar la idea.')
        return redirect(url_for('ideas'))
    
    idea = get_idea_by_id(id_mejora)
    if idea is None:
        flash('¡Idea no encontrada!')
        return redirect(url_for('ideas'))

    return render_template('eliminar_ideas.html', idea=idea)

if __name__ == '__main__':
    app_ideas.run(debug=True,port=5010)