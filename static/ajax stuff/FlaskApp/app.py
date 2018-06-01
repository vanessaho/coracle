from flask import Flask, render_template, request
import json
from flask import jsonify
app = Flask(__name__)

@app.route('/signup')
def signup():	
    return render_template('signup.html')

@app.route('/signupuser', methods=['POST'])
def signupuser():
    user = request.form['username']
    password = request.form['password']
    return jsonify({'andy': 320, 'status':'OK', 'user': user, 'pass': password})

if __name__ == "__main__":
    app.run()