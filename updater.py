from src import data
import time

covid = data.CovidData()

def main():
    while True:
        print(time.localtime())
        covid.update()
        time.sleep(3*60*60)

if __name__ == '__main__':
    main()
