from flask import Flask, render_template, redirect,request
from database import db

app=Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
@app.route('/teachers')
def teachers():
    return render_template('teachers.html',teachers=db.teachers())
    
@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/error404')
def error404():
    return render_template('404.html')
 
@app.route('/teachers_details/')
@app.route('/teachers_details/<ID>')
def teachers_details(ID="Arsham"):
    rule = request.url_rule
    url_rule = '/'
    print rule
    teacher=db.teacher(ID)
    if teacher:
        return render_template('teachers-details.html')
    else:
        return redirect('/error404')
    
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')
    
    
@app.route('/knowledge_base')
def knowledge_base():
    return render_template('knowledgebase.html')
    
@app.route('/index_two')
def index_two():
    return render_template('index-two.html')
    
@app.route('/gallery_full_width')
def gallery_full_width():
    return render_template('gallery-fullwidth.html')
    
@app.route('/gallery_4_column')
def gallery_4_column():
    return render_template('gallery-4-column.html')

@app.route('/gallery_3_column')
def gallery_3_column():
    return render_template('gallery-3-column.html')
    
@app.route('/gallery_2_column')
def gallery_2_column():
    return render_template('gallery-2-column.html')

@app.route('/single')
def single():
    return render_template('single.html')
    
@app.route('/single_sidebar')
def single_sidebar():
    return render_template('single-sidebar.html')

@app.route('/event_list')
def event_list():
    return render_template('event-list.html')
    
@app.route('/event_grid')
def event_grid():
    return render_template('event-grid.html')
    
   
@app.route('/event_details')
def event_details():
    return render_template('event-details.html')

@app.route('/course_list')
def course_list():
    return render_template('course-list.html')
    
@app.route('/course_grid')
def course_grid():
    return render_template('course-grid.html')

@app.route('/course_details')
def course_details():
    return render_template('course-details.html')
    
@app.route('/contact')
def contact():
    return render_template('contact.html')
    
@app.route('/code_of_contact')
def code_of_contact():
    return render_template('code-of-contact.html')
    
@app.route('/blog')
def blog():
    return render_template('blog.html')
    
@app.route('/blog_sidebar')
def blog_sidebar():
    return render_template('blog-sidebar.html')
        
@app.route('/about_us')
def about_us():
    return render_template('about-us.html')    
            

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0',port=8080)
    
    
    
