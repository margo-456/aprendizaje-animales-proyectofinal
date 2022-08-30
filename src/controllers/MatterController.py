from app import*
from app import render_template
# Index matters
@app.route('/matters', methods=['GET'])
def mattersIndex():
    matters = mongo.db.matters.find() # iniciaizar el valor para enviar los datos de las materias
    classrooms = mongo.db.classrooms.find()# inicializar los datos para enviar los datos del aula
    return render_template('pages/matters/index.html', matters = matters, classrooms = classrooms)

# Show matter
@app.route('/matters/<id>', methods=['GET'])
def mattersShow(id): #obtenemos los datos para poder guardar los datos mongo
    matter = mongo.db.matters.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(matter)
    return Response(response, mimetype="application/json")

# Store matter
@app.route('/matters', methods=['POST'])
def mattersStore():
    name = request.form['name']
    classroom = mongo.db.classrooms.find_one({'_id': ObjectId(request.form['classroom']) })

    if name and classroom: #sentencia que permite validar un curso y materia 
        mongo.db.matters.insert_one({
            'name': name,
            'classroom': classroom # nombre de la materia y el aula
        })

    return redirect(url_for("mattersIndex"))

# Update matter
@app.route('/matters/update/<_id>', methods=['POST'])
def mattersUpdate(_id):
    name = request.form['name']
    classroom = mongo.db.classrooms.find_one({'_id': ObjectId(request.form['classroom']) })

    if name and classroom: #sentencia que permite eliminar los adatos ingresados
        mongo.db.matters.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {
                'name': name,
                'classroom': classroom
            }
        })
    return redirect(url_for("mattersIndex"))

# Delete matter
@app.route('/matters/delete/<id>', methods=['POST'])# permite las acciones de poder eliminar las materias
def mattersDestroy(id):
    mongo.db.matters.delete_one({'_id': ObjectId(id)})
    return redirect(url_for("mattersIndex"))