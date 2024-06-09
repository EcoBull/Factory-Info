'''
app = Flask(__name__, template_folder='QC/templates')
app.config.from_object(config.Config)
# config.py 파일이 있는 경로를 지정해야 합니다.

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 모델 정의
class YourModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(20), nullable=False)
    qc_status = db.Column(db.String(20), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"YourModel(serial_number={self.serial_number}, qc_status={self.qc_status}, image_path={self.image_path}, date_added={self.date_added})"

# 라우트 정의
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_data/')
def get_data():
    data = YourModel.query.all()
    return jsonify([item.to_dict() for item in data])

if __name__ == "__main__":
    app.run(debug=True)

'''