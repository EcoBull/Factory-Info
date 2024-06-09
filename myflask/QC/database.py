# databse
from myflask import db, TrafficSystem

# 데이터베이스 생성
db.create_all()

# 예시 데이터 추가
traffic_system = TrafficSystem(name='Example', serial_number='1234567890', size='M', line='#1', judgement='Passed', image_path='example.jpg')
db.session.add(traffic_system)
db.session.commit()
