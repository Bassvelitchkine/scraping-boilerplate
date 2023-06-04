"""
This module contains the Parser class which is used to parse the HTML of a website
and extract relevant data.
"""
import re
from utils.utilities import set_func_headers, phone_number_normalizer


class Parser:
    """
    This class is used to parse the HTML of a website and extract new emails
    and phone numbers from it for instance. it all depends on the use case.

    But you'll mostly find methods to extract specific patterns using regular expressions.
    """

    def __init__(self):
        """
        Initialize the object and pass.
        """
        pass

    # Every extraction method below
    @set_func_headers(headers=["emails"], func_type="extractor", order=1)
    def __extract_new_emails(self, html_page_content):
        """
        Extracts new email addresses from the website HTML.

        Args:
            html_page_content: HTML content of the website

        Returns:
            A dictionary with key 'emails' and the new_emails as value
        """
        # Regular expression pattern to match email addresses
        # Test it here: https://regex101.com/r/N4CA8t/1
        email_regex_pattern = (
            r"[A-Za-z0-9._%+-]{1,200}@[A-Za-z0-9.-]{1,200}\.[A-Za-z]{2,}"
        )

        # Extract email addresses from the website HTML using regular expressions
        matches = re.finditer(email_regex_pattern, html_page_content)
        email_addresses = [match.group() for match in matches]

        return {
            "emails": [email for email in email_addresses if not email.endswith("gif")]
        }

    @set_func_headers(headers=["phone_numbers"], func_type="extractor", order=2)
    def __extract_new_phone_number(self, html_page_content):
        """
        Extracts new phone numbers from the website HTML.

        Args:
            html_page_content: HTML content of the website

        Returns:
            Dictionary with key 'phone_numbers' and a list of normalized phone numbers as value.
        """
        # Regular expression pattern to match phone numbers
        # Test it here: https://regex101.com/r/64CYbo/1
        phone_regex_pattern = (
            r"""(?<=['\"\s])\+?\(?(33|0)\)?[\.\- ]?[1-9]([\-\. ]?\d{2}){4}(?=[^\d])"""
        )

        # Extract phone numbers from the website HTML using regular expressions
        matches = re.finditer(phone_regex_pattern, html_page_content)
        return {
            "phone_numbers": [
                phone_number_normalizer(match.group()) for match in matches
            ]
        }

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

    @set_func_headers(headers=["facebook_urls"], func_type="extractor", order=4)
    def __extract_facebook_urls(self, html_page_content):
        """
        Extract facebook urls from the website HTML and return them as a dictionary.

        Args:
            html_page_content: HTML content of the website

        Returns:
            Dictionary with key 'facebook_urls' and the urls found as value
        """
        # Regular expression pattern to match linkedin urls
        facebook_regex_pattern = (
            r"https?:\/\/(www\.)?facebook\.com\/[a-zA-Z%\däëüïöâêûîôàèùìòé\-_,\.\/]{3,}"
        )

        # Extract facebook urls from the website HTML using regular expressions
        matches = re.finditer(facebook_regex_pattern, html_page_content)
        return {"facebook_urls": [match.group() for match in matches]}

    def __get_extractors_in_order(self):
        """
           Get all the extractor methods that are part of the Parser class
           sorted by their order (an attribute of the function, set by a decorator)

        Returns:
                A list of parser methods that are part of the Parser class sorted by their order
        """

        def filterout_non_extractors(func):
            """
            Filter out functions that aren't extractors.
            An extractor is a function that has an attribute func_type set to 'extractor'

            Args:
                func: The function to filter in or out

            Returns:
                True if the function is an extractor, False otherwise
            """
            try:
                _ = func.func_type == "extractor"
                return True
            except AttributeError:
                return False

        class_attributes = Parser.__dict__.values()
        extractor_methods_only = filter(filterout_non_extractors, class_attributes)
        sorted_by_order = sorted(extractor_methods_only, key=lambda val: val.order)
        return sorted_by_order

    def get_headers(self):
        """
        Get headers from all extractors in order and concatenate them.

        Returns:
            A list of headers from all extractors in order.
        """
        extractors_in_order = self.__get_extractors_in_order()

        headers = []
        for extractor in extractors_in_order:
            headers += extractor.headers
        return headers

    def extract(self, html_content):
        """
           Extract content from HTML content using all the extractor methods in order.

        Args:
            html_content: The HTML to parse. Should be a string.

        Returns:
            A dictionary of all the content extracted keyed by content type.
        """
        extractors = self.__get_extractors_in_order()
        res = {}
        for extractor in extractors:
            extracted = extractor(self, html_content)
            res.update(extracted)
        return res
