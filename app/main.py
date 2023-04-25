import numpy as np
import os
import json
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import app.db as data
from app.util.helpers import upload_file_to_s3, read_files_from_s3

AWS_BUCKET_NAME=os.getenv('AWS_BUCKET_NAME')
AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY=os.getenv('AWS_SECRET_KEY')
AWS_LOCATION=os.getenv('AWS_LOCATION')

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['S3_BUCKET'] = AWS_BUCKET_NAME
app.config['S3_KEY'] = AWS_ACCESS_KEY
app.config['S3_SECRET'] = AWS_SECRET_KEY
app.config['S3_LOCATION'] = AWS_LOCATION

@app.route("/upload", methods=['POST'])
def user_upload():
    if request.method == 'POST':
        uploaded_predictions = json.loads(request.form.get('predictions'))
        uploaded_files = request.files.getlist('files[]')
        for pred in uploaded_predictions:
            filename = pred['filename']
            filename = filename.replace(" ", "_")
            image_url = "https://soy-api-s3.s3.us-east-2.amazonaws.com/" + filename
            segmented_url = "https://soy-api-s3.s3.us-east-2.amazonaws.com/" + filename
            data.insert_image_data(filename,pred["prediction"], image_url, segmented_url, pred["accuracy"])
        
        # change the filename to the segmented filename eventually
        for file in uploaded_files:
            if file.filename == '':
                return "No selected file"
            output = upload_file_to_s3(file)
            if output:
                print("uploaded {}",file.filename)
            else:
                print("not uploaded")
        return ""

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
    if request.method == 'POST':
        raw_data = json.loads(request.form.get('inputFields'))
        for i in raw_data:
            data.insert_dry_weight(i['solution'], i['dryWeight'])
        return {"INSERTED DATA": "VALID"}
    
    
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
    if request.method == 'POST':
        solution = request.form.get('solution')
        recordDate = request.form.get('recordDate')
        uptakeAmount = request.form.get('uptakeAmount')
        data.insert_water_uptake(solution,uptakeAmount,recordDate)
        return {"Succesffully inserted data"}
    
    
@app.route("/db/solution_data", methods=['GET','POST'])
def solution_data():
    if request.method == 'GET':
        columns = ["id","solution","calcium", "magnesium", "sodium", "potassium", "boron", "co_3", "hco_3", "so_4", 
                   "chlorine", "no3_n", "phosphorus", "ph", "conductivity", "sar", "iron", "zinc", "copper", "manganese", "arsenic",
                   "barium", "nickel","cadmium", "lead", "chromium", "fluorine", "cb"]
        raw_data = data.get_solution_data()
        response = {"row_data":[]}
        for row in raw_data:
            append_obj = {}
            for i in range (len(columns)):
                append_obj[columns[i]] = row[i]
            response['row_data'].append(append_obj)
        return response
    if request.method == 'POST':
        values = {"Calcium" : ""}
        columns = [ 'solution',
                    'Calcium',
                    'Magnesium',
                    'Sodium',
                    'Potassium',
                    'Boron',
                    'CO_3',
                    'HCO_3',
                    'SO_4',
                    'Chlorine',
                    'NO3_n',
                    'Phosphorus',
                    'pH',
                    'Conductivity',
                    'SAR',
                    'Iron',
                    'Zinc',
                    'Copper',
                    'Manganese',
                    'Arsenic',
                    'Barium',
                    'Nickel',
                    'Cadmium',
                    'Lead',
                    'Chromium',
                    'Fluorine',
                    'Cb']
        for col in columns:
            if(col != "solution"):
                values[col] = int(request.form.get(col))
            else:
                values[col] = request.form.get(col)
        data.insert_solution_data(**values)
        return {}

@app.route("/db/image_data", methods=['GET','POST'])
def image_data():
    if request.method == 'GET':
        raw_data = data.get_image_data()
        response = {"row_data":[]}
        columns = ["id","image_name", "day_prediction", "image_url", "segmented_image_url",  "accuracy"]
        for row in raw_data:
            append_obj = {}
            for i in range (len(columns)):
                append_obj[columns[i]] = row[i]
            response['row_data'].append(append_obj)
        return response
    
@app.route("/db/interpolated_data", methods=['GET','POST'])
def interpolated_data():
    if request.method == 'GET':
        raw_data = data.get_image_data()
        print(raw_data)
        response = {"row_data":[]}
        columns = ["id","image_name", "day_prediction", "image_url", "segmented_image_url",  "accuracy"]
        for row in raw_data:
            append_obj = {}
            for i in range (len(columns)):
                append_obj[columns[i]] = row[i]
            response['row_data'].append(append_obj)
        return response

@app.route("/db/image_data/<id>", methods=['GET'])
def image(id):
    if request.method == 'GET':
        raw_data = data.get_image(id)
        response = {"raw_data":[]}
        columns = ["id","image_name", "day_prediction", "image_url", "segmented_image_url",  "accuracy"]
        for i in range (len(raw_data)):
            response["raw_data"].append({columns[i] : raw_data[i]})
        return response