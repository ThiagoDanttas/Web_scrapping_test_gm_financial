from playwright.sync_api import Page, Response
from loguru import logger


# Health Check function
def health_check(page: Page, url) -> Response:

    try:
        response = page.goto(url=url, timeout=10000)

    except Exception as e:
        logger.error(f"Failed connection - {e}")

    return response


# Function to find the category of books
def get_categories(page: Page) -> list:
        categories: list[str] = page.locator("div.side_categories").all_inner_texts()
        categories: list = [str(category).replace("\n", ",") for category in categories]
        categories: list[str] = categories[0].split(",")
        categories: list[str] = [category.lower() for category in categories]
        return categories



# Function to to parse a string -> int
def parser_rating(rating: str) -> int:

    match(rating):
        case "one":
            return 1
        case "two":
            return 2
        case "three":
            return 3
        case "four":
            return 4
        case "five":
            return 5
        case _:
            return None




