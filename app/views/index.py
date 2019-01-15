from flask import render_template, Blueprint
from flask_login import login_required, current_user
from .. import app_info

index_bp = Blueprint('index', __name__)


@index_bp.route('/', methods=['GET'])
# @login_required
def index():
    return render_template('index.html', app_info=app_info, user=current_user)
