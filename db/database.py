# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base

# 替换以下参数以匹配你的数据库设置
DATABASE_URL = "mysql+mysqlconnector://juewu:password123@localhost/salestech"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


def initialize_database():
    Base.metadata.create_all(engine)
