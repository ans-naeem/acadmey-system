from flask import Blueprint,render_template,url_for,request
from dao.databaseConnection import connection
from dao.databaseHandler import databaseHandler

auth = Blueprint('auth',__name__)

@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/login',methods=['GET', 'POST'])
def login():
    if(request.method == 'GET'):
        return render_template("login.html")
    elif (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']

        #if we need to fetch data from any table just pass the query name to databasehandler and it will return the result
        dbhandler=databaseHandler()
        result=dbhandler.getter("fetchUsers")
        for user in result:
            if user[1] == username and user[2] == password:
                if(user[5]=="yes"):
                    allow=1
                else:
                    allow=0
                return render_template("index.html",allowed=allow)

        return 'Invalid username or password. Please try again.'

#
#
# @auth.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         # Here you can add your login logic
#         # For example, check if username and password are valid
#
#         # Example check (don't use in production)
#         if username == 'admin' and password == 'password':
#             return 'Login successful!'
#         else:
#             return 'Invalid username or password. Please try again.'
