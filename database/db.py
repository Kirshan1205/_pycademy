
import pickle

with open('webDb.pkl','rb') as f:
    webDb=pickle.load(f)

def teachers():
    return webDb['teachers']
    
def teacher(ID):
    for teacher in webDb['teachers']:
        if teacher['ID']==ID:
            return teacher
    return False
    
def otherTeachers(ID):
    return webDb['teachers']