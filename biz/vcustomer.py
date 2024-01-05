from sqlalchemy import desc

from db.database import Session
from db.models import VCustomer


def update(vc: VCustomer):
    session = Session()
    session.query(VCustomer).filter_by(id=vc.id).update(vc.to_dict())
    session.commit()
    pass


def add(vc: VCustomer):
    session = Session()
    session.add(vc)
    session.commit()
    pass


def list_all() -> list[VCustomer]:
    session = Session()
    return session.query(VCustomer).order_by(desc('id')).all()
