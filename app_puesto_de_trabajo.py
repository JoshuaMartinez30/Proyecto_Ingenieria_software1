from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app_puesto_de_trabajo = Flask(__name__)
app_puesto_de_trabajo.secret_key = 'your_secret_key'  # Cambia 'your_secret_key' por una clave secreta segura

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

def insert_puesto_de_trabajo(id_documento, fecha, hora_inicio, hora_fin, puesto_trabajo, salario):
    connection = create_connection()
    if connection is None:
        print("Error: No se pudo conectar a la base de datos.")
        return False
    cursor = connection.cursor()
    query = """INSERT INTO puesto_de_trabajo (id_documento, fecha, hora_inicio, hora_fin, puesto_trabajo, salario) 
               VALUES (%s, %s, %s, %s, %s, %s)"""
    values = (id_documento, fecha, hora_inicio, hora_fin, puesto_trabajo, salario)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Puesto de trabajo insertado exitosamente.")
        return True
    except Error as e:
        print(f"Error al insertar el puesto_de_trabajo: {e}")
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
            SELECT p.id_puesto, p.id_documento, p.fecha, 
                   p.hora_inicio, p.hora_fin, p.puesto_trabajo, p.salario, 
                   d.documento AS documento
            FROM puesto_de_trabajo p
            JOIN documento_empleado d ON p.id_documento = d.id_documento
            WHERE {search_criteria} LIKE %s 
            LIMIT %s OFFSET %s
        """
        values = (f'%{search_query}%', per_page, offset)
    else:
        query = """
            SELECT p.id_puesto, p.id_documento, p.fecha, 
                   p.hora_inicio, p.hora_fin, p.puesto_trabajo, p.salario, 
                   d.documento AS documento
            FROM puesto_de_trabajo p
            JOIN documento_empleado d ON p.id_documento = d.id_documento
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

def get_documento_empleado():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT id_documento, nombre, documento FROM documento_empleado"
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

def update_puesto_de_trabajo(id_puesto, fecha, hora_inicio, hora_fin, puesto_trabajo, salario):
    connection = create_connection()
    if connection is None:
        print("Error: No se pudo conectar a la base de datos.")
        return False
    
    cursor = connection.cursor()
    query = """
    UPDATE puesto_de_trabajo
    SET fecha = %s,
        hora_inicio = %s,
        hora_fin = %s,
        puesto_trabajo = %s,
        salario = %s
    WHERE id_puesto = %s
    """
    try:
        cursor.execute(query, (fecha, hora_inicio, hora_fin, puesto_trabajo, salario, id_puesto))
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
    documento_empleado = get_documento_empleado()  # Corregido a documento_empleado
    return render_template('index_puesto_de_trabajo.html', documento_empleado=documento_empleado)

@app_puesto_de_trabajo.route('/submit', methods=['POST'])
def submit():
    id_documento = request.form.get('id_documento')
    fecha = request.form.get('fecha')  # Corregido 'id_fecha' a 'fecha'
    hora_inicio = request.form.get('hora_inicio')
    hora_fin = request.form.get('hora_fin')
    puesto_trabajo = request.form.get('puesto_trabajo')
    salario = request.form.get('salario')
    
    # Imprimir los datos para depuración
    print(f"id_documento: {id_documento}")
    print(f"fecha: {fecha}")
    print(f"hora_inicio: {hora_inicio}")
    print(f"hora_fin: {hora_fin}")
    print(f"puesto_trabajo: {puesto_trabajo}")
    print(f"salario: {salario}")
    
    try:
        salario_decimal = float(salario)  # Asegurarse de que el salario sea un número decimal
    except ValueError:
        flash('El salario debe ser un número decimal válido.')
        return redirect(url_for('index_puesto_de_trabajo'))
    
    if insert_puesto_de_trabajo(id_documento, fecha, hora_inicio, hora_fin, puesto_trabajo, salario_decimal):
        flash('Puesto de trabajo agregado exitosamente!')
    else:
        flash('Error al agregar el puesto de trabajo.')

    return redirect(url_for('index_puesto_de_trabajo'))


@app_puesto_de_trabajo.route('/puesto_de_trabajo')
def puesto_de_trabajo():
    search_query = request.args.get('search_query', '')
    search_criteria = request.args.get('search_criteria', 'id_puesto')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    puesto_de_trabajo, total_count = get_puesto_de_trabajo(page, per_page, search_criteria, search_query)

    puesto_de_trabajo_con_documento_empleado = [
        (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7])  
        for item in puesto_de_trabajo
    ]

    total_pages = (total_count // per_page) + (1 if total_count % per_page > 0 else 0)

    return render_template(
        'puesto_de_trabajo.html',
        puesto_de_trabajo=puesto_de_trabajo_con_documento_empleado,
        page=page,
        total_pages=total_pages,
        search_query=search_query,
        search_criteria=search_criteria,
        per_page=per_page
    )

@app_puesto_de_trabajo.route('/edit_puesto_de_trabajo/<int:id_puesto>', methods=['GET', 'POST'])
def edit_puesto_de_trabajo(id_puesto):
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        hora_inicio = request.form.get('hora_inicio')
        hora_fin = request.form.get('hora_fin')
        puesto_trabajo = request.form.get('puesto_trabajo')
        salario = request.form.get('salario')

        if not fecha or not hora_inicio or not hora_fin or not puesto_trabajo or not salario:
            flash('¡Todos los campos obligatorios deben ser completados!')
            return redirect(url_for('edit_puesto_de_trabajo', id_puesto=id_puesto))

        if update_puesto_de_trabajo(id_puesto, fecha, hora_inicio, hora_fin, puesto_trabajo, salario):
            flash('Puesto de trabajo editado exitosamente!')
        else:
            flash('Error al editar el puesto de trabajo.')

        return redirect(url_for('puesto_de_trabajo'))
    else:
        puesto_de_trabajo = get_puesto_de_trabajo_by_id(id_puesto)
        documento_empleado = get_documento_empleado()  # Para cargar los datos en el formulario de edición

        if puesto_de_trabajo:
            return render_template(
                'edit_puesto_de_trabajo.html', 
                puesto_de_trabajo=puesto_de_trabajo,
                documento_empleado=documento_empleado
            )
        else:
            flash('El puesto de trabajo no existe.')
            return redirect(url_for('puesto_de_trabajo'))

        


@app_puesto_de_trabajo.route('/eliminar_puesto_de_trabajo/<int:id_puesto>', methods=['GET', 'POST'])
def eliminar_puesto_de_trabajo(id_puesto):
    if request.method == 'POST':
        if delete_puesto_de_trabajo(id_puesto):
            flash('¡Puesto de trabajo eliminado exitosamente!')
        else:
            flash('Ocurrió un error al eliminar el puesto de trabajo.')
        return redirect(url_for('puesto_de_trabajo'))

    puesto_de_trabajo = get_puesto_de_trabajo_by_id(id_puesto)
    if puesto_de_trabajo is None:
        flash('¡Puesto de trabajo no encontrado!')
        return redirect(url_for('puesto_de_trabajo'))
    
    return render_template('eliminar_puesto_de_trabajo.html', puesto_de_trabajo=puesto_de_trabajo)

    


@app_puesto_de_trabajo.route('/get_documento/<int:id_documento>', methods=['GET'])
def get_documento(id_documento):
    connection = create_connection()
    if connection is None:
        return {'documento': ''}  # Devuelve un objeto JSON vacío en caso de error
    
    cursor = connection.cursor()
    query = "SELECT documento FROM documento_empleado WHERE id_documento = %s"
    try:
        cursor.execute(query, (id_documento,))
        result = cursor.fetchone()
        if result:
            return {'documento': result[0]}  # Devuelve el documento encontrado como JSON
        else:
            return {'documento': ''}  # Si no se encuentra el documento, devuelve vacío
    except Error as e:
        print(f"Error al obtener el documento: {e}")
        return {'documento': ''}
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    app_puesto_de_trabajo.run(debug=True,port=5007)
