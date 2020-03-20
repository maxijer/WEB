import json
import random
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/member')
def login():
    with open("templates/chel.json", "rt", encoding="utf8") as f:
        team = json.loads(f.read())
    return render_template('base1.html', team=team)


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.run(port=8080, host='127.0.0.1')
