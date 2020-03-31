from app import resize
from data.olymp import Olymp
from data import db_session

db_session.global_init("db/olymp.sqlite")
session = db_session.create_session()
for mast in session.query(Olymp).all():
    if not mast.image is None:
        resize(f"static/img/{mast.image}")
