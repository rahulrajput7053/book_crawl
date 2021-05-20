from scrapy import Spider
from scrapy.http import Request
import scrapy

def product_info(response, value):
    return response.xpath('//th[text()= "'+ value +'"]/following-sibling::td/text()').extract_first()

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com'] 

    def parse(self, response):
        book_url = response.xpath('//h3/a/@href').extract()
        for books in book_url:
            absolute_url = response.urljoin(books)
            yield Request(absolute_url, callback =self.parse_book)
            
        #product next_page
        next_page_url = response.xpath('//a[text()="next"]/@href').extract_first() 
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)

    def parse_book(self, response):
         title = response.xpath('//div[@class = "col-sm-6 product_main"]/h1/text()').extract_first()
         price = response.xpath('//p[@class = "price_color"]/text()').extract_first()
         img_url = response.xpath('//img/@src').extract_first()
         img_url = img_url.replace('../..','http://books.toscrape.com')
         rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
         rating = rating.replace('star-rating', '')
         discription = response.xpath('//*[@id = "product_description"]/following-sibling::p/text()').extract_first()
         upc = product_info(response, 'UPC')
         Product_Type =product_info(response, 'Product Type')
         Price_excl_tax =product_info(response, 'Price (excl. tax)') 
         Price_incl_tax = product_info(response, 'Price (incl. tax)')
         Tax =product_info(response, 'Tax')
         Availability = product_info(response, 'Availability')
         Number_of_reviews =product_info(response, 'Number of reviews')
         

         yield{
             'Title' : title,
             'Price' : price,
             'img_url': img_url,
             'Rating' : rating,
             'Discription' : discription,
             'upc': upc,
             'Product_Type': Product_Type,    
             'Price_(excl. tax)': Price_excl_tax,                                                         
             'Price_(incl. tax)': Price_incl_tax,
             'Tax': Tax,
             'Availability': Availability,
             'Number_of_reviews': Number_of_reviews}
         