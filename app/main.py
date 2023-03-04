import tensorflow as tf
import numpy as np
import keras
import os
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import app.db as data
from app.util.helpers import upload_file_to_s3

AWS_BUCKET_NAME=os.getenv('AWS_BUCKET_NAME')
AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY=os.getenv('AWS_SECRET_KEY')
AWS_LOCATION=os.getenv('AWS_LOCATION')

model = keras.models.load_model("soybeans.h5")

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['S3_BUCKET'] = AWS_BUCKET_NAME
app.config['S3_KEY'] = AWS_ACCESS_KEY
app.config['S3_SECRET'] = AWS_SECRET_KEY
app.config['S3_LOCATION'] = AWS_LOCATION
# app.config['S3_BUCKET'] = os.getenv('AWS_BUCKET_NAME')
# app.config['S3_KEY'] = os.getenv('AWS_ACCESS_KEY')
# app.config['S3_SECRET'] = os.getenv('AWS_SECRET_KEY')
# app.config['S3_LOCATION'] = os.getenv('AWS_BUCKET_NAME')


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

@app.route("/upload", methods=['POST'])
def user_upload():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files[]')
        for file in uploaded_files:
            if file.filename == '':
                return "No selected file"
            output = upload_file_to_s3(file)
            if output:
                print("uploaded")
            else:
                print("not uploaded")
        return ""

@app.route("/predict", methods=['GET','POST'])
def user_predict():
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
def dry_weight():
    if request.method == 'GET':
        raw_data = data.get_dry_weight()
        response = {"row_data":[]}
        columns = ["id", "solution", "dry weight"]
        for row in raw_data:
            append_obj = {}
            for i in range (len(columns)):
                append_obj[columns[i]] = row[i]
            response['row_data'].append(append_obj)
    return response
    
    
@app.route("/db/water_uptake", methods=['GET','POST'])
def water_uptake():
    if request.method == 'GET':
        raw_data = data.get_water_uptake()
        response = {"row_data":[]}
        columns = ["id","solution","uptake amount"]
        for row in raw_data:
            append_obj = {}
            for i in range (len(columns)):
                append_obj[columns[i]] = row[i]
            response['row_data'].append(append_obj)
        return response
    
    
@app.route("/db/solution_data", methods=['GET','POST'])
def solution_data():
    if request.method == 'GET':
        raw_data = data.get_solution_data()
        response = {"row_data":[]}
        columns = ["id","solution", "concentration", "calcium", "magnesium", "sodium", "potassium", "boron", "co_3", "hco_3", "so_4", 
                   "chlorine", "no3_n", "phosphorus", "ph", "conductivity", "sar", "iron", "zinc", "copper", "manganese", "arsenic",
                   "barium", "nickel","cadmium", "lead", "chromium", "fluorine", "cb"]
        for row in raw_data:
            append_obj = {}
            for i in range (len(columns)):
                append_obj[columns[i]] = row[i]
            response['row_data'].append(append_obj)
        return response

@app.route("/db/image_data", methods=['GET','POST'])
def image_data():
    if request.method == 'GET':
        response = data.get_image_data()
        return response