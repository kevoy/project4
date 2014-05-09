""" main.py is the top level script.

Return "Hello World" at the root URL.
"""
from flask import Flask, request
from flask import render_template
import urllib2
import json
import random
import uuid
from google.appengine.api import users
from google.appengine.api import channel
from utilities import funnames
import os
import sys
import httplib
from google.appengine.ext import db
# sys.path includes 'server/lib' due to appengine_config.py
app = Flask(__name__.split('.')[0])

class Comment(db.Model):
  username = db.StringProperty(default='')
  useropponent = db.StringProperty(default='')
  userstatus = db.StringProperty(default='')
  userscore = db.StringProperty(default='')
  
@app.route('/')
def hello(name=None):
  """ Return hello template at application root URL."""
  return render_template('home.html')
@app.route('/<name>/<opponent>')
def player(name, opponent):
  """ Return hello template at application root URL."""
  token = channel.create_channel(name)
  userHistory = displayUser(name)
  leaderBoard = displayWinners()
  templateValues = {
                    
                    "token": channel.create_channel(name),
                    "opponent": str(opponent),
                    "p1Name": name,
                    "p2Name": opponent,
                    "history": userHistory,
                    "leaderBoard": leaderBoard
                    }
 # db = sqlite3.connect('./cards.db')
  #cur = db.execute('insert into users (name) values (\'kevoy\')')
  #print cur
  return render_template('cards.html', values=templateValues)

@app.route('/sendmessage/<opponent>/<msg>', methods=['GET', 'POST'])
def sendMessage(opponent,msg):
  channel.send_message(opponent, msg)
  return "yes"
@app.route('/me')
def me(name=None):
  """ Return me template at application /me URL."""
  return "what?"
@app.route('/data')
def data():
  comment = Comment(username='Andrelle', gamesplayed='1')
  comment.put()
  return ""
@app.route('/data/<name>/<status>/<opponent>', methods=['GET', 'POST'])
def data2(name, status, opponent):
  comment = Comment(username=name, useropponent = opponent, userstatus = status)
  comment.put()
  return ""
@app.route('/data/<name>/<score>', methods=['GET', 'POST'])
def data3(name, score):
  comment = Comment(username=name, userscore = score)
  comment.put()
  return ""

def display():
  query = Comment.all()
  lst = ""
  for comment in query:
    if comment.userstatus:
      lst+=comment.username+"."
      lst+=comment.useropponent+"."
      lst+=comment.userstatus +";"
  return lst

def displayUser(user):
  query = Comment.all()
  lst = ''
  for comment in query:
    if comment.userstatus and comment.username == user:
      lst+='<h1 class=\'leaderplayers\'>You '
      lst+=comment.userstatus
      lst+=' a Game Against '+ comment.useropponent+'</h1>'
  return lst

@app.route('/display')
def displayWinners():
  query = Comment.all()
  lst = ''
  for comment in query:
    if comment.userscore:
      lst+='<h1 class=\'leaderplayers\'>'+comment.username+' Matches: '
      lst+=comment.userscore+'</h1>'
  return lst