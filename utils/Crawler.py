"""
The Crawler class is responsible for crawling the websites and extracting the data from them.
"""
import csv
import datetime
import pickle as pk
import time
from functools import reduce

import requests


class Crawler:
    """
    The Crawler class is responsible for crawling the websites and extracting the data from them.
    """

    def __init__(
        self, parser=None, input_file=None, output_folder="./run", rate_limit=None
    ):
        """
        The init method of the Crawler class.
        Sets attributes, computes header indexes.

        Parameters
        ----------
        parser : Parser
            The custom parser to use for the crawling. It's an instance of the Parser class.
        input_file : str
            The path to the input file
        output_folder : str, optional
            The path to the output folder, by default './run'
        rate_limit : int, optional
            A rate limit to slow down the crawling if needed, by default None
        """
        self.crawling_progression_ = output_folder + "progression.txt"

        # We look for a crawling_progression_ file
        try:
            # If one is found we load it
            with open(self.crawling_progression_, "rb") as file:
                unpickler = pk.Unpickler(file)
                self.__dict__ = unpickler.load()
        except FileNotFoundError:
            # Otherwise we set the attributes to their default values
            self.index_ = -1
            self.rate_limit = rate_limit
            self.parser = parser
            self.output_file_ = output_folder + "extracted_data.csv"
            self.logger_ = output_folder + "logs.log"
            self.header_indexes_ = self.__compute_header_indexes()
            self.__set_input_file(input_file)

    def __set_input_file(self, input_file):
        """
        Sets the input file attribute if the input file has the required columns.

        Parameters
        ----------
        input_file : str
            The path to the input file

        Raises
        ------
        ValueError
            If the input file_ doesn't have a website column
        """
        with open(input_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)

            if "website" in header:
                self.input_file_ = input_file
            else:
                raise ValueError("You need a 'website' column in your input csv file.")

    def __log(self, website, outcome, print_it=True):
        """
        Logs the crawling progression in the logger file and prints the progression if print_it is True.

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
        Computes the header indexes of the input file.

        Returns
        -------
        dict
            A dict with the column names as keys and their indexes as values
        """
        with open(self.input_file_, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            return {column: header.index(column) for column in header}

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
        with open(self.crawling_progression_, "wb") as file:
            pickler = pk.Pickler(file)
            pickler.dump(self.__dict__)
