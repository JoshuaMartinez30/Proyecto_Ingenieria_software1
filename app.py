from flask import Flask, render_template, request, redirect, url_for, flash
#import tkinter as tk
#from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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

def insert_user(nombre, categoria, precio):
    connection = create_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    query = "INSERT INTO producto (nombre, categoria, precio) VALUES (%s, %s, %s)"
    values = (nombre, categoria, precio)
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
    #try:
    #    cursor.execute(query, values)
    #    connection.commit()
    #    messagebox.showinfo("Success", "User inserted successfully")
    #except Error as e:
    #    messagebox.showerror("Error", f"The error '{e}' occurred")
    #finally:
    #    cursor.close()
    #    connection.close()
def get_producto():
    connection = create_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    query = "SELECT * FROM producto"
    try:
        cursor.execute(query)
        producto = cursor.fetchall()
        return producto
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()

def get_producto_by_id(Id_producto):
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    query = "SELECT * FROM producto WHERE Id_producto = %s"
    try:
        cursor.execute(query, (Id_producto,))
        producto = cursor.fetchone()
        return producto
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()
        connection.close()

def update_user(Id_producto, nombre, categoria, precio):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "UPDATE producto SET nombre = %s, categoria = %s, precio = %s WHERE Id_producto = %s"
    values = (nombre, categoria, precio, Id_producto)
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

def delete_user(Id_producto):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = "DELETE FROM producto WHERE Id_producto = %s"
    try:
        cursor.execute(query, (Id_producto,))
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
    query = "SELECT * FROM producto WHERE nombre LIKE %s OR categoria LIKE %s OR precio LIKE %s"
    values = (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
    try:
        cursor.execute(query, values)
        producto = cursor.fetchall()
        return producto
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
        connection.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/producto')
def producto():
    #producto = get_producto()
    #return render_template('producto.html', producto = producto)
    search_query = request.args.get('search')
    if search_query:
        producto = search_users(search_query)
    else:
        producto = get_producto()
    return render_template('producto.html', producto = producto, search_query=search_query)

@app.route('/submit', methods=['POST'])
def submit():

    nombre = request.form['nombre']
    categoria = request.form['categoria']
    precio = request.form['precio']

    if not nombre or not categoria or not precio:
        flash('All fields are required!')
        return redirect(url_for('index'))

    #try:
    #    age = int(age)
    #except ValueError:
    #    flash('Age must be an integer!')
    #    return redirect(url_for('index'))

    if insert_user(nombre, categoria, precio):
        flash('Insertado exitosamente!')
    else:
        flash('Error al insertar.')
    
    return redirect(url_for('index'))

@app.route('/edit/<int:Id_producto>', methods=['GET', 'POST'])
def edit(Id_producto):
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']

        if not nombre or not categoria or not precio:
            flash('Se necesitan todos los campos!')
            return redirect(url_for('editar', Id_producto=Id_producto))

        #try:
        #    age = int(age)
        #except ValueError:
        #    flash('Age must be an integer!')
        #    return redirect(url_for('edit_user', user_id=user_id))

        if update_user(Id_producto, nombre, categoria, precio):
            flash('Actualizado exitosamente!')
        else:
            flash('Ocurrio un error al actualizar.')
        
        return redirect(url_for('producto'))

    producto = get_producto_by_id(Id_producto)
    if producto is None:
        flash('No encontrado')
        return redirect(url_for('producto'))
    return render_template('edit.html', producto=producto)

@app.route('/eliminar/<int:Id_producto>', methods=['GET', 'POST'])
def eliminar(Id_producto):
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']

        if not nombre or not categoria or not precio:
            flash('Se requieren todos los campos!')
            return redirect(url_for('eliminar', Id_producto=Id_producto))
        if delete_user(Id_producto):
            flash('Eliminado exitosamente!')
        else:
            flash('Error al eliminar .')
        return redirect(url_for('producto'))

    producto = get_producto_by_id(Id_producto)
    if producto is None:
        flash('No encontrado!')
        return redirect(url_for('producto'))
    return render_template('eliminar.html', producto=producto)



if __name__ == '__main__':
    app.run(debug=True)

#def submit():
#    nombre = nombre_entry.get()
#    categoria = categoria_entry.get()
#    precio = precio_entry.get()

#    if not nombre or not categoria or not precio:
#        messagebox.showwarning("Input Error", "All fields are required")
#        return

#    insert_user(nombre, categoria, precio)

#app = tk.Tk()
#app.title("User Data Entry")

#tk.Label(app, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
#nombre_entry = tk.Entry(app)
#nombre_entry.grid(row=0, column=1, padx=10, pady=10)

#tk.Label(app, text="Categoria:").grid(row=1, column=0, padx=10, pady=10)
#categoria_entry = tk.Entry(app)
#categoria_entry.grid(row=1, column=1, padx=10, pady=10)

#tk.Label(app, text="Precio:").grid(row=2, column=0, padx=10, pady=10)
#precio_entry = tk.Entry(app)
#precio_entry.grid(row=2, column=1, padx=10, pady=10)

#submit_button = tk.Button(app, text="Submit", command=submit)
#submit_button.grid(row=4, columnspan=2, pady=20)

#app.mainloop()