'''
# store_data.py
import firebase_admin
from firebase_admin import credentials, firestore
from QC import create_app, db
from QC.models import YourModel
from datetime import datetime  # datetime 임포트 추가

# Firebase 설정
cred = credentials.Certificate('factory-info-a8045-firebase-adminsdk-e52rt-53ce709c19.json')
firebase_admin.initialize_app(cred)

# Firestore 클라이언트 초기화
db_firestore = firestore.client()

# Flask 앱 생성
app = create_app()

def store_data():
    with app.app_context():
        # Firestore 데이터 가져오기
        docs = db_firestore.collection('factory-info').stream()

        for doc in docs:
            data = doc.to_dict()
            # Firestore 데이터 구조에 따라 데이터 추출
            serial_number = data.get('serial number')
            qc_status = data.get('QC')
            image_path = data.get('img')
            
            # 데이터베이스에 저장
            new_entry = YourModel(serial_number=serial_number, qc_status=qc_status, image_path=image_path, date_added=datetime.utcnow())
            db.session.add(new_entry)
            db.session.commit()
            print("Data stored successfully.")

if __name__ == "__main__":
    store_data()




========================================================================


# store_data.py

import firebase_admin
from firebase_admin import credentials, firestore
from QC import create_app, db
from QC.models import YourModel
from datetime import datetime  # datetime 임포트 추가

# Firebase 설정
cred = credentials.Certificate('factory-info-a8045-firebase-adminsdk-e52rt-53ce709c19.json')
firebase_admin.initialize_app(cred)

# Firestore 클라이언트 초기화
db_firestore = firestore.client()

# Flask 앱 생성
app = create_app()

def on_snapshot(doc_snapshot, changes, read_time):
    with app.app_context():
        for change in changes:
            if change.type.name == 'ADDED':
                data = change.document.to_dict()
                serial_number = data.get('serial number')
                qc_status = data.get('QC')
                image_path = data.get('img')

                # 데이터베이스에 저장
                new_entry = YourModel(serial_number=serial_number, qc_status=qc_status, image_path=image_path, date_added=datetime.utcnow())
                db.session.add(new_entry)
                db.session.commit()
                print(f"New data added: {serial_number}, {qc_status}")

            elif change.type.name == 'MODIFIED':
                # 데이터 수정 로직 추가 (필요 시)
                print(f"Modified data: {change.document.id}")
                
            elif change.type.name == 'REMOVED':
                # 데이터 삭제 로직 추가 (필요 시)
                print(f"Removed data: {change.document.id}")

def listen_to_firestore():
    doc_ref = db_firestore.collection('factory-info')
    doc_ref.on_snapshot(on_snapshot)

if __name__ == "__main__":
    listen_to_firestore()
    print("Listening to Firestore for updates...")


'''


