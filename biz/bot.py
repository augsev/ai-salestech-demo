from sqlalchemy import desc

from db.database import Session
from db.models import Bot


def update(bot: Bot):
    session = Session()
    session.query(Bot).filter_by(id=bot.id).update(bot.to_dict())
    session.commit()
    pass


def add(bot: Bot):
    session = Session()
    session.add(bot)
    session.commit()
    pass


def list_all() -> list[Bot]:
    session = Session()
    return session.query(Bot).order_by(desc('id')).all()
