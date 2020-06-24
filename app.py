import os
import functools
from flask import Flask,flash,request, render_template, redirect, url_for,g,session
import mysql.connector
import MySQLdb.cursors

app = Flask(__name__)
app.config.from_object('secret_config')
wsgi_app = app.wsgi_app
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def connect_db():
    g.conn=mysql.connector.connect(
            host=app.config['DATABASE_HOST'],
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASSWORD'],
            database=app.config['DATABASE_NAME']
    )

    g.cursr=g.conn.cursor()
    return g.cursr


def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

def login_required(f):
    @functools.wraps(f)
    def wrap (*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Login required')
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET','POST'])
def login():
    #db = get_db()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cnx = mysql.connector.connect(user='suresh', passwd='Covid@19LIVEIT',
                                      host='127.0.0.1', db='website'
                                      )
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT username FROM admin WHERE username = %s AND password = %s', (username, password))
        session['logged_in'] = True

        account = cursor.fetchone()

        if account:
            session['account'] = account[0]
            return redirect(url_for('homepage'))
        else:
            flash('Incorrect credentials')
    return render_template('login.html')


@app.route('/homepage')
@login_required
def homepage():
    if not (session.get('logged_in') == True):
        return render_template('login.html')
    else:
        return render_template('layout.html')


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))




@app.route('/homepage/addurl/', methods = ['POST', 'GET'])
def addurl() :
    if request.method == 'POST':
        url = request.form.get('url')
        cnx = mysql.connector.connect(user='suresh', passwd='Covid@19LIVEIT',
                                      host='127.0.0.1', db='pythondb'
                                      )
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO buslinks (id,filename,url,description) VALUES('"+str(id)+","+str(filename)+","+str(url)+","+str(description)+"')")
        cnx.commit()
    return render_template('url.html')


@app.route('/homepage/deleteurl/', methods = ['POST', 'GET'])
def deleteurl() :
    if request.method == 'POST':
        url = request.form.get('url')
        cnx = mysql.connector.connect(user='suresh', passwd='Covid@19LIVEIT',
                                      host='127.0.0.1', db='pythondb'
                                      )
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM buslinks where filename= '+filename+' ")
        cnx.commit()
    return render_template('delete.html')


@app.route('/login/homepage/modifyurl/', methods = ['POST', 'GET'])
def modifyurl(id) :
    if not session.get('user') :
        return redirect(url_for('login'))
    if request.method == 'POST':
        url = request.form.get('urlmodify')
        cnx = mysql.connector.connect(user='suresh', passwd='Covid@19LIVEIT',
                                      host='127.0.0.1', db='pythondb'
                                      )
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE `buslinks` SET `url`= '"+url+"' WHERE 'id' = "+id+" ")
        cnx.commit()
    return render_template('modifyurl.html')

@app.route('/homepage/techentries')
@login_required
def techentries() :
    db = get_db()
    db.execute('SELECT id, filename,url FROM techlinks')
    tech = db.fetchall()
    return render_template('technology.html',tech=tech)


@app.route('/homepage/busentries')
@login_required
def busentries() :
    db = get_db()
    db.execute('SELECT id, filename,url FROM buslinks')
    buss = db.fetchall()
    return render_template('Business.html', buss = buss)



@app.teardown_appcontext
def close_db(error) :
    if hasattr(g, 'db') :
        g.db.close()



if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5757'))
    except ValueError:
        PORT = 5757
    app.run(HOST, PORT, debug=True)

