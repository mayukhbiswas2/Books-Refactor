from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required
from models import User, Books
from db import db

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'message': 'Missing username or password...'}, 400
        if User.query.filter_by(username=username).first():
            return {'message': 'Username already taken...'}, 400

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully...'}, 200

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200

        return {'message': 'Invalid data...'}, 401



class BookResource(Resource):
    @jwt_required()
    def get(self):
        books = Books.query.all()
        return [{'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year} for book in books], 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        year = data.get('year')

        new_book = Books(title=title, author=author, year=year)
        db.session.add(new_book)
        db.session.commit()
        return {'message': 'Book added successfully...'}, 201


