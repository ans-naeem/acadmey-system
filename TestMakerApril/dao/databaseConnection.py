import mysql.connector
import flask
def connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="believer.31",
        database="test_maker"
    )
    print("going to return the connection")
    return conn
    # chapname="theorms"
    # cursor=conn.cursor()
    # cursor.execute("INSERT INTO `chapter` (`chap_id`, `chap_name`, `subject_id`) VALUES ('3', chapname, '1');")
    # conn.commit()
    # cursor.execute("select * from chapter;")
    # data=cursor.fetchall()
    # for row in data:
    #     print(row)
    #
    # cursor.close()
    # conn.close()
    # app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:summer vine@localhost/form'
    # db =SQLAlchemy(app)

