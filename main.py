from src import data

def main():
    cd = data.CovidData()

    cd.update()


if __name__ == '__main__':
    main()
