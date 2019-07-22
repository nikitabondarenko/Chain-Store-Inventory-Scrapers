# -*- coding: utf-8 -*-
import csv
import re
import datetime
import urllib
import urlparse


RE_EMAIL = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))


def regex_extractor(regex, text, group):
    data = None
    if regex and text:
        data_search = re.search(regex, text, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        if data_search:
            data = data_search.group(group).strip()
    return data


def flatten(l):
    return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]


def convert_date_string(date_string, old_format, new_format):
    converted = None
    if date_string and old_format and new_format:
        date = datetime.datetime.strptime(date_string, old_format)
        converted = date.strftime(new_format)
    return converted


def extract_min_int_from_string(x):
    min_value = None
    if x:
        numbers = re.findall("\d+", x)
        if numbers:
            min_value = min(numbers)
    return min_value


def extract_emails(x):
    """Returns an iterator of matched emails found in string s."""
    # Removing lines that start with '//' because the regular expression
    # mistakenly matches patterns like 'http://foo@bar.com' as '//foo@bar.com'.
    emailGen = (email[0] for email in re.findall(RE_EMAIL, x) if not email[0].startswith("//"))
    return list(set(emailGen))


def add_params_to_url(url, **kwargs):
    """
    Add all kwargs as params to url
    """
    # Split url on parts
    url_parts = list(urlparse.urlparse(url))
    # Convert query parameters to dict
    query = dict(urlparse.parse_qsl(url_parts[4]))
    # Append to kwargs to this dict
    query.update(kwargs)

    # Make new url with parameters
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)


def safe_list_get(l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default


def fill_loader_from_response(loader, response):
    item_fields = vars(loader.default_item_class).get("fields", None)
    if item_fields:
        for key in item_fields.keys():
            value = response.meta.get(key, None)
            if value:
                loader.add_value(key, value)
    return loader


def get_csv_columns(input_csv, columns_map, delimiter=",", dialect=csv.excel_tab):
    result = []
    with open(input_csv, "rU") as data_file:
        data = csv.reader(data_file, delimiter = delimiter, dialect = dialect)
        for row in data:
            if row:
                output_row = {}
                for key, value in columns_map.items():
                    output_row[key] = safe_list_get(row, value, None)

                if output_row:
                    result.append(output_row)
    return result



def get_asp_headers(hxs):
    payload = {}
    asp_headers = []
    asp_headers.extend(hxs.xpath("//input[@type='hidden' and starts-with(@id, '__')]"))
#    asp_headers.extend(hxs.xpath("//input[starts-with(@id, 'ctl00$')]"))
#    asp_headers.extend(hxs.xpath("//input[starts-with(@id, 'ctl00_')]"))
    for asp_header in asp_headers:
        header_name = "".join(asp_header.xpath("@id").extract())
        header_value = "".join(asp_header.xpath("@value").extract())
        payload[header_name] = header_value
    return payload


def read_input_file(input_file):
    result = []
    with open(input_file, "rU") as data_file:
        data = csv.reader(data_file, delimiter=",", dialect=csv.excel_tab)
        for row in data:
            if row:
                result.extend(row)
    return result


def read_lines_from_file(file_name):
    result = []
    with open(file_name) as data_file:
        lines = data_file.readlines()
        for line in lines:
            if line and line.strip():
                result.append(line.strip())
    return result

