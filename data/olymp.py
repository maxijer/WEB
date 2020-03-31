import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

class Olymp(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'olymp'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    nazv = sqlalchemy.Column(sqlalchemy.String)
    information = sqlalchemy.Column(sqlalchemy.String)
    ssilka = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)
    predmet = sqlalchemy.Column(sqlalchemy.String)
