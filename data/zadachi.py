import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


class Zadacha(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'zadachi'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    about = sqlalchemy.Column(sqlalchemy.String)
    chel = sqlalchemy.Column(sqlalchemy.String)
    zadacha = sqlalchemy.Column(sqlalchemy.String)
    predmet = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)
    otvet = sqlalchemy.Column(sqlalchemy.String)
