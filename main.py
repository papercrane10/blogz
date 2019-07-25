from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from function import is_valid, validate
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:monday2019!@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '765)m8&1#743'

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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

    def __init__(self, username, password):
        self.username = username
        self.password = password
        

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
       

@app.route("/blog", methods=['GET'])
def index():
    username = User.query.filter_by(username=session['username']).first()
    if request.method == 'GET':
        blogid = request.args.get('id')
        post = Blog.query.all()
        #username = User.query.filter_by(id=post.owner_id).first()
        if blogid is not None:
            post = Blog.query.filter_by(id=blogid).first()
            username = User.query.filter_by(id=post.owner_id).first()

            return render_template('single_post.html', post=post, username=username)
        else:
            username=User.query.all()
            
            return render_template('all_posts.html', post=post, username=username)
    return render_template('all_posts.html', post=post, username=username)
        
        
   
@app.route('/newpost', methods=['POST', 'GET'])
def blogpost():
    username = User.query.filter_by(username=session['username']).first()
    title = ''
    content = ''
    blog = ''
    blogs_key=''
    title_error = ''
    post_error = ''
    
  

    if request.method == 'POST':
        # blog_id = int(request.form['blogid'])
        # blog = Blog.query.get(blog_id)
        post_name = request.form['post_name']
        post_content = request.form['post_content']
        
        if is_valid(post_name) and is_valid(post_content):
            new_post= Blog(post_name, post_content, username.id)
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

    return render_template('post.html',post_name=title, blog_post=content, post_error=post_error, title_error=title_error)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['password_confirm']  
        existing_user = User.query.filter_by(username=username).first()
        
        if validate(username, password, verify):
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
            else:
                username_error = 'User already exists'
                password= ''
                return render_template('signup.html', username=username, password=password,username_error=username_error)

        if not is_valid(username):
            username_error = 'Username not valid'
            if not is_valid(password):
                password_error = 'password not valid'
                return render_template('signup.html', username='',username_error=username_error, password='', password_error=password_error)
        else:
            if not is_valid(password):
                password = 'password not valid'
                return render_template('signup.html', username=username, password_error=password)
            else:
                if not is_valid(verify):
                    password = 'validation incorrect'
                    return render_template('signup.html', username=username, validation_error=password)
            

    else:
        return render_template('signup.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username= request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            
            username_error = 'Username invalid'
            password_error = 'Password invalid'
            
            #return redirect('/newpost')
            return render_template("login.html", username_error=username_error, password_error=password_error)       


    else:
        return render_template("login.html")       


@app.route('/')
def home():
    all_users=User.query.all()
    return render_template('index.html', all_users=all_users)
@app.route('/logout')
def logout():
    
    del session['username']

    return redirect('/blog')

if __name__ == '__main__':
    app.run()