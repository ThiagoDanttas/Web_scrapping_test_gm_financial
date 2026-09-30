
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


