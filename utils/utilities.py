"""
Utility functions for the project.
"""


def set_func_headers(headers, func_type, order):
    """
    A decorator that sets the headers, func_type and order atributes of a function.

    What I call headers are the names of the data the function returns.
    For example, the function that extracts emails from a website will have the header 'emails'

    It's a decorator to use on methods in a class
    and these methods should be called in a specific order, hence the order attribute.

    Args:
        headers: A list of headers that the function should have
        func_type: The type of function to be called (eg. 'extractor')
        order: The order of the function to be called ( 1 2... )

    Returns:
        The function that performs the attributes assignment
    """

    def do_assignment(to_func):
        """
        Assign headers func_type and order to a function.

        Args:
            to_func: function to be assigned headers, func_type and order

        Returns:
            the function with its assigned attributes
        """
        to_func.headers = headers
        to_func.func_type = func_type
        to_func.order = order
        return to_func

    return do_assignment


def phone_number_normalizer(phone_number):
    """
    Takes a phone number and normalizes its format. Phone numbers can have various formats.
    Standardization enables for comparison between phone numbers.

    The normalization is based on the following rules :
    1. There is no space between numbers.
    2. If there's no country code yet, it's changed to '+33'

    Args:
        phone_number

        Returns:
        The normalized phone number or None if the phone number is invalid.
    """
    just_numbers = "".join([elm for elm in phone_number if elm in "+1234567890"])
    # Returns the string representation of just_numbers withtout spaces.
    if len(just_numbers) > 0:
        if just_numbers[0] == "+":
            # Phone numbers that start with a '+' should have 11 digits.
            if len(just_numbers[1:]) == 11:
                return just_numbers
            else:
                return None
        else:
            # Phone numbers that don't start with a '+' but start with a '0' should have 10 digits.
            if just_numbers[0] == "0" and len(just_numbers) == 10:
                return "+33" + just_numbers[1:]
            # Phone numbers that don't start with a '+',
            # don't start with a '0' and have 9 digits,
            # just need a leading country code
            elif just_numbers[0] != 0 and len(just_numbers) == 9:
                return "+33" + just_numbers
            else:
                return None
    else:
        return None
