from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Enum


import enum

Base = declarative_base()


class LineType(enum.Enum):
    Tram = 0
    Metro = 1
    TBus = 2
    Bus = 3


class Line(Base):
    """
    """

    __tablename__ = "lines"

    number = Column(String(10), primary_key=True)
    description = Column(String(100))
    departure = Column('from', String(100))
    terminal = Column('to', String(100))
    route_color = Column(String(10))
    route_text_color = Column(String(10))
    mode = Column('type', Enum(LineType))

    def __init__(self, **data):
        self.number = data['number']
        self.description = data['description']
        self.departure = data['departure']
        self.terminal = data['terminal']
        self.route_color = data['route_color']
        self.route_text_color = data['route_text_color']
