from dao.databaseQueryHandler import databaseQueryHandler
from dao.databaseConnection import connection

class databaseHandler:
    def inserter(self,queryname,name,id=None,number=None):

        dbhandler=databaseQueryHandler()
        query=getattr(dbhandler,queryname)
        conn=connection()
        cursor=conn.cursor()
        if(id==None and number==None):
            cursor.execute(query, (name,))
        elif(number==None and id != None):
            cursor.execute(query,(name,id,))
        else:
            cursor.execute(query,(name,id,number,))
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
            print("Select chap_ids are :"+str(id))
            #finding the count to make equal number of place holders
            temp_ids=len(id)

            #now if we see there is a word place holder in our query.we need to replace that with
            #equal number of %S so we just do this.
            placeholders = ', '.join(['%s'] * temp_ids)

            query=query.replace("placeholders",placeholders)

            print("Query being used to fetch questions: "+query)
            cursor.execute(query, (*id, type))
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





