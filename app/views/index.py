from flask import render_template, Blueprint
from flask_login import login_required, current_user
from .. import app_info
from flask import request, redirect, url_for
from ..search import elastic_search as search_method
from .. import log
from .. import config
import random

index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET'])
# @login_required
def index():
    categories = config.config['categories']
    top_level_cat = list(categories.keys())
    print(top_level_cat)
    return render_template('index.html', app_info=app_info, user=current_user, top_level_cat=top_level_cat)

@index_bp.route('/handle_form', methods=['POST'])
def handle_form():
    q = request.form['query']
    categories = request.form.getlist('top_level_cat')

    if 'search_button' in request.form:
        return redirect(url_for('index.search', q=q, c=categories))
    elif 'lucky_button' in request.form:
        return redirect(url_for('index.lucky', q=q))
    return redirect(url_for('index.search', q=q, c=categories))

@index_bp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    c = request.args.getlist('c')
    log.query_log(q)
    results = search_method(q, c)
    return render_template('search.html', app_info=app_info, user=current_user, q=q,results=results)

@index_bp.route('/lucky', methods=['GET'])
def lucky():
    q = request.args.get('q')
    log.query_log(q)
    results = search_method(q)
    rand = random.randint(0, len(results))
    url = results[rand]['doc']['url']
    return redirect(url_for('index.url', l=url))

@index_bp.route('/url', methods=['GET'])
def url():
    idx = request.args.get('i')
    l = request.args.get('l')
    log.click_log(idx, l)
    return redirect(l)

