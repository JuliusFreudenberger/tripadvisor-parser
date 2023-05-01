from tripadvisor_attraction import TripadvisorAttraction, TripadvisorReview

TABLE_HEADING = "username^review_title^review_text^posting_date^count_stars^count_likes^translated_by"


def export_attraction(attraction: TripadvisorAttraction):
    export_string: str = TABLE_HEADING + '\n'
    for review in attraction.reviews:
        export_string += line_for_review(review) + '\n'

    with open(f'export/{attraction.title} ({attraction.count_of_reviews}).csv', 'w') as export_file:
        export_file.writelines(export_string)


def line_for_review(review: TripadvisorReview):
    return f'{review.username}^{review.review_title}^{review.review_text}^' \
           f'{review.posting_date}^{review.count_stars}^{review.count_likes}^{review.translated_by}'
