from flask import Blueprint, jsonify

from functions import load_posts, new_get_post_by_pk
from logger import get_logger

api_bp = Blueprint(name='api_bp', url_prefix='/api', import_name='/api_bp')
logger = get_logger('api_bp')


@api_bp.route('/post/')
def api_posts():
    posts = load_posts()
    logger.info('load posts')
    return jsonify(posts)


@api_bp.route('/post/<int:pk>')
def api_post(pk):
    post = new_get_post_by_pk(pk)
    logger.info('load post {pk}')
    return jsonify(post)
