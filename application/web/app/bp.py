import logging
from datetime import datetime

from flask import Blueprint, send_from_directory, request, jsonify

from .models import Cluster
from .utils import generate_signed_url

bp = Blueprint('endpoints', __name__)


@bp.route('/', methods=['GET'])
def index():
    return send_from_directory('./frontend/dist', 'index.html')

@bp.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('./frontend/dist/js', path)

@bp.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('./frontend/dist/assets', path)

@bp.route('/brief')
def brief():
    date = request.args.get('date')
    if not date:
        date = datetime.now()
    try:
        date = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        logging.info('invalid date')
        return jsonify({'error': 'invalid data'}), 400
    articles = Cluster.query.with_entities(
        Cluster.title, Cluster.content, Cluster.source, Cluster.cluster_num).filter(
        Cluster.publish_time == date).all()
    articles = sorted(articles, key=lambda x: x[3])
    articles = [{
        'title': title, 'content': content,
        'source': source}
        for title, content, source, _ in articles]
    audio_prefix = date.strftime('%Y_%m_%d_0')
    signed_url = generate_signed_url('dailybrief', f'audio/{audio_prefix}.wav')
    return jsonify({'articles': articles, 'audio_url': signed_url}), 200
