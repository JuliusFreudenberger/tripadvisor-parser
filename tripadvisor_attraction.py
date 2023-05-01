class TripadvisorReview:
    posting_date: str
    username: str
    review_title: str
    review_text: str
    count_stars: float
    count_likes: int
    translated_by: str

    def __str__(self):
        return f'{self.posting_date}: {self.review_title} - {self.review_text}'


class TripadvisorAttraction:
    title: str
    count_of_reviews: int
    reviews: [TripadvisorReview]

    def __str__(self):
        return f'{self.title} ({len(self.reviews)} parsed of {self.count_of_reviews} total reviews)'
