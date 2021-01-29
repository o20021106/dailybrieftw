from flask import Blueprint, send_from_directory

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
