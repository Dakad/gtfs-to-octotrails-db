import pygtfs


def main():
    sched = pygtfs.Schedule('sqlite:///data/gtfs.sqlite')
    pygtfs.append_feed(sched, "./data/versions/gtfs.zip")
    print(sched)


if __name__ == "__main__":
    main()
