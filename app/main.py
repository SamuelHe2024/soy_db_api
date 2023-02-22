import tensorflow as tf
import numpy as np
import keras
import os
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import app.db as data



model = keras.models.load_model("soybeans.h5")

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

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

@app.route("/predict", methods=['GET','POST'])
def user_upload():
    output = {}
    if request.method == 'POST':
        #need to get image from POST request
        f = request.files["image"]
        print(request.files)
        # #create img_path to call model
        basepath = os.path.dirname(__file__)
        img_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(img_path)
        # #call model
        pred = model_predict(img_path)
        pred = pred.tolist()
        output = output_statement(pred)
        os.remove(img_path)
        output = {"message": output["message"], "accuracy": output["accuracy"]}
        return {"message": output["message"], "accuracy": output["accuracy"]}

    elif request.method == 'GET':
        response = output
        response["MESSAGE"] = "API is running!"
        return response
    
@app.route("/db/dry_weight", methods=['GET','POST'])
def database_info():
    if request.method == 'GET':
        response = data.get_dry_weight()
        return response