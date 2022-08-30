from app import*
from controllers.ClassroomController import classroomsShow
import json
from app import mongo

# Index Students
@app.route('/students', methods=['GET'])
def studentsIndex(): #renderizacion de la pagina del estudiante 
    students = mongo.db.students.find() #inicializa los  datos tanto del curso y periodo
    classrooms = mongo.db.classrooms.find()
    periods = mongo.db.periods.find()
    return render_template('pages/administration/students/index.html', students = students, classrooms = classrooms, periods = periods)

# Show Student
@app.route('/students/<id>', methods=['GET'])
def studentsShow(id): #mostrar los datos y enviar a la base de datos coleccione students
    student = mongo.db.students.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(student)
    return Response(response, mimetype = "application/json")

# Store Students
@app.route('/students', methods=['POST'])
def studentsStore(): # registrar un estudiante por su nombre y apellido
    name = request.form['name'] 
    lastname = request.form['lastname']
    course = mongo.db.classrooms.find_one({'_id': ObjectId(request.form['course']), })
    period = mongo.db.periods.find_one({'_id': ObjectId(request.form['period']), })
   #sentencia 
    if request.files['photo']: #sentencia que permite elegir la foto para cada estudiete
        photo = request.files['photo']
        photo.save(PATH_FILE + photo.filename) # selecciona los fotos desde una carpeta almacenada
        photo_name = photo.filename
    else:
        photo_name = ''

    if name and lastname and course and period:
        course['note'] = 0
        course['attempts'] = 0

        mongo.db.students.insert_one({ #insertar los datos en mongo nombre, apellido, curso, foto y periodo
            'name': name,
            'lastname': lastname,
            'course': course,
            'photo': photo_name,
            'period': period
        })

    return redirect(url_for("studentsIndex"))

# Update Students
@app.route('/students/update/<_id>', methods=['POST'])
def studentsUpdate(_id):
    name = request.form['name']# tomaa los datos de el curso y periodp para presentar en la tabla
    lastname = request.form['lastname']
    course = mongo.db.classrooms.find_one({'_id': ObjectId(request.form['course']), })
    period = mongo.db.periods.find_one({'_id': ObjectId(request.form['period']), })

    if name and lastname and course and period and _id:
        student = mongo.db.students.find_one({'_id': ObjectId(_id), })
        course['note'] = int(student['course']['note'])
        course['attempts'] = int(student['course']['attempts'])

        if request.files['photo']:
            photo = request.files['photo']
            photo.save(PATH_FILE + photo.filename)
            photo_name = photo.filename
        else:
            photo_name = student['photo']
            #permite el actulizado de los datos ingresados para el estudiante
        mongo.db.students.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {
                'name': name,
                'lastname': lastname,
                'course': course,
                'photo': photo_name,
                'period': period
            }
        })
    return redirect(url_for("studentsIndex"))

# Delete Students
@app.route('/students/delete/<id>', methods=['POST'])
def studentsDestroy(id):
    mongo.db.students.delete_one({'_id': ObjectId(id)})
    return redirect(url_for("studentsIndex"))

# Notes
@app.route('/students/note/<_id>', methods=['POST'])
def studentNote(_id):
    student = mongo.db.students.find_one({'_id': ObjectId(_id)}) #asignar la nota de los estudietes por parte del docente
    course = mongo.db.classrooms.find_one({'_id': student['course']['_id'] })

    if request.form['note']:# sentencia que valida si el estudiente pertenece a un curso y tiene nota
        auxNote = request.form['note']
        if request.form['attempt'] == True: # sentencia que toma los datos de curso, nota del estudiante
            course['attempts'] = student['course']['attempts'] + 1
            note = (student['course']['note'] + auxNote) / course['attempts']
            course['note'] = note
        else:
            course['note'] = auxNote
            course['attempts'] = int(student['course']['attempts'])
    else:
        course['note'] = student['course']['note']
        course['attempts'] = student['course']['attempts']
    
    course['note'] = int(course['note'])
    course['attempts'] = int(course['attempts'])
    # guaradar la nota de los estudientes
    mongo.db.students.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
        {'$set': {
            'course': course
        }
    })

    return redirect(request.referrer)