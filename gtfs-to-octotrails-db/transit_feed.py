
import os.path
import sys

import requests as req

from config import Config

BASE_URL = Config.TRANSITFEED_API_URL + Config.TRANSITFEED_API_VERSION
GET_feed_versions_URL = "/getFeedVersions"
GET_lastest_version_URL = "/getLatestFeedVersion"


class TransitFeed(object):
    """Handle the request to TransitFeed API

    Arguments:


    Returns:

    """

    FILE_CHUNK_SIZE = 1024**2

    def getLastFeedVersion(self):
        """Retrieve the Last Version of the STIB Feed

        Returns:
            object -- Data about the last version feed
        """

        feed_version = None
        res = req.get(BASE_URL + GET_feed_versions_URL, params={
            "key": Config.TRANSITFEED_API_KEY,
            "feed": Config.TRANSITFEED_STIB_ID,
            "page": 1,
            "limit": 3,
            "err": 0,
            "warn": 0
        }, headers={
            "Accept": "application/json"
        })
        data = res.json()
        if data['status'] == 'OK':
            last_version = data['results']['versions'][0]
            id = last_version['id'][51:].replace('/', '_')
            feed_version = {
                "id": id,
                "size": last_version['size'],
                "registred_date": last_version['ts'],
                "url": last_version['url'],
                "start_date": last_version['d']['s'],
                "finish_date": last_version['d']['f']
            }
        return feed_version

    def downloadLastVersion(self, file_name="gtfs.zip"):
        """Download/save the last Version of the STIB Feed

        Returns:

        """

        res = req.get(BASE_URL + GET_lastest_version_URL, params={
            "key": Config.TRANSITFEED_API_KEY,
            "feed": Config.TRANSITFEED_STIB_ID
        }, stream=True)
        if res.status_code == 200:
            file_name = os.path.join(Config.GTFS_DIR, file_name)
            total_size = int(res.headers['Content-Length'])
            read = 0
            with open(file_name, "wb") as gtfs:
                for chunk in res.iter_content(chunk_size=TransitFeed.FILE_CHUNK_SIZE):
                    percent = 100 * read / total_size
                    print("%3d% %" % percent)
                    gtfs.write(chunk)
                    read += TransitFeed.FILE_CHUNK_SIZE


if __name__ == "__main__":
    t1 = TransitFeed()
    feed_version = t1.getLastFeedVersion()
    print(feed_version)
    gtfs_zip_filename = feed_version['id'] + ".zip"
    t1.downloadLastVersion(file_name=gtfs_zip_filename)
    # print(l_v.headers)
