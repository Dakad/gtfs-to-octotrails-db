from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Unicode, Integer, Float, TIMESTAMP, Enum, String, BigInteger
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
# line_stops = Table("lines_stops", Base.metadata,
#                    Column('line_number', Unicode, ForeignKey('lines.number')),
#                    Column('stop_feed_id', Unicode, ForeignKey('stops.stop_id'))
#                    )
# TODO Change line_stops to real Class


class LineStop(Base):
    """
    Entity representing the relation between a line and stop

    Arguments:
        line_number {Unicode} -- The line number
        stop_id {Unicode}  - The Stop Id
        trip_id {Unicde} - The trip Id in the feed
    """

    __tablename__ = "line_stop"
    _plural_name_ = "line_stops"

    id = Column(Integer, autoincrement=True, primary_key=True)
    line_number = Column(Unicode, ForeignKey('lines.number'), nullable=True)
    stop_id = Column(Unicode, ForeignKey('stops.stop_id'), nullable=True)
    trip_id = Column(BigInteger)

    lines = relationship("Line")


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

    # stops = relationship("Stop", secondary=LineStop, back_populates="lines")

    def __repr__(self):
        return '<Line #%s: %s  (%s)>' % (self.number, self.description, self.mode)

    def __init__(self, **data):
        self.feed_id = data['feed_id']
        self.number = data['route_short_name']
        self.description = data['route_long_name']
        self.departure, self.terminal = self.description.split(' - ')
        self.route_color = data['route_color']
        self.route_text_color = data['route_text_color']
        self.mode = LineType(int(data['route_type']))


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

    lines = relationship("LineStop")

    localisation = relationship(
        "Localisation", backref="stops", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return '<Stop %s: %s>' % (self.stop_id, self.feed_name)

    def __init__(self, **data):
        self.feed_id = data['feed_id']
        self.stop_id = data['stop_id']
        self.description_fr = data['stop_name']
        self.description_nl = data['stop_name']


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
        self.longitude = float(data['stop_lon'])
        self.latitude = float(data['stop_lat'])


def init(engine):
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///data/app.sqlite', echo=True)
    init(engine)
