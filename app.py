import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})


@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    file_name = f'static/file-{mytime}.{extension}'
    file.save(file_name)

    foto = request.files["foto_give"]
    extension = foto.filename.split('.')[-1]
    foto_name = f'static/foto-{mytime}.{extension}'
    foto.save(foto_name)

    time = today.strftime('%Y.%m.%d')

    doc = {
        'file': file_name,
        'foto': foto_name,
        'title': title_receive,
        'content': content_receive,
        'time': time,
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': 'Data Berhasil Disimpan!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
