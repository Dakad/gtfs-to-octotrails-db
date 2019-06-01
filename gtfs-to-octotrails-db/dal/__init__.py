from .table_def import init as table_def_init
from .extract_gtfs import init as extract_gtfs_init


def save_new_feed_version(feed_version, db_session):
    from .table_def import FeedVersion

    version = db_session.get(feed_version['id'])

    if version is None:
        db_session.add(FeedVersion(id=feed_version))
        db_session.commit()
        return True
    else:
        return False
