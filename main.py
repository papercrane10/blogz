from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
#how does sql alchemy work? how do the block content work? what varaibles do I need?href the blog titles so that it turns filters on
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://buildablog:password123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(120))
    post_content = db.Column(db.String(1500)) 
 

    def __init__(self, post_name, post_content):
        self.post_name = post_name
        self.post_content = post_content

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
    title_error = ''
    post_error = ''
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
            new_post= Blog(post_name, post_content)
            db.session.add(new_post)
            db.session.commit()
            posts = Blog.query.filter_by(post_name=post_name).first_or_404(description='There is no data with {}'.format)
            title = posts.post_name
            content= posts.post_content
            blogid=posts.id
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
#valididate the posts entry content, if its valid reroute to the main page with a filter for the post. If empty send them back with errors
    else:
        return render_template('post.html',post_name=title, blog_post=content, post_error=post_error, title_error=title_error)



if __name__ == '__main__':
    app.run()