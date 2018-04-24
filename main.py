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

    def validate(self):
        if self.title and self.body:
            return True
        else:
            return False

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
    allowed_routes = ['login', 'register', 'blogs' , 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', title=blog, users=users)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_title = request.form['blog']
        blog_body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        new_blog = Blog(blog_title, blog_body, owner)
        title_error = ''
        blog_error = ''

        if new_blog.validate():
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/singletemplate?id=" + str(new_blog.id))
        if blog_title == '':
            flash("Please enter a title", 'error')
            # return render_template('newpost.html', blog_body=blog_body)
        if blog_body == '':
            flash("Please enter a blog post", 'error')
            return render_template('newpost.html', blog_title=blog_title)
        if title_error == '' or blog_error == '':
            flash("Please enter a blog title", 'error')
            return render_template('newpost.html', blog_title=blog_title)
        else:
            return redirect('/blogpost?id={0}&user={1}'.format(blog_id, owner))

        
    else:
        return render_template('newpost.html')


@app.route('/singletemplate', methods=['GET'])
def singletemplate():

    blog_id = request.args.get('id')
    entries = Blog.query.filter_by(id=blog_id).first()

    return render_template('singletemplate.html', entries=entries)


if __name__ == "__main__":
    app.run()