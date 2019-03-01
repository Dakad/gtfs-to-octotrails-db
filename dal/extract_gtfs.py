import os
import csv
from threading import Thread
import logging

from dal.table_def import Line, Stop, Localisation, LineStop


def init(gtfs_file_path, SessionMaker):
    logging.info('Unziping the GTFS feed ... ')
    feed_version_id = unzip_gtfs(gtfs_file_path)

    logging.info('Extracting the GTFS data in DB ... ')
    process_gtfs_files(feed_version_id, SessionMaker)


def unzip_gtfs(gtfs_light_zip):
    from zipfile import ZipFile

    gtfs_zip = ZipFile(gtfs_light_zip, "r")

    extract_dir = gtfs_zip.filename[:-4]
    gtfs_zip.extractall(extract_dir)
    return extract_dir


def process_gtfs_files(gtfs_dir, session_maker):
    feed_id = os.path.basename(gtfs_dir)
    light_files = ['stops', 'routes']
    threads = []
    for light in light_files:
        gtfs_file_name = os.path.join(gtfs_dir, light + ".txt")

        logging.info('Processing %s ' % gtfs_file_name)
        p = LightGTFSProcess(kind=light, light_file=gtfs_file_name,
                             db_session=session_maker, feed_id=feed_id)
        p.start()
        threads.append(p)

    # Wait for all LightsGtfsProcess to complete
    for t in threads:
        t.join()

    # Process the GTFS translations.txt to get the nl version
    gtfs_file_name = os.path.join(gtfs_dir, "translations.txt")
    logging.info('Processing %s ' % gtfs_file_name)
    tr = GTFSTranslationProcess(
        translation_file=gtfs_file_name,
        db_session=session_maker,
        feed_id=feed_id)
    tr.start()

    # Process the GTFS trip.txt
    gtfs_file_name = os.path.join(gtfs_dir, "trips.txt")
    logging.info('Processing %s ' % gtfs_file_name)
    tr = GTFSTripProcess(gtfs_trip_file=gtfs_file_name,
                         db_session=session_maker)
    tr.start()

#    # Waitin for GtfsTripProcesss to complete
    tr.join()

    # TODO Add GtfsStopTripProcesss

    # TODO Add GtfsTripProcesss

    # TODO Add Nominatem Reverse GeoAdress to Localisation


class LightGTFSProcess(Thread):
    """
    Task to process the specific GTFS 

    Arguments:
        kind {string} -- Kind of GTFS
        light_file {string} -- The GTFS filename
        db_session {sqlalchemy.orm.sessionmaker} -- The SQLAchemy Session
    """

    def __init__(self, **args):
        Thread.__init__(self)
        self.kind = args['kind']
        self.feed_id = args['feed_id']
        self.light_file = args['light_file']
        self.db_session = args['db_session']()

    def run(self):
        try:
            for line in _read_gtfs_csv(self.light_file):

                line['feed_id'] = self.feed_id
                if(self.kind == "routes"):
                    if(('route_color' in line) == False):
                        continue
                    self.db_session.add(Line(**line))
                else:
                    # print(line)
                    self.db_session.add(Stop(**line))
                    self.db_session.add(Localisation(**line))
            self.db_session.commit()
        except Exception as ex:
            print(ex, line)
            self.db_session.rollback()


class GTFSTranslationProcess(Thread):
    """
    Task to process the GTFS translation file

    Arguments:
        feed_id {string} -- The FeedVersion id
        translation_file {string} -- The GTFS translation file
        db_session {sqlalchemy.orm.sessionmaker} -- The SQLAchemy Session
    """

    def __init__(self, **args):
        Thread.__init__(self)
        self.feed_id = args['feed_id']
        self.translation_file = args['translation_file']
        self.db_session = args['db_session']()

    def run(self):
        try:
            sess = self.db_session.query(Stop)
            for line in _read_gtfs_csv(self.translation_file):
                if(line['lang'] == 'fr'):
                    continue
                row = sess.filter(Stop.description_fr == line['trans_id'])
                row.update({"description_nl": line['translation']})
            self.db_session.commit()
        except Exception as ex:
            print(ex, line)
            self.db_session.rollback()


class GTFSTripProcess(Thread):
    """
    Task to process the  GTFS file : trip.txt as new Line_Stop Entity

    Arguments:
        trip_file {string} -- The GTFS filename
        db_session {sqlalchemy.orm.sessionmaker} -- The SQLAchemy Session
    """

    def __init__(self, **args):
        Thread.__init__(self)
        self.trip_file = args['gtfs_trip_file']
        self.db_session = args['db_session']()

    def run(self):
        try:
            for (i, line) in enumerate(_read_gtfs_csv(self.trip_file)):
                print('%d' % i)
                new_line_stop = LineStop(
                    trip_id=line['trip_id'],
                    stop_id=line['route_id']
                )
                self.db_session.add(new_line_stop)
            self.db_session.commit()
        except Exception as ex:
            print(ex)
            self.db_session.rollback()


def _read_gtfs_csv(light_file_name):
    with open(light_file_name, "r") as gtfs:
        gtfs_reader = csv.reader(gtfs)
        head = next(gtfs_reader)

        for row in gtfs_reader:
            new_line = dict(zip(head, row))
            new_line = dict((k, v)
                            for k, v in new_line.items() if v != '')
            yield new_line


if __name__ == "__main__":
    import sqlalchemy
    from table_def import init as tableInit
    db_connection = "sqlite:///data/app.sqlite"
    db_engine = sqlalchemy.create_engine(db_connection, echo=False)
    tableInit(db_engine)
    SessionMaker = sqlalchemy.orm.sessionmaker(bind=db_engine)
    init("./data/versions/527_20190223.zip", SessionMaker)
