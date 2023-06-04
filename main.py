"""
Main file to run the crawler
"""
from utils.Parser import Parser
from utils.Crawler import Crawler

INPUT_FILE = "./data/sample.csv"

my_crawler = Crawler(Parser(), INPUT_FILE)

try:
    # You can play with the limit
    my_crawler.crawl(limit=5)
except Exception as e:
    print(f"Something went wrong while crawling: {e}")
finally:
    # Saves the progression.
    # If you execute the code again, you'll pick up where you left off
    my_crawler.save()
