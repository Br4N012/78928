from flask import flask, render_template
from modelos import Producto

app=flask(__name__)

@app.route('/')
def inicio():
    productos =[Producto["Manzanas",12],Producto["Pera",11]]
    return render_template('index.html', xxx=productos)

if __name__ =='__main__':
app.run(host='0.0.0.0', debug=True)