from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Enum, Integer, TIMESTAMP, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

import enum

Base = declarative_base()


class FeedVersion(Base):
    """
    Entity representing a TransitFeed version data

    Arguments:
        Base {[type]} -- [description]
    """

    __tablename__ = "feedversions"

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

    stops = relationship("Stop", secondary=line_stops, back_populates="lines")

    def __init__(self, **data):
        self.number = data['number']
        self.description = data['description']
        self.departure = data['departure']
        self.terminal = data['terminal']
        self.route_color = data['route_color']
        self.route_text_color = data['route_text_color']


"""Association table btwn Lines && Stops
"""
line_stops = Table("lines_stops", Base.metadata,
                   Column('line_id', String, ForeignKey('lines.id')),
                   Column('stop_id', String, ForeignKey('stops.id'))
                   )


class Stop(Base):
    """
    Entity representing a Stop

    Arguments:
        feed_id {string} -- The feed_id in GTFS
    """

    __tablename__ = "stops"

    feed_id = Column(String(10), primary_key=True)
    tech_id = Column(String(10), nullable=True)
    description_fr = Column(String(100))
    description_nl = Column(String(100))

    lines = relationship("Line", secondary=line_stops, back_populates="stops")

    def __init__(self, **data):
        self.feed_id = data['feed_id']
        self.tech_id = data['tech_id']
        self.description_fr = data['description_fr']
        self.description_nl = data['description_nl']
