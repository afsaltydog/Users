from flask import Flask, render_template, request, redirect, session
from sqlcon import connectToMySQL
app= Flask(__name__)
app.secret_key='ASFI W dhadfjkahs j1245!@'

@app.route('/')
def index():
    mysql = connectToMySQL('Users')
    user = mysql.query_db('SELECT * FROM users;')
    print('users is '+str(user))

    return render_template('index.html', dbInfo=user)

@app.route('/users')
def all_users():
    mysql = connectToMySQL('Users')
    user = mysql.query_db('SELECT * FROM users;')
    print(str(user))

    #return render_template('index.html', dbInfo=user)
    return redirect('/')

@app.route('/users/new', methods=['get'])
def new_user():
    print('request is '+str(request.form))

    return render_template('add.html')

@app.route('/users/create', methods=['post'])
def create_user():
    print('request is '+str(request.form))

    mysql = connectToMySQL('users')
    query = "INSERT INTO users (first_name, last_name, email) VALUES (%(fn)s, %(ln)s, %(em)s);"
    data = {"fn": request.form['fname'],
           "ln": request.form['lname'],
           "em": request.form['form_email']
    }
    print('query is '+str(query))

    new_user_id = mysql.query_db(query, data)
    print('new user id is '+str(new_user_id))

    return redirect('/users/id')
    #return render_template('add.html')

@app.route('/users/<id>', methods=['get'])
def show_user(id):
    print('id is '+str(id))

    mysql = connectToMySQL('users')
    query = "SELECT * FROM users where id = "+id+";"
     
    print('query is '+str(query))

    user = mysql.query_db(query)
    print('user is '+str(user))

    return render_template('show.html', dbInfo=user)

@app.route('/users/<id>/edit', methods=['get'])
def edit_user(id):
    #print('request is '+str(request.form))
    
    mysql = connectToMySQL('users')
    query = "SELECT * FROM users where id = "+id+";"
     
    print('query is '+str(query))

    user = mysql.query_db(query)
    print('user is '+str(user))

    return render_template('edit.html', dbInfo=user)

@app.route('/users/<id>/update', methods=['post'])
def update_user(id):
    print('request is '+str(request.form))

    mysql = connectToMySQL('users')
    
    data = {
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "email": request.form['form_email'],
        "id": id
    }

    user = mysql.query_db("UPDATE Users SET first_name = %(fname)s, last_name = %(lname)s, email = %(email)s WHERE id = "+id+";", data)

    print('user is '+str(user))

    return redirect('/users/id')
    # return render_template('edit.html', dbInfo=user)

@app.route('/users/<id>/destroy', methods=['get'])
def destroy_user(id):
    #print('request is '+str(request.form))
    
    mysql = connectToMySQL('users')
    query = "DELETE FROM users where id = "+id+";"
     
    print('query is '+str(query))

    user = mysql.query_db(query)
    print('user is '+str(user))

    return redirect('/users')
    #return render_template('edit.html', dbInfo=user)

if __name__=="__main__":
    app.run(debug=True)