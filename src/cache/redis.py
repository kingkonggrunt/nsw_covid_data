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

    def __delitem__(self, key):
        if key in self:
            self.r.delete(key)

    def __contains__(self, key):
        return self.r.exists(key)

    def __repr__(self):
        return f"RedisDictionary(redis.Redis, db={self.db})"

    def __len__(self):
        return len(self.r.scan_iter("*"))

    def find_keys(self, pattern):
        """Search Redis Keys according to a pattern"""
        return list(self.r.scan_iter(pattern))  # TODO: find the way (i forgot) to modify output to non-list if len is zero (without if statements)

    def multi_set(self, d):
        """multi_set
            uses redis' multi set ability to set multiple key:value pairings at once

        Parameters
        ----------
        d : dict
            Dictionary of key:value pairings

        """
        self.r.mset(d)
