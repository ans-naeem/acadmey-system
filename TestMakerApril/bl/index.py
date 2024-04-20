from flask import Blueprint,render_template,url_for
from dao.databaseHandler import databaseHandler

index_blueprint=Blueprint('index_blueprint',__name__)
@index_blueprint.route('/')
def index():
    return render_template('mainpage.html')


@index_blueprint.route('/generateclasses/<queryname>')
def generateclasses(queryname):
    dbhandler = databaseHandler()
    result=dbhandler.getter(queryname)
    classes=[row[1]for row in result]
    return render_template("generation.html",subjects=classes)


