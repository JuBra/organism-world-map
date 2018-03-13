import os
import argparse
import sys
import requests
import logging
import json
import pandas as pd
from lxml import etree
from string import digits, whitespace


LOGGER = logging.getLogger(__name__)
HDLR = logging.StreamHandler()
HDLR.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
LOGGER.addHandler(HDLR)
LOGGER.setLevel(logging.INFO)

# Get script path
BASEPATH = os.path.dirname(os.path.abspath(__file__))
CWD = os.getcwd()

# Generate path to data files
SVG = os.path.join(BASEPATH, "data", "map_world.svg")
CODES = os.path.join(BASEPATH, "data", "codes.txt")
MAPPING = os.path.join(BASEPATH, "data", "mapping_loc_country.json")

# Check files exist
assert os.path.isfile(SVG), "Could not find map file at: '{}'".format(SVG)
assert os.path.isfile(CODES), "Could not find country code file at: '{}'".format(CODES)
assert os.path.isfile(MAPPING), "Could not find location to country mapping file at: '{}'".format(MAPPING)

# Webservice of catalogue of life
URL = "http://webservice.catalogueoflife.org/col/webservice?id={0}&format=json&response=full"


class APIError(BaseException):
    pass


def load_mapping(path=MAPPING):
    """ Load mapping between sampling locations and country codes

    :param path: str,
        File containing the mapping
    :return: substitutions: dict,
        Parsed mapping
    """

    with open(path) as f:
        mapping = json.load(f)

    # Convert to lowercase
    mapping = {k.lower(): v.lower()
               for k, v in mapping.items()}
    assert mapping, "The file containing the location to country mapping appears to be empty"

    return mapping


def load_codes(path=CODES):
    """ Load the country codes file

    :param path: str,
        File containing the country codes
    :return: country_codes: pd.Dataframe,
        Mapping between country names and country codes

    """

    # Parse file and convert to lowercase
    country_codes = pd.read_csv(path, sep="\t", index_col=0, header=0, na_filter=False)
    country_codes.index = country_codes.index.str.lower()
    return country_codes


def get_country_codes(locations):
    """ Get the locations where a species has been reported

    :param orgid: str,
        Organism id from the Catalogue of Life
    :return:


    """

    result = set()

    # Load data
    country_codes = load_codes()
    substitutions = load_mapping()

    for loc in locations:
        loc_lower = loc.lower()

        # Some locations are not actual countries,
        # try to substitute them from a lookup table
        if loc_lower in substitutions:
            loc_lower = substitutions[loc_lower]

        if loc_lower in country_codes.index:
            result.add(country_codes.ix[loc_lower]["iso3a2"])
        else:
            LOGGER.warning("Unknown country for location: '{0!s}'".format(loc))

    return result


def get_information(orgid):
    """ Download the locations from Catalogue of Life

    The catalogue of life offers a list of locations
    an organism has been isolated from. Use the api
    provided by COF for retrieval of the list.

    See format specs: http://webservice.catalogueoflife.org/

    :param orgid: str
    :return: set
    """

    locations = set()

    response = requests.get(URL.format(orgid))
    data = response.json()

    # Check if webservice signals an error
    if data["error_message"]:
        raise APIError(data["error_message"])

    try:
        results = data["results"]
    except KeyError:
        raise APIError("No results section found in response.")

    if not results:
        raise APIError("The results section is empty.")
    elif len(results) > 1:
        LOGGER.warning("There are more than one results, using the first one.")

    result = results[0]
    try:
        distribution = result["distribution"]
    except KeyError:
        raise APIError("No distribution section found in result.")

    if distribution:
        locations.update(x.strip(digits + whitespace)
                         for x in distribution.split(";"))

    org_name = result["name"] or orgid

    return org_name, locations


def main(id, color, out):

    # Download information
    try:
        name, locations = get_information(id)
    except:
        LOGGER.error("Error downloading data from Catalogue of Life:", exc_info=True)
        sys.exit(1)

    if not locations:
        LOGGER.error("No sampling locations recorded for {0!s}".format(name))
        sys.exit(1)

    # Translate to country codes
    country_codes = get_country_codes(locations)

    # Color map by matching country codes (ids) with the reported ones
    map_svg = etree.parse(SVG)
    countries = list(map_svg.getroot())[1]
    for country in countries:
        for chunk in country.attrib["id"].split("-"):
            if chunk in country_codes:
                country.attrib["style"] = "fill: {};".format(color)

    # Construct standard path if not specified
    if not out:
        out = os.path.join(CWD, name.lower().replace(" ", "_")+".svg")

    map_svg.write(out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True, help="Organism id from Catalogue of Life")
    parser.add_argument("--color", help="Color to mark countries (default: Green)", default="Green")
    parser.add_argument("--out", help="Path to the final map (default: '{}/<organme>')".format(CWD), default=None)
    args = parser.parse_args()

    main(args.id, args.color, args.out)

