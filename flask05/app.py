from flask import Flask, redirect, render_template, request, Response, url_for
from producto import Producto
import sqlite3


app = Flask(__name__)

#productos = [Producto("Computadora", 200), Producto("Impresora", 500)]

@app.route('/')
def index():
    con=conexion()
    productos = con.execute('SELECT * FROM productos').fetchall()
    print("Productos en la lista:", productos)  # Depuración
    con.close()
    return render_template('productos.html', productos=productos)

#@app.route('/editar/<producto>/<precio>')
@app.route('/editar/<id>')
#def editar(producto, precio):
def editar(id):
    con=conexion()
    p=con.execute('select *from productos where id = ? ',(id)).fetchone()
    con.close()

    #print(f"Producto: {producto}, Precio: {precio}")
    return render_template('editar.html', producto=p)


@app.route('/eliminar/<id>')
def eliminar(id):
    con = conexion()
    con.execute('DELETE FROM productos WHERE id = ?', (id,))
    con.commit()
    con.close()
    # Buscar y eliminar el producto de la lista
    #i= 0
    #for e in productos:
     #   if e.nombre == nombre:
      #      productos.pop(i)    
       #     print(f"{e.nombre}{e.precio}")
        #i += 1
    return Response("eliminado", headers={'Location': '/'}, status=302)
    

@app.route('/crear', methods=['POST'])
def crear():
    n = request.form.get('nombre')
    p = request.form.get('precio')
    #productos.append(Producto(n,p))
    con=conexion()
    con.execute('INSERT INTO productos(nombre, precio) VALUES (?,?)',(n,p))
    con.commit()
    con.close()
    return redirect(url_for('index'))


def conexion():
    con = sqlite3.connect('basededatos.db')
    #row factory
    #hace que las consultas se vuelvan diccionarios pudiendo seleccionar valores mediante
    #[nombre_columna]
    con.row_factory = sqlite3.Row
    return con

def iniciar_db():
    con=conexion()
    #se crea la tabla en caso de que no exista
    con.execute('''CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL
    )
''')
    con.commit()#Salva los datos despues de la ejecucion
    con.close() 

   
    

@app.route('/guardar', methods=['POST'])
def guardar():
    n = request.form.get('nombre')
    p = request.form.get('precio')
    id = request.form.get('id')
    print(f"{n} {p} {id}")
    con=conexion()
    con.execute('UPDATE productos SET nombre = ?, precio = ? WHERE id = ?',(n,p,id))
    con.commit()
    con.close()
   # print(n, p)
   # i = 0
   # for e in productos:
    #    if e.nombre == n:
     #       productos[i] = Producto(n, p)
      #      print(f"{e.nombre}{e.precio}")
       # i += 1
    return Response("guardado", headers={'Location': '/'}, status=302)

if __name__ == '__main__':
    #Arrancamos e inicializamos la base de datos
    iniciar_db()
    app.run(host='0.0.0.0', debug=True)