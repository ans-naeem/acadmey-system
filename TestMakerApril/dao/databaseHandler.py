from dao.databaseQueryHandler import databaseQueryHandler
from dao.databaseConnection import connection

class databaseHandler:
    def inserter(self,queryname,params):
        dbhandler=databaseQueryHandler()
        query=getattr(dbhandler,queryname)
        conn=connection()
        cursor=conn.cursor()
        cursor.execute(query,params)
        conn.commit()
        cursor.close()
        conn.close()

#this functionality not been implemented yet as its logic seems rough and tough right now

    def updater(self,tableName,params):
        dbhandler = databaseQueryHandler()
        query = getattr(dbhandler, tableName)
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()

    def getter(self,queryname):
        dbhandler = databaseQueryHandler()
        query=getattr(dbhandler,queryname)
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(query)
        data=cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    def getterWithId(self,queryname,id,type=None):
        dbhandler = databaseQueryHandler()
        query=getattr(dbhandler,queryname)

        conn = connection()
        cursor = conn.cursor()
        if(type==None):
            cursor.execute(query,(id,))
        else:
            cursor.execute(query,(id,type,))
        data=cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    # def getterwithId(self,queryname,id,type):
    #     dbhandler = databaseQueryHandler()
    #     query=getattr(dbhandler,queryname)
    #     conn=connection()
    #     cursor = conn.cursor()
    #     cursor.execute(query,(id,type,))
    #     data=cursor.fetchall()
    #     cursor.close()
    #     conn.close()
    #     return data





