from app import*
from app import render_template
from app import mongo 
from app import request

# Index Roles
@app.route('/roles', methods=['GET'])
def rolesIndex():
    roles = mongo.db.roles.find()
    return render_template('pages/authorization/roles/index.html', roles = roles)

# Show Roles
@app.route('/roles/<id>', methods=['GET'])
def rolesShow(id): #permite asiganar los roles de los usuarios
    role = mongo.db.roles.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(role)
    return Response(response, mimetype = "application/json")

# Store Roles
@app.route('/roles', methods=['POST'])
def rolesStore(): #agregar los datos de los roles
    role = request.form['role']
    alias = request.form['alias']

    if role and alias:
        mongo.db.roles.insert_one({
            'role': role,
            'alias': alias
        })

    return redirect(url_for("rolesIndex"))

# Update Roles
@app.route('/roles/update/<_id>', methods=['POST'])
def rolesUpdate(_id):#funcion que permite guardar los datos ingresados
    role = request.form['role']
    alias = request.form['alias']

    if role and alias and _id:
        mongo.db.roles.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {
                'role': role,
                'alias': alias
            }
        })
    return redirect(url_for("rolesIndex"))

# Delete Roles
@app.route('/roles/delete/<id>', methods=['POST'])
def rolesDestroy(id):
    mongo.db.roles.delete_one({'_id': ObjectId(id)})
    return redirect(url_for("rolesIndex"))