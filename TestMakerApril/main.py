from dao.databaseConnection import connection
from dao.databaseQueryHandler import databaseQueryHandler
from bl.auth import auth as auth_blueprint
from bl.index import index_blueprint as index_blueprint
from flask import Flask
print("staring")

def create_app():
    app = Flask(__name__)
    app.secret_key = 'my_test_maker'

    app.register_blueprint(index_blueprint)
    app.register_blueprint(auth_blueprint)
    return app

if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0',port=1051,debug=True)




# con=connection()
# dbhandler=databaseQueryHandler()
#
# chapname="theorms"
#
# cursor=con.cursor()
# # cursor.execute("INSERT INTO `chapter` (`chap_id`, `chap_name`, `subject_id`) VALUES ('3', chapname, '1');")
# # con.commit()
# params=('11th ics',)
# temp='insertClass'
# query = getattr(dbhandler, temp)
#
# cursor.execute(query,params)
# con.commit()
# # data=cursor.fetchall()
# # for row in data:
# #     print(row)
#
# cursor.close()
# con.close()