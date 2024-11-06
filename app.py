import pymysql
from flask import Flask, request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from views import UserRegister, UserLogin, BookResource

app = Flask(__name__)
pymysql.install_as_MySQLdb()

app.config['SECRET_KEY'] = 'SUPER-SECRET-KEY'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:wb52k2964@localhost:3306/book_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register_user():
    return UserRegister().post()


@app.route('/login', methods=['POST'])
def login_user():
    return UserLogin().post()


@app.route('/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'POST':
        return BookResource().post()
    else:
        return BookResource().get()


if __name__ == '__main__':
    app.run(debug=True)