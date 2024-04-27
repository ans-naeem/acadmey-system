from flask import Blueprint, render_template, url_for, request
from dao.databaseHandler import databaseHandler
from flask import make_response
import json
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

    serilized_Data=json.dumps(classes_and_ids)
    response=make_response(render_template("generation.html",idsandname=classes_and_ids))
    response.set_cookie('class', '', expires=0)
    response.set_cookie('subject', '', expires=0)
    response.set_cookie('chapter', '', expires=0)

    #response.set_cookie('class',serilized_Data)
    return response

@index_blueprint.route('/generatetable/<queryname>/<id>/<name>')
def generatetable(queryname,id,name):
    dbhandler = databaseHandler()
    result=dbhandler.getterWithId(queryname,id)
    classes_and_ids = [(row[0], row[1]) for row in result]
    #passing query name to recognize in html pages
    resp=make_response(render_template("dynamicgeneration.html",idsandname=classes_and_ids,query=queryname))
    if("subject" in queryname.lower()):
        resp.set_cookie('class',name)
        print("there exist a subject in queryname")
        print(request.cookies.get('class'))

    if("chapter" in queryname.lower()):
        resp.set_cookie('subject',name)
        print("there exist a chapter in queryname")
        print(request.cookies.get('subject'))






    #data=[row[1] for row in result]
    # if(request.cookies.get('subject')):
    #     resp.set_cookie('chapter', json.dumps(name))
    # else:
    #     resp.set_cookie('subject',json.dumps(name))
    # if(request.cookies.get('class')!=None and request.cookies.get('subject')!=None):
    #     resp.set_cookie('chapter',name)
    #     print("chapter: ")
    #
    #     print(request.cookies.get('chapter'))
    # elif(request.cookies.get('class')!=None):
    #     resp.set_cookie('subject',name)
    #     print("subject: ")
    #
    #     print(request.cookies.get('subject'))
    # else:
    #     print("class: ")
    #
    #
    #

    return resp



@index_blueprint.route('/generatequestion/<queryname>/<id>/<type>')
def generatequestion(queryname,id,type):
    dbhandler=databaseHandler()
    result=dbhandler.getterWithId(queryname,id,type)
    questions=[row[1] for row in result]
    return render_template("generatequestions.html",questions=questions)




