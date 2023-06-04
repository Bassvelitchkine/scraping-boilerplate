<div align="center">
<h1 align="center">
<img src="https://prompthero.com/rails/active_storage/representations/proxy/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJaWxoTlRsbVlURm1PQzAwTURObUxUUTJOMlV0T1RneU9TMHhPRFl5T1RRNU1HWTNPR1VHT2daRlZBPT0iLCJleHAiOm51bGwsInB1ciI6ImJsb2JfaWQifX0=--6de2b5c6b269ea95bc713621a198d6c02ea62da4/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaDdDRG9MWm05eWJXRjBPZ2wzWldKd09oUnlaWE5wZW1WZmRHOWZiR2x0YVhSYkIya0NBQWd3T2dwellYWmxjbnNKT2hOemRXSnpZVzF3YkdWZmJXOWtaVWtpQjI5dUJqb0dSVlE2Q25OMGNtbHdWRG9PYVc1MFpYSnNZV05sVkRvTWNYVmhiR2wwZVdsZiIsImV4cCI6bnVsbCwicHVyIjoidmFyaWF0aW9uIn19--9e9280d525ba1fc2f95c971c0fbcb4a2ca8b55dd/prompthero-prompt-59db295c17f.png" width="400" />
<br>
scraping-boilerplate
</h1>
<h3 align="center">📍 Scrape with ease using this Boilerplate!</h3>
<h3 align="center">⚙️ Developed with the software and tools below:</h3>

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white" alt="Python" />
</p>
</div>

---

## 📚 Table of Contents

- [📚 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [📂 Project Structure](#project-structure)
- [🧩 Modules](#modules)
- [🚀 Getting Started](#-getting-started)

---

## 📍 Overview

This codebase provides a web crawling and data extraction tool for scraping websites using regular expressions. The main script initiates the crawling from a CSV input file using a Parser object and saves the progress of the crawler.

The Crawler class provides the ability to extract data and process it, while the Parser class uses regular expressions to extract new emails, phone numbers, linkedin URLs, and Facebook URLs from the HTML of a website.

The value proposition of this project is to automate the scraping process and extract relevant data efficiently and accurately but, most importantly, to provide a boilerplate for future scraping projects.

---

<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-github-open.svg" width="80" />

## 📂 Project Structure

---

<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-src-open.svg" width="80" />

## 🧩 Modules

<details closed><summary>Root</summary>

| File         | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Module             |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----------------- |
| main.py      | The code initiates a web crawler from the provided CSV input file using a Parser object to parse web data, limits the crawling to only 5 web pages (but could be more depanding on the chosen value), and saves the progress of the crawler. In case of any exception, it prints an error message.                                                                                                                                                      | main.py            |
| Crawler.py   | The provided code snippet consists of a Crawler class that has the ability to crawl websites and extract data from them. The class takes in parameters such as the parser to use, input file, output folder, and rate limit. It contains methods to compute header indexes, process extracted data, log progression, and save the crawling progression. One can use the crawl method to scrape websites and write the extracted data to an output file. | utils\Crawler.py   |
| Parser.py    | The provided code snippet contains a Parser class that uses regular expressions to extract new emails, phone numbers, linkedin URLs, and Facebook URLs from the HTML of a website. These extraction methods are decorated with the @set_func_headers decorator to specify headers and order. The Parser class also has methods to get headers and extract content from HTML using all extractor methods in order.                                       | utils\Parser.py    |
| utilities.py | The provided code snippet contains two utility functions. The first function is a decorator that assigns attributes such as headers, func_type, and order to a function. The second function normalizes a phone number based on predefined rules, such as removing spaces and adding country codes.                                                                                                                                                     | utils\utilities.py |

</details>

---

## 🚀 Getting Started

### 🖥 Installation

1. Clone the scraping-boilerplate repository:

```sh
git clone D:/Utilisateurs/Bastien/Documents/Programmation/scraping-boilerplate
```

2. Change to the project directory:

```sh
cd scraping-boilerplate
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

### 🤖 Using scraping-boilerplate

Add your own extractors in the Crawler class following the same structure as the linkedin and facebook extractors for instance:

```python
@set_func_headers(headers=["linkedin_urls"], func_type="extractor", order=3)
def __extract_linkedin_urls(self, html_page_content):
    """
    Extract linkedin urls from the website HTML.

    Args:
        html_page_content: The content of the website HTML page

    Returns:
        A dictionary with the key 'linkedin_urls' and the urls found as value
    """
    # Regular expression pattern to match linkedin urls
    linkedin_regex_pattern = (
        r"https?:\/\/(www\.)?linkedin\.com\/[a-zA-Z%\däëüïöâêûîôàèùìòé\-_,\/]{4,}"
    )

    # Extract linkedin_urls from the website HTML using regular expressions
    matches = re.finditer(linkedin_regex_pattern, html_page_content, re.IGNORECASE)
    return {"linkedin_urls": [match.group() for match in matches]}
```

Change the limit of the crawler in the main.py script. It's currently set to 5, but you can change it to any number you want.

```python
my_crawler.crawl(limit=5)
```

Then, run the main.py script to start the crawler:

```sh
python main.py
```

---
