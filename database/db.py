
import random,os,json,uuid
from pymongo import MongoClient
con = MongoClient("mongodb://maysam:0183552313@ds149479.mlab.com:49479/pycademy")
db = con.pycademy

# Reset DB

def resetDB():
    db.teachers.drop()
    db.courses.drop()
    db.images.drop()
    db.stat.drop()
    db.sidebar.drop()
    db.blogs.drop()
    return 'done!'

# Teachers

def teachers():
    return list(db.teachers.find())

def teacher(ID):
    return db.teachers.find_one({'tid':ID}) or {}


def otherTeachers(ID):
    return list(db.teachers.find({"tid":{"$ne": ID}}).limit(4))

def addTeacher(info,imgfile):
    tid='t{}'.format(db.teachers.count()+1)
    imagefilename= os.path.join('static/img/teacher-img/{}.png'.format(tid))
    info['tid']=tid
    info['image']=imagefilename
    imgfile.save(imagefilename)
    print info
    db.teachers.insert(info)
    return True

def updateTeacher(info,imgfile,ID):
    tid = ID
    imagefilename= os.path.join('static/img/teacher-img/{}.png'.format(tid))
    info['image']=imagefilename
    imgfile.save(imagefilename)
    print info
    db.teachers.update({"tid":tid}, {"$set":info})
    return True

# Courses

def courses():
    return list(db.courses.find())

def course(ID):
    c=db.courses.find_one({'cid':ID}) or {}
    c['prerequisite']=list(db.courses.find({"cid":{"$in":c['prerequisiteIDs']}}))
    c['relateds']=list(db.courses.find({"cid":{"$in":c['relatedIDs']}}))
    return c
    
def creatCourse(info,coursefile,imgfile):
    cid="c{}".format(db.courses.count()+1)

    coursefilename = os.path.join('static/files/course-plans/{}.pdf'.format(cid))
    imagefilename= os.path.join('static/img/course-img/{}.png'.format(cid))
    imgfile.save(imagefilename)
    coursefile.save(coursefilename)

    info['cid']=cid
    info['image']=imagefilename
    info['coursePlan']=coursefilename
    print info
    db.courses.insert(info)
    return True
    
def editCourse(info,coursefile,imgfile,ID):
    cid=ID
    coursefilename = os.path.join('static/files/course-plans/{}.pdf'.format(cid))
    imagefilename= os.path.join('static/img/course-img/{}.png'.format(cid))
    imgfile.save(imagefilename)
    coursefile.save(coursefilename)
    info['image']=imagefilename
    info['coursePlan']=coursefilename
    db.courses.update({"cid":cid}, {"$set":info})
    return True

# Images/Gallery

def images():
    return list(db.images.find())

# Blogs

def tagsCloud():
    return ["event","workshop","e-commerce"]
    
def categoryTags():
    return ["business","education","tourist"]

def recentPost():
    return [{"image":"bla.jpg", "title":"7 Quick Ways to Make a Great Event Fail", "time":"25 min ago"},{"image":"bla.jpg", "title":"How to Pick the Wrong Event Titles for Your Events", "time":"48 min ago"},{"image":"bla.jpg", "title":"Science & IT Fair Going Away From Your University", "time":"55 min ago"}]

def blogInfo():
    return list(db.blogs.find())

def blog(ID):
    return db.blogs.find_one({'bid':ID}) or {}

def blogSidebarInfo():
    posts = []
    postsDirs = os.walk(os.getcwd()+'/database/blogs').next()
    for postDir in postsDirs[1]:
        post = "{}/{}/post.json".format(postsDirs[0],postDir)
        with open(post) as a:
             posts.append(json.load(a))
    return posts
    
def addBlog(info,imgfile):
    bid=uuid.uuid4()
    imagefilename= os.path.join('static/img/blog-img/{}.png'.format(bid))
    info['bid']=bid
    info['image']=imagefilename
    imgfile.save(imagefilename)
    print info
    db.blogs.insert(info)
    return True
    
# Stat

def updateStat(stat):
    # stat={"data":"general",
    #     "countTeachers":db.teachers.count(),
    #     "countCourses":db.courses.count(),
    #     "countStudents":db.students.count(),
    #     "countBlogs":db.blogs.count(),
    #     "countEvents":db.Events.count()}
    stat["data"]="general"
    db.stats.drop()
    db.stats.insert(stat)
    return str(stat)
    
def stat():
    try:
        return db.stats.find({"data":"general"}).next()
    except:
        return {}
