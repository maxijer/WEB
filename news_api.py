import flask
from flask import jsonify
from data.jobs import Jobs
from data import db_session
from data.olymp import Olymp
from data.zadachi import Zadacha
from data.users import User

blueprint = flask.Blueprint('news_api', __name__,
                            template_folder='templates')


def ok(sup, cl, chto):
    session = db_session.create_session()
    if sup != 'all':
        fiz_olymp = session.query(cl).filter(cl.predmet == sup)
    else:
        fiz_olymp = session.query(cl).all()
    return jsonify(
        {
            'all_zadach':
                [item.to_dict(only=chto)
                 for item in fiz_olymp]
        }
    )


@blueprint.route('/api/fizika')
def fiz():
    return ok('Физика', Olymp, ("nazv", "information", "ssilka", "image", "predmet"))


@blueprint.route('/api/math')
def math():
    return ok('Математика', Olymp, ("nazv", "information", "ssilka", "image", "predmet"))


@blueprint.route('/api/inform')
def information():
    return ok('Информатика', Olymp, ("nazv", "information", "ssilka", "image", "predmet"))


@blueprint.route('/api/vse_olymp')
def vse():
    return ok('all', Olymp, ("nazv", "information", "ssilka", "image", "predmet"))


@blueprint.route('/api/vse_zadach')
def all_zadach():
    return ok("all", Zadacha, ('about', 'zadacha', 'predmet', 'image'))


@blueprint.route('/api/zadachi_fiz')
def zad_fiz():
    return ok("Физика", Zadacha, ('about', 'zadacha', 'predmet', 'image'))


@blueprint.route('/api/zadachi_math')
def zad_math():
    return ok("Математика", Zadacha, ('about', 'zadacha', 'predmet', 'image'))


@blueprint.route('/api/zadachi_inform')
def zad():
    return ok("Информатика", Zadacha, ('about', 'zadacha', 'predmet', 'image'))


@blueprint.route('/api/news')
def get_news():
    return ok("all", Jobs, ('about', 'news', 'image'))


@blueprint.route('/api/users')
def users():
    return ok("all", User, ('surname', 'name', 'age', 'email', 'hashed_password'))
