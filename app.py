
from flask import Flask, jsonify, abort, make_response, request, url_for 
app = Flask('app')

class Todo():
    def __init__(self,id,title,description):
        self.id = id
        self.title = title
        self.description = description 


todos = [{
        'id': 1,
        'title':'flask',
        'description':''
        },
        {
        'id': 2,
        'title':'Python',
        'description':'Learn Python the hard way'
        },


]

@app.route('/todo',methods=['GET'])
def all_todos():
    return  jsonify(sorted(todos, key = lambda i: i['id']))

@app.route('/todo',methods=['POST'])
def add_todo():
    if not request.json or not 'title' in request.json:
        abort(400)

    todo = {
        'id':todos[-1]['id']+1,
        'title':request.json['title'],
        'description':request.json.get('description', '')
    } 

    todos.append(todo)
    return jsonify({ 'todo' : todo }),201




@app.route('/todo/<int:pk>', methods=['GET'])
def todo_details(pk):
    todo = list(filter(lambda t: t['id'] == pk, todos))
    if len(todo) == 0:
        abort(404)
    return jsonify({ 'todo' : todo[0] })


@app.route('/todo/<int:pk>', methods=['PUT'])
def update_todo(pk):
    todo = list(filter(lambda t:t['id'] == pk, todos))
    if len(todo) == 0:
        abort(400)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['description']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) != str:
        abort(400)

    todo[0]['title'] = request.json.get('title', todo[0]['title'])
    todo[0]['description'] = request.json.get('description', todo[0]['description'])
    return jsonify({ 'todo' : todo[0] })



@app.route('/todo/<int:pk>',methods=['DELETE'])
def delete_todo(pk):
    todo = list(filter(lambda t: t['id'] == pk, todos))
    if len(todo) == 0:
        abort(400)
    list_id = [i for i in range(len(todos))]
    if pk not in list_id:
        return 'id not found'
    todos.remove(todo[0])
    return jsonify({ 'result': 'Item has been deleted' })


app.run()