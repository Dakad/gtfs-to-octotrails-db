from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Enum, Integer, Float, TIMESTAMP, ForeignKey, Table
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


"""Association table btwn Lines && Stops
"""
line_stops = Table("lines_stops", Base.metadata,
                   Column('line_number', String, ForeignKey('lines.number')),
                   Column('stop_feed_id', String, ForeignKey('stops.feed_id'))
                   )


class Line(Base):
    """
    """

    __tablename__ = "lines"

    number = Column('number', String(10), primary_key=True)
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
    localisation = relationship("Localisation", backref="stops", uselist=False)

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

    stop_id = Column(String, ForeignKey(Stop.feed_id), primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)
    address_fr = Column(String(250))
    address_nl = Column(String(250))

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
