# QC/views/main_views.py

from flask import Blueprint, render_template
from QC.models import YourModel

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    # 데이터베이스에서 모든 데이터 가져오기
    data = YourModel.query.all()
    return render_template('index.html', data=data)
