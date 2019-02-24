
import requests as req

from config import Config

BASE_URL = Config.TRANSITFEED_API_URL + Config.TRANSITFEED_API_VERSION
GET_feed_versions = "/getFeedVersions"


class TransitFeed(object):
    """Handle the request to TransitFeed API

    Arguments:


    Returns:

    """

    def getLastFeedVersion(self):
        """Retrieve the Last Version of the STIB Feed

        Returns:
            object -- Data about the last version feed
        """

        feed_version = None
        res = req.get(BASE_URL+GET_feed_versions, params={
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
            feed_version = {
                "id": last_version['id'],
                "size": last_version['size'],
                "registred_date": last_version['ts'],
                "url": last_version['url'],
                "start_date": last_version['d']['s'],
                "finish_date": last_version['d']['f']
            }
        return feed_version


if __name__ == "__main__":
    t1 = TransitFeed()
    l_v = t1.getLastFeedVersion()
    print(l_v)
