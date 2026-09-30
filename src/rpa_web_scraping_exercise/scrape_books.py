from decimal import Decimal
from playwright.sync_api import Page
from loguru import logger
from urllib.parse import urljoin

from utils.helpers import parser_rating
from utils.extraction import extract_datas_books
from models.book_model import BookData



class ScrapeBook:

  def __init__(self):
    self.url_base: str = "https://books.toscrape.com"

  def scrape_books(self, page: Page, *, category: str | None, max_books: int) -> list[BookData]:
      """Scrape book data from https://books.toscrape.com/.

      After navigating to the site homepage, scrapes book data following this
      contract:

      - `category` is `None`: scrape all books, following the pagination from
        the homepage without navigating into any category. ---OK

      - `category` matches a sidebar category (case-insensitive): scrape only
        that category's books, following its pagination. --- OK

      - `category` does not match any sidebar category (or is empty /
        whitespace-only): return an empty list. --- OK

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

      

    
      # Start web (Health Check)
      
      try:
        response = page.goto(self.url_base, timeout=10000)

        if response.ok:
          logger.success(f"Success connection - status code:{response.status}")
          
        else:
          logger.error(f"Failed connection - status code:{response.status}, body:{response.body()}")
          return
        
      except Exception as e:
          logger.error(f"Failed connection - {e}")

      # Category list 
      categories: list[str] = page.locator("div.side_categories").all_inner_texts()
      categories: list = [str(cat).replace("\n", ",") for cat in categories]
      categories: list[str] = categories[0].split(",")
      categories: list[str] = [categorie.lower() for categorie in categories]


      # Validations 

      """

      - `category` does not match any sidebar category (or is empty /
          whitespace-only): return an empty list.
      
      """
      if category is not None and not category.strip():
        logger.warning(f"Invalid category: {category}")
        return []   

      """

       If `max_books` is less than or equal to zero, an
      empty list is returned.
      
      """
      
      if max_books <= 0:
        logger.warning(f"max_books must be > 0, got {max_books}")
        return []   


      """

      - `category` is `None`: scrape all books, following the pagination from
        the homepage without navigating into any category.

      """
      if category is None:
        
        try:
          url: str = f"{self.url_base}/catalogue/category/books_1/index.html"
          
          response = page.goto(url=url, wait_until="domcontentloaded")

          if response.ok:
            logger.success("Main page loaded successfully.")

          else:
            logger.error(f"Main page failed to load.")

        except Exception as e:
          logger.error(f"Failed to load main page - {e}")


        logger.info("Extracting books")
        extraction: list[BookData] = extract_datas_books(page=page, max_books=max_books)

        if extraction:
          logger.success(f"All books extracted successfully")
          return extraction
                  
        logger.warning(f"Failed to extract books: no books found")
        return []
      
      else:

        """

        - `category` matches a sidebar category (case-insensitive): scrape only
            that category's books, following its pagination.
        
        """
        
        if category.lower() in categories:

          logger.success(f"Category {category.title()} in category list")
          
          category_index = categories.index(category.lower())
          url: str = f'{self.url_base}/catalogue/category/books/{category.lower() + "_" + str(category_index + 1)}/index.html' 

          try:
            
            response = page.goto(url=url, wait_until="domcontentloaded")

            if response.ok:
              logger.success(f"{category.title()} page loaded successfully.")

            else:
              logger.error(f"{category.title()} page failed to load.")

          except Exception as e:
            logger.error(f"Failed to load {category.title()} page - {e}")
        
          next_page = page.locator("li.next a")

          if next_page.is_visible():

            logger.info(f"Extracting {category.title()} books")
            extraction: list[BookData] = extract_datas_books(page=page, max_books=max_books)

            if extraction:
              logger.success(f"Successfully extracted {category.title()} books")
              return extraction
                                      
            logger.warning(f"Failed to extract books: no books found")
            return []
            
          else:

            logger.info(f"Extracting {category.title()} books")
            
            articles: list = page.get_by_role('article').all()
            book_list: list[BookData] = [] 

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

              if len(book_list) == max_books:
                logger.info(f"Extrated {max_books} books")
                logger.success(f"Successfully extracted {category.title()} books")
                return book_list

            if book_list:
              logger.success(f"Successfully extracted {category.title()} books")
              return book_list
                                
            logger.warning(f"Failed to extract {category.title()} books: no books found")
            return []

        """- `category` does not match any sidebar category """  
        logger.warning(f"Category '{category}' not in category list")
        return []

