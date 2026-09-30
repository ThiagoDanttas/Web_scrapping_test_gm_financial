from playwright.sync_api import Page
from models.book_model import BookData
from loguru import logger
from urllib.parse import urljoin
from decimal import Decimal
from utils.helpers import parser_rating


def extract_datas_books(page: Page, max_books: int) -> list[BookData]:
          
    book_list: list[BookData] = [] 

    articles: list = page.get_by_role('article').all()
    next_page = page.locator("li.next a") 

    while True:
              
        for article in articles:
                
            rating: str = article.locator(".star-rating").get_attribute("class")
            rating: str = parser_rating(str(rating.split()[-1]).lower())
            book_title: str = article.locator('a[title]').get_attribute("title")
            price: Decimal = Decimal(article.locator("p.price_color").inner_text().strip("£"))
            in_stock: bool = str(article.locator(".availability").inner_text()).strip() == "In stock"
            url: str = urljoin(page.url, article.locator("h3 a").get_attribute('href'))

            book_list.append(
                BookData(
                    url=url, 
                    name=book_title, 
                    rating=rating, 
                    price=price, 
                    in_stock=in_stock
                )
            )

            """
            Stops as soon as `max_books` books have been collected and never request
            pages beyond the limit.
            """
            if len(book_list) == max_books:
                logger.info(f"Extracted {max_books} books")
                logger.success(f"Books successfully extracted")
                return book_list

        if not next_page.is_visible():
            return book_list
        
        next_page.click()
        page.wait_for_load_state()

    

    

    