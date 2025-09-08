from flask import Flask, render_template, request, jsonify, redirect, url_for,flash, get_flashed_messages,session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'thisisthesecretkey'

client = MongoClient('mongodb://localhost:27017/')

db = client['YeildX']
collection = db['Users']

@app.route('/')
def about():
    return render_template('about.html')

@app.route('/index')
def index():
    if 'user_name' in session:
        return render_template('index.html',user_name = session['user_name'])
    else:
        return render_template('index.html',user_name = None)

@app.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        flash("User Added Successfully")
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)

        user_data = {"name":name , "password":hashed_password,"email":email}
        collection.insert_one(user_data )
        flash('User added sucessfully')
        return redirect(url_for('signin'))
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find user by email
        user = collection.find_one({"email": email})

        if user and check_password_hash(user['password'], password):
            # Save user info in session
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password, TryAgain")
            return redirect(url_for('signin'))

    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug = True)