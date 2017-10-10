from flask import Flask, render_template, redirect,request, url_for, flash
from database import db
from werkzeug.utils import secure_filename
import os, json
from pymongo import MongoClient
con = MongoClient("mongodb://maysam:0183552313@ds149479.mlab.com:49479/pycademy")
database = con.pycademy

app=Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
@app.route('/teachers')
def teachers():
    print db.teachers()
    return render_template('teachers.html',teachers=db.teachers())
    
@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/error404')
def error404():
    return render_template('404.html')

def allowed_file(filename,ALLOWED_EXTENSIONS):
    # ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/edit_course', methods=["POST","GET"])
@app.route('/create_course', methods=["POST","GET"])
def create_course(cid=None):
    print request.url.split('/')[-1][:11]
    if request.method == "GET":
        if request.url.split('/')[-1][:11]=='edit_course':
            ID = request.args.get('ID','null')
            course=db.course(ID)
            return render_template('createcourse.html',course=course,action="edit_course?ID={}".format(ID))
        return render_template('createcourse.html',course={},action="create_course")
    else:
        if ('image' not in request.files) or ('course_plan' not in request.files):
            #flash('No file part')
            return redirect(request.url)
        imagefile = request.files['image']
        coursefile = request.files['course_plan']
        if imagefile.filename == '' or coursefile.filename == '':
            #flash('No selected file')
            return redirect(request.url)

        if (imagefile and allowed_file(imagefile.filename,['png']))and(coursefile and allowed_file(coursefile.filename,['pdf'])):
            if request.url.split('/')[-1][:11]=='edit_course':
                ID = request.args.get('ID','null')
                if ID:
                    database.courses.find({c})
                    db.editCourse(dict(request.form),coursefile,imagefile,ID)
            else:
                db.creatCourse(dict(request.form),coursefile,imagefile)
            return str(request.form)
        return 'not successful'
        
@app.route('/edit_teacher')
@app.route('/add_teacher', methods=["POST","GET"])
def add_teacher(tid=None):
    if request.method == "GET":
        ID = request.args.get('ID','')
        if ID:
            teacher=db.teacher(ID)
        else:
            teacher={}
        if request.url.split('/')[-1][:12]=='edit_teacher':
            ID = request.args.get('ID','')
            teacher=db.teacher(ID)
            return render_template('add_teacher.html',teacher=teacher)
        return render_template('add_teacher.html',teacher={})
    else:
        if ('TeachersImage' not in request.files):
            #flash('No file part')
            return redirect(request.url)
        imagefile = request.files['TeachersImage']
        if imagefile.filename == '':
            #flash('No selected file')
            return redirect(request.url)

        if imagefile and allowed_file(imagefile.filename,['png']):
            db.addTeacher(dict(request.form),imagefile)
            return str(request.form)
        return 'not successful'

@app.route('/teachers_details')
def teachers_details():
    ID = request.args.get('ID','guest')
    teacher=db.teacher(ID)
    otherTeachers=db.otherTeachers(ID)
    print otherTeachers ,'-'*10
    stat=db.stat()
    if teacher:
        return render_template('teachers-details.html',teacher=teacher, otherTeachers=otherTeachers,stat=stat)
    else:
        return redirect('/error404')
   
@app.route('/add_blog', methods=["POST", "GET"])
def add_blog():
    if request.method == "GET":
        postInfo = db.blogInfo()
        categoryTags = db.categoryTags()
        tagsCloud = db.tagsCloud()
        recentPosts = db.recentPost()
        postData = db.blogSidebarInfo()
        return render_template('add_blog.html',  postInfo={})
    else:
        if ('BlogImage' not in request.files):
            #flash('No file part')
            return redirect(request.url)
        imagefile = request.files['BlogImage']
        # if imagefile.filename == '':
        #     #flash('No selected file')
        #     return redirect(request.url)
        if imagefile and allowed_file(imagefile.filename,['png']):
            db.addBlog(dict(request.form),imagefile)
            return str(request.form)
        return 'not successful'
    
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
    images=db.images()
    return render_template('gallery-fullwidth.html', images=images)
    
@app.route('/gallery_4_column')
def gallery_4_column():
    images=db.images()
    return render_template('gallery-4-column.html', images=images)

@app.route('/gallery_3_column')
def gallery_3_column():
    images=db.images()
    return render_template('gallery-3-column.html', images=images)
    
@app.route('/gallery_2_column')
def gallery_2_column():
    images=db.images()
    return render_template('gallery-2-column.html', images=images)

@app.route('/single')
def single():
    return render_template('single.html')
    
@app.route('/single_blog')
def single_sidebar():
    categoryTags = db.categoryTags()
    tagsCloud = db.tagsCloud()
    recentPosts = db.recentPost()
    postInfo = db.blogInfo()
    return render_template('single-blog.html', categoryTags=categoryTags, tagsCloud=tagsCloud, recentPosts=recentPosts, postInfo=postInfo)

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
    courses=db.courses()
    page = request.args.get('page','0')
    print page
    return render_template('course-list.html', courses=courses)
    
@app.route('/course_grid')
def course_grid():
    courses=db.courses()
    page = request.args.get('page','0')
    print page
    return render_template('course-grid.html', courses=courses)

@app.route('/course_details')
def course_details():
    ID = request.args.get('ID','null')
    course=db.course(ID)
    if course:
        p
        return render_template('course-details.html', course=course)
    else:
        return redirect('/error404')
    
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
    postInfo = db.blogInfo()
    categoryTags = db.categoryTags()
    tagsCloud = db.tagsCloud()
    recentPosts = db.recentPost()
    postData = db.blogSidebarInfo()
    return render_template('blog-sidebar.html', postData=postData, postInfo=postInfo, categoryTags=categoryTags, tagsCloud=tagsCloud, recentPosts=recentPosts)
        
@app.route('/about_us')
def about_us():
    return render_template('about-us.html')    
            

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0',port=8080)
