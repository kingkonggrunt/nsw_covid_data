import time
import redis
from src import data
from src.cache.redis import RedisDictionary

covid = data.CovidData()
r = RedisDictionary(redis.Redis, db=5)

def main():
    """Update the sources every three hours"""

    while True:
        print(time.localtime())
        print("Clearing Cache")
        for key in r.find_keys("*"):
            del r[key]
        print("Cache Cleared")
        covid.update()
        time.sleep(3*60*60)

if __name__ == '__main__':
    main()
