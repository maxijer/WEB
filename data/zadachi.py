import sqlalchemy
from .db_session import SqlAlchemyBase


class Zadacha(SqlAlchemyBase):
    __tablename__ = 'zadachi'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    about = sqlalchemy.Column(sqlalchemy.String)
    chel = sqlalchemy.Column(sqlalchemy.String)
    zadacha = sqlalchemy.Column(sqlalchemy.String)
    data = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)
