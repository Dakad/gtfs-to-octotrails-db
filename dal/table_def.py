from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Enum, Integer, TIMESTAMP


import enum

Base = declarative_base()


class FeedVersion(Base):
    """
    Entity representing a TransitFeed version data

    Arguments:
        Base {[type]} -- [description]
    """

    id = Column(String(100), primary_key=True)
    size = Column(Integer)
    registred_date = Column(TIMESTAMP)
    start_date = Column(String(10))     # Date inf format YYYYMMDD
    finish_date = Column(String(10))    # Date inf format YYYYMMDDs
    download_url = Column(String(250), unique=True)

    def __init__(self, **data):
        self.id = data['feed_version_id']
        self.size = data['size']
        self.registred_date = data['registred_date']
        self.start_date = data['start_date']
        self.finish_date = data['finish_date']
        self.download_url = data['url']


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
