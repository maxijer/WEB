from flask import Flask, render_template, request, redirect, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, Email
from data.users import User
from data.zadachi import Zadacha
from data.jobs import Jobs
import flask
from data.olymp import Olymp
from data import db_session
import hashlib
from PIL import Image
from requests import get
import news_api

name_and_surname = ''
norm_rashir = ['jpg', 'png', 'jpeg']

app = Flask(__name__)



class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    Repeat_password = PasswordField('Пароль', validators=[DataRequired()])
    surname = StringField('surname', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    age = StringField('age', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class Dobavlenie(FlaskForm):
    about = StringField('about', validators=[DataRequired()])
    content = StringField('about', validators=[DataRequired()])
    fiz = BooleanField('Физика')
    math = BooleanField('Математика')
    informatick = BooleanField('Информатика')
    news = BooleanField('Новость')
    photo = FileField("Фото")
    submit = SubmitField('Добавить')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Вход')
    regist = SubmitField('Регистрация')


def resize(path):
    img = Image.open(path)
    img.thumbnail((600, 200), Image.ANTIALIAS)
    img.save(path)


def norm_pokaz(content):
    spi = list()
    for i in content.split():
        new = ''
        if len(new) + len(i) + 1 < 120:
            new += " " + i
        else:
            spi.append(new)
            new = ''
    return spi


def zadach_ses(about, content, predmet, image=None):
    db_session.global_init("db/olymp.sqlite")
    session = db_session.create_session()
    zad = Zadacha()
    zad.about = about
    zad.zadacha = content
    zad.predmet = predmet
    if not image is None:
        zad.image = image
    session.add(zad)
    session.commit()


def proverka_zagolovka(predmet, zagolovok):
    db_session.global_init("db/olymp.sqlite")
    session = db_session.create_session()
    count = 0
    for a in session.query(Zadacha).filter(Zadacha.predmet == predmet):
        if a.about == zagolovok:
            count += 1
    if count == 0:
        return True
    return False


def obrabotka_zadach(form, predmet, about, content):
    if form.photo.data != '':
        if not str(form.photo.data).split()[1][1:-1].split('.')[1] in norm_rashir:
            return 0
        elif not proverka_zagolovka(predmet, about):
            return 2
        else:
            ras = str(form.photo.data).split()[1][1:-1].split('.')[1]
            image = form.photo.data.read()
            nazv = f'static/img/{predmet}_{about}.{ras}'
            with open(nazv, 'wb') as file:
                file.write(image)
            resize(nazv)
            zadach_ses(about, content, predmet, nazv)
    else:
        if not proverka_zagolovka(predmet, about):
            return 2
        else:
            zadach_ses(about, content, predmet)
            return 1


@app.route("/dobav", methods=['GET', 'POST'])
def dobavim():
    form = Dobavlenie()
    if request.method == "GET":
        return render_template("dobavlenie.html", form=form, gad=1)
    elif request.method == "POST":
        spi = list()
        if form.submit.data:
            about = request.form.get('about')
            content = request.form.get('content')
            if len(about) > 50:
                return render_template("dobavlenie.html", form=form, gad=3)
            for i in content.split():
                if len(i) > 30:
                    return render_template("dobavlenie.html", form=form, gad=4)
            if len(content) > 540:
                return render_template("dobavlenie.html", form=form, gad=5)
            if form.fiz.data:
                spi.append(obrabotka_zadach(form, "Физика", about, content))
            if form.math.data:
                spi.append(obrabotka_zadach(form, "Математика", about, content))
            if form.informatick.data:
                spi.append(obrabotka_zadach(form, "Информатика", about, content))
            if form.news.data:
                db_session.global_init("db/olymp.sqlite")
                session = db_session.create_session()
                zad = Jobs()
                zad.about = about
                zad.news = content
                if form.photo.data != '':
                    if not str(form.photo.data).split()[1][1:-1].split('.')[1] in norm_rashir:
                        return render_template("dobavlenie.html", form=form, gad=0)
                    else:
                        ras = str(form.photo.data).split()[1][1:-1].split('.')[1]
                        image = form.photo.data.read()
                        nazv = f'static/img/Новость_{about}.{ras}'
                        with open(nazv, 'wb') as file:
                            file.write(image)
                        resize(nazv)
                        zad.image = nazv
                        session.add(zad)
                        session.commit()
                else:
                    session.add(zad)
                    session.commit()
            if spi.count(0) > 0:
                return render_template("dobavlenie.html", form=form, gad=0)
            elif spi.count(2) > 0:
                return render_template("dobavlenie.html", form=form, gad=2)
            else:
                return redirect('/news')
        return render_template("dobavlenie.html", form=form, gad=1)


@app.route('/news')
def news():
    db_session.global_init("db/olymp.sqlite")
    session = db_session.create_session()
    spi = list()
    for lud in reversed(session.query(Jobs).all()):
        z = list()
        z.append(lud.about)
        z.append(lud.news)
        if lud.image is None:
            z.append('0')
        else:
            z.append(lud.image)
        spi.append(z)
    return render_template('news.html', news_list=spi)


def otobrazh(predmet):
    db_session.global_init("db/olymp.sqlite")
    session = db_session.create_session()
    spi = list()
    for mast in reversed(list(session.query(Zadacha).filter(Zadacha.predmet == predmet))):
        z = list()
        z.append(mast.about)
        z.append(mast.zadacha)
        if mast.image is None:
            z.append('0')
        else:
            z.append(mast.image)
        spi.append(z)
    return spi


def obrabotka_olymp(predmet):
    db_session.global_init("db/olymp.sqlite")
    session = db_session.create_session()
    spi = list()
    for olymp in session.query(Olymp).filter(Olymp.predmet == predmet):
        z = list()
        z.append(olymp.nazv)
        z.append(olymp.information)
        if olymp.image is None:
            z.append('0')
        else:
            z.append(f'/static/img/{olymp.image}')
        z.append(olymp.ssilka)
        spi.append(z)
    return spi


@app.route('/fizika')
def fizika():
    return render_template('zadachka.html', zadacha_list=otobrazh('Физика'))


@app.route('/fiz_olimp')
def fiz_olimp():
    ol = obrabotka_olymp('Физика')
    return render_template('olimpiada.html', olymp_list=ol)


@app.route('/math_olimp')
def math_olimp():
    ol = obrabotka_olymp('Математика')
    return render_template('olimpiada.html', olymp_list=ol)


@app.route('/inform_olimp')
def inform_olimp():
    ol = obrabotka_olymp('Информатика')
    return render_template('olimpiada.html', olymp_list=ol)


@app.route('/inform')
def informa():
    return render_template('zadachka.html', zadacha_list=otobrazh('Информатика'))


@app.route('/math')
def math():
    return render_template('zadachka.html', zadacha_list=otobrazh('Математика'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        pasword = request.form.get('password')
        Repeat_password = request.form.get('Repeat_password')
        surname = request.form.get('surname')
        name = request.form.get('name')
        age = request.form.get('age')
        if pasword == Repeat_password:
            user = User()
            user.name = name
            user.surname = surname
            user.email = email
            user.age = age
            user.hashed_password = hashlib.md5(pasword.encode('utf-8')).hexdigest()
            db_session.global_init("db/olymp.sqlite")
            session = db_session.create_session()
            count = 0
            for user in session.query(User).filter(User.email == email):
                count += 1
            if count == 0:
                session.add(user)
                session.commit()
                return redirect('/login')
    return render_template('login.html', title='Авторизация', form=form)


def check_prav(email, password):
    db_session.global_init("db/olymp.sqlite")
    session = db_session.create_session()
    has = hashlib.md5(password.encode('utf-8')).hexdigest()
    for user in session.query(User).all():
        if user.email == email and user.hashed_password == has:
            return True
    return False


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "GET":
        return render_template("vhod.html", form=form)
    elif request.method == 'POST':
        if form.regist.data:
            return redirect('/register')
        if form.submit.data:
            if check_prav(form.email.data, form.password.data):
                return redirect('/news')
    return render_template('vhod.html', form=form)


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    db_session.global_init("db/olymp.sqlite")
    app.register_blueprint(news_api.blueprint)
    app.run(host='127.0.0.1', port=8080)
