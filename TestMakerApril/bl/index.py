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
    if(queryname=="..."):
        return"its a traiTOR"
    result=dbhandler.getter(queryname)
    #classes=[row[1]for row in result]
    classes_and_ids = [(row[0], row[1]) for row in result]

    serilized_Data=json.dumps(classes_and_ids)
    response=make_response(render_template("generateClasses.html",idsandname=classes_and_ids))
    response.set_cookie("class", '', expires=0)
    response.set_cookie("subject", '', expires=0)
    response.set_cookie("chapter", '', expires=0)

    #response.set_cookie('class',serilized_Data)
    return response

@index_blueprint.route('/generatesubject/<queryname>/<id>/<name>')
def generatesubject(queryname,id,name):
    dbhandler = databaseHandler()
    result=dbhandler.getterWithId(queryname,id)
    classes_and_ids = [(row[0], row[1]) for row in result]
    #passing query name to recognize in html pages
    resp=make_response(render_template("generateSubjects.html",idsandname=classes_and_ids,query=queryname))
    resp.set_cookie("class",name)
    print(request.cookies.get('class'))
    return resp

@index_blueprint.route('/generatechapter/<queryname>/<id>/<name>')
def generatechapter(queryname,id,name):
    dbhandler = databaseHandler()
    result=dbhandler.getterWithId(queryname,id)
    classes_and_ids = [(row[0], row[1]) for row in result]
    #passing query name to recognize in html pages
    resp=make_response(render_template("generateChapters.html",idsandname=classes_and_ids,query=queryname))
    resp.set_cookie("subject",name)
    print(request.cookies.get('subject'))
    return resp

@index_blueprint.route('/generatequestion/<queryname>',methods=['GET','POST'])
def generatequestion(queryname):
    #getting the list from form and concatenate "," to work with sql query.
    selected_chapters=request.form.getlist('selected_chapters[]')
    selected_chapters = selected_chapters[0].split(',')

    #selected_chapters = ",".join(str(chapter_id) for chapter_id in selected_chapters)
    #after that selected_chapters will look like this:1,2,3,4

    dbhandler=databaseHandler()
    result=dbhandler.getterWithId(queryname,selected_chapters,"S")
    questions=[row[1] for row in result]
    clas=request.cookies.get('class')
    subject=request.cookies.get('subject')
    return render_template("generatequestions.html",questions=questions,clas=clas,subject=subject,type="Short")


# @index_blueprint.route('/submitChapter/queryname',methods=['GET','POST'])
# def submitChapter(queryname):
#     dbhandler=databaseHandler()
#     result=dbhandler.getterWithId(queryname,selected_chapters)
#     return selected_chapters

@index_blueprint.route('/submitquestion',methods=['GET','POST'])
def submitquestion():
    selected_questions = request.form.getlist('selected_questions[]')
    # Process the checked questions as needed
    print(selected_questions)
    return 'Checked questions: ' + ', '.join(selected_questions)