import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static\images')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    # UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static\images')  # 이미지 업로드 디렉토리 설정
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 허용된 이미지 확장자 설정
    SQLALCHEMY_TRACK_MODIFICATIONS = False


#print(BASE_DIR) : c:\Users\user\Desktop\flask_project\myflask
