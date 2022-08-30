from app import*

# Index users
#funciones para guardar los datos de los usuarios con roles y permisos
@app.route('/users', methods=['GET'])
def usersIndex():
    users = mongo.db.users.find() #funcion de usuarios
    permissions = mongo.db.permissions.find() #funcion de los permisos
    roles = mongo.db.roles.find() #funcion de los roles
    return render_template('pages/users/index.html', users = users, roles = roles, permissions = permissions)

# Show user
@app.route('/users/<id>', methods=['GET'])
def usersShow(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id), })#funcion que permite obtener el id de cada elemento
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")#guarda los datos en un archivo json de mongodb

# Store user
""" funcion que permite tomar los datos que seran enviados a traves del metodo POST"""
@app.route('/users', methods=['POST'])
def usersStore(): 
    name = request.form['name']# traer los datos al formulario en este caso nombre
    lastname = request.form['lastname'] #traer los datos al formulario en este caso apellido
    username = request.form['username'] #traer los datos al formulario en este caso usuario
    email = request.form['email']#traer los datos al formulario en este caso nombre email
    password = request.form['password']  #traer los datos al formulario en este caso clave
    role = mongo.db.roles.find_one({'_id': ObjectId(request.form['role']), }) #guardado de datos en la coleccion role

    if name and lastname and username and email and password:

        """funcion para insertar los datos al momgoDB tomando los campos necesarios"""
        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({ #insertar datos a la base de datos
            'name': name,
            'lastname': lastname,
            'username': username,
            'email': email,
            'password': hashed_password,
            'role': role,
            'active': True,
        })

    return redirect(url_for("usersIndex"))

# Update user
@app.route('/users/update/<_id>', methods=['POST']) # actualizar los datos enviados y mostrar en el formulario y enviar 
def usersUpdate(_id):
    name = request.form['name']
    lastname = request.form['lastname']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    role = mongo.db.roles.find_one({'_id': ObjectId(request.form['role']), })#agregar datos al formulario

    if name and lastname and username and email and _id:
        if password:
            hashed_password = generate_password_hash(password) #generar una contraseña encriptada 
        else:
            user = mongo.db.users.find_one({'_id': ObjectId(_id) })
            hashed_password = user['password']

        mongo.db.users.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, # guardar los datos
            {'$set': { #los datos que se alcenan en mongo db
                'name': name, 
                'lastname': lastname,
                'username': username,
                'email': email,
                'password': hashed_password,
                'role': role,
                'active': user['active'],
            }
        })
    return redirect(url_for("usersIndex")) #para mostrar los dotos del formulario

# Delete user
@app.route('/users/delete/<id>', methods=['POST'])
def usersDestroy(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)}) #elimimar un registro mediante delete
    return redirect(url_for("usersIndex"))

# Disable user
@app.route('/users/disable/<_id>', methods=['POST'])#ruta para la pagina de los usuarios 
def usersDisable(_id):
    if _id:
        mongo.db.users.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {
                'active': False,
            }
        })
    return redirect(url_for("usersIndex"))#redireccionamiento a lo

# Enable user
@app.route('/users/enable/<_id>', methods=['GET'])
def usersEnable(_id):
    if _id:
        mongo.db.users.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {
                'active': True,
            }
        })
    return redirect(url_for("usersIndex"))