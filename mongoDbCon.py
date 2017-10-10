from pymongo import MongoClient
con = MongoClient("mongodb://maysam:0183552313@ds149479.mlab.com:49479/pycademy")
db = con.pycademy

# collectionNames = db.collection_names()
# for colName in collectionNames[1:]:
#     c=db[colName].find()
#     print colName
#     print '-'*50
#     while True:
#         try:
#             print c.next()
#         except:
#             break


# course={
#     "title": "baking cake",
#     "cid":"baking",
#     "description": "I am awesome in getting my friend to cook",
#     "teacherID": "tabitha",
#     "price": "RM600",
#     "enrolled": "20",
#     "duration": "4 Months",
#     "seats": "200",
#     "start": "17th January 2017",
#     "end": "26th May 2017",
#     "location": "Kidocode",
#     "overview": "",
#     "longDescription": "",
#     "prerequisiteIDs": ["Python", "Pythonwebdev"],
#     "relatedIDs": ["Cooking", "b", "c"]
# }

#db.courses.drop()
# db.teachers.drop()
# print list(db.teachers.find())
#db.courses.drop()
print 'this is it',db.sttttt.count()
print 'this is it',list(db.courses.find({},{"cid":1, "_id":0}))[:20]

# db.courses.delete_one({"title":"asrf"})

# print db.courses.find_one({"tid":"kirshan"})
# courses = []
# for c in db.courses.find():
#     courses.append(c)

# for Course in courses:
#     print Course['title'].title()
    
    
# print "-"*100

# update stat

# newStat={u'complete': 13, u'freeCourses': 565, u'studentEnrolled': 1300, u'teachers': 900, u'sid': u'participationStat'}
# db.stats.update_one({"sid":"participationStat"},{"$set":newStat},upsert=False)
# print "-"*100

# print db.stats.find({"sid":"participationStat"}).next()



# ------update teachers -------
# newTeacher= {"tid":"tabitha",
#             "name": "Tabitha Yap Cho",
#             "image": "arsham",
#             "fb": "http:\\\\fb.com\\wolfisam",
#             "twitter": "http:\\\\fb.com\\pycademy",
#             "skype": "0060183552313",
#             "dribbble": "http:\\\\fb.com\\pycademy",
#             "position": "junior lecturer",
#             "details": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit,sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.Ut wisi enim ad minim veniam,quis nostrud exerci tation ullamcorper suscipit lobortis nisl",
#             "youtube": "http:\\\\youtube.com\\pycademy"}
            
# db.teachers.update_one({"tid":"tabitha"},{"$set":newTeacher},upsert=False)
# print "-"*100

# print db.teachers.find({"tid":"tabitha"}).next()
