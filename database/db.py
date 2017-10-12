
import pickle,random,os,json
from pymongo import MongoClient
con = MongoClient("mongodb://maysam:0183552313@ds149479.mlab.com:49479/pycademy")
db = con.pycademy

with open('webDb.pkl','rb') as f:
    webDb=pickle.load(f)
    


def teachers():
    c=db.teachers.find()
    teachers=[]
    while True:
        try:
            t=c.next()
            # teachers.add(t)
            teachers.append(t)
        except:
            break
    return teachers

def teacher(ID):
    t=db.teachers.find_one({'tid':ID.lower()})
    if t:
        return t
    else:
        return {}
    # return webDb['teachers'].get(ID.lower(),False)
    

    
def otherTeachers(ID):
    c=db.teachers.find({"tid":{"$ne": ID}}).limit(4)
    teachers=[]
    while True:
        try:
            t=c.next()
            # teachers.add(t)
            teachers.append(t)
        except:
            break
    return teachers
    # teachers=dict(webDb['teachers'])
    # try:
    #     del(teachers[ID.lower()])
    # except:
    #     pass

    # if len(teachers)<5:
    #     return teachers
    # else:
    #     return {i:teachers[i] for i in random.sample(teachers,4)}
    
def courses():
    c=db.courses.find()
    courses=[]
    while True:
        try:
            C=c.next()
            # teachers.add(t)
            courses.append(C)
        except:
            break
    return courses
    # return webDb['courses']

def course(ID):
    c=db.courses.find_one({'cid':ID})
    if c:

        pr=db.courses.find({"cid":{"$in":c['prerequisiteIDs']}})
        prc=[]
        while True:
            try:
                p=pr.next()
                prc.append(p)
            except:
                break
        c['prerequisite']=prc
        
        pr=db.courses.find({"cid":{"$in":c['relatedIDs']}})
        prc=[]
        while True:
            try:
                p=pr.next()
                prc.append(p)
            except:
                break
        c['relateds']=prc
        return c
    else:
        return {}
    # return webDb['courses'].get(ID,False)

    
def images():
    c=db.images.find()
    images=[]
    while True:
        try:
            i=c.next()
            # teachers.add(t)
            images.append(i)
        except:
            break
    return images
    # return webDb['images']

def tagsCloud():
    return ["event","workshop","e-commerce"]
    
def categoryTags():
    return ["business","education","tourist"]

def recentPost():
    return [{"image":"bla.jpg", "title":"7 Quick Ways to Make a Great Event Fail", "time":"25 min ago"},{"image":"bla.jpg", "title":"How to Pick the Wrong Event Titles for Your Events", "time":"48 min ago"},{"image":"bla.jpg", "title":"Science & IT Fair Going Away From Your University", "time":"55 min ago"}]

def blogInfo():
    c=db.blogs.find()
    blogs=[]
    while True:
        try:
            i=c.next()
            # teachers.add(t)
            blogs.append(i)
        except:
            break
    return blogs
    
def blogSidebarInfo():
    posts = []
    postsDirs = os.walk(os.getcwd()+'/database/blogs').next()
    for postDir in postsDirs[1]:
        post = "{}/{}/post.json".format(postsDirs[0],postDir)
        with open(post) as a:
             posts.append(json.load(a))
    return posts
    
    
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
    
def addTeacher(info,imgfile):
    tid='t{}'.format(db.teachers.count()+1)
    imagefilename= os.path.join('static/img/teacher-img/{}.png'.format(tid))
    info['tid']=tid
    info['image']=imagefilename
    imgfile.save(imagefilename)
    print info
    db.teachers.insert(info)
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

def updateTeacher(info,imgfile,ID):
    tid = ID
    imagefilename= os.path.join('static/img/teacher-img/{}.png'.format(tid))
    info['image']=imagefilename
    imgfile.save(imagefilename)
    print info
    db.teachers.update({"tid":tid}, {"$set":info})
    return True
    
def addBlog(info,imgfile):
    bid='t12'
    imagefilename= os.path.join('static/img/blog-img/{}.png'.format(bid))
    info['bid']=bid
    info['image']=imagefilename
    imgfile.save(imagefilename)
    print info
    db.blogs.insert(info)
    return True
    
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
    # db.stats.update_one({"data":"general"},{'$set':stat}, upsert=False)
    return str(stat)
    
def stat():
    try:
        return db.stats.find({"data":"general"}).next()
    except:
        return {}
    # return db.stats.find({"sid":"participationStat"}).next()
