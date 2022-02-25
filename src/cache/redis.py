import redis


class RedisDictionary():
    """
    A redis connnection that behaves like a Python Dictionary (by design)

    rdict = RedisDictionary(db=1)
    ridct["key"] = "value"
    rdict["key"]
    >>> "value"

    Parameters
    ----------
    r : redis.Redis
        An uninstanced Redis Class
    db : int
        database number for the redis connection

    """

    def __init__(self, r: redis.Redis, db):

        self.db = db
        self.r = r(db=self.db)

    def __getitem__(self, key):
        return self.r.get(key).decode('utf-8')

    def __setitem__(self, key, value):
        self.r.set(key, value)

    def __contains__(self, key):
        return self.r.exists(key)

    def __repr__(self):
        return f"RedisDictionary(redis.Redis, db={self.db})"

    def multi_set(self, d):
        """multi_set
            uses redis' multi set ability to set multiple key:value pairings at once

        Parameters
        ----------
        d : dict
            Dictionary of key:value pairings

        """
        self.r.mset(d)
