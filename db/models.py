from typing import Any

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), nullable=False)
    passwd = Column(String(255), nullable=False)
    ctime = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    active = Column(Integer, nullable=False, default=1)

    sessions = relationship("Session", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', active={self.active}, ctime={self.ctime})>"


class Session(Base):
    __tablename__ = 'session'
    uid = Column(Integer, ForeignKey('user.id'), primary_key=True)
    token = Column(String(255), nullable=False)
    etime = Column(TIMESTAMP)
    utime = Column(TIMESTAMP)

    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<Session(uid={self.uid}, token='{self.token}', etime={self.etime}, utime={self.utime})>"


class VCustomer(Base):
    __tablename__ = 'vcustomer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cname = Column(String(255), nullable=False, comment='虚拟客户名')
    notes = Column(String(255), default=None, comment='描述')
    config = Column(Text, comment='设置')
    prompt = Column(Text, comment='提示词')
    putime = Column(TIMESTAMP, default=None, comment='提示词生成时间')
    ctime = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    active = Column(Integer, nullable=False, default=1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "cname": self.cname,
            "notes": self.notes,
            "config": self.config,
            "prompt": self.prompt,
            "putime": self.putime,
            "ctime": self.ctime,
            "active": self.active
        }

    def __repr__(self):
        return f"<VCustomer(id={self.id}, cname='{self.cname}', notes='{self.notes}', config='{self.config}', \
        prompt='{self.prompt}', putime='{self.putime}', ctime='{self.ctime}', active={self.active})>"


class VTrainer(Base):
    __tablename__ = 'vtrainer'

    id = Column(Integer, primary_key=True)
    tname = Column(String(255), nullable=False, comment='虚拟培训师名')
    notes = Column(String(255), default=None, comment='描述')
    config = Column(Text, comment='设置')
    prompt = Column(Text, comment='提示词')
    putime = Column(TIMESTAMP, default=None, comment='提示词生成时间')
    ctime = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    active = Column(Integer, nullable=False, default=1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "tname": self.tname,
            "notes": self.notes,
            "config": self.config,
            "prompt": self.prompt,
            "putime": self.putime,
            "ctime": self.ctime,
            "active": self.active
        }

    def __repr__(self):
        return f"<VTrainer(id={self.id}, tname='{self.tname}', notes='{self.notes}', config='{self.config}', \
        prompt='{self.prompt}', putime='{self.putime}', ctime='{self.ctime}', active={self.active})>"


class Scene(Base):
    __tablename__ = 'scene'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, comment='场景名')
    stype = Column(Integer, nullable=False, default=0, comment='场景类型')
    description = Column(Text, comment='场景介绍')
    notes = Column(Text, comment='备注')

    vcustomers = relationship("VCustomer", secondary='scene_vcustomer')
    vtrainers = relationship("VTrainer", secondary='scene_vtrainer')

    def __repr__(self):
        return f"<Scene(id={self.id}, name='{self.name}')>"


class SceneVCustomer(Base):
    __tablename__ = 'scene_vcustomer'

    sid = Column(Integer, ForeignKey('scene.id'), primary_key=True)
    vcid = Column(Integer, ForeignKey('vcustomer.id'), primary_key=True)


class SceneVTrainer(Base):
    __tablename__ = 'scene_vtrainer'

    sid = Column(Integer, ForeignKey('scene.id'), primary_key=True)
    vtid = Column(Integer, ForeignKey('vtrainer.id'), primary_key=True)


class Bot(Base):
    __tablename__ = 'bot'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='机器人ID')
    name = Column(String(255), nullable=False, comment='名称')
    prompts = Column(Text, nullable=False, comment='提示词')
    notes = Column(String(255), default=None, comment='描述，JSON文件，包含了用于生成提示词的详细描述')

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "notes": self.notes,
            "prompts": self.prompts
        }

    def __repr__(self):
        return f"<Bot(id={self.id}, name='{self.name}', prompts='{self.prompts}', notes='{self.notes}')>"
