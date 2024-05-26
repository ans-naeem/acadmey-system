from dao.databaseHandler import databaseHandler

class utilities:
    def fetchClasses(queryname):
        dbhandler = databaseHandler()
        result = dbhandler.getter(queryname)
        # classes=[row[1]for row in result]
        return result


    def fetchSubjects(queryname,chapid):
        dbhandler = databaseHandler()
        result = dbhandler.getterWithId(queryname,chapid)
        # classes=[row[1]for row in result]
        return result


    def fetchChapters(queryname,subjectid):
        dbhandler = databaseHandler()
        result = dbhandler.getterWithId(queryname, subjectid)
        # classes=[row[1]for row in result]
        return result

