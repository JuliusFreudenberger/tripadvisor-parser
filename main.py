from concurrent.futures import ThreadPoolExecutor

from csv_exporter import export_attraction
from tripadvisor_parser import TripadvisorAttractionParser


def parse_and_export_attraction(url: str):
    parser = TripadvisorAttractionParser(url.strip())
    attraction = parser.parse()
    export_attraction(attraction)


def get_urls() -> [str]:
    with open("urls.txt", "r") as urls_file:
        return urls_file.readlines()


def main():
    with ThreadPoolExecutor() as executor:
        executor.map(parse_and_export_attraction, get_urls())


if __name__ == "__main__":
    main()
