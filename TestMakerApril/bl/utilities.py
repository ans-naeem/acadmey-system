from dao.databaseHandler import databaseHandler


def fetchClasses(queryname):
    dbhandler = databaseHandler()
    result = dbhandler.getter(queryname)
    # classes=[row[1]for row in result]
    return result