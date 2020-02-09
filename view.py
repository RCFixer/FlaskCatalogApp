from flask import render_template
from flask import request
from flask import redirect, url_for

from app import app
from models import *


@app.context_processor
def context_processor():
    tags = Tags.query.all()
    languages = []
    for tag in tags:
        languages.append(tag.name)
    return dict(languages=languages)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/<tag>', methods=['POST', 'GET'])
def tag_sites(tag):
    tag = Tags.query.filter(Tags.name == tag).first_or_404()
    return render_template('tag_sites.html', tag=tag)
