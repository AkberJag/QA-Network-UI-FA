import re


def validate_ip_address_string(ip_address: str) -> bool:
    """Check whether the given string is an IP address or not

    Args:
        ip_address (str): a string accepted from the user

    Returns:
        bool: True if the given string is a valid IP address
    """
    # https://www.geeksforgeeks.org/python-program-to-validate-an-ip-address/
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if re.search(regex, ip_address):
        return True
    return False
