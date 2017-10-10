from flask import Flask, render_template
import base64

app=Flask(__name__)
 
with open("static/img/gallery/py2.jpg", "rb") as imageFile:
    strImage = base64.b64encode(imageFile.read())

    
with open("imageToSave2.png", "wb") as fh:
    fh.write(strImage.decode('base64'))
    
@app.route('/')
def index():
    with open("static/img/gallery/py2.jpg", "rb") as imageFile:
        strImage = base64.b64encode(imageFile.read())
        print strImage
    return render_template('indexBase64.html',strImage=strImage)
    
if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=8081)