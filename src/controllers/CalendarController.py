from app import*

# Index calendars
@app.route('/calendars', methods=['GET'])
def calendarsIndex(): #para mostrar los datos de los calendarios academicos
    calendars = mongo.db.calendars.find()
    return render_template('pages/calendars/index.html', calendars = calendars)

# Show calendar
@app.route('/calendars/<id>', methods=['GET'])
def calendarsShow(id): #obtener los datos para enviar a la base de datos
    calendar = mongo.db.calendars.find_one({'_id': ObjectId(id), }) 
    response = json_util.dumps(calendar)
    return Response(response, mimetype="application/json")

# Store calendar
@app.route('/calendars', methods=['POST'])
def calendarsStore():
    name = request.form['name']
    start_at = request.form['start_at']
    end_at = request.form['end_at']

    if name and start_at and end_at:
        mongo.db.calendars.insert_one({
            'name': name,
            'start_at': start_at,
            'end_at': end_at
        })

    return redirect(url_for("calendarsIndex"))

# Update calendar
@app.route('/calendars/update/<_id>', methods=['POST'])
def calendarsUpdate(_id):
    name = request.form['name']
    start_at = request.form['start_at']
    end_at = request.form['end_at']

    if name and start_at and end_at and _id:
        mongo.db.calendars.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {
                'name': name,
                'start_at': start_at,
                'end_at': end_at
            }
        })
    return redirect(url_for("calendarsIndex"))

# Delete calendar
@app.route('/calendars/delete/<id>', methods=['POST'])
def calendarsDestroy(id):
    mongo.db.calendars.delete_one({'_id': ObjectId(id)})
    return redirect(url_for("calendarsIndex"))