import os

PROJECT = os.getcwd()
if 'notebooks' in PROJECT:
    PROJECT = PROJECT.split('notebooks')[0]
REPORTS = os.path.join(PROJECT, 'reports')
RESULTS = os.path.join(PROJECT, 'results')
DATA = os.path.join(PROJECT, 'data')
DATA_EXTERNAL = os.path.join(DATA, 'external')
DATA_RAW = os.path.join(DATA, 'raw')
DATA_INTERIM = os.path.join(DATA, 'interim')
DATA_PROCESSED = os.path.join(DATA, 'processed')
TEMP = os.path.join(PROJECT, 'tmp')
