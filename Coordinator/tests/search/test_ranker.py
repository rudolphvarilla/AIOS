from core.search.result import SearchResult
from core.search.ranker import SearchRanker


def main():

    ranker = SearchRanker()

    results = [

        SearchResult(
            title="Random Blog",
            url="https://randomblog.xyz",
            snippet="Random travel blog."
        ),

        SearchResult(
            title="Wikipedia",
            url="https://wikipedia.org/wiki/Tokyo",
            snippet="Tokyo article."
        ),

        SearchResult(
            title="Booking",
            url="https://booking.com",
            snippet="Tokyo hotels."
        ),

        SearchResult(
            title="TripAdvisor",
            url="https://tripadvisor.com",
            snippet="Hotel reviews."
        ),

    ]

    ranked = ranker.rank(results)

    print("\n===== RANKED RESULTS =====\n")

    for result in ranked:

        print(result.url)


if __name__ == "__main__":

    main()