from .table_def import init as table_def_init
from .extract_gtfs import init as extract_gtfs_init


def save_new_feed_version(feed_version, db_session):
    from .table_def import FeedVersion

    version = dbion_session.filter(
        FeedVersion.feed_id == feed_version['id']).first()

    if version is None:
        db_session.add(FeedVersion(feed_version))
        return True

    return False
