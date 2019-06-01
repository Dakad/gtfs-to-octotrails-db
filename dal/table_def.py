from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Unicode, Integer, Float, TIMESTAMP, Enum, String, BigInteger
from sqlalchemy.orm import relationship, backref, validates, synonym, foreign
import sqlalchemy

import enum

Base = declarative_base()


class FeedVersion(Base):
    """
    Entity representing a TransitFeed version data

    Arguments:
        Base {[type]} -- [description]
    """

    __tablename__ = "feed_versions"
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
        self.feed_id = data.get('id')
        self.size = data.get('size')
        self.registred_date = data.get('registred_date')
        self.start_date = data.get('start_date')
        self.finish_date = data.get('finish_date')
        self.download_url = data.get('url')


class LineType(enum.Enum):
    Tram = 0
    Metro = 1
    TBus = 2
    Bus = 3


"""Association table btwn Lines && Stops
"""
# line_stops = Table("lines_stops", Base.metadata,
#                    Column('line_route', Unicode, ForeignKey('lines.route')),
#                    Column('stop_feed_id', Unicode, ForeignKey('stops.stop_id'))
#                    )
# TODO Change line_stops to real Class


class Line(Base):
    """
    """

    __tablename__ = "lines"
    _plural_name_ = 'lines'

    feed_id = Column(Unicode(100), ForeignKey(
        FeedVersion.id), nullable=False)
    route = Column('route', Unicode(10), primary_key=True)
    id = synonym('route')
    description = Column(Unicode(100))
    departure = Column('from', Unicode(100))
    terminal = Column('to', Unicode(100))
    route_color = Column(Unicode(10))
    route_text_color = Column(Unicode(10))
    mode = Column('type', Enum(LineType))

    # stops = relationship("Stop", secondary=LineStop, back_populates="lines")

    def __repr__(self):
        return '<Line #%s: %s  (%s)>' % (self.route, self.description, self.mode)

    def __init__(self, **data):
        self.feed_id = data['feed_id']
        self.route = data['route_short_name']
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

    feed_id = Column(Unicode(100), ForeignKey(
        FeedVersion.id), primary_key=True)
    stop_id = Column(Unicode(10), primary_key=True, nullable=False)
    id = synonym('stop_id')
    description_fr = Column(Unicode(100))
    description_nl = Column(Unicode(100))

    # lines = relationship("LineStop")

    # localisation = relationship(
    #     "Localisation", backref="stops", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return '<Stop %s: %s>' % (self.stop_id, self.feed_name)

    def __init__(self, **data):
        self.feed_id = data['feed_id']
        self.stop_id = data['stop_id']
        self.description_fr = data['stop_name']
        self.description_nl = data['stop_name']


class LineStop(Base):
    """
    Entity representing the relation between a line and stop

    Arguments:
        trip_id {String} - The trip Id in the feed
        line_route {Unicode} -- The line route numbers
        stop_id {Unicode}  - The Stop Id
    """

    __tablename__ = "line_stop"
    _plural_name_ = "line_stops"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    trip_id = Column(String(50))
    line_route = Column(Unicode(10), nullable=True)
    stop_id = Column(Unicode(10), nullable=True)

    lines = relationship("Line")

    def __repr__(self):
        return '<LineStop #{} [{}] S:({}) >'.format(self.trip_id, self.line_route, self.stop_id)

    def __init__(self, *data):
        self.trip_id = data[0]
        self.line_route = data[1]


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

    feed_id = Column(Unicode(100), ForeignKey(
        FeedVersion.id), primary_key=True, nullable=False)
    stop_id = Column(Unicode(10), ForeignKey(
        Stop.stop_id), primary_key=True, nullable=False)
    longitude = Column(Float)
    latitude = Column(Float)
    address_fr = Column(Unicode(250))
    address_nl = Column(Unicode(250))

    PrimaryKeyConstraint('feed_id', 'stop_id', name='localisation_pk')

    def __init__(self, **data):
        self.stop_id = data['stop_id']
        self.longitude = float(data['stop_lon'])
        self.latitude = float(data['stop_lat'])


def init(db_uri):
    print(db_uri)
    db_engine = sqlalchemy.create_engine(db_uri, echo=False)
    Base.metadata.create_all(db_engine)
    SessionMaker = sqlalchemy.orm.sessionmaker(bind=db_engine)
    return SessionMaker


if __name__ == "__main__":
    init('sqlite:///data/app.sqlite')
