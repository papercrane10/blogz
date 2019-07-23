from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:monday2019!@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '765)m8&1#743'

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.String(20), db.ForeignKey('user.id'))
    post_name = db.Column(db.String(120))
    post_content = db.Column(db.String(1500)) 
 

    def __init__(self, post_name, post_content, owner):
        self.post_name = post_name
        self.post_content = post_content
        self.owner_id = owner

class User(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(256))
    blog = db.relationship('Blog', backref='owner')

    def __init__(self, username, password, blog):
        self.username = username
        self.password = password
        self.blog = blog

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
       

@app.route("/blog", methods=['GET'])
def index():
    if request.method == 'GET':
        blogid = request.args.get('id')
        post = Blog.query.all()
        if blogid is not None:
            post = Blog.query.filter_by(id=blogid).first()

            return render_template('single_post.html', post=post)
        else:
            return render_template('home.html', post=post, blogid=blogid)
        
        
   
@app.route('/newpost', methods=['POST', 'GET'])
def blogpost():
    title = ''
    content = ''
    blog = ''
    blogs_key=''
    title_error = ''
    post_error = ''
    user = User.query.filter_by(username=username).first()
    def is_valid(user_input):
        length = len(str(user_input))
        if length >= 3 and length<=120:
            return True
        else:            
            return False

    if request.method == 'POST':
        # blog_id = int(request.form['blogid'])
        # blog = Blog.query.get(blog_id)
        post_name = request.form['post_name']
        post_content = request.form['post_content']
        if is_valid(post_name) and is_valid(post_content):
            new_post= Blog(post_name, post_content, owner)
            db.session.add(new_post)
            db.session.commit()
            posts = Blog.query.filter_by(post_name=post_name).first_or_404(description='There is no data with {}'.format)
            title = posts.post_name
            content= posts.post_content
            blogid=posts.id
            blogs_key=posts.owner_id
                    
            
            return redirect('/blog?id={0}'.format(blogid))
        else:
            if is_valid(post_name) == False:
                title_error = 'Post name not valid'
                
                if not is_valid(post_content):
                    post_error = 'Content not valid'
                    return render_template('post.html',post_name=post_name, blog_post=post_content,post_error=post_error, title_error=title_error)
                else: 
                    post_error = ''
                    return render_template('post.html',post_name=post_name, blog_post=post_content, post_error=post_error, title_error=title_error)
            else:
                if not is_valid(post_content):
                    post_error = 'Content not valid'
                    title_error = ''
                    return render_template('post.html',post_name=post_name, blog_post=post_content, post_error=post_error, title_error=title_error)
    else:
        return render_template('post.html',post_name=title, blog_post=content, post_error=post_error, title_error=title_error)

@app.route('/signup')
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            if validate(username):
                username = 'Username not valid'
                if validate(password):
                    password = 'password not valid'
            return redirect('/signup', username=username, password=password)

@app.route('/login', method = ['POST'])
def login():
    username = ''
    password = ''
    owner_id = ''
    username = request.form=['username']
    password = request.form=['password']
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session['username'] = username
        flash("Logged in")
        return redirect('/newpost')
    else:
        errors = 'there are erroor'
        return render_template("login.html", errors=errors)       



    return redirect('/blog', owner_id=owner_id)

@app.route('/index')
def home():
    all_users=User.query.all()
    return render_template('home.html', all_users=all_users)
@app.route('/logout')
def logout():
    
    del session['username']

    return redirect('/')

if __name__ == '__main__':
    app.run()