from sqlalchemy import desc

from db.database import Session
from db.models import VTrainer


def add(vt: VTrainer):
    session = Session()
    session.add(vt)
    session.commit()
    pass


def update(vt: VTrainer):
    session = Session()
    session.query(VTrainer).filter_by(id=vt.id).update(vt.to_dict())
    session.commit()
    pass


def list_all() -> list[VTrainer]:
    session = Session()
    return session.query(VTrainer).order_by(desc('id')).all()
