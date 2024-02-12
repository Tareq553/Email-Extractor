import scrapy
import csv
import re

class EmailExtractorSpider(scrapy.Spider):
    name = 'email_extractor'

    def start_requests(self):
        # Change the path to your CSV file containing website links
        csv_file = 'websites.csv'
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield scrapy.Request(url=row['website'], callback=self.parse, meta={'url': row['website']})

    def parse(self, response):
        # Extract text from the response
        text = response.text
        # Extract URL from meta
        url = response.meta['url']
        # Use regex to find unique email addresses
        emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        # Save emails to a CSV file along with the URL
        with open('emails.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # Check if file is empty
            if file.tell() == 0:
                # Write header only if file is empty
                writer.writerow(['url', 'email'])
            for email in emails:
                writer.writerow([url, email])
                       
#Open cmd and put [scrapy runspider email_extractor.py]
