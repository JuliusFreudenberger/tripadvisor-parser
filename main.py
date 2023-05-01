from csv_exporter import export_attraction
from tripadvisor_attraction import TripadvisorAttraction
from tripadvisor_parser import TripadvisorAttractionParser


def parse_locations(urls: [str]) -> [TripadvisorAttraction]:
    attractions = []
    for url in urls:
        attractions.append(parse_location(url))

    return attractions


def parse_location(url: str) -> TripadvisorAttraction:
    parser = TripadvisorAttractionParser(url.strip())
    return parser.parse()


def get_urls() -> [str]:
    with open("urls.txt", "r") as urls_file:
        return urls_file.readlines()


if __name__ == "__main__":
    attractions = parse_locations(get_urls())
    for attraction in attractions:
        export_attraction(attraction)
