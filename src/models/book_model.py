from decimal import Decimal
from typing import TypedDict

class BookData(TypedDict):
    url: str
    name: str
    rating: int
    price: Decimal
    in_stock: bool