from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '|z\xa0!\xc0n\xb6\x86J\xc9G\xaa\r\x06R5 Y\xdf\x19\xba*\xde\xcd'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def validate(self):
        if self.title and self.body:
            return True
        else:
            return False



@app.route('/', methods=['POST', 'GET'])
def blog():

    entries = Blog.query.all()

    return render_template('blog.html', title=blog, entries=entries)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_title = request.form['blog']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body)

        if new_blog.validate():
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/singletemplate?id=" + str(new_blog.id))
        if blog_title == '':
            title_error = "error"
        if blog_body == '':
            blog_error = "error"
        if title_error == blog_error == '':
            return redirect("/blog?id={}".format(blog_id))
        else:
            return render_template('newpost.html', blog_title=blog_title, blog_body=blog_body, title_error=title_error, blog_error=blog_error)

    else:
        return render_template('newpost.html')


@app.route('/singletemplate', methods=['GET'])
def singletemplate():

    blog_id = request.args.get('id')
    entries = Blog.query.filter_by(id=blog_id).first()

    return render_template('singletemplate.html', entries=entries)


if __name__ == "__main__":
    app.run()