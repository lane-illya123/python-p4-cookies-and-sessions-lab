#!/usr/bin/env python3

from urllib import response
from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate



from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    new_article = []
    
    for a in Article.query.all():
        article_dict = {
            "id": a.id,
            "author": a.author,
            "title": a.title,
            "content": a.content,
            "preview": a.preview,
            "minutes_to_read": a.minutes_to_read,
            "date": a.date,
        }
        new_article.append(article_dict)

    response = make_response(
        jsonify(new_article),
        200
    )



    pass

@app.route('/articles/<int:id>')
def show_article(id):
    
    session['page_views'] = session.get('page_views', 0) + 1

    if session['page_views'] <= 3:
        article = Article.query.filter(Article.id == id).first()
        article_dict = article.to_dict()
        response = make_response(article_dict, 200)
    else:
        response = make_response({'message': 'Maximum pageview limit reached'}, 401)

    return response

if __name__ == '__main__':
    app.run(port=5555)
