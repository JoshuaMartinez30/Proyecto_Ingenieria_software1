from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

app_login = Flask(__name__)
app_login.secret_key = 'your_secret_key'

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

def insert_user(primer_nombre, primer_apellido, correo, password):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "INSERT INTO usuarios (primer_nombre, primer_apellido, correo, password, usuario_activo, super_usuario) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (primer_nombre, primer_apellido, correo, password, 1, 1)
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

def verify_user(correo, password):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE correo = %s AND password = %s"
    values = (correo, password)
    try:
        cursor.execute(query, values)
        user = cursor.fetchone()
        return user is not None  # Retorna True si el usuario existe, de lo contrario False
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()


@app_login.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    correo = request.form['correo']
    password = request.form['password']

    if verify_user(correo, password):
        flash('Usuario encontrado exitosamente.')
        # Redirige a la URL específica después de un login exitoso
        return redirect('http://127.0.0.1:5501/index.html')
    else:
        flash('Correo o contraseña incorrectos.')
        return redirect(url_for('index_login'))

@app_login.route('/index_principal')
def index_principal():
    return render_template('index.html')


@app_login.route('/')
def index_login():
    return render_template('index_login.html')

@app_login.route('/registro')
def index_registro():
    return render_template('index_registro.html')

@app_login.route('/submit', methods=['POST'])
def submit():
    primer_nombre = request.form['primer_nombre']
    primer_apellido = request.form['primer_apellido']
    correo = request.form['correo']
    password = request.form['password']

    valid, message = validate_user_data(primer_nombre, primer_apellido, correo, password)
    if not valid:
        flash(message)
        return redirect(url_for('index_registro'))  # Asegúrate de redirigir a 'index_registro'

    if insert_user(primer_nombre, primer_apellido, correo, password):
        flash('Usuario ingresado exitosamente.')
    else:
        flash('Ocurrió un error al ingresar el usuario.')
    
    return redirect(url_for('index_login'))  # Después de registrar, redirige a la página de login

if __name__ == '__main__':
    app_login.run(debug=True, port=5030)
