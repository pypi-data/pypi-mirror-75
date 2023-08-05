# Add descriptions here

import logging
import hashlib

log = logging.getLogger(__name__)

# Look at the requests module
try:
    import requests
    from requests.exceptions import HTTPError
except ModuleNotFoundError:
    print("There is some issue with the module requests")
    raise


def check_pwd(pwd):
    """Check if the given passwpord has been breached online.
    The password is basically checked in the pwnedpasswords
    website.

    Parameters
    ----------
        pwd : str
            Password

    Returns
    -------
        tuple:
            hashpwd password in has
            count the number of appearance
    """
    # Convert password into hash format
    hashpwd = hashlib.sha1(pwd.encode("utf-8")).hexdigest().upper()
    # Slice the password into two parts
    head, tail = hashpwd[:5], hashpwd[5:]
    # Define the url appended with the head
    url = "https://api.pwnedpasswords.com/range/" + head
    # Check the url status
    try:
        log.info("Accessing https://api.pwnedpasswords.com/range/")
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_error:
        log.warning(f"HTTP error occurred: {http_error}")
    except Exception as error:
        log.warning(f"Other error occurred: {error}")
    else:
        log.info("Success!")
    # Format all the corresponding entries
    hashes = (line.split(":") for line in response.text.splitlines())
    # Count the number of times the pwd appears
    count = next((int(count) for t, count in hashes if t == tail), 0)
    # Return the hashed pwd and count
    return hashpwd, count
