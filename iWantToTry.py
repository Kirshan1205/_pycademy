import os,json

# print os.getcwd()

# print os.listdir(os.getcwd())
dirs=os.walk(os.getcwd()+'/database/courses').next()


for d in dirs[1]:
    jsonAddress= '/home/ubuntu/workspace/database/courses/{}/course_details.json'.format(d) 
    with open(jsonAddress) as f:
        courseDetail= json.load(f)
    courseDetail['image']= '/home/ubuntu/workspace/database/courses/{}/course_image.jpg'.format(d) 
    courseDetail['course_plan']= '/home/ubuntu/workspace/database/courses/{}/course_plan.pdf'.format(d) 
    print courseDetail

print "-"*100
imageDirs=os.walk(os.getcwd()+'/static/img/gallery/').next()
images={}
for i,d in enumerate(imageDirs[2]):
    images[i] = {"address":"/static/img/gallery/" + d}
