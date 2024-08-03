from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from datetime import datetime, date
from mysql.connector import Error
import re

app_capacitacion = Flask(__name__)
app_capacitacion.secret_key = 'your_secret_key'

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

def insert_capacitacion(id_empleado, tema, fecha_capacitacion, duracion, resultado):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()

    query = """
    INSERT INTO capacitacion (id_empleado, tema, fecha_capacitacion, duracion, resultado)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (id_empleado, tema, fecha_capacitacion, duracion, resultado)
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

def get_capacitaciones(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    query = """
    SELECT c.id_capacitacion, e.nombre, c.tema, c.fecha_capacitacion, c.duracion, c.resultado
    FROM capacitacion c
    JOIN empleados e ON c.id_empleado = e.id_empleado
    LIMIT %s OFFSET %s
    """
    
    try:
        cursor.execute(query, (per_page, offset))
        capacitaciones = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM capacitacion")
        total_count = cursor.fetchone()[0]

        return capacitaciones, total_count
    except Exception as e:
        print(f"Error: {e}")
        return [], 0
    finally:
        cursor.close()
        connection.close()


def get_capacitacion_by_id(id_capacitacion):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM capacitacion WHERE id_capacitacion = %s"
    try:
        cursor.execute(query, (id_capacitacion,))
        capacitacion = cursor.fetchone()
        return capacitacion
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_capacitacion(id_capacitacion, id_empleado, tema, fecha_capacitacion, duracion, resultado):
    connection = create_connection()
    if connection is None:
        print("No se pudo conectar a la base de datos.")
        return False
    cursor = connection.cursor()
    query = """
    UPDATE capacitacion
    SET id_empleado = %s, tema = %s, fecha_capacitacion = %s, duracion = %s, resultado = %s
    WHERE id_capacitacion = %s
    """
    values = (id_empleado, tema, fecha_capacitacion, duracion, resultado, id_capacitacion)
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

def delete_capacitacion(id_capacitacion):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM capacitacion WHERE id_capacitacion = %s"
    try:
        cursor.execute(query, (id_capacitacion,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def get_empleados():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_empleado, nombre FROM empleados"
    try:
        cursor.execute(query)
        empleados = cursor.fetchall()
        print("Empleados obtenidos:", empleados)  # Verificar datos obtenidos
        return empleados
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()



def search_capacitaciones(search_criteria, search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    # Ajusta la consulta para incluir el campo nombre del empleado
    query = f"""
    SELECT c.id_capacitacion, e.nombre, c.tema, c.fecha_capacitacion, c.duracion, c.resultado
    FROM capacitacion c
    JOIN empleados e ON c.id_empleado = e.id_empleado
    WHERE {search_criteria} LIKE %s 
    LIMIT %s OFFSET %s
    """
    
    try:
        cursor.execute(query, (f'%{search_query}%', per_page, offset))
        capacitaciones = cursor.fetchall()

        # Ajusta el conteo total para considerar la búsqueda en la tabla de empleados
        count_query = f"""
        SELECT COUNT(*)
        FROM capacitacion c
        JOIN empleados e ON c.id_empleado = e.id_empleado
        WHERE {search_criteria} LIKE %s
        """
        cursor.execute(count_query, (f'%{search_query}%',))
        total_count = cursor.fetchone()[0]

        return capacitaciones, total_count
    except Exception as e:
        print(f"Error: {e}")
        return [], 0
    finally:
        cursor.close()
        connection.close()



@app_capacitacion.route('/')
def index_capacitacion():
    empleados = get_empleados()  # Obtiene la lista de empleados
    today = datetime.now().strftime('%Y-%m-%dT%H:%M')  # Formatea la fecha actual para el input datetime-local
    return render_template('index_capacitacion.html', empleados=empleados, today=today)

@app_capacitacion.route('/capacitaciones')
def capacitaciones():
    search_query = request.args.get('search_query')
    search_criteria = request.args.get('search_criteria', 'tema')  # Aquí puedes definir un criterio predeterminado, como 'tema'
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    if search_query:
        capacitaciones, total_count = search_capacitaciones(search_criteria, search_query, page, per_page)
    else:
        capacitaciones, total_count = get_capacitaciones(page, per_page)
    
    total_pages = (total_count + per_page - 1) // per_page

    return render_template('capacitaciones.html', capacitaciones=capacitaciones, search_query=search_query, page=page, total_pages=total_pages, per_page=per_page)

@app_capacitacion.route('/submit', methods=['POST'])
def submit_capacitacion():
    id_empleado = request.form['id_empleado']
    tema = request.form['tema']
    fecha_capacitacion = request.form['fecha_capacitacion']
    duracion = request.form['duracion']
    resultado = request.form['resultado']

    # Validaciones
    errors = []
    if not tema or not re.match(r'^[a-zA-Z\s]+$', tema):
        errors.append('El tema debe ser texto sin números ni símbolos.')
    
    if not duracion.isdigit():
        errors.append('La duración debe ser un número entero.')
    
    if not resultado.isdigit():
        errors.append('El resultado debe ser un número entero.')

    try:
        # Ajustar el formato a 'YYYY-MM-DDTHH:MM' para datetime-local
        fecha = datetime.strptime(fecha_capacitacion, '%Y-%m-%dT%H:%M')
        if fecha < datetime.now():
            errors.append('La fecha de capacitación no puede ser en el pasado.')
    except ValueError:
        errors.append('El formato de la fecha es incorrecto.')

    if errors:
        flash(' '.join(errors))
        return redirect(url_for('index_capacitacion'))

    # Inserta la capacitación en la base de datos
    if insert_capacitacion(id_empleado, tema, fecha_capacitacion, duracion, resultado):
        flash('Capacitación insertada correctamente!')
    else:
        flash('Ocurrió un error al insertar la capacitación.')

    return redirect(url_for('index_capacitacion'))


@app_capacitacion.route('/edit/<int:id_capacitacion>', methods=['GET', 'POST'])
def edit_capacitacion(id_capacitacion):
    if request.method == 'POST':
        id_empleado = request.form['id_empleado']
        tema = request.form['tema']
        fecha_capacitacion = request.form['fecha_capacitacion']
        duracion = request.form['duracion']
        resultado = request.form['resultado']

        # Validaciones
        errors = []
        if not tema or not re.match(r'^[a-zA-Z\s]+$', tema):
            errors.append('El tema debe ser texto sin números ni símbolos.')
        
        if not duracion.isdigit():
            errors.append('La duración debe ser un número entero.')
        
        if not resultado.isdigit():
            errors.append('El resultado debe ser un número entero.')

        try:
            fecha = datetime.strptime(fecha_capacitacion, '%Y-%m-%dT%H:%M')
            if fecha < datetime.now():
                errors.append('La fecha de capacitación no puede ser en el pasado.')
        except ValueError:
            errors.append('El formato de la fecha es incorrecto.')

        if errors:
            flash(' '.join(errors))
            return redirect(url_for('edit_capacitacion', id_capacitacion=id_capacitacion))

        if update_capacitacion(id_capacitacion, id_empleado, tema, fecha_capacitacion, duracion, resultado):
            flash('Capacitación actualizada correctamente!')
        else:
            flash('Ocurrió un error al actualizar la capacitación.')
        return redirect(url_for('capacitaciones'))

    capacitacion = get_capacitacion_by_id(id_capacitacion)
    empleados = get_empleados()
    today = datetime.now().strftime('%Y-%m-%dT%H:%M')

    # Asegúrate de que los datos sean correctos
    if not capacitacion:
        flash('Capacitación no encontrada!')
        return redirect(url_for('capacitaciones'))

    return render_template('edit_capacitacion.html', capacitacion=capacitacion, empleados=empleados, today=today)

@app_capacitacion.route('/eliminar/<int:id_capacitacion>', methods=['GET', 'POST'])
def eliminar_capacitacion(id_capacitacion):
    if request.method == 'POST':
        if delete_capacitacion(id_capacitacion):
            flash('Capacitación eliminada exitosamente!')
        else:
            flash('Ocurrió un error al eliminar la capacitación.')
        return redirect(url_for('capacitaciones'))

    capacitacion = get_capacitacion_by_id(id_capacitacion)
    if capacitacion is None:
        flash('Capacitación no encontrada!')
        return redirect(url_for('capacitaciones'))
    
    return render_template('eliminar_capacitacion.html', capacitacion=capacitacion)

if __name__ == '__main__':
    app_capacitacion.run(debug=True,port=5021)
