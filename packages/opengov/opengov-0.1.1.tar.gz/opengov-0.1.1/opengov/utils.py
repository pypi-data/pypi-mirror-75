import requests

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

# Create a dictionary for available data sources in this package
def populate_data_sources():
    data_sources = dict()
    data_sources["Available"] = ['FDA - US Food & Drug Administration', 'FTC - Federal Trade Commission']
    data_sources["In Development"] = ['SEC - US Securities & Exchange Commission']
    data_sources["Planned"] = ["FHFA - Federal Housing Finance Agency", "CFPB - Consumer Financial Protection Bureau"]
    return data_sources

# Constructs the API endpoint for openFDA
def constructFDAEndpoint(fda_base_url: str, endpoint_type: str, file_name: str, search: str, sort: str, count: str, limit: str, skip: str) -> str:
    return fda_base_url + "/" + endpoint_type + "/" + file_name + "?" + "search=" + search + "&sort=" + sort + "&count=" + count + "&limit=" + limit
