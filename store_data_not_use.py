
# import firebase_admin
# from firebase_admin import credentials, firestore
# from QC import create_app, db
# from QC.models import YourModel
# from datetime import datetime
# from flask_socketio import SocketIO, emit

# # Firebase 초기화
# cred = credentials.Certificate('factory-info-a8045-firebase-adminsdk-e52rt-53ce709c19.json')
# # firebase_admin.initialize_app(cred)
# # db_firestore = firestore.client()
# # myflask\factory-info-a8045-firebase-adminsdk-e52rt-53ce709c19.json
 
# socketio = None  # SocketIO 인스턴스를 나중에 할당

# def on_snapshot(doc_snapshot, changes, read_time):
#     print("Start a on_snapshot...")
#     for change in changes:
#         data = change.document.to_dict()
#         serial_number = data.get('serial number')
#         qc_status = data.get('QC')
#         image_path = data.get('img')
#         date_added = datetime.utcnow()

#         if change.type.name == 'ADDED':
#             print("added a Data...")
#             new_data = {
#                 'serial_number': serial_number,
#                 'qc_status': qc_status,
#                 'image_path': image_path,
#                 'date_added': date_added.isoformat()
#             }
#             socketio.emit('new_data', new_data)
#             print(f"New data added: {serial_number}, {qc_status}")

#         elif change.type.name == 'MODIFIED':
#             print("modified a Data...")
#             modified_data = {
#                 'serial_number': serial_number,
#                 'qc_status': qc_status,
#                 'image_path': image_path,
#                 'date_added': date_added.isoformat()
#             }
#             socketio.emit('modified_data', modified_data)
#             print(f"Data modified: {serial_number}, {qc_status}")

#         elif change.type.name == 'REMOVED':
#             print("remove a Data...")
#             removed_data = {
#                 'serial_number': serial_number
#             }
#             socketio.emit('removed_data', removed_data)
#             print(f"Data removed: {serial_number}")

# def listen_to_firestore(socketio_instance):
#     global socketio
#     socketio = socketio_instance
#     print("Listening to Firestore for updates...")
#     doc_ref = db_firestore.collection('factory-info')
#     doc_ref.on_snapshot(on_snapshot)
