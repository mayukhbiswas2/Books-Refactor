from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, Book
from db import db

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        if not username or not password:
            return {'message': 'Missing username or password...'}, 400
        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists...'}, 400

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully...'}, 200

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials...'}, 401

class BookResources(Resource):
    @jwt_required()
    def get(self):
        books = Book.query.all()
        return {'books': [{'id': book.id, 'title': book.title, 'author': book.author} for book in books]}, 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        title = data['title']
        author = data['author']

        if not title or not author:
            return {'message': 'Missing title or author...'}, 400

        new_book = Book(title=title, author=author)
        db.session.add(new_book)
        db.session.commit()
        return {'message': 'Book created successfully...'}, 200