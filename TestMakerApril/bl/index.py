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
    #classes=[row[1]for row in result]
    classes_and_ids = [(row[0], row[1]) for row in result]

    return render_template("generation.html",idsandname=classes_and_ids)

@index_blueprint.route('/generatetable/<queryname>/<id>')
def generatetable(queryname,id):
    dbhandler = databaseHandler()
    result=dbhandler.getterWithId(queryname,id)
    classes_and_ids = [(row[0], row[1]) for row in result]

    #data=[row[1] for row in result]
    return render_template("dynamicgeneration.html",idsandname=classes_and_ids,query=queryname)




