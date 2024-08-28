from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app_sar = Flask(__name__)
app_sar.secret_key = 'your_secret_key'

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
            print("Conexión exitosa a la base de datos MySQL")
    except Error as e:
        print(f"Error '{e}' ocurrió")
    return connection

def insert_sar(rtn, cai, fecha_emision, fecha_vencimiento, rango_inicial, rango_final, id_sucursal, secuencial, estado):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    INSERT INTO sar 
    (rtn, cai, fecha_emision, fecha_vencimiento, rango_inicial, rango_final, id_sucursal, secuencial, estado)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (rtn, cai, fecha_emision, fecha_vencimiento, rango_inicial, rango_final, id_sucursal, secuencial, estado)
    try:
        cursor.execute(query, values)
        connection.commit()
        return True
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

def get_sar():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = """
    SELECT s.id_sar, s.rtn, s.cai, s.fecha_emision, s.fecha_vencimiento, s.rango_inicial, s.rango_final, su.ciudad, s.secuencial, s.estado
    FROM sar s
    JOIN sucursales su ON s.id_sucursal = su.id_sucursal
    """
    try:
        cursor.execute(query)
        sar = cursor.fetchall()
        return sar
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return []
    finally:
        cursor.close()
        connection.close()

def get_sar_by_id(id_sar):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = """
    SELECT s.id_sar, s.rtn, s.cai, 
           DATE_FORMAT(s.fecha_emision, '%Y-%m-%d'), 
           DATE_FORMAT(s.fecha_vencimiento, '%Y-%m-%d'), 
           s.rango_inicial, s.rango_final, 
           s.id_sucursal, s.secuencial, s.estado,
           su.ciudad
    FROM sar s
    JOIN sucursales su ON s.id_sucursal = su.id_sucursal
    WHERE s.id_sar = %s
    """
    try:
        cursor.execute(query, (id_sar,))
        sar = cursor.fetchone()
        return sar
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return None
    finally:
        cursor.close()
        connection.close()


def update_sar(id_sar, rtn, cai, fecha_emision, fecha_vencimiento, rango_inicial, rango_final, id_sucursal, secuencial, estado):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
    UPDATE sar
    SET rtn = %s, cai = %s, fecha_emision = %s, fecha_vencimiento = %s, rango_inicial = %s, rango_final = %s, id_sucursal = %s, secuencial = %s, estado = %s
    WHERE id_sar = %s
    """
    values = (rtn, cai, fecha_emision, fecha_vencimiento, rango_inicial, rango_final, id_sucursal, secuencial, estado, id_sar)
    try:
        cursor.execute(query, values)
        connection.commit()
        return True
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_sar(id_sar):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM sar WHERE id_sar = %s"
    try:
        cursor.execute(query, (id_sar,))
        connection.commit()
        return True
    except Error as e:
        print(f"Error '{e}' ocurrió")
        return False
    finally:
        cursor.close()
        connection.close()

@app_sar.route('/')
def index_sar():
    connection = create_connection()
    if connection is None:
        return render_template('index_sar.html', sucursales=[])
    cursor = connection.cursor()

    cursor.execute("SELECT id_sucursal, ciudad FROM sucursales")
    sucursales = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('index_sar.html', sucursales=sucursales)

@app_sar.route('/sars')
def sars():
    sar = get_sar()
    return render_template('sars.html', sar=sar)

@app_sar.route('/submit', methods=['POST'])
def submit():
    rtn = request.form['rtn']
    cai = request.form['cai']
    fecha_emision = request.form['fecha_emision']
    fecha_vencimiento = request.form['fecha_vencimiento']
    rango_inicial = request.form['rango_inicial']
    rango_final = request.form['rango_final']
    id_sucursal = request.form['id_sucursal']
    secuencial = request.form['secuencial']
    estado = request.form['estado']

    if not rtn or not cai or not fecha_emision or not fecha_vencimiento or not rango_inicial or not rango_final or not id_sucursal or not secuencial or not estado:
        flash('Todos los campos son requeridos!')
        return redirect(url_for('index_sar'))

    if insert_sar(rtn, cai, fecha_emision, fecha_vencimiento, rango_inicial, rango_final, id_sucursal, secuencial, estado):
        flash('SAR insertado exitosamente!')
    else:
        flash('Ocurrió un error al insertar el SAR.')
    
    return redirect(url_for('index_sar'))

@app_sar.route('/edit_sar/<int:id_sar>', methods=['GET', 'POST'])
def edit_sar(id_sar):
    if request.method == 'POST':
        rtn = request.form['rtn']
        cai = request.form['cai']
        fecha_emision = request.form['fecha_emision']
        fecha_vencimiento = request.form['fecha_vencimiento']
        rango_inicial = request.form['rango_inicial']
        rango_final = request.form['rango_final']
        id_sucursal = request.form['id_sucursal']
        secuencial = request.form['secuencial']
        estado = request.form['estado']

        if not rtn or not cai or not fecha_emision or not fecha_vencimiento or not rango_inicial or not rango_final or not id_sucursal or not secuencial or not estado:
            flash('Todos los campos son requeridos!')
            return redirect(url_for('edit_sar', id_sar=id_sar))

        if update_sar(id_sar, rtn, cai, fecha_emision, fecha_vencimiento, rango_inicial, rango_final, id_sucursal, secuencial, estado):
            flash('SAR actualizado exitosamente!')
        else:
            flash('Ocurrió un error al actualizar el SAR.')
        
        return redirect(url_for('sars'))

    sar = get_sar_by_id(id_sar)
    if sar is None:
        flash('SAR no encontrado!')
        return redirect(url_for('sars'))

    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT id_sucursal, ciudad FROM sucursales")
    sucursales = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('edit_sar.html', sar=sar, sucursales=sucursales)

@app_sar.route('/eliminar_sar/<int:id_sar>', methods=['GET', 'POST'])
def eliminar_sar(id_sar):
    if request.method == 'POST':
        if delete_sar(id_sar):
            flash('SAR eliminado exitosamente!')
        else:
            flash('Ocurrió un error al eliminar el SAR.')
        return redirect(url_for('sars'))

    sar = get_sar_by_id(id_sar)
    if sar is None:
        flash('SAR no encontrado!')
        return redirect(url_for('sars'))
    return render_template('eliminar_sar.html', sar=sar)

if __name__ == "__main__":
    app_sar.run(debug=True, port=5027)
