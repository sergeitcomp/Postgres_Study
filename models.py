from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from enum import Enum as PyEnum

Base = declarative_base()


class Topic(PyEnum):
    LIFE = "Быт"
    SCHOLARSHIP = "Стипендии"
    STUDY = "Учебный процесс"
    SPORT = "Спорт"
    INTERNATIONAL = "Международные вопросы"

class Status(PyEnum):
    NEW = "Новое"
    IN_PROGRESS = "На рассмотрении"
    RESOLVED = "Решено"

class Appeal(Base):
    __tablename__ = 'appeals'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=False)
    topic = Column(Enum(Topic), nullable=False)
    text = Column(String(1000), nullable=False)
    status = Column(Enum(Status), default=Status.NEW)
    response = Column(String(1000))
    manager_id = Column(Integer, ForeignKey('managers.id'))
    #st = Column(String(20))

    manager = relationship("Manager", back_populates="appeals")

class Manager(Base):
    __tablename__ = 'managers'

    id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    topic = Column(Enum(Topic), nullable=False)

    appeals = relationship("Appeal", back_populates="manager")
