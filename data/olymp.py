import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Olymp(SqlAlchemyBase):
    __tablename__ = 'olymp'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    nazv = sqlalchemy.Column(sqlalchemy.String)
    information = sqlalchemy.Column(sqlalchemy.String)
    ssilka = sqlalchemy.Column(sqlalchemy.String)
    ataps = sqlalchemy.ColumnDefault(sqlalchemy.String)
