from flask import Blueprint, render_template, url_for, request, jsonify, session
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
    # you can make columns specified in select statement if you dont want to do this.
    classes_and_ids = [(row[0], row[1]) for row in result]
    #passing query name to recognize in html pages
    resp=make_response(render_template("generateChapters.html",idsandname=classes_and_ids,query=queryname))
    resp.set_cookie("subject",name)
    print(request.cookies.get('subject'))
    return resp

@index_blueprint.route('/generatequestion/<queryname>',methods=['GET','POST'])
def generatequestion(queryname):
    #getting the list from form and concatenate "," to work with sql query.
    question_type = str(request.form.get('question_type'))
    selected_chapters=request.form.getlist('selected_chapters[]')
    #storing chapter ids in session for querying again when switching from short->long->mcqs
    session['selected_chapter_ids'] = selected_chapters

    if(question_type=="short"):
        question_type="S"
    elif(question_type=="long"):
        question_type="L"
    else:
        question_type="M"
    print (question_type)
    questions=""
    if(selected_chapters):
        dbhandler=databaseHandler()
        result=dbhandler.getterWithId(queryname,selected_chapters,question_type)
        questions=[row[1] for row in result]
    clas=request.cookies.get('class')
    subject=request.cookies.get('subject')
    return render_template("generatequestions.html",questions=questions,clas=clas,subject=subject,type=question_type)


# @index_blueprint.route('/submitChapter/queryname',methods=['GET','POST'])
# def submitChapter(queryname):
#     dbhandler=databaseHandler()
#     result=dbhandler.getterWithId(queryname,selected_chapters)
#     return selected_chapters
@index_blueprint.route('/switchQuestionType/<type>')
def switchQuestionType(type):
    if (type == "short"):
        type = "S"
    elif (type == "long"):
        type = "L"
    else:
        type = "M"
    dbhandler = databaseHandler()
    chapter_ids=session.get('selected_chapter_ids')
    result=dbhandler.getterWithId('fetchQuestions',chapter_ids,type)
    questions = [row[1] for row in result]
    clas = request.cookies.get('class')
    subject = request.cookies.get('subject')
    return render_template("generatequestions.html", questions=questions, clas=clas, subject=subject,type=type)


@index_blueprint.route('/submitquestion',methods=['GET','POST'])
def submitquestion():
    selected_questions = request.form.getlist('selected_questions[]')
    # Process the checked questions as needed
    print(selected_questions)
    return 'Checked questions: ' + ', '.join(selected_questions)


@index_blueprint.route('/create_section', methods=['POST'])
def create_section():
    # Extract selected questions from the POST request
    selected_questions = request.json.get('selected_questions')
    # Return a success response
    return jsonify({'status': 'success'}), 200