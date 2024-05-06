class databaseQueryHandler:
    insertChapter="INSERT INTO `test_maker`.`chapter` (`chap_name`, `subject_id`, `chapter_number`) VALUES (%s,%s,%s);"
    insertQuestion=""
    insertTranslation=""
    insertTest=""
    insertSubject="INSERT INTO `test_maker`.`subject` (`subject_name`, `class_id`) VALUES (%s,%s);"
    insertClass="""INSERT INTO `test_maker`.`class` (`class_name`) VALUES (%s);"""
    insertLanguage=""
    insertUser="""INSERT INTO `test_maker`.`user` (`user_name`, `password`, `institute_name`, `institute_Address`, `is_allowed_to_make_changes`) VALUES (%s,%s,%s,%s,%s);"""

    fetchUsers="SELECT * FROM `test_maker`.`user`;"
    fetchClasses="SELECT * FROM `test_maker`.`class`;"

    fetchSubjects="SELECT * FROM `test_maker`.`subject` WHERE `class_id`=%s;"
    fetchChapters = "SELECT * FROM `test_maker`.`chapter` WHERE `subject_id`=%s;"
    fetchQuestions="SELECT * FROM `test_maker`.`question` WHERE `chapter_id` IN (%s) and `question_type`=%s;"
    updateQuestion = ""
    updateTranslation = ""
    updateTest = ""
    updateSubject = ""
    updateClass = ""
    updateLanguage=""

