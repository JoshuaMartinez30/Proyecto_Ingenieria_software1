from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error
import re

app_login = Flask(__name__)
app_login.secret_key = 'your_secret_key'

# Diccionario para almacenar intentos fallidos
failed_attempts = {}

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
    query = "SELECT id_usuario, primer_nombre, primer_apellido, correo, password, usuario_activo, super_usuario, id_sucursal FROM usuarios WHERE correo = %s"
    values = (correo,)
    try:
        cursor.execute(query, values)
        user = cursor.fetchone()
        if user:
            # Verifica si la contraseña es correcta y si el usuario está activo
            if user['password'] == password:
                if user['usuario_activo'] == 0:
                    return False
                # Resetea intentos fallidos si el login es exitoso
                if correo in failed_attempts:
                    del failed_attempts[correo]
                return user
            else:
                # Incrementa el contador de intentos fallidos
                if correo not in failed_attempts:
                    failed_attempts[correo] = 0
                failed_attempts[correo] += 1
                # Bloquea el usuario si se alcanzan 3 intentos fallidos
                if failed_attempts[correo] >= 3:
                    cursor.execute("UPDATE usuarios SET usuario_activo = 0 WHERE correo = %s", (correo,))
                    connection.commit()
                return False
        return False
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

    user = verify_user(correo, password)
    if user:
        if user['usuario_activo'] == 0:
            flash('Usuario está bloqueado, por favor comuníquese con el administrador.')
            return redirect(url_for('index_login'))
        else:
            # Almacena los datos del usuario en la sesión
            session['primer_nombre'] = user['primer_nombre']
            session['primer_apellido'] = user['primer_apellido']
            session['super_usuario'] = user['super_usuario']
            session['correo'] = user['correo']
            session['id_sucursal'] = user['id_sucursal'] 
            flash('Usuario encontrado exitosamente.')
            return redirect(url_for('index_principal'))
    else:
        flash('Correo o contraseña incorrectos.')
        return redirect(url_for('index_login'))


@app_login.route('/index_principal')
def index_principal():
    primer_nombre = session.get('primer_nombre')  # Obtiene el nombre del usuario desde la sesión
    primer_apellido = session.get('primer_apellido')
    correo = session.get('correo')
    id_sucursal = session.get('id_sucursal')
    return render_template('index.html', primer_nombre=primer_nombre, primer_apellido=primer_apellido, correo=correo, id_sucursal=id_sucursal)

@app_login.route('/')
def index_login():
    return render_template('index_login.html')

@app_login.route('/registro')
def index_registro():
    return render_template('index_registro.html')

if __name__ == '__main__':
    app_login.run(debug=True, port=5030)
