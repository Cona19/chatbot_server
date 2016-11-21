#-*- coding:utf-8 -*-
#!flask/bin/python
from flask import Flask
from flask import request
from flask_socketio import SocketIO
from flask_socketio import send, emit
import wikiroid
import json

"""
Initialize Flask, socketio, and wikiroid instance
"""
app = Flask(__name__)
socketio = SocketIO(app)
handler = wikiroid.Handler()

"""
Root address routes to simple message"
"""
@app.route('/')
def index():
    return "Server running"

"""
Receive query message from socketio and reply answer
"""
@socketio.on('query')
def handle_message(json):
    print('receive message: ' + str(json))
    emit('get', json)
    try:
        question = json['question']
        print question
        if type(question) == unicode:
            question = question.encode('utf-8')
        print type(question)
        print question
        handler.reply(question, emit)
    except Exception as e:
        print "--------------------------------"
        print e
        print "--------------------------------"

"""
Add new category in wikiroid
"""
@app.route('/new', methods=['POST']) # MUST CHANGE TO POST
def add_new_category():
    name = request.form.get('name')
    if type(name) is unicode:
        name = name.encode('utf-8')
    print type(name)
    print name

    desc = request.form.get('desc')
    if type(desc) is unicode:
        name = name.encode('utf-8')
    print type(desc)
    print desc

    corpus = json.loads(request.form.get('corpus'))
    print type(corpus)
    for idx in range(len(corpus)):
        if type(corpus[idx]) is unicode:
            corpus[idx] = corpus[idx].encode('utf-8')
    print str(corpus)

    reprDict = json.loads(request.form.get('reprDict'))
    for k in reprDict.keys():
        for idx in range(len(reprDict[k])):
            if type(reprDict[k][idx]) is unicode:
                reprDict[k][idx] = reprDict[k][idx].encode('utf-8')
    print type(reprDict)
    print str(reprDict)

    findFunc = request.form.get('findFunc')
    if type(findFunc) is unicode:
        findFunc = findFunc.encode('utf-8')
    print type(findFunc)
    print findFunc

    distMethod = json.loads(request.form.get('distMethod'))
    for k in distMethod.keys():
        if type(distMethod[k]) is unicode:
            distMethod[k] = distMethod[k].encode('utf-8')
    print type(distMethod)
    print str(distMethod)

    if handler.addCategory(name, desc, corpus, reprDict, findFunc, distMethod) and handler.build():
        return 'Succeed'
    else:
        return 'Failed'

    """
    except Exception as e:
        print "--------------------------------"
        print e
        print "--------------------------------"
        return 'Failed'
    """

"""
Return Category informations
"""
@app.route('/list', methods=['GET']) # MUST CHANGE TO POST
def getCategoryList():
    return json.dumps(handler.getCategoryList())

if __name__ =='__main__':
    socketio.run(app, host='0.0.0.0', port=10101)
