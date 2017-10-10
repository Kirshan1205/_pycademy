import pickle, json, pprint, os
from pymongo import MongoClient
con = MongoClient("mongodb://maysam:0183552313@ds149479.mlab.com:49479/pycademy")
db = con.pycademy
pp= pprint.PrettyPrinter(indent=4)

dirs=os.walk(os.getcwd()+'/database/courses').next()

#  ----- reading db from json file------

with open('db.json') as f:
    print f
    webDb= json.load(f)

# ----- reading courses from courses directory -------
courses={}
for d in dirs[1]:
    jsonAddress= '/home/ubuntu/workspace/database/courses/{}/course_details.json'.format(d) 
    with open(jsonAddress) as f:
        courseDetail= json.load(f)
    courseDetail['image']= '/home/ubuntu/workspace/database/courses/{}/course_image.jpg'.format(d) 
    courseDetail['course_plan']= '/home/ubuntu/workspace/database/courses/{}/course_plan.pdf'.format(d) 
    courses[d]=courseDetail

# course detail enrichment
for ID,course in courses.iteritems():
    course['teacher']=webDb["teachers"][course['teacherID'].lower()]['name']

# course detail enrichment
for ID,course in courses.iteritems():
    course['teacher']=webDb["teachers"][course['teacherID'].lower()]['name']


# --------------reading images from gallery --------
imageDirs=os.walk(os.getcwd()+'/static/img/gallery/').next()
images={}
for i,d in enumerate(imageDirs[2]):
    images[i] = {"address":"/static/img/gallery/" + d}

    
webDb['courses']=courses    
webDb['images']=images

db.teachers.drop()
db.courses.drop()
db.images.drop()

teachers = db.teachers
for tid, teacher in webDb['teachers'].iteritems():
    teacher['tid']=tid
    teachers.insert(teacher)

courses = db.courses
for cid, course in webDb['courses'].iteritems():
    course['cid']=cid
    courses.insert(course)

images = db.images
for iid, image in webDb['images'].iteritems():
    image['iid']=iid
    images.insert(image)

blogs = db.blogs
postsDirs = os.walk(os.getcwd()+'/database/blogs').next()
for postDir in postsDirs[1]:
    post = "{}/{}/post.json".format(postsDirs[0],postDir)
    with open(post) as a:
        blogs.insert(json.load(a))
    
stats = db.stats
for sid, stat in webDb['stat'].iteritems():
    stat['sid']=sid
    stats.insert(stat)

pp.pprint(webDb)


# ------- save to db ------

with open('webDb.pkl','wb') as f:
    pickle.dump(webDb, f , pickle.HIGHEST_PROTOCOL)