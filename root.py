from flask import Flask, render_template, redirect,request, url_for, flash
from database import db
from werkzeug.utils import secure_filename
import os, json, uuid, ast
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_mail import Message
from flask_mail import Mail
import uuid

myEmail="kidocodeictschool@gmail.com"

app = Flask(__name__)
app.secret_key = 'YOLO'

app.config.update(
    DEBUG = True,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = myEmail,
    MAIL_PASSWORD = "weareprogrammerz" #not secure!!!!
)
mail = Mail(app)

def send_mail(sender, email, message):
    msg = Message(
        'DONOTREPLY',
        sender = sender,
        recipients=[email]
        )
    msg.body = message
    mail.send(msg)

#-----------------Index-----------------

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', stats=db.stat())

#-----------------Other Pages-----------------

@app.route('/error404')
def error404():
    return render_template('404.html')

def allowed_file(filename,ALLOWED_EXTENSIONS):
    # ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/contact')
def contact():
    return render_template('contact.html')
    
@app.route('/code_of_contact')
def code_of_contact():
    return render_template('code-of-contact.html')
        
@app.route('/about_us')
def about_us():
    return render_template('about-us.html')   

@app.route('/knowledge_base')
def knowledge_base():
    return render_template('knowledgebase.html')
    
@app.route('/index_two')
def index_two():
    return render_template('index-two.html')

#-----------------Courses-----------------

@app.route('/course_list')
def course_list():
    courses=db.courses()
    page = request.args.get('page','0')
    print page
    return render_template('course-list.html', courses=courses)
    
@app.route('/course_grid')
def course_grid():
    courses=db.courses()
    for course in courses:
        print course.get('courseActive')
    page = request.args.get('page','0')
    print page
    return render_template('course-grid.html', courses=courses)

@app.route('/course_details')
def course_details():
    ID = request.args.get('ID','null')
    course=db.course(ID)
    if course:
        print course
        return render_template('course-details.html', course=course,ID=ID)
    else:
        return redirect('/error404')


@app.route('/create_course', methods=["POST","GET"])
def create_course(cid=None):
    if request.method == "GET":
        return render_template('createcourse.html',course={},action="create_course")
    else:
        if ('image' not in request.files) or ('course_plan' not in request.files):
            flash('No file part')
            return redirect(request.url)
        imagefile = request.files['image']
        coursefile = request.files['course_plan']
        if imagefile.filename == '' or coursefile.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if (imagefile and allowed_file(imagefile.filename,['png']))and(coursefile and allowed_file(coursefile.filename,['pdf'])):
            db.creatCourse(dict(request.form),coursefile,imagefile)
            flash('Course Added Successfully, Add New Course!!')
            return redirect(request.url)
        flash('File Format Is Not Acceptable, Try Using PNG!')
        return redirect(request.url)

@app.route('/edit_course', methods=["POST","GET"])
def edit_course(cid=None):
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
                    db.editCourse(dict(request.form),coursefile,imagefile,ID)
            else:
                db.creatCourse(dict(request.form),coursefile,imagefile)
            return redirect("/course_grid")
        return 'not successful'
        
# -----------------Teachers-----------------

@app.route('/teachers')
def teachers():
    return render_template('teachers.html',teachers=db.teachers())

@app.route('/add_teacher', methods=["POST","GET"])
def add_teacher(tid=None):
    if request.method == "GET":
        return render_template('add_teacher.html',teacher={},action="add_teacher")
    else:
        if ('TeachersImage' not in request.files):
            flash('No file part')
            return redirect(request.url)
        imagefile = request.files['TeachersImage']
        if imagefile.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        info=ast.literal_eval(json.dumps(request.form.to_dict()))
        info["file"]=imagefile
        
        if imagefile and allowed_file(imagefile.filename,['png']):
            db.addTeacher(info)
            flash('Teacher added successfully, add new teacher')
            return redirect(request.url)
        flash('file format is not acceptable, try PNG!')
        return redirect(request.url)

@app.route('/edit_teacher', methods=["POST","GET"])
def edit_teacher(tid=None):
    if request.method == "GET":
        ID = request.args.get('ID','')
        teacher=db.teacher(ID)
        if teacher:
            return render_template('add_teacher.html',teacher=teacher,action="edit_teacher?ID={}".format(ID))
        else:
            return redirect('error404')
        
    else:
        if ('TeachersImage' not in request.files):
            flash('No file part')
            return redirect(request.url)
            
        imagefile = request.files['TeachersImage']
        # if imagefile.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)

        ID = request.args.get('ID','null')
        teacherInfo=ast.literal_eval(json.dumps(request.form.to_dict()))
        teacherInfo['ID']=ID
       
        if imagefile:
            if not(allowed_file(imagefile.filename,['png'])):
                flash('try PNG')
                return redirect(request.url)
            teacherInfo['file']=imagefile
        
        db.updateTeacher(teacherInfo)
        return redirect("/teachers_details?ID={}".format(ID))

@app.route('/teachers_details')
def teachers_details():
    ID = request.args.get('ID','guest')
    teacher=db.teacher(ID)
    otherTeachers=db.otherTeachers(ID)
    print otherTeachers ,'-'*10
    stat=db.stat()
    if teacher:
        return render_template('teachers-details.html',teacher=teacher, otherTeachers=otherTeachers,ID=ID , stats=db.stat())
    else:
        return redirect('/error404')

# -----------------Blogs-----------------

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
    return render_template('blog-sidebar.html',postData=postData, postInfo=postInfo, categoryTags=categoryTags, tagsCloud=tagsCloud, recentPosts=recentPosts)

@app.route('/single')
def single():
    return render_template('single.html')
    
@app.route('/single_blog')
def single_sidebar():
    ID = request.args.get('ID','guest')
    categoryTags = db.categoryTags()
    tagsCloud = db.tagsCloud()
    recentPosts = db.recentPost()
    postInfo = db.blogInfo()
    return render_template('single-blog.html', categoryTags=categoryTags, tagsCloud=tagsCloud, recentPosts=recentPosts, postInfo=postInfo)

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

@app.route('/edit_blog', methods=["POST", "GET"])
def edit_blog():
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

#-----------------Images/Gallery-----------------

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

#-----------------Register And Login-----------------

class RegistrationForm(Form):
    username = TextField("Username", [validators.Length(min=4, max=20)])
    email = TextField("Email Address", [validators.Length(min=6, max=50)])
    password = PasswordField("Password", [validators.Required(),validators.EqualTo('confirm', message="Passwords Must Match")])
    confirm = PasswordField("Repeat Password")
    accept_tos = BooleanField("I Accept The <a href='/tos'>Terms of Service</a> And The <a href='/privacy/'>Privacy Notice</a> (Last Updated Jan 15 2015)", [validators.Required()])

@app.route('/register', methods=['GET','POST'])
def register_page():
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            realUUID = str(uuid.uuid4())[:20]
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            activate = realUUID
            # c,conn = connection()
            # x = c.execute("SELECT * FROM users WHERE (username = (%s) OR email = (%s))",(thwart(username), thwart(email)))
            # y = c.fetchall()

            # if int(x) > 0:
            if True: # there is already a person with that name
                flash("That username or email is already taken, please choose another")
                return render_template('register.html', form=form)
            else:
                # add the user to db
                pass
                # c.execute("DELETE FROM users WHERE username=(%s)",(thwart(username)))
                # c.execute("DELETE FROM users WHERE email=(%s)",(thwart(email)))
                # c.execute("INSERT INTO users (username, password, email, activate, tracking) VALUES (%s, %s, %s, %s, %s)",
                # (thwart(username), thwart(password), thwart(email), thwart(activate), thwart("/introduction-to-python-programming/")))
                
                # conn.commit()
                # flash("Thanks for registering please check your email!!!")
                # c.close()
                # conn.close()
                # gc.collect()
                
                # session["username"] = username
                # session["email"] = email
                # session["activate"] = activate
                
                send_mail(myEmail,email,"Please Go To This Link To Verify Your Account:"+"\n"+"flaskblueprint-arshamalishirkouhi.c9users.io/verified/"+ realUUID) # has to be fixed
                return redirect('/') #"Please Check Your Email"
        return render_template("register.html", form=form)
    except Exception as e:
        return(str(e))

@app.route('/activate')
def activate():
    # get the activationCode
    # send the activation code to db to activate
    # flash back proper message coming from db
    pass

@app.route('/login')
def login():
    return render_template('login.html')

#-----------------Event-----------------

@app.route('/event_list')
def event_list():
    return render_template('event-list.html')
    
@app.route('/event_grid')
def event_grid():
    return render_template('event-grid.html')
    
@app.route('/event_details')
def event_details():
    return render_template('event-details.html')

#-----------------Stats-----------------

@app.route('/edit_stats', methods=["POST","GET"])
def edit_Stats():
    if request.method =="POST":
        db.updateStat(dict(request.form))
        return redirect(request.url)
    else:
        stat=db.stat()
        print stat,'-=-=-'*100
        return render_template('edit_stats.html', stats=stat)

@app.route('/test')
def test():
    return render_template('test.html')
    
@app.route('/test2', methods=["POST"])
def test2():
    return str(list(request.files['img']))
    
@app.route('/profile')
def profile():
    return render_template('profile.html')
    
@app.route('/forget_password')
def forget_password():
    return render_template('forget_password.html')

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0',port=8080)
