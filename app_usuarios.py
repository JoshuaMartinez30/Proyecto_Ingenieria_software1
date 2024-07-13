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

def get_usuarios():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM usuarios"
    try:
        cursor.execute(query)
        usuarios = cursor.fetchall()
        return usuarios
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
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

def search_users(search_query):
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM usuarios WHERE primer_nombre LIKE %s OR primer_apellido LIKE %s OR correo LIKE %s OR password LIKE %s OR usuario_activo LIKE %s"
    values = (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
    try:
        cursor.execute(query, values)
        usuarios = cursor.fetchall()
        return usuarios
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
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
    search_query = request.args.get('search')
    if search_query:
        usuarios = search_users(search_query)
    else:
        usuarios = get_usuarios()
    return render_template('usuarios.html', usuarios=usuarios, search_query=search_query)

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

    hashed_password = generate_password_hash(password)
    if insert_user(primer_nombre, primer_apellido, correo, hashed_password):
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

        hashed_password = generate_password_hash(password)
        if update_user(id_usuario, primer_nombre, primer_apellido, correo, hashed_password, usuario_activo):
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
