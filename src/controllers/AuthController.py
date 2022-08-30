from unicodedata import name
from app import*
import json
from app import render_template
from app import redirect 

@app.route('/login', methods=['GET', 'POST'])
def login(): #llamada de renderizacion en el formulario de login
    if request.method == "GET":
        if "user" in session:
            return redirect(url_for("index"))
        return render_template('login.html') #llamada de renderizacion en el formulario de login

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pass"]#validar la contraseña
        user = mongo.db.users.find_one({'email': email})

        if user:#permite validar si el usuario esta inactivo o activo
            if user['active']:
                if check_password_hash(user['password'], password):
                    session["user"] = json.loads(json_util.dumps(user))
                    return redirect(url_for('index'))
                else:#mensajes de validacion de contraseña
                    message = 'Contraseña incorrecta'
                    return render_template('login.html', message = message)
            else:#mensaje de validacion para el usuario inactivo
                message = 'Usuario inactivo'
                return render_template('login.html', message = message)
        else:
            message = 'Usuario no registrado'
            return render_template('login.html', message = message)

@app.route('/logout', methods=['GET'])
def logout():
    if "user" in session:
        session.pop("user", None)
        return redirect(url_for('login'))
    return redirect(url_for('index'))

@app.route('/login/student', methods=['GET'])
def studentLogin():
    if "student" in session:
        return redirect(url_for("indexStudent"))
    
    students = mongo.db.students.find()
    return render_template('pages/student/login.html', students = students)

@app.route('/login/student/<id>', methods=['GET'])#para ingresar al login del estudiante
def studentSession(id):
    if id:
        session["student"] = id
        return redirect(url_for('indexStudent'))
    else:
        return redirect(url_for('studentLogin'))

@app.route('/logout/student', methods=['GET'])#cerrar cesion de los estudientes
def studentLogout():
    if "student" in session:
        session.pop("student", None)
        return redirect(url_for('studentLogin'))
    return redirect(url_for('indexStudent'))