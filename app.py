from flask import Flask, render_template, redirect, request, url_for
from controllers import citizenHandler
from models import classes

handler = citizenHandler.CitizenHandler()
app = Flask(__name__)

@app.route('/')
def index():
    next_citizen = handler.show_next_citizen()
    return render_template('index.html', next_citizen=next_citizen)

@app.route('/add', methods=['POST'])
def add():
    cedula = request.form['cedula']
    nombre = request.form['nombre']
    tramite = request.form['tramite']
    hora = request.form['hora']
    citizen = classes.Citizen(cedula, nombre, tramite, hora)
    handler.add_citizen(citizen)
    return redirect(url_for('index'))

@app.route('/serve')
def serve():
    handler.serve_citizen()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
