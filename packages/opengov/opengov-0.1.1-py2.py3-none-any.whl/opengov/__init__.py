"""Top-level package for OpenGov."""
import requests
import opengov
from .utils import *
from .fda import *
from .__version__ import __version__

data_sources = dict()
data_sources["Available"] = []
data_sources["In Development"] = ['SEC - US Securities & Exchange Commission', 'FDA - US Food & Drug Administration', 'FTC - Federal Trade Commission']
data_sources["Planned"] = ["FHFA - Federal Housing Finance Agency", "CFPB - Consumer Financial Protection Bureau"]
