from decimal import Decimal
from playwright.sync_api import Page
from loguru import logger
from urllib.parse import urljoin

from utils.helpers import parser_rating
from models.book_model import BookData



class ScrapeBook:

  def __init__(self):
    self.url_base: str = "https://books.toscrape.com"

  def scrape_books(self, page: Page, *, category: str | None, max_books: int) -> list[BookData]:
      """Scrape book data from https://books.toscrape.com/.

      After navigating to the site homepage, scrapes book data following this
      contract:

      - `category` is `None`: scrape all books, following the pagination from
        the homepage without navigating into any category.
      - `category` matches a sidebar category (case-insensitive): scrape only
        that category's books, following its pagination.
      - `category` does not match any sidebar category (or is empty /
        whitespace-only): return an empty list.

      Stops as soon as `max_books` books have been collected and never request
      pages beyond the limit. If `max_books` is less than or equal to zero, an
      empty list is returned.

      Args:
          page: A Playwright page, already created and navigable.
          category: The category to scrape, or `None` to scrape all books.
          max_books: Maximum number of books to scrape.

      Returns:
          A list of the scraped books.
      """

      
      book_list: list[BookData] = [] 
      


      # Start web (Health Check)
      try:
        response = page.goto(self.url_base, timeout=10000)

        if response.ok:
          logger.success(f"Success connection - status code:{response.status}")
          
        else:
          logger.warning(f"Failed connection - status code:{response.status}, body:{response.body()}")
          return
        
      except Exception as e:
          logger.warning(f"Failed connection - {e}")

      # Category list 
      categories: list[str] = page.locator("div.side_categories").all_inner_texts()
      categories: list = [str(cat).replace("\n", ",") for cat in categories]
      categories: list[str] = categories[0].split(",")
      categories: list[str] = [categorie.lower() for categorie in categories]

      
      if category is None:
        
        try:
          url: str = "https://books.toscrape.com/catalogue/category/books_1/index.html"
          
          response = page.goto(url=url, wait_until="domcontentloaded")

          if response.ok:
            logger.success("Main page loaded successfully.")

          else:
            logger.warning(f"Main page failed to load.")

        except Exception as e:
          logger.warning(f"Failed to load - {e}")

        
        next_page = page.locator("li.next a")
        
        logger.info("Extracting all books")

        while True:   
          
          articles: list = page.get_by_role('article').all()
          
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

          if not next_page.is_visible():
            break  

          next_page.click()
          page.wait_for_load_state("domcontentloaded")

        if book_list:
          logger.success("Extract books successfully")
          return book_list
        
        logger.warning("Extract books failed: No books found")
        return []
      
      else:

        if category.lower() in categories:

          logger.success(f"Category {category.lower()} in category list")
          
          category_index = categories.index(category.lower())
          url: str = f'{self.url_base}/catalogue/category/books/{category.lower() + "_" + str(category_index + 1)}/index.html' 

          try:
            
            response = page.goto(url=url, wait_until="domcontentloaded")

            if response.ok:
              logger.success(f"{category.title()} page loaded successfully.")

            else:
              logger.warning(f"{category.title()} page failed to load.")

          except Exception as e:
            logger.warning(f"Failed to load - {e}")

          next_page = page.locator("li.next a")

          
          if next_page.is_visible():
            logger.info(f"Extracting {category.title()} books")
                      
            while True:   
                      
              articles: list = page.get_by_role('article').all()

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
            
              if not next_page.is_visible():
                break
                
              next_page.click()
              page.wait_for_load_state("domcontentloaded")

            if book_list:
              logger.success(f"Extract {category.title()} books successfully")
              return book_list
                    
            logger.warning(f"Extract {category.title()} books failed: No books found")
            return []
            
          else:

            logger.info(f"Extracting {category.title()} books")
            articles: list = page.get_by_role('article').all()

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

            if book_list:
              logger.success(f"Extract {category.title()} books successfully")
              return book_list
                                
            logger.warning(f"Extract {category.title()} books failed: No books found")
            return []
          
      logger.warning(f"Category {category} not in category list")
      return []

      




      
      


      
  


