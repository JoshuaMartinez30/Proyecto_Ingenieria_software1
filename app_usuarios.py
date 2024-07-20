from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re
from werkzeug.security import generate_password_hash

app_usuarios = Flask(__name__)
app_usuarios.secret_key = 'your_secret_key'

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

def insert_user(primer_nombre, primer_apellido, correo, password):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "INSERT INTO usuarios (primer_nombre, primer_apellido, correo, password, usuario_activo) VALUES (%s, %s, %s, %s, %s)"
    hashed_password = generate_password_hash(password)
    values = (primer_nombre, primer_apellido, correo, hashed_password, 1)
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

def get_usuarios(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS * FROM usuarios LIMIT %s OFFSET %s"
    try:
        cursor.execute(query, (per_page, offset))
        usuarios = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_usuarios = cursor.fetchone()[0]
        return usuarios, total_usuarios
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def get_usuarios_by_id(id_usuario):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM usuarios WHERE id_usuario = %s"
    try:
        cursor.execute(query, (id_usuario,))
        usuarios = cursor.fetchone()
        return usuarios
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_user(id_usuario, primer_nombre, primer_apellido, correo, password, usuario_activo):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE usuarios SET primer_nombre = %s, primer_apellido = %s, correo = %s, password = %s, usuario_activo = %s WHERE id_usuario = %s"
    hashed_password = generate_password_hash(password)
    values = (primer_nombre, primer_apellido, correo, hashed_password, usuario_activo, id_usuario)
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

def delete_user(id_usuario):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM usuarios WHERE id_usuario = %s"
    try:
        cursor.execute(query, (id_usuario,))
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
    query = """
    SELECT SQL_CALC_FOUND_ROWS * 
    FROM usuarios 
    WHERE {} LIKE %s 
    LIMIT %s OFFSET %s
    """.format(
        {
            'nombre': 'primer_nombre',
            'apellido': 'primer_apellido',
            'correo': 'correo'
        }.get(search_field, 'primer_nombre')  # Default to 'primer_nombre' if no valid field
    )
    values = (f'%{search_query}%', per_page, offset)
    try:
        cursor.execute(query, values)
        usuarios = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_usuarios = cursor.fetchone()[0]
        return usuarios, total_usuarios
    except Error as e:
        print(f"The error '{e}' occurred")
        return [], 0
    finally:
        cursor.close()
        connection.close()


def validate_user_data(primer_nombre, primer_apellido, correo, password):
    if not primer_nombre or not primer_apellido or not correo or not password:
        return False, 'Todos los campos son requeridos.'

    if len(primer_nombre) < 3 or len(primer_nombre) > 15 or len(primer_apellido) < 3 or len(primer_apellido) > 15:
        return False, 'Nombre y apellido deben tener entre 3 y 15 caracteres.'

    if re.search(r'[^A-Za-z]', primer_nombre) or re.search(r'[^A-Za-z]', primer_apellido):
        return False, 'Nombre y apellido deben contener solo letras.'

    if re.search(r'(.)\1{2,}', primer_nombre) or re.search(r'(.)\1{2,}', primer_apellido):
        return False, 'No se permiten tres letras repetidas consecutivamente.'

    if not re.match(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+', correo):
        return False, 'Formato de correo inválido.'

    if len(password) < 6 or len(password) > 20:
        return False, 'La contraseña debe tener entre 6 y 20 caracteres.'

    return True, 'Validación exitosa.'

@app_usuarios.route('/')
def index_usuarios():
    return render_template('index_usuarios.html')

@app_usuarios.route('/usuarios')
def usuarios():
    search_query = request.args.get('search', '')
    search_field = request.args.get('search_field', 'nombre')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if search_query:
        usuarios, total_usuarios = search_users(search_query, search_field, page, per_page)
    else:
        usuarios, total_usuarios = get_usuarios(page, per_page)

    total_pages = (total_usuarios + per_page - 1) // per_page
    return render_template('usuarios.html', usuarios=usuarios, search_query=search_query, search_field=search_field, page=page, per_page=per_page, total_usuarios=total_usuarios, total_pages=total_pages)

@app_usuarios.route('/submit', methods=['POST'])
def submit():
    primer_nombre = request.form['primer_nombre']
    primer_apellido = request.form['primer_apellido']
    correo = request.form['correo']
    password = request.form['password']

    valid, message = validate_user_data(primer_nombre, primer_apellido, correo, password)
    if not valid:
        flash(message)
        return redirect(url_for('index_usuarios'))

    if insert_user(primer_nombre, primer_apellido, correo, password):
        flash('Usuario ingresado exitosamente.')
    else:
        flash('Ocurrió un error al ingresar el usuario.')
    
    return redirect(url_for('index_usuarios'))

@app_usuarios.route('/edit_usuarios/<int:id_usuario>', methods=['GET', 'POST'])
def edit_usuarios(id_usuario):
    if request.method == 'POST':
        primer_nombre = request.form['primer_nombre']
        primer_apellido = request.form['primer_apellido']
        correo = request.form['correo']
        password = request.form['password']
        usuario_activo = request.form['usuario_activo']

        valid, message = validate_user_data(primer_nombre, primer_apellido, correo, password)
        if not valid:
            flash(message)
            return redirect(url_for('edit_usuarios', id_usuario=id_usuario))

        if update_user(id_usuario, primer_nombre, primer_apellido, correo, password, usuario_activo):
            flash('Usuario actualizado exitosamente.')
        else:
            flash('Ocurrió un error al actualizar el usuario.')
        
        return redirect(url_for('usuarios'))

    usuarios = get_usuarios_by_id(id_usuario)
    if usuarios is None:
        flash('Usuario no encontrado.')
        return redirect(url_for('usuarios'))
    return render_template('edit_usuarios.html', usuarios=usuarios)

@app_usuarios.route('/eliminar_usuarios/<int:id_usuario>')
def eliminar_usuarios(id_usuario):
    if delete_user(id_usuario):
        flash('Usuario eliminado exitosamente.')
    else:
        flash('Ocurrió un error al eliminar el usuario.')
    return redirect(url_for('usuarios'))

if __name__ == '__main__':
    app_usuarios.run(debug=True, port=5012)
