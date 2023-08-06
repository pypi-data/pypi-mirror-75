import os, sys

base_dir = os.path.dirname(__file__)
sys.path.append(base_dir)

from nlutools.classifier import Classifier
from nlutools.nlu import NLU
# from nlutools.query.query_parse import Query
