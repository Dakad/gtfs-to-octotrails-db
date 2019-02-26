from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import (Unicode, Integer, Float, TIMESTAMP, Enum, String)
from sqlalchemy.orm import relationship, backref, validates, synonym, foreign

import enum

Base = declarative_base()


class FeedVersion(Base):
    """
    Entity representing a TransitFeed version data

    Arguments:
        Base {[type]} -- [description]
    """

    __tablename__ = "feed_version"
    _plural_name_ = 'feed_versions'

    feed_id = Column(Unicode(100), primary_key=True)
    id = synonym('feed_id')
    size = Column(Integer)
    registred_date = Column(TIMESTAMP)
    start_date = Column(String(10))     # Date inf format YYYYMMDD
    finish_date = Column(String(10))    # Date inf format YYYYMMDD
    download_url = Column(Unicode(250), unique=True)

    stops = relationship("Stop", backref=(
        "feedversions"), cascade="all, delete-orphan")
    lines = relationship("Line", backref=("feedversions"),
                         cascade="all, delete-orphan")

    def __repr__(self):
        return '<FeedVersion %s: %d >' % (self.feed_id, self.registred_date)

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


"""Association table btwn Lines && Stops
"""
line_stops = Table("lines_stops", Base.metadata,
                   Column('line_number', Unicode, ForeignKey('lines.number')),
                   Column('stop_feed_id', Unicode, ForeignKey('stops.stop_id'))
                   )


class Line(Base):
    """
    """

    __tablename__ = "lines"
    _plural_name_ = 'lines'

    feed_id = Column(Integer, ForeignKey(FeedVersion.id), primary_key=True)
    number = Column('number', Unicode(10), primary_key=True)
    id = synonym('number')
    description = Column(Unicode(100))
    departure = Column('from', Unicode(100))
    terminal = Column('to', Unicode(100))
    route_color = Column(Unicode(10))
    route_text_color = Column(Unicode(10))
    mode = Column('type', Enum(LineType))

    stops = relationship("Stop", secondary=line_stops, back_populates="lines")

    def __repr__(self):
        return '<Line %s: %s  (%s)>' % (self.number, self.description, self.mode)

    def __init__(self, **data):
        self.number = data['number']
        self.description = data['description']
        self.departure = data['departure']
        self.terminal = data['terminal']
        self.route_color = data['route_color']
        self.route_text_color = data['route_text_color']


class Stop(Base):
    """
    Entity representing a Stop

    Arguments:
        feed_id {string} -- The FeedVersion id in GTFS
    """

    __tablename__ = "stops"
    _plural_name_ = 'stops'

    feed_id = Column(Integer, ForeignKey(FeedVersion.id), primary_key=True)
    stop_id = Column(Unicode, primary_key=True, index=True)
    id = synonym('stop_id')
    description_fr = Column(Unicode(100))
    description_nl = Column(Unicode(100))

    lines = relationship("Line", secondary=line_stops, back_populates="stops")
    localisation = relationship(
        "Localisation", backref="stops", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return '<Stop %s: %s>' % (self.stop_id, self.feed_name)

    def __init__(self, **data):
        self.feed_id = data['feed_id']
        self.tech_id = data['tech_id']
        self.description_fr = data['description_fr']
        self.description_nl = data['description_nl']


class Localisation(Base):
    """
    Entity representing a Localisation of a stop

    Arguments:
        stop_id {string} -- The stop_id
        longitude {float} -- The longitude
        latitude {float} -- The latitude
        address_fr {string} -- The french address version of the localisation 
        address_nl {string} -- The deutsch address version of the localisation 
    """

    __tablename__ = "localisations"
    _plural_name_ = 'localisations'

    stop_id = Column(Unicode, ForeignKey(Stop.id), primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)
    address_fr = Column(Unicode(250))
    address_nl = Column(Unicode(250))

    def __init__(self, **data):
        self.stop_id = data['stop_id']
        self.longitude = data['longitude']
        self.latitude = data['latitude']


def init(engine):
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///data/app.db', echo=True)
    init(engine)
