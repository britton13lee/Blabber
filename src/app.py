from flask import Flask, jsonify

app=Flask(__name__)

#@app.route('/')
#def index():
#  return'Index Page'
  
@app.route('/greetings', methods=['GET'])
def greet():
  return jsonify(['Hello, friend!', 'Top of the morning to ya!', 'Come on in, the water's warm!', 'Welcome, traveler!', 'Cheers!'])
