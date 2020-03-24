from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, Email
from data.users import User
from data import db_session
import hashlib

name_and_surname = ''

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    Repeat_password = PasswordField('Пароль', validators=[DataRequired()])
    surname = StringField('surname', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    age = StringField('age', validators=[DataRequired()])
    submit = SubmitField('Submit')


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


@app.route("/dobav", methods=['GET', 'POST'])
def dobavim():
    form = Dobavlenie()
    print(1)
    print(form.submit.data)
    if request.method == 'POST':
        if form.validate_on_submit():
            print(form.photo.data)
            print(form.fiz.data)
            return "Всё ок"
    return render_template("dobavlenie.html", form=form)


@app.route('/1')
def rabota():
    form = LoginForm()
    return render_template('base1.html', title='Авторизация', form=form)


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
                return "Всё добавленно"
            else:
                return "ВЫ допустили ошибку"
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('vhod.html', form=form)


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.run(host='127.0.0.1', port=8080)
