"""
The Crawler class is responsible for crawling the websites and extracting the data from them.
"""
import csv
import datetime
import pickle as pk
import time
from functools import reduce

import requests

from utils.utilities import phone_number_normalizer


class Crawler:
    """
    The Crawler class is responsible for crawling the websites and extracting the data from them.
    """

    def __init__(
        self,
        parser,
        input_file,
        output_file="output.csv",
        logger="logs.log",
        crawling_progression="progression.txt",
        rate_limit=None,
    ):
        """
        The init method of the Crawler class.
        Sets attributes, computes header indexes and existing emails and phone numbers.

        Parameters
        ----------
        parser : Parser
            The custom parser to use for the crawling. It's an instance of the Parser class.
        input_file : str
            The path to the input file_
        output_file : str, optional
            The path to the output file, by default 'output.csv'
        logger : str, optional
            The path to the file to log the progress, by default 'logs.log'
        crawling_progression : str, optional
            The file where to save the crawler instance after a crawling session,
            by default 'progression.txt'
        rate_limit : _type_, optional
            A rate limit to slow down the crawling if needed, by default None
        """
        self.crawling_progression_ = crawling_progression
        self.index_ = -1
        self.rate_limit = rate_limit
        self.parser = parser

        self.__set_input_file(input_file)
        self.__set_output_file(output_file)
        self.__set_logger(logger)

        # If there's a file to load, we load it
        self.__load()

    def __load(self):
        """
        Loads the crawler instance from the crawling_progression_ file if there's been
        a previous crawling session.
        """
        # We look for a crawling_progression_ file
        try:
            # If one is found we load it
            with open(self.crawling_progression_, "rb") as f:
                unpickler = pk.Unpickler(f)
                self.__dict__ = unpickler.load()
        # Otherwise we set the attributes to their default values
        # By computing header indexes and existing emails and phone numbers
        except FileNotFoundError:
            self.header_indexes_ = self.__compute_header_indexes()
            (
                self.existing_emails_,
                self.existing_phone_numbers_,
            ) = self.__list_existing_phones_and_emails()

    def __set_input_file(self, input_file):
        """
        Sets the input file_ attribute if the input file_ has the required columns.

        Parameters
        ----------
        input_file : str
            The path to the input file_

        Raises
        ------
        ValueError
            If the input file_ doesn't have the required columns
        """
        with open(input_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            has_required_columns = all(
                column in header for column in ["website", "email", "phone"]
            )

            if has_required_columns:
                self.input_file_ = input_file
            else:
                raise ValueError(
                    "You need a 'website', an 'email' and a 'phone' column in your input csv file. Modify your file or try with a different one"
                )

    def __set_output_file(self, output_file):
        """
        Sets the output file_ attribute.

        Parameters
        ----------
        output_file : str
            The path to the output file
        """
        self.output_file_ = output_file

    def __set_logger(self, logger):
        """
        Sets the logger attribute.

        Parameters
        ----------
        logger : str
            The path to the logger file
        """
        self.logger_ = logger

    def __log(self, website, outcome, print_it=True):
        """
        Logs the crawling progression in the logger_ file and prints the progression if print_it is True.

        Parameters
        ----------
        website : str
            The website that has been crawled
        outcome : str
            The outcome of the crawling (success or failure)
        print_it : bool, optional
            Whether to print the progress or not, by default True
        """
        if print_it:
            print(f"{website} - {outcome}")

        # We keep only the first part of the date
        now = str(datetime.datetime.now()).split(".")[0]
        with open(self.logger_, "a", newline="\n", encoding="utf-8") as logger:
            logger.write(f"{website} , {outcome} , {now}\n")

    def __compute_header_indexes(self):
        """
        Computes the header indexes of the input file_.

        Returns
        -------
        dict
            A dict with the column names as keys and their indexes as values
        """
        with open(self.input_file_, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            return {column: header.index(column) for column in header}

    def __list_existing_phones_and_emails(self):
        """
        Lists the existing emails and phone numbers from the input file_.

        Returns
        -------
        tuple
            A tuple containing the sets of existing emails and phone numbers
        """
        # Open the input CSV file
        with open(self.input_file_, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            _ = next(reader)

            # Read existing email and phone numbers from the input file and store them in sets
            existing_emails = set()
            existing_phone_numbers = set()

            for row in reader:
                emails = row[self.header_indexes_["email"]]
                # If there are emails in the cell
                if emails:
                    # split them in a list and remove trailing whitespaces
                    emails_list = [email.strip().lower() for email in emails.split(",")]
                    for email in emails_list:
                        # If the email is not empty, we add it to the set
                        if email:
                            existing_emails.add(email)

                phones = row[self.header_indexes_["phone"]]
                # If there are phone numbers in the cell
                if phones:
                    # split them in a list and remove trailing whitespaces
                    phones_list = [phone.strip().lower() for phone in phones.split(",")]
                    for phone in phones_list:
                        # If the phone number is not empty, we add it to the set
                        if phone:
                            existing_phone_numbers.add(phone_number_normalizer(phone))

        return existing_emails, existing_phone_numbers

    def __process_extracted_data(self, headers, extracted_data):
        """
        From a dict of headers as keys and lists of extracted data as values,
        returns a dict of headers as keys and strings of extracted data as values.

        Values are comma separated if there are several values.

        Parameters
        ----------
        headers : list
            Every header that should be in the output file in the right order
        extracted_data : dict
            The extracted data from the website in the form of a dict with headers as keys and
            lists of extracted data as values
        """

        def reducer(accumulator, key_val):
            """
            A helper function to reduce the extracted data dict to a dict of strings.

            Parameters
            ----------
            accumulator : dict
                The dict that will be returned that accumulates the data
            key_val : tuple
                The tuple of key and value to be processed from the extracted data dict

            Returns
            -------
            list
                The new row with the extracted data
            """
            header = key_val[0]
            data = set(key_val[1])

            if header == "emails":
                # We update the set of existing emails with the new ones
                self.existing_emails_.update(data)
                # We compute the new emails by removing the existing ones from the new ones
                new_emails = data.difference(self.existing_emails_)
                accumulator[header] = ", ".join(new_emails)
            elif header == "phone_numbers":
                # We update the set of existing phone numbers with the new ones
                self.existing_phone_numbers_.update(data)
                # We compute the new phone numbers by removing the existing ones from the new ones
                new_phone_numbers = data.difference(self.existing_phone_numbers_)
                accumulator[header] = ", ".join(new_phone_numbers)
            else:
                accumulator[header] = ", ".join(data)

            return accumulator

        processed_data = dict(reduce(reducer, extracted_data.items(), {}))

        res = []
        for _, header in enumerate(headers):
            res.append(processed_data[header])

        return res

    def crawl(self, limit=100):
        """
        Crawls the websites in the input file and writes the extracted data in the output file.

        Parameters
        ----------
        limit : int, optional
            The limit number of websites to crawl at once, by default 100
        """
        scraped_this_time = 0
        additional_headers = self.parser.get_headers()

        # Create a new/open CSV file to append the crawled URLs data
        with open(self.output_file_, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            with open(self.input_file_, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader)

                # If the file is empty, write the header
                if self.index_ == -1:
                    writer.writerow(header + additional_headers)

                for index, row in enumerate(reader):
                    # If the row has already been scraped, we skip it
                    # If the limit has been reached, we stop
                    if index > self.index_ and scraped_this_time < limit:
                        website = row[self.header_indexes_["website"]]

                        # Check if website exists
                        try:
                            response = requests.get(website, timeout=5)
                            # Raise an exception for non-successful status codes
                            response.raise_for_status()
                        except (
                            requests.RequestException,
                            requests.exceptions.MissingSchema,
                        ):
                            # If website does not exist or crawling failed,
                            # add empty results and continue to the next row
                            # after incrementing the index
                            writer.writerow(row + len(additional_headers) * [""])
                            self.__log(website, "error")
                            scraped_this_time += 1
                            continue

                        html_content = response.text

                        # Extract the data from the website
                        extracted_data = self.parser.extract(html_content)

                        # Format the extracted data as a list of strings
                        formatted_data = self.__process_extracted_data(
                            additional_headers, extracted_data
                        )

                        writer.writerow(row + formatted_data)

                        self.index_ = index
                        self.__log(website, "success")
                        scraped_this_time += 1

                        # Pause for the rate limit if needed
                        if self.rate_limit:
                            time.sleep(self.rate_limit)

    def save(self):
        """
        Saves the crawling progression in a pickle file.
        """
        with open(self.crawling_progression_, "wb") as f:
            pickler = pk.Pickler(f)
            pickler.dump(self.__dict__)
