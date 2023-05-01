import math

import requests
from bs4 import BeautifulSoup, Tag

from tripadvisor_attraction import TripadvisorAttraction, TripadvisorReview

USERAGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0"
HEADERS = {"User-Agent": USERAGENT}


class ReviewsPageInformation:
    page_size: int
    page_count: int

    def __init__(self, page_size, page_count):
        self.page_size = page_size
        self.page_count = page_count


class TripadvisorAttractionReviewParser:
    reviews_page_information: ReviewsPageInformation
    base_url: str
    review_urls: [str]
    raw_reviews: [str]
    review_soups: [BeautifulSoup]

    def __init__(self, reviews_page_information: ReviewsPageInformation, base_url: str):
        self.reviews_page_information = reviews_page_information
        self.base_url = base_url
        self.review_urls = []
        self.raw_reviews = []
        self.review_soups = []

    def parse_reviews(self) -> [TripadvisorReview]:
        print("Constructing Review URLs")
        self.construct_reviews_urls()
        print("Requesting Reviews")
        self.request_reviews()
        print("Souping Reviews")
        self.soup_reviews()

        reviews = []
        print("Parsing Reviews")
        for review_soup in self.review_soups:
            review_cards = review_soup.find_all("div", attrs={"data-automation": "reviewCard"})
            parsed_review_cards = self.parse_review_card(review_cards)
            reviews.extend(parsed_review_cards)

        return reviews

    def construct_reviews_urls(self):
        [prefix, suffix] = self.base_url.split("-Reviews-")
        self.review_urls.append(self.base_url)
        for review_index in range(self.reviews_page_information.page_size,
                                  self.reviews_page_information.page_size * self.reviews_page_information.page_count,
                                  self.reviews_page_information.page_size):
            self.review_urls.append(f'{prefix}-Reviews-or{review_index}-{suffix}')

    def request_reviews(self):
        for review_url in self.review_urls:
            self.raw_reviews.append(requests.get(review_url, headers=HEADERS).text)

    def soup_reviews(self):
        for review in self.raw_reviews:
            self.review_soups.append(BeautifulSoup(review, features="html.parser"))

    def parse_review_card(self, soups: [Tag]) -> [TripadvisorReview]:
        reviews = []
        for soup in soups:
            reviews.append(self.parse_review(soup))
        return reviews

    def parse_review(self, soup: Tag) -> TripadvisorReview:
        [review_title, review_text] = soup.find_all("span", class_="yCeTE")
        review = TripadvisorReview()
        review.review_title = review_title.text
        review.review_text = review_text.text
        posting_date_tag = soup.find("div", class_="RpeCd")
        if posting_date_tag is not None:
            review.posting_date = posting_date_tag.text.split(" •")[0]
        else:
            review.posting_date = ""
        review.username = soup.find("a", class_="ukgoS").text
        review.count_stars = float(soup.find("svg", class_="H0").get("aria-label").split(" ")[0].replace(',', '.'))
        review.count_likes = int(soup.find("span", class_="biGQs _P FwFXZ").text)
        translation_hint = soup.find("span", class_="Ne d Vm")
        if translation_hint is not None:
            review.translated_by = translation_hint.img.get("alt")
        else:
            review.translated_by = ""
        return review


class TripadvisorAttractionParser:
    url: str
    soup: BeautifulSoup

    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print("No status code 200")

        html = response.text
        self.soup = BeautifulSoup(html, features="html.parser")

    def parse(self) -> TripadvisorAttraction:
        attraction = TripadvisorAttraction()
        attraction.title = self.parse_title()
        attraction.count_of_reviews = self.parse_count_of_reviews()
        attraction.reviews = self.parse_reviews()

        return attraction

    def parse_title(self) -> str:
        return self.soup.find("h1", attrs={"data-automation": "mainH1"}).text

    def parse_count_of_reviews(self) -> int:
        return int(
            self.soup.find("span", class_="KAVFZ").text.split("\xa0", maxsplit=2)[0].replace(',', '').replace('.', ''))

    def parse_reviews(self) -> [TripadvisorReview]:
        pagination_info = self.soup.find("div", class_="Ci").text
        first_review_index = int(pagination_info.split(" ")[1].split(" ")[0])
        last_review_index = int(pagination_info.split(" ")[3].split(" ")[0])
        total_review_count = int(self.soup.find("button", class_="OKHdJ z Pc PQ Pp PD W _S Gn Z B2 BF _M PQFNM wSSLS").get("aria-label").split('(')[-1].split(')')[0].replace('.', ''))
        page_size = last_review_index - first_review_index + 1
        reviews_page_information = ReviewsPageInformation(page_size,
                                                          page_count=math.ceil(total_review_count / page_size))

        return TripadvisorAttractionReviewParser(reviews_page_information, self.url).parse_reviews()
