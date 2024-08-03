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
    query = "INSERT INTO usuarios (primer_nombre, primer_apellido, correo, password, usuario_activo, super_usuario) VALUES (%s, %s, %s, %s, %s, %s)"
    hashed_password = generate_password_hash(password)
    values = (primer_nombre, primer_apellido, correo, hashed_password, 1, 1)
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

def update_user(id_usuario, primer_nombre, primer_apellido, correo, password, usuario_activo, super_usuario):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE usuarios SET primer_nombre = %s, primer_apellido = %s, correo = %s, password = %s, usuario_activo = %s, super_usuario = %s WHERE id_usuario = %s"
    hashed_password = generate_password_hash(password)
    values = (primer_nombre, primer_apellido, correo, hashed_password, usuario_activo, super_usuario, id_usuario)
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

def get_usuarios(page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = "SELECT SQL_CALC_FOUND_ROWS id_usuario, primer_nombre, primer_apellido, correo, password, usuario_activo, super_usuario FROM usuarios LIMIT %s OFFSET %s"
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

def search_usuarios(search_criteria, search_query, page, per_page):
    connection = create_connection()
    if connection is None:
        return [], 0
    cursor = connection.cursor()
    offset = (page - 1) * per_page
    query = f"SELECT SQL_CALC_FOUND_ROWS * FROM usuarios WHERE {search_criteria} LIKE %s LIMIT %s OFFSET %s"
    values = (f'%{search_query}%', per_page, offset)
    try:
        cursor.execute(query, values)
        usuarios = cursor.fetchall()
        cursor.execute(f"SELECT FOUND_ROWS()")
        total_count = cursor.fetchone()[0]
        return usuarios, total_count
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
    query = "SELECT id_usuario, primer_nombre, primer_apellido, correo, password, usuario_activo, super_usuario FROM usuarios WHERE id_usuario = %s"
    cursor.execute(query, (id_usuario,))
    usuarios = cursor.fetchone()
    cursor.close()
    connection.close()
    return usuarios

 

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
    search_criteria = request.args.get('search_criteria', 'ciudad')
    search_query = request.args.get('search_query', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))

    if search_query:
        usuarios, total_count = search_usuarios(search_criteria, search_query, page, per_page)
    else:
        usuarios, total_count = get_usuarios(page, per_page)
    
    total_pages = (total_count + per_page - 1) // per_page

    return render_template('usuarios.html', usuarios=usuarios, search_criteria=search_criteria, search_query=search_query, page=page, total_pages=total_pages, per_page=per_page)

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
        super_usuario = request.form['super_usuario']

        valid, message = validate_user_data(primer_nombre, primer_apellido, correo, password)
        if not valid:
            flash(message)
            return redirect(url_for('edit_usuarios', id_usuario=id_usuario))

        if update_user(id_usuario, primer_nombre, primer_apellido, correo, password, usuario_activo, super_usuario):
            flash('Usuario actualizado exitosamente.')
        else:
            flash('Ocurrió un error al actualizar el usuario.')
        
        return redirect(url_for('usuarios'))

    usuarios = get_usuarios_by_id(id_usuario)
    if usuarios is None:
        flash('Usuario no encontrado.')
        return redirect(url_for('usuarios'))
    return render_template('edit_usuarios.html', usuarios=usuarios)


@app_usuarios.route('/eliminar_usuarios/<int:id_usuario>', methods=['GET', 'POST'])
def eliminar_usuarios(id_usuario):
    if request.method == 'POST':
        if delete_user(id_usuario):
            flash('¡usuarios eliminada exitosamente!')
            return redirect(url_for('usuarios'))
        else:
            flash('Ocurrió un error al eliminar la usuarios. Por favor, intente nuevamente.')
            return redirect(url_for('usuarios'))

    usuarios = get_usuarios_by_id(id_usuario)
    if usuarios is None:
        flash('usuarios no encontrada.')
        return redirect(url_for('usuarios'))

    return render_template('eliminar_usuarios.html', usuarios=usuarios)

if __name__ == '__main__':
    app_usuarios.run(debug=True)
