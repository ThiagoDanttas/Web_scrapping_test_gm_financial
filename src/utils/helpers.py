from playwright.sync_api import Page

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


# Function to find the category of books
def get_categories(page: Page) -> list:
        categories: list[str] = page.locator("div.side_categories").all_inner_texts()
        categories: list = [str(category).replace("\n", ",") for category in categories]
        categories: list[str] = categories[0].split(",")
        categories: list[str] = [category.lower() for category in categories]
        return categories