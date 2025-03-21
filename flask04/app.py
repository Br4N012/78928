from flask import Flask, redirect, render_template, request, Response, url_for
from producto import Producto

app = Flask(__name__)

productos = [Producto("Computadora", 200), Producto("Impresora", 500)]

@app.route('/')
def index():
    print("Productos en la lista:", productos)  # Depuración
    return render_template('productos.html', productos=productos)

@app.route('/editar/<producto>/<precio>')
def editar(producto, precio):
    print(f"Producto: {producto}, Precio: {precio}")
    return render_template('editar.html', producto=producto, precio=precio)


@app.route('/eliminar/<nombre>')
def eliminar(nombre):
    # Buscar y eliminar el producto de la lista
    i= 0
    for e in productos:
        if e.nombre == nombre:
            productos.pop(i)    
            print(f"{e.nombre}{e.precio}")
        i += 1
    return Response("eliminado", headers={'Location': '/'}, status=302)
    #global productos
    #productos = [p for p in productos if p.nombre != producto]
    #print(f"Producto eliminado: {producto}")

@app.route('/crear/<nombre>/<precio>', methods=['POST'])
def crear():
    n = request.form.get('nombre')
    p = request.form.get('precio')
    productos.append(Producto(n,p))
    return redirect(url_for('index'))
   
    

@app.route('/guardar', methods=['POST'])
def guardar():
    n = request.form.get('nombre')
    p = request.form.get('precio')
    print(n, p)
    i = 0
    for e in productos:
        if e.nombre == n:
            productos[i] = Producto(n, p)
            print(f"{e.nombre}{e.precio}")
        i += 1
    return Response("guardado", headers={'Location': '/'}, status=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)