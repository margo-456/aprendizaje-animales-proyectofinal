from app import*
from app import mongo
# Index classrooms

""" funciones de la pagina de index"""

@app.route('/classrooms', methods=['GET'])
def classroomsIndex(): 
    classrooms = mongo.db.classrooms.find()
    calendars = mongo.db.calendars.find()
    teachers = mongo.db.users.find({'role.role': 'teacher' }) # inicializa el usuario docete con las aulas asignadas
    return render_template('pages/classrooms/index.html', classrooms = classrooms, teachers = teachers, calendars = calendars)

# Show classrooms
@app.route('/classrooms/<id>', methods=['GET'])
def classroomsShow(id):
    classroom = mongo.db.classrooms.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(classroom)
    return Response(response, mimetype = "applicatns/json")

# Store classrooms
@app.route('/classrooms', methods=['POST'])
def classroomsStore():
    classroom = request.form['classroom']
    parallel = request.form['parallel']
    capacity = request.form['capacity']
    tutor = mongo.db.users.find_one({'_id': ObjectId(request.form['tutor']) })
    calendar = mongo.db.calendars.find_one({'_id': ObjectId(request.form['calendar']) })

    if classroom and parallel and capacity:
        mongo.db.classrooms.insert_one({
            'classroom': classroom,
            'parallel': parallel,
            'capacity': capacity,
            'tutor': tutor,
            'calendar': calendar
        })

    return redirect(url_for("classroomsIndex"))

# Update classrooms
@app.route('/classrooms/update/<_id>', methods=['POST'])
def classroomsUpdate(_id):
    classroom = request.form['classroom']
    parallel = request.form['parall']
    capacity = request.form['capacity']
    tutor = mongo.db.users.find_one({'_id': ObjectId(request.form['tutor']) })

    if classroom and parallel and capacity and _id:
        mongo.db.classrooms.update_one({'_id': ObjectId(_id['$oid']) if 'oid' in _id else ObjectId(_id)},
            {'$set': {
                'classroom': classroom,
                'parallel': parallel,
                'capacity': capacity,
                'tutor': tutor
            }
        })
    return redirect(url_for("classroomsIndex"))

# Delete classrooms
@app.route('/classrooms/delete/<id>', methods=['POST'])
def classroomsDestroy(id):
    mongo.db.classrooms.delete_one({'_id': ObjectId(id)})
    return redirect(url_for("classroomsIndex"))