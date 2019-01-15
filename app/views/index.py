from flask import render_template, Blueprint
from flask_login import login_required, current_user
from .. import app_info
from flask import request, redirect, url_for

from gsearch.googlesearch import search as gsearch
from .. import log

index_bp = Blueprint('index', __name__)


@index_bp.route('/', methods=['GET'])
# @login_required
def index():
    return render_template('index.html', app_info=app_info, user=current_user)

@index_bp.route('/handle_form', methods=['POST'])
def handle_form():
    q = request.form['query']
    return redirect(url_for('index.search', q=q))

@index_bp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    log.query_log(q)
    results = gsearch(q)
    return render_template('search.html', app_info=app_info, user=current_user, q=q,results=results)

@index_bp.route('/url', methods=['GET'])
def url():
    idx = request.args.get('i')
    l = request.args.get('l')
    log.click_log(idx, l)
    return redirect(l)

