from itertools import count
from app import*
import json

@app.route('/', methods=['GET'])
def index():
    if "user" in session:
        if session['user']['role']['role'] == 'admin': #metodo controlador del inicio para la pagina de administrador
            classrooms = mongo.db.classrooms.find() #para acceder al menu de classroom
            nUsers = mongo.db.users.count_documents({}) # para acceder al menu del usuario
            nStudets = mongo.db.students.count_documents({}) #para acceder al menu de estudiantes
            nCalendars = mongo.db.calendars.count_documents({}) # para acceder al menu de calendarios
            nClassrooms = mongo.db.classrooms.count_documents({}) # para acceder al menu del las aulas
            return render_template('index.html', classrooms = classrooms, nUsers = nUsers, nStudets = nStudets, nCalendars = nCalendars, nClassrooms = nClassrooms)
        if session['user']['role']['role'] == 'teacher':
            classrooms = mongo.db.classrooms.find({ 'tutor._id': ObjectId(session['user']['id']['oid']) })
            return render_template('pages/home/teacher/index.html', classrooms = classrooms)
    else:
        return redirect(url_for("login"))

@app.route('/student', methods=['GET']) #iniciar sesion en la pagina de los estudiantes
def indexStudent():
    if "student" in session:
        return render_template('pages/student/game.html')# renderizacion a la pagina del juego
    else:
        return redirect(url_for("studentLogin"))

# Index users
@app.route('/game', methods=['GET'])
def game():
    return render_template('pages/student/gam.html')

# Course
@app.route('/course/<id>', methods=['GET'])
def course(id):
    classroom = mongo.db.classrooms.find_one({'id': ObjectId(id), }) #los objetos de curso para guardar los datos en mongo
    students = mongo.db.students.find({'course.id': ObjectId(id), })# los objetos de los estudieantes para guardar los datos en mongo
    return render_template('pages/teachr/course.html', students = students, classroom = classroom)