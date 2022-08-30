from flask import Flask, Response, request, session, jsonify, render_template, url_for, redirect, send_from_directory
from importlib.resources import path
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from os import getcwd

PATH_FILE = getcwd() + '/sr/files/'

app = Flask(__name__)
app.secret_key = 'development'
app.config['MONGO_URI'] = 'mongodb://localhost/JOHANASALAZAR'
mongo = PyMongo(app)

@app.errorhandler(404)
def not_found(error=None):
    return render_template('404.html')
    
@app.errorhandler(500)
def not_found(error=None):
    return render_template('500.html')

@app.get('/file/<string:file_name>')
def get_file(file_name):
    return send_from_directory(PATH_FILE, path = file_name, as_attachment=False)

from controllers.AuthController import *
from controllers.HomeController import *
from controllers.UserController import *
from controllers.TeacherController import *
from controllers.StudentController import *
from controllers.RoleController import *
from controllers.PermissionController import *
from controllers.ClassroomController import *
from controllers.MatterController import *
from controllers.CalendarController import *
from controllers.PeriodController import *
from controllers.QualifyController import *

if __name__ == "__main__":
    app.run(debug=True)