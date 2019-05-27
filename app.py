import os
import logging
from logging.handlers import RotatingFileHandler

from config import Config


def config_log(log_instance="app"):
    if Config.LOG_TO_STDOUT:
        stream_handler = logging.StreamHandler()
        logging.root.addHandler(stream_handler)
    else:
        os.makedirs(Config.LOG_DIR, exist_ok=True)
        my_file_handler = RotatingFileHandler(
            filename=os.path.join(Config.LOG_DIR, '%s.log' % log_instance),
            maxBytes=1024*10,
            backupCount=3,
            encoding='utf-8'
        )
        my_file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s:[in %(pathname)s:%(lineno)d] %(message)s '))
        logging.root.addHandler(my_file_handler)

    logging.root.setLevel(logging.INFO)
    logging.info('[Config] Logging : DONE ')


def main(run='all'):
    from transit_feed import TransitFeed
    from dal import table_def_init, save_new_feed_version, extract_gtfs_init

    try:
        logging.info("Exec from Main")

        config_log()

        logging.info("Creating app tables ...")
        DBSessionMaker = table_def_init(Config.DB_URI)
        session = DBSessionMaker()

        logging.info("Fecthing TransitFeedAPI ...")
        tf = TransitFeed()

        feed_version = tf.getLastFeedVersion()
        is_new = save_new_feed_version(feed_version, session)

        if is_new is False:
            raise Exception("Feed #%s from %s is the newest" %
                            (feed_version['id'], feed_version['start_date']))
        else:
            session.commit()

        logging.info("Downloading TransitFeed Version : %s ..." %
                     feed_version['id'])
        # gtfs_zip_filename = feed_version['id'] + ".zip"
        gtfs_zip_filename = "527_20190223.zip"

        tf.downloadLastVersion(file_name=gtfs_zip_filename)

        logging.info("Extracting GTFS data into Octotrails DB ...")

        gtfs_zip_path = os.path.join(Config.GTFS_DIR, gtfs_zip_filename)
        extract_gtfs_init(gtfs_zip_path, DBSessionMaker)
    except Exception as ex:
        logging.critical(ex)


def remove_gtfs_files():
    from zipfile import ZipFile
    light_files = ['stops',  'translations', 'routes', 'trips', 'stop_times']

    def is_ok_for_gtfs_light(i): return i.filename[:-4] in light_files

    with ZipFile('./data/versions/gtfs.zip', 'r') as gtfs:
        with ZipFile('./data/versions/gtfs-light.zip', 'w') as gtfs_light:
            only_files = list(filter(is_ok_for_gtfs_light, gtfs.infolist()))
            for light_file in only_files:
                buffer = gtfs.read(light_file.filename)
                gtfs_light.writestr(light_file, buffer)


if __name__ == "__main__":
    # import argparse
    # arg_parser = argparse.ArgumentParser()
    # arg_parser.add_argument(
    #     "-r", "--run",
    #     choices=['pipeline', 'web', 'all'],
    #     const='all', default='all', nargs='?',
    #     help="Which part of the app to run : pipeline, web, all (by default: %(default)s)")

    # args = vars(arg_parser.parse_args())
    # main(**args)
    main()
