from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '|z\xa0!\xc0n\xb6\x86J\xc9G\xaa\r\x06R5 Y\xdf\x19\xba*\xde\xcd'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template('index.html', title="Blogz", users=users)

@app.route('/blog', methods=['GET'])
def blog():
    blogs = Blog.query.all()
    blog_id=request.args.get('id')
    if blog_id:
        post = Blog.query.get(blog_id)
        return render_template('singletemplate.html', blogs=blogs, post=post)

    else:
        return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'GET':
        return render_template('newpost.html')


    if request.method == 'POST':
        blog_title = request.form.get('title')
        blog_body = request.form.get('body')
        owner = User.query.filter_by(username=session['username']).first()
        newblog = Blog(blog_title, blog_body, owner)
        db.session.add(newblog)
        db.session.commit()
        newblogid = newblog.id
        title_error = ''
        blog_error = ''
        
        if blog_title == '':
            flash("Please enter a title", 'error')
        if blog_body == '':
            flash("Please enter a blog post", 'error')
            return render_template('newpost.html', blog_title=blog_title, blog_body=blog_body)
        if title_error == '' or blog_error == '':
            return redirect("/blog?id={}".format(newblogid))
        else:    
            return render_template('newpost.html', blog_title=blog_title, blog_body=blog_body, title_error=title_error, blog_error=blog_error)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            flash("Error!", 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username_error = ''
    password_error = ''
    passwordverify_error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwordverify = request.form['passwordverify']


        if username == '':
            username_error  = "Invalid username"
        elif len(username) > 20 or len(username) < 3 or ' ' in username:
            username_error  = "That's not a valid username"

        if password == '':
            password_error = "Invalid password"
        elif len(password) > 20 or len(password) < 3 or ' ' in password:
            password_error = "Invalid password"

        if passwordverify != password or len(passwordverify) < 3:
            passwordverify_error = "Passwords do not match"

        if username_error  == passwordverify_error == password_error == '':
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username

            return redirect('/newpost')
        return render_template('signup.html', username_error =username_error , password_error=password_error,
                               passwordverify_error=passwordverify_error, username=username)
    return render_template('signup.html')

@app.route('/singletemplate', methods=['GET'])
def singletemplate():

    blog_id = request.args.get('id')
    post = Blog.query.filter_by(id=blog_id).first()

    return render_template('singletemplate.html', post=post)

if __name__ == "__main__":
    app.run()