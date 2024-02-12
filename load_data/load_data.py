import argparse
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
import json
from sklearn.preprocessing import StandardScaler
from joblib import dump
from tld import get_tld
import re
from urllib.parse import urlparse


def process_tld(url):
    """
    Extracts the top-level domain (TLD) from the given URL using the 'tldextract' library.

    Args:
        - url (str): The URL from which to extract the TLD.

    Returns:
        - str or None: The top-level domain extracted from the URL. Returns None if the extraction fails.

    Example:
        >>> process_tld("https://www.example.com/path/to/page")
        'www.example.com'
    """
    try:
        res = get_tld(url, as_object=True, fail_silently=False, fix_protocol=True)
        pri_domain = res.parsed_url.netloc
    except:
        pri_domain = None
    return pri_domain


def abnormal_url(url):
    """
    Checks if the given URL does not contain its hostname, which may indicate abnormal URL patterns.

    Args:
        - url (str): The URL to check for abnormal patterns.

    Returns:
        - int: Returns 1 if the URL contains its hostname; otherwise returns 0, suggesting an abnormal pattern.

    Example:
        >>> abnormal_url("https://www.example.com/path/to/page")
        1
    """
    hostname = urlparse(url).hostname
    hostname = str(hostname)
    match = re.search(hostname, url)
    if match:
        return 1
    else:
        return 0


def http_secure(url):
    """
    Checks if the given URL uses the HTTPS protocol for a secure connection.

    Args:
        - url (str): The URL to check for the use of HTTPS.

    Returns:
        - int: Returns 1 if the URL uses HTTPS, indicating a secure connection; otherwise, returns 0.

    Example:
        >>> http_secure("https://www.example.com/path/to/page")
        1
    """
    htp = urlparse(url).scheme
    match = str(htp)
    if match == 'https':
        return 1
    else:
        return 0


def digit_count(url):
    """
    Counts the number of digits in the given URL.

    Args:
        - url (str): The URL in which to count numeric digits.

    Returns:
        - int: The count of numeric digits in the URL.

    Example:
        >>> digit_count("https://www.example123.com/path/to/page")
        3
    """
    digits = 0
    for i in url:
        if i.isnumeric():
            digits += 1
    return digits


def letter_count(url):
    """
    Counts the number of alphabetic letters in the given URL.

    Args:
        - url (str): The URL in which to count alphabetic letters.

    Returns:
        - int: The count of alphabetic letters in the URL.

    Example:
        >>> letter_count("https://www.example.com/PathToPage")
        28
    """
    letters = 0
    for i in url:
        if i.isalpha():
            letters += 1
    return letters


def shortening_service(url):
    """
    Checks if the given URL is associated with a URL shortening service.

    Args:
        - url (str): The URL to check for association with URL shortening services.

    Returns:
        - int: Returns 1 if the URL is associated with a URL shortening service; otherwise, returns 0.

    Example:
        >>> shortening_service("https://bit.ly/abc123")
        1
    """
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return 1
    else:
        return 0


def ip_address(url):
    """
    Checks if the given URL contains an IP address.

    Args:
        - url (str): The URL to check for the presence of an IP address.

    Returns:
        - int: Returns 1 if the URL contains an IP address; otherwise, returns 0.

    Example:
        >>> ip_address("https://192.168.0.1/path/to/page")
        1
    """
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4 with port
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
        '([0-9]+(?:\.[0-9]+){3}:[0-9]+)|'
        '((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)', url)  # Ipv6
    if match:
        return 1
    else:
        return 0


def _load_data(args):
    # Load dataset
    df = pd.read_csv('malicious_phish.csv')
    df['url'] = df['url'].replace('www.', '', regex=True)
    rem = {"Category": {"benign": 0, "defacement": 1, "phishing": 2, "malware": 3}}
    df['Category'] = df['type']
    df = df.replace(rem)

    # Features extraction
    df['url_len'] = df['url'].apply(lambda x: len(str(x)))
    df['domain'] = df['url'].apply(lambda i: process_tld(i))
    features = ['@', '?', '-', '=', '.', '#', '%', '+', '$', '!', '*', ',', '//']
    for feature in features:
        df[feature] = df['url'].apply(lambda i: i.count(feature))
    df['abnormal_url'] = df['url'].apply(lambda i: abnormal_url(i))
    df['https'] = df['url'].apply(lambda i: http_secure(i))
    df['digits'] = df['url'].apply(lambda i: digit_count(i))
    df['letters'] = df['url'].apply(lambda i: letter_count(i))
    df['shortening_service'] = df['url'].apply(lambda i: shortening_service(i))
    df['ip_address'] = df['url'].apply(lambda i: ip_address(i))

    # Test & Train split
    x = df.drop(['url', 'type', 'Category', 'domain'], axis=1)
    y = df['Category']

    scaler = StandardScaler()
    X = scaler.fit_transform(x)
    dump(scaler, args.scaler)
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

    # Creates `data` structure to save and
    # share train and test datasets.
    data = {'x_train': x_train.tolist(), 'y_train': y_train.tolist(), 'x_test': x_test.tolist(),
            'y_test': y_test.tolist()}

    # Creates a json object based on `data`
    data_json = json.dumps(data)

    # Saves the json object into a file
    with open(args.data, 'w') as out_file:
        json.dump(data_json, out_file)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str)
    parser.add_argument('--scaler', type=str)

    args = parser.parse_args()

    # Creating the directory where the output file will be created
    # (the directory may or may not exist).
    Path(args.data).parent.mkdir(parents=True, exist_ok=True)
    Path(args.scaler).parent.mkdir(parents=True, exist_ok=True)

    _load_data(args)
