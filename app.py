from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from views import UserRegister, UserLogin, BookResources


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPER-SECRET-KEY'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(BookResources, '/books')


if __name__ == '__main__':
    app.run(debug=True)