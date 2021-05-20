from scrapy import Spider
from scrapy.http import Request
import scrapy
import os
import glob
import csv
#import MySQLdb
import mysql.connector
#import mysqlclient
#from pymysql import *

def product_info(response, value):
    return response.xpath('//th[text()= "'+ value +'"]/following-sibling::td/text()').extract_first()

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']
    # def __init__(self, category):
    #     self.start_urls = [category]

    def parse(self, response):
        book_url = response.xpath('//h3/a/@href').extract()
        for books in book_url:
            absolute_url = response.urljoin(books)
            yield Request(absolute_url, callback =self.parse_book)

        #product next_page
        # next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        # absolute_next_page_url = response.urljoin(next_page_url)
        # yield Request(absolute_next_page_url)

    def parse_book(self, response):
         title = response.xpath('//div[@class = "col-sm-6 product_main"]/h1/text()').extract_first()
        #  price = response.xpath('//p[@class = "price_color"]/text()').extract_first()
        #  img_url = response.xpath('//img/@src').extract_first()
        #  img_url = img_url.replace('../..','http://books.toscrape.com')
         rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
         rating = rating.replace('star-rating', '')
        #discription = response.xpath('//*[@id = "product_description"]/following-sibling::p/text()').extract_first()
         upc = product_info(response, 'UPC')
         Product_Type =product_info(response, 'Product Type')
        #  Price_excl_tax =product_info(response, 'Price (excl. tax)')
        #  Price_incl_tax = product_info(response, 'Price (incl. tax)')
        #  Tax =product_info(response, 'Tax')
        #  Availability = product_info(response, 'Availability')
        #  Number_of_reviews =product_info(response, 'Number of reviews')


         yield{
             'Title' : title,
            #  'Price' : price,
            #  'img_url': img_url,
             'Rating' : rating,
            #  'Discription' : discription,
             'upc': upc,
             'Product_Type': Product_Type}
            #  'Price_(excl. tax)': Price_excl_tax,
            #  'Price_(incl. tax)': Price_incl_tax,
            #  'Tax': Tax,
            #  'Availability': Availability,
            #  'Number_of_reviews': Number_of_reviews}
    def close(self, reason):
         csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
         #print(csv_file)
         mydb = mysql.connector.connect(host = 'localhost', user= 'root', passwd = '1234@', db = 'book1_db')
         cursor = mydb.cursor()
         with open(csv_file, 'r') as csvfile:
            csv_data = csv.reader(csvfile)
            row_count = 0
            for row in csv_data:
                if row_count != 0:
                    cursor.execute('INSERT IGNORE INTO books1_table(Title, Rating, upc, Product_Type) VALUES(%s, %s, %s, %s)', row)
                row_count += 1
         mydb.commit()
         mydb.commit()
         
     #     # cursor = mydb.cursor()
    #     csv_data = csv.reader(csv_file)
    #     row_count = 0
    #     for row in csv_data:
    #         print(row)
    #     #     if row_count != 0:
    #     #         cursor.execute('INSERT IGNORE INTO books_table(Title, Rating, upc, Product_Type) VALUES(%s, %s, %s, %s)', row)
    #     #     row_count += 1
    #     # mydb.commit()
    #     # mydb.commit()
