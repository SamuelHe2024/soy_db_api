import tensorflow as tf
import numpy as np
import keras
import os

from flask import Flask, render_template, request, jsonify
# from keras import preprocessing
# from keras import models
# from keras.models import load_model, loaded_model
# from keras.preprocessing import image
from werkzeug.utils import secure_filename


model = keras.models.load_model("soybeans.h5")

app = Flask(__name__)

def model_predict(img_path):
    #load the image, make sure it is the target size (specified by model code)
    img = keras.utils.load_img(img_path, target_size=(224,224))
    #convert the image to an array
    img = keras.utils.img_to_array(img)
    #normalize array size
    img /= 255           
    #expand image dimensions for keras convention
    img = np.expand_dims(img, axis = 0)

    #call model for prediction
    opt = keras.optimizers.RMSprop(learning_rate = 0.01)
    model.compile(optimizer = opt, loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
    pred = model.predict(img)
    return pred

def output_statement(pred):
    #need to figure out what the fuck the outputs are in order to write output statements.
    index = -1
    compareVal = -1
    for i in range(len(pred[0])):
        if(compareVal < pred[0][i]):
            compareVal = pred[0][i]
            index = i
    if index == 0:
        #output this range of days
        msg = 'Model Prediction: Your plant is within Day 9 and Day 12 of the growth cycle.'
    elif index == 1:
        #output this range
        msg = 'Model Prediction: Your plant is within Day 13 and Day 16 of the growth cycle.'
    elif index == 2:
        #output this range
        msg = 'Model Prediction: Your plant is within Day 17 and Day 20 of the growth cycle.'
    elif index == 3:
        #output this range
        msg = 'Model Prediction: Your plant is within Day 21 and Day 28 of the growth cycle.'
    else:
        return 'Error: Model sent prediction out of the prescribed range. Please try again.'
    return {"message": msg, "accuracy": compareVal}

#this is a basic link to an html and is the landing page at the moment. 
#want to change the landing page to be stylized with buttons that link to the other html pages
#May need to have additional app routes with this same code in it so that the buttons are available
#from all pages.
#Then, I need to add a button somewhere, or everywhere, to upload an image for the DL model 
@app.route("/predict", methods=['GET','POST'])
# def home():
#     if request.method == 'POST':
#         if request.form.get('action1') == 'Home':
#             return render_template('index.html') #this is the default or home page
#         elif request.form.get('action2') == 'How To Use':
#             return render_template('howtouse.html') #fill this in when howtouse.html is written
#         elif request.form.get('action3') == 'About':
#             return render_template('about.html') #this is the about page. can add additional things to it
#     elif request.method == 'GET':
#         return render_template('index.html')
#     return render_template("index.html")

# @app.route('/predict', methods = ['POST'])
def user_upload():
    if request.method == 'POST':
        #need to get image from POST request
        f = request.files["image"]
        # #create img_path to call model
        basepath = os.path.dirname(__file__)
        img_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(img_path)
        # #call model
        pred = model_predict(img_path)
        pred = pred.tolist()
        output = output_statement(pred)
        os.remove(img_path)
        return {"message": output["message"], "accuracy": output["accuracy"]}
        # response = {}
        # name = request.args.get("name", None)
        # if not name:
        #     response["ERROR"] = "No name found"
        # else:
        #     response["MESSAGE"] = f"Welcome {name} to our awesome API!"
        # return jsonify(response)

    elif request.method == 'GET':
        response = {}
        response["MESSAGE"] = "Soybean Prediciton API is running!"
        return response