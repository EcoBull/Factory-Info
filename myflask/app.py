# flask server
from flask import Flask, render_template, jsonify, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
import config
from flask_socketio import SocketIO, emit
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app, storage
import csv
import requests
from flask import send_from_directory
from flask import request
import cv2
import base64
from datetime import datetime, timedelta


PROJECT_ID = "factory-info-a8045"
DB_IMG_DIR = "factory-info-a8045.appspot.com/images"
UPLOAD_FOLDER = 'images'

# 새로운 JSON 키 파일의 경로
cred = credentials.Certificate('factory-info-a8045-firebase-adminsdk-e52rt-53ce709c19.json')
default_app = firebase_admin.initialize_app(cred, {'storageBucket': f"{PROJECT_ID}.appspot.com"})
app = Flask(__name__, template_folder='QC/templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'

collection_name = 'factory_info'
local_directory = 'new_images'

# Firebase 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate(cred)
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'factory-info-a8045.appspot.com'
    })

db = firestore.client()
bucket = storage.bucket()

def make_blob_public_and_get_url(blob):
    # 파일이 존재하는지 확인
    if not blob.exists():
        print("The specified file does not exist.")
        return None

    # 파일을 공개로 설정
    blob.make_public()

    # 공개 URL 가져오기
    public_url = blob.public_url
    return public_url

def download_image(url, local_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image downloaded and saved to {local_path}")
    else:
        print("Failed to download the image")

def download_all_images_from_bucket(local_dir):
    blobs = bucket.list_blobs(prefix='images/')
    
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    
    for blob in blobs:
        if blob.name.endswith('/'):
            # This is a directory, skip it
            continue
        
        print(f"Processing {blob.name}")
        public_url = make_blob_public_and_get_url(blob)
        local_path = os.path.join(local_dir, os.path.basename(blob.name))
        download_image(public_url, local_path)

# Function to get data from Firestore
def get_data_from_database():
    docs = db.collection(collection_name).stream()
    data = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    return data

# Function to encode image to base64
def encode_image(filepath):
    img = cv2.imread(filepath)
    _, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer).decode('utf-8')
    return img_str

@app.route('/')
def index():
    data = get_data_from_database()
    
    # Construct image paths dynamically
    for entry in data:
        entry['img'] = f"/api/get_image/{entry['id']}.jpg"  # 이미지 파일의 동적 경로 생성
    
    # Write data to CSV
    csv_file_path = 'data.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    return render_template('index.html', data=data)

@app.route('/api/get_image/<filename>')
def get_image(filename):
    file_path = f"myflask/images/{filename}"
    url = get_image_download_url(file_path)
    if url:
        return jsonify({'url': url}), 200
    else:
        return jsonify({'error': 'Image not found'}), 404

# Function to get image download URL
def get_image_download_url(file_path):
    blob = bucket.blob(file_path)

    # 파일이 존재하는지 확인
    if not blob.exists():
        print("The specified file does not exist.")
        return None

    # URL 생성 (토큰 포함)
    download_url = blob.generate_signed_url(timedelta(seconds=300), method='GET')
    return download_url

@app.route('/api/get_data/')
def get_data():
    data = get_data_from_database()
    download_all_images_from_bucket(local_dir=local_directory )
    
    return jsonify(data)

if __name__ == '__main__':
    app.run()

    #     last_fail = next((item for item in reversed(data) if item['QC'] == 'FAIL'), None)
    # if last_fail:
    #     flash(f"Defective production : {last_fail['QC']}, {last_fail['id']}")
    # download_all_images_from_bucket(local_dir=local_directory)