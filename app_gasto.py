from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

app_gasto = Flask(__name__)
app_gasto.secret_key = 'your_secret_key'

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
            print("Conexión exitosa a la base de datos MySQL")
    except Error as e:
        print(f"Ocurrió el error '{e}'")
    return connection

def insert_gasto(fecha, monto, descripcion):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "INSERT INTO gasto (fecha_gasto, monto, descripcion) VALUES (%s, %s, %s)"
    values = (fecha, monto, descripcion)
    try:
        cursor.execute(query, values)
        connection.commit()
        return True
    except Error as e:
        print(f"Ocurrió el error '{e}'")
        return False
    finally:
        cursor.close()
        connection.close()

def get_gastos():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM gasto"
    try:
        cursor.execute(query)
        gastos = cursor.fetchall()
        return gastos
    except Error as e:
        print(f"Ocurrió el error '{e}'")
        return []
    finally:
        cursor.close()
        connection.close()

def get_gasto_by_id(id_gasto):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM gasto WHERE id_gasto = %s"
    try:
        cursor.execute(query, (id_gasto,))
        gasto = cursor.fetchone()
        return gasto
    except Error as e:
        print(f"Ocurrió el error '{e}'")
        return None
    finally:
        cursor.close()
        connection.close()

def update_gasto(id_gasto, fecha, monto, descripcion):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE gasto SET fecha_gasto = %s, monto = %s, descripcion = %s WHERE id_gasto = %s"
    values = (fecha, monto, descripcion, id_gasto)
    try:
        cursor.execute(query, values)
        connection.commit()
        return True
    except Error as e:
        print(f"Ocurrió el error '{e}'")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_gasto(id_gasto):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM gasto WHERE id_gasto = %s"
    try:
        cursor.execute(query, (id_gasto,))
        connection.commit()
        return True
    except Error as e:
        print(f"Ocurrió el error '{e}'")
        return False
    finally:
        cursor.close()
        connection.close()

@app_gasto.route('/')
def index():
    return render_template('index_gasto.html')

@app_gasto.route('/gastos')
def gastos():
    gastos = get_gastos()
    return render_template('gastos.html', gastos=gastos)

@app_gasto.route('/submit', methods=['POST'])
def submit():
    fecha = request.form['fecha']
    monto = request.form['monto']
    descripcion = request.form['descripcion']

    if not fecha or not monto or not descripcion:
        flash('Todos los campos son requeridos.')
        return redirect(url_for('index'))

    # Verificar que monto sea mayor a cero
    if float(monto) <= 0:
        flash('Monto debe ser mayor a cero.')
        return redirect(url_for('index'))

    # Verificar repetición de la misma letra
    if re.match(r'^(.)\1*$', descripcion):
        flash('Descripción no puede contener repetición de la misma letra.')
        return redirect(url_for('index'))

    # Verificar que descripción no contenga solo signos
    if re.match(r'^[!-/:-@[-`{-~]+$', descripcion):
        flash('Descripción no puede contener solo signos.')
        return redirect(url_for('index'))

    # Verificar que descripción no contenga signos
    if re.search(r'[!-/:-@[-`{-~]', descripcion):
        flash('Descripción no puede contener signos.')
        return redirect(url_for('index'))

    if insert_gasto(fecha, monto, descripcion):
        flash('Gasto insertado exitosamente.')
    else:
        flash('Error al insertar el gasto.')
    
    return redirect(url_for('index'))

@app_gasto.route('/edit/<int:id_gasto>', methods=['GET', 'POST'])
def edit(id_gasto):
    if request.method == 'POST':
        fecha = request.form['fecha']
        monto = request.form['monto']
        descripcion = request.form['descripcion']

        if not fecha or not monto or not descripcion:
            flash('Todos los campos son requeridos.')
            return redirect(url_for('edit', id_gasto=id_gasto))

        # Verificar que monto sea mayor a cero
        if float(monto) <= 0:
            flash('Monto debe ser mayor a cero.')
            return redirect(url_for('edit', id_gasto=id_gasto))

        # Verificar repetición de la misma letra
        if re.match(r'^(.)\1*$', descripcion):
            flash('Descripción no puede contener repetición de la misma letra.')
            return redirect(url_for('edit', id_gasto=id_gasto))

        # Verificar que descripción no contenga solo signos
        if re.match(r'^[!-/:-@[-`{-~]+$', descripcion):
            flash('Descripción no puede contener solo signos.')
            return redirect(url_for('edit', id_gasto=id_gasto))
        
        if re.match(r'^[j]+$', descripcion):
            flash('Dehshsh')
            return redirect(url_for('edit', id_gasto=id_gasto))

        # Verificar que descripción no contenga signos
        if re.search(r'[!-/:-@[-`{-~]', descripcion):
            flash('Descripción no puede contener signos.')
            return redirect(url_for('edit', id_gasto=id_gasto))

        if update_gasto(id_gasto, fecha, monto, descripcion):
            flash('Gasto actualizado exitosamente.')
        else:
            flash('Error al actualizar el gasto.')
        
        return redirect(url_for('gastos'))

    gasto = get_gasto_by_id(id_gasto)
    if gasto is None:
        flash('Gasto no encontrado.')
        return redirect(url_for('gastos'))
    return render_template('edit_gasto.html', gasto=gasto)

@app_gasto.route('/eliminar/<int:id_gasto>', methods=['GET', 'POST'])
def eliminar(id_gasto):
    if request.method == 'POST':
        if delete_gasto(id_gasto):
            flash('Gasto eliminado exitosamente.')
        else:
            flash('Error al eliminar el gasto.')
        return redirect(url_for('gastos'))

    gasto = get_gasto_by_id(id_gasto)
    if gasto is None:
        flash('Gasto no encontrado.')
        return redirect(url_for('gastos'))
    return render_template('eliminar_gasto.html', gasto=gasto)

if __name__ == '__main__':
    app_gasto.run(debug=True, port=5002)
