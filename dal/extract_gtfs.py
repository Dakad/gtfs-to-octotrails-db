import pygtfs


def main():
    gtfs_dir = unzip_gtfs("./data/versions/gtfs-light.zip")


def unzip_gtfs(gtfs_light_zip: str) -> str:
    from zipfile import ZipFile

    gtfs_zip = ZipFile(gtfs_light_zip, "r")
    extract_dir = gtfs_zip.filename[:-4]
    gtfs_light_zip.extractall(extract_dir)
    return extract_dir


if __name__ == "__main__":
    main()
