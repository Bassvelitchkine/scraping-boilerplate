"""
Main file to run the crawler
"""
from utils.Parser import Parser
from utils.Crawler import Crawler

INPUT_FILE = "./data/sample.csv"
OUTPUT_FILE = "./run/extracted_data.csv"
LOGGER_FILE = "./run/logs.log"
PROGRESSION_FILE = "./run/progression.txt"

my_crawler = Crawler(
    Parser(),
    INPUT_FILE,
    output_file=OUTPUT_FILE,
    logger=LOGGER_FILE,
    crawling_progression=PROGRESSION_FILE,
)

try:
    my_crawler.crawl()
except Exception as e:
    print(f"Something went wrong while crawling: {e}")
finally:
    my_crawler.save()
