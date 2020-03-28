import sqlalchemy
from .db_session import SqlAlchemyBase


class Zadacha(SqlAlchemyBase):
    __tablename__ = 'zadachi'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    chel = sqlalchemy.Column(sqlalchemy.String)
    zadacha = sqlalchemy.Column(sqlalchemy.String)
    predmet = sqlalchemy.Column(sqlalchemy.String)
    clas = sqlalchemy.Column(sqlalchemy.String)
