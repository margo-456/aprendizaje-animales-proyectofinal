from app import*
from app import mongo
from app import render_template
# Index permissions
@app.route('/permissions', methods=['GET'])
def permissionsIndex():
    permissions = mongo.db.permissions.find()
    return render_template('pages/authorization/permissions/index.html', permissions = permissions)

# Show permissions
@app.route('/permissions/<id>', methods=['GET'])
def permissionsShow(id):
    permission = mongo.db.permissions.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(permission)
    return Response(response, mimetype = "application/json")

# Store permissions
@app.route('/permissions', methods=['POST'])
def permissionsStore():
    permission = request.form['permission']
    alias = request.form['alias']

    if permission and alias:
        mongo.db.permissions.insert_one({
            'permission': permission,
            'alias': alias
        })

    return redirect(url_for("permissionsIndex"))

# Update permissions
@app.route('/permissions/update/<_id>', methods=['POST'])
def permissionsUpdate(_id):
    permission = request.form['permission']
    alias = request.form['alias']

    if permission and alias and _id:
        mongo.db.permissions.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {
                'permission': permission,
                'alias': alias
            }
        })
    return redirect(url_for("permissionsIndex"))

# Delete permissions
@app.route('/permissions/delete/<id>', methods=['POST'])
def permissionsDestroy(id):
    mongo.db.permissions.delete_one({'_id': ObjectId(id)})
    return redirect(url_for("permissionsIndex"))