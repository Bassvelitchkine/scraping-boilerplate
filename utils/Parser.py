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

    @set_func_headers(headers=["renting_keywords"], func_type="extractor", order=5)
    def __extract_renting_keywords_(self, html_page_content):
        """
        Extract keywords from the HTML page content that suggest the company has renting activities.

        Args:
            html_page_content: String with HTML page content

        Returns:
            Dictionary with key 'renting_keywords' and the keywords found as value
        """
        renting_regex = r"\b(lo(uer|cation)|alquiler|rent(al)?)"
        matches = re.finditer(renting_regex, html_page_content, re.IGNORECASE)
        return {"renting_keywords": [match.group() for match in matches]}

    @set_func_headers(
        headers=["industry_kw", "most_likely_industry", "probability"],
        func_type="extractor",
        order=6,
    )
    def __extract_industry_kw_data_(self, html_content):
        """
        Extract industry keywords from HTML content.
        This method is used to extract keywords that suggests a specific industry,
        such as bike, nautism, etc.

        Args:
            html_content: String containing HTML content. Must be of type str.

        Returns:
            Dictionary with keys 'industry_kw', 'most_likely_industry' and 'probability':
            - The value of 'industry_kw' is a list of keywords found in the HTML content.
            - The value of 'most_likely_industry' is the industry that is most likely
                to be the industry of the company
            - The value of 'probability' is the probability that the company
                is in the industry 'most_likely_industry'.
        """
        regex_patterns = {
            "bike": r"v[ée]lo|bi(ke|cycle(tte)?|cloo)|cycle|(2|deux) roues",
            "nautism": r"paddle|k(ayak|ite)|cano[eë]|nauti(que|c|sme)|bateaux?|jet\-?ski|voile|embarcations?|water|glisse|plaisance",
            "ski": r"ski|snow(\-?board)?|pistes?|mou?nta(in|gne)|neige|glisse",
            "diy": r"jardin(age|erie)?|outil(lage|s)?|motoculture|tondeuse",
            "scooter": r"moto|scoot(er)?|(deux|2) roues",
        }

        # Finding all the keywords
        nb_keywords_found = {}
        all_keywords = []
        total_keywords = 0

        # Find keywords in the html_content and add them to the keywords_found dictionary.
        for industry, regex in regex_patterns.items():
            matches = re.finditer(regex, html_content, re.IGNORECASE)
            keywords = [match.group() for match in matches]
            nb_keywords = len(keywords)

            nb_keywords_found[
                industry
            ] = nb_keywords  # Update the number of keywords found for the industry
            total_keywords += nb_keywords  # Update the total number of keywords found
            all_keywords += keywords  # Update the list of all keywords found

        # Finding the most likely industry
        probability = 0
        most_likely_industry = ""

        # Calculate the probability of the most likely industry.
        if total_keywords > 0:
            # Iterate through industries and their kw to find the most likely one.
            for industry, nb_kw in nb_keywords_found.items():
                computed_prob = nb_kw / total_keywords

                # If the probability is higher than the current one, update the most likely industry.
                if computed_prob > probability:
                    probability = computed_prob
                    most_likely_industry = industry

        return {
            "industry_kw": all_keywords,
            "most_likely_industry": [most_likely_industry],
            "probability": [str(round(probability, ndigits=3))],
        }

    @set_func_headers(
        headers=["software_link", "software_name"], func_type="extractor", order=7
    )
    def __extract_software(self, html_content):
        """
        Extract renting software urls from HTML content.
        Lokki has competitors that offer renting softwares.
        We want to spot such softwares in the HTML content.

        Args:
            html_content: String containing HTML content.

        Returns:
            Dictionary with keys 'software_link' and 'software_name':
                - The value of 'software_link' is a list of urls of the softwares found in the HTML content.
                - The value of 'software_name' is a list of the names of the softwares found in the HTML content.
        """
        regex_patterns = {
            "Skilou": r"skilou(resa)?\.com",
            "Ouibike": r"ouibike\.net",
            "Rodeeo": r"(my\.)?rodeeo\.app",
            "Notre Sphère": r"notresphere\.com",
            "Elloha": r"reservation\.elloha\.com",
            "Regiondo": r"(pro\.)?regiondo\.(com|fr|net)",
            "Trekker": r"book\.trekker\.fr",
            "Canoego": r"www\.canoego\.fr",
            "Axyomes": r"axyomes\.com",
            "Nautic Manager": r"www\.nauticmanager\.com",
            "SamBoat": r"cdn\.samboat\.fr",
            "Guidap": r"(cart\.)?guidap\.(com|net)|(?<=\<)guidap(?=\-)",
            "Surfnow": r"app\.surfnow\.fr",
            "Awoo": r"awoo\.fr",
            "FareHarbor": r"fareharbor\.com",
            "Ginkoia": r"[gG]inkoia",
            "Cilea": r"[cC]ilea",
        }

        software_names = set()
        software_links = set()

        # Find all the software links in the html_content.
        for software, regex in regex_patterns.items():
            matches = re.finditer(regex, html_content)
            links = {match.group() for match in matches}

            # Add found software links to the set of software links.
            # Add the corresponding name too
            if len(links) > 0:
                software_links.update(links)
                software_names.add(software)

        return {
            "software_link": list(software_links),
            "software_name": list(software_names),
        }

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
