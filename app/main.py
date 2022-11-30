from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
def index():
  return '<h1>I want to Deploy Flask to Heroku</h1>'