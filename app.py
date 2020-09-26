from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
import json
import collections


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
db = SQLAlchemy(app)
app.config['SQL_DATABASE_URI'] = 'sqlite:///react-note.db'
migrate = Migrate(app,db)

class Todo(db.Model):
    def __init__(self,title,completed):
        self.title = title
        self.completed = completed

    
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return '<Todo {}>'.format(self.title)


class TodoSerializer:
    def __init__(self, todo):
        self.todo = todo


    def to_dict(self):
        return collections.OrderedDict([
            ('id', self.todo.id),
            ('title', self.todo.title),
            ('completed', self.todo.completed)
        ])



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        todos = Todo.query.all()
        serialized = [TodoSerializer(todo).to_dict() for todo in todos]
        return jsonify({
            'todos': serialized,
            'next_id': 3
        })
    elif request.method == 'POST':
        title = request.json['title']
        completed = False
        todo = Todo(title, completed)
        db.session.add(todo)
        db.session.commit()
        serialized = TodoSerializer(todo).to_dict()
        return jsonify(serialized)
    


@app.route('/api/delete/<id>', methods=['DELETE', "GET"])
def delete():
    if request.method == 'DELETE':
        new_id = request.json['id']
        print(new_id)
        todo = Todo.query.get(new_id)
        db.session.delete(todo)
        db.session.commit()
        todos = Todo.query.all()
        serialized = [TodoSerializer(todo).to_dict() for todo in todos]
        return jsonify(serialized)
    elif request.method == "GET":
        todos = Todo.query.filter_by(id=id)
        serialized = [TodoSerializer(todo).to_dict() for todo in todos]
        return jsonify(serialized)



@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        title = request.form['title']
        completed = True
        todo = Todo(title,completed)
        db.session.add(todo)
        db.session.commit()
        return jsonify({"success": f"{title} successfully added"})


@app.route('/api/complete/<id>', methods=['GET', 'PUT'])
def completed():
    if request.method == 'PUT':
        new_id = request.json['id']
        todo = Todo.query.get(new_id)
        if todo.completed == True:
            todo.completed = False
        else:
            todo.completed = True
        print(todo.completed)
        db.session.add(todo)
        db.session.commit()
        serialized = TodoSerializer(todo).to_dict()
        return jsonify(serialized)


if (__name__) =='__main__':
    db.create_all()
    app.run(debug=True)
