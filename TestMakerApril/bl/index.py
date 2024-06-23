from flask import Blueprint, render_template, url_for, request, jsonify, session

from bl.PDFGenerator import PDFGenerator
from dao.databaseHandler import databaseHandler
from flask import make_response
import json
from bl.utilities import utilities

index_blueprint=Blueprint('index_blueprint',__name__)
@index_blueprint.route('/')
def index():
    return render_template('mainpage.html')


@index_blueprint.route('/generateclasses/<queryname>')
def generateclasses(queryname):
    result=utilities.fetchClasses(queryname)
    classes_and_ids= [(row[0], row[1]) for row in result]
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
    name = request.cookies.get('username')

    pdf=PDFGenerator(name)
    pdf.generate_pdf(selected_questions)
    print(selected_questions)
    return 'Checked questions: ' + ', '.join(selected_questions)


@index_blueprint.route('/create_section', methods=['POST'])
def create_section():
    # Extract selected questions from the POST request
    selected_questions = request.json.get('selected_questions')
    # Return a success response
    return jsonify({'status': 'success'}), 200

@index_blueprint.route('/addition')
def addition():
    return render_template('addition.html')

@index_blueprint.route('/get_classes', methods=['GET'])
def get_classes():
    queryname='fetchClasses'

    classes=utilities.fetchClasses(queryname)
    classes = [{'id': row[0], 'name': row[1]} for row in classes]
    return jsonify(classes)

@index_blueprint.route('/get_subject_question_types',methods=['GET'])
def get_subject_question_types():
    queryname='fetchQuestionTypes'
    result=utilities.fetcherWithoutId(queryname)
    subjectQuestionType = [{'id': row[0], 'name': row[1]} for row in result]
    return jsonify(subjectQuestionType)


@index_blueprint.route('/get_subjects/<int:classid>', methods=['GET'])
def get_subjects(classid):
    try:
        queryname='fetchSubjects'
        print("fetching subjects")
        subjects=utilities.fetchSubjects(queryname,classid)
        subjects = [{'id': row[0], 'name': row[1]} for row in subjects]
        return jsonify(subjects)
    except Exception as e:
        return jsonify({'status': 'failure', 'message': f"subject cant be fetched!!"})

@index_blueprint.route('/get_chapters/<int:subjectid>',methods=['GET'])
def get_chapters(subjectid):
    try:
        queryname='fetchChapters'
        print("fetching Chapters")
        chapters=utilities.fetchChapters(queryname,subjectid)
        chapters = [{'id': row[0], 'name': row[1]} for row in chapters]
        return jsonify(chapters)
    except Exception as e:
        return jsonify({'status': 'failure', 'message': f"subject cant be fetched!!"})

@index_blueprint.route('/add_subject', methods=['POST'])
def add_subject():
    try:
        class_selected = request.form['class']
        print(class_selected)
        subject_name = request.form['subject_name']
        question_types = request.form.getlist('subjectQuestionTypes[]')
        print(question_types)
        dbhandler=databaseHandler()
        dbhandler.inserter("insertSubject",subject_name,class_selected)
        # i have added the subject but to add the respective question type with it we need to fetch the id which is
        # auto generated so i need to fetch all subjects of a class and need to filter so that i can have subject_id
        try:
            queryname = 'fetchSubjects'
            print("fetching subjects to get the id so that question types for that subject can be inserted")
            subjects = utilities.fetchSubjects(queryname, class_selected)
            subject_id=0
            for subject in subjects:
                if subject[1]==subject_name:
                    subject_id=subject[0]
                    print(f'The recently added subject have subject id= "{subject_id}"')
                    break
        except Exception as e:
            print("An Exeption occure while fetching the subject id in route='add_subject'"+e)
        for qtype in question_types:
            dbhandler.inserter("insertSubjectQuestionTypes",subject_id,qtype)

        return jsonify({'status': 'success', 'message': f'Subject "{subject_name}" added to {class_selected}'})
    except Exception as e:
        return jsonify({'status': 'failure', 'message': f"Subject cant be added!!"})

@index_blueprint.route('/add_class',methods=['POST'])
def add_class():
    try:
        class_name = request.form['class_name']
        dbhandler=databaseHandler()
        dbhandler.inserter("insertClass",class_name)
        return jsonify({'status': 'success', 'message': f'Subject "{class_name}" added!!'})
    except Exception as e:
        return jsonify({'status': 'failure', 'message': f"class cant be added!!"})

@index_blueprint.route('/add_chapter', methods=['POST'])
def add_chapter():
    try:
        class_selected = request.form['class']
        subject_selected=request.form['subject']
        print(class_selected+","+subject_selected)
        chapter_no = request.form['chapter_no']

        chapter_name = request.form['chapter_name']
        dbhandler=databaseHandler()
        dbhandler.inserter("insertChapter",chapter_name,subject_selected,chapter_no)
        return jsonify({'status': 'success', 'message': f'chapter {chapter_name} added to {class_selected} {subject_selected}'})
    except Exception as e:
        return jsonify({'status': 'failure', 'message': f"Chapter cant be added!!"})

@index_blueprint.route('/add_question',methods=['POST'])
def add_question():
    try:
        class_selected = request.form['class']
        subject_selected = request.form['subject']
        chapter_selected=request.form['chapter']
        print("going to add question")
        question_desc = request.form['question_description']
        option_A = request.form['option_A']
        option_B = request.form['option_B']
        option_C = request.form['option_C']
        option_D = request.form['option_D']

        question_type = request.form['question_type']
        if question_type=="Short":
            question_type="S"
        elif question_type=="Long":
            question_type="L"
        elif question_type=="MCQS":
            question_type="M"

        if question_type=="M":
            dbhandler=databaseHandler()
            dbhandler.insertMcqs("insertMcqs",chapter_selected,question_desc,option_A,option_B,option_C,option_D)
            return jsonify({'status': 'success', 'message': f'MCQS added to {chapter_selected} '})
        else:
            dbhander=databaseHandler()
            dbhander.inserter("insertQuestion",question_desc,chapter_selected,question_type)
            return jsonify({'status': 'success', 'message': f'Question added to {chapter_selected} '})

    except Exception as e:
        return jsonify({'status': 'failure', 'message': f"Question cant be added!!"})
