from flask import Flask,render_template,request
from tensorflow.keras.utils import img_to_array,load_img
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
app=Flask(__name__)

model=load_model('/media/revanth/Data/Jupyter/flower.h5')

IMAGE_SIZE=64
IMAGE_FOLDER=os.path.join('static','images')
app.config['UPLOAD_FLODER']=IMAGE_FOLDER
ALLOWED_EXTENSIONS={'png','jpg','jpeg'}
class_indices = {'early_blight': 0, 'healthy': 1, 'late_blight': 2}
class_names = ['early_blight', 'healthy', 'late_blight']

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def predict():
    
    for f in os.listdir('static/images'):
        os.remove(os.path.join('static/images', f))

    imagefile = request.files['imagefile']

    if(not imagefile):
        return render_template('index.html', nofile="error")
    
    if(not allowed_file(imagefile.filename)):
        return render_template('index.html', notimage="error")

    
    full_image_path = os.path.join(app.config['UPLOAD_FLODER'], imagefile.filename)
    imagefile.save(full_image_path)
    image = load_img(full_image_path, target_size=(IMAGE_SIZE,IMAGE_SIZE))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    

    result = model.predict(image)
    print(result)
    a=""
    if result[0][0]==1:
        a="This is Daisy"
    elif result[0][1]==1:
        a="This is Dandelion"
    elif result[0][2]:
        a="This is Rose"
    elif result[0][3]==1:
        a="This is Sunflower"
    elif result[0][4]==1:
        a="This si Tulip"



    return render_template('index.html', image=full_image_path,prediction=a)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host='0.0.0.0', port=8000)

