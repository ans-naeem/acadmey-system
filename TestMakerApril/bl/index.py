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
    response.set_cookie("class", '', expires=0)
    response.set_cookie("subject", '', expires=0)
    response.set_cookie("chapter", '', expires=0)

    #response.set_cookie('class',serilized_Data)
    return response

@index_blueprint.route('/generatetable/<queryname>/<id>/<name>')
def generatetable(queryname,id,name):
    dbhandler = databaseHandler()
    result=dbhandler.getterWithId(queryname,id)
    classes_and_ids = [(row[0], row[1]) for row in result]
    #passing query name to recognize in html pages
    resp=make_response(render_template("dynamicgeneration.html",idsandname=classes_and_ids,query=queryname))
    print(type(name))
    # name=name.replace(" ","")
    name=name.strip()

    if("subject" in queryname.lower()):
        resp.set_cookie("class",name)
        print("there exist a subject in queryname")
        print(request.cookies.get('class'))

    if("chapter" in queryname.lower()):
        resp.set_cookie("subject",name)
        print("there exist a chapter in queryname")
        print(request.cookies.get('subject'))

    return resp



@index_blueprint.route('/generatequestion/<queryname>/<id>/<type>')
def generatequestion(queryname,id,type):
    dbhandler=databaseHandler()
    result=dbhandler.getterWithId(queryname,id,type)
    questions=[row[1] for row in result]
    clas=request.cookies.get('class')
    subject=request.cookies.get('subject')
    print(clas)
    print(request.cookies.get('subject'))
    return render_template("generatequestions.html",questions=questions,clas=clas,subject=subject,type="Long" if type=='L' else "Short")



@index_blueprint.route('/submitquestion',methods=['GET','POST'])
def submitquestion():
    selected_questions = request.form.getlist('selected_questions[]')
    # Process the checked questions as needed
    print(selected_questions)
    return 'Checked questions: ' + ', '.join(selected_questions)