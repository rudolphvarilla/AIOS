from core.search.result import SearchResult
from core.search.summarizer import SearchSummarizer


def main():

    summarizer = SearchSummarizer()

    results = [

        SearchResult(

            title="Wikipedia",

            url="https://wikipedia.org",

            snippet="Tokyo is the capital of Japan."

        ),

        SearchResult(

            title="Booking",

            url="https://booking.com",

            snippet="Compare more than 19,000 hotels."

        ),

        SearchResult(

            title="Tripadvisor",

            url="https://tripadvisor.com",

            snippet="Traveler hotel reviews."

        ),

    ]

    summary = summarizer.summarize(

        "best hotels in tokyo",

        results,

    )

    print(summary.text)


if __name__ == "__main__":

    main()
