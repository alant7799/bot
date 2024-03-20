import scrapy


class BookscraperSpider(scrapy.Spider):
    name = "bookscraper"
    allowed_domains = ["books.toscrape.com"] # prevent spider from crawling into other websites by links in the scraping material
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        
        books = response.css("article.product_pod")
        
        for book in books: # yield es un return pero por item, no espera a que termine ejecucion y devolver todos juntos
            yield {
                'name' : book.css("h3 a::text").get(),
                'price' : book.css(".product_price .price_color::text").get(),
                'url' : book.css("h3 a").attrib["href"]
            }
            
            next_page_relative_url = response.css('li.next a').attrib["href"]
            
            if next_page_relative_url is not None:
                if "catalogue/" in next_page_relative_url:
                    next_page = "https://books.toscrape.com/" + next_page_relative_url
                else:
                    next_page = "https://books.toscrape.com/catalogue/" + next_page_relative_url
                yield response.follow(next_page, callback=self.parse)
                
    def parse_parse_book_