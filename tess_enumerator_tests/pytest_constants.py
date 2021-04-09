import os
import tempfile

ENCODING = 'utf-8'
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TESTABLE_BUCKET_NAME = 'tess-enumerator'
TESTABLE_REGION = 'us-east-1'
TESTABLE_BUCKET_URL_WITH_MUTABLE_FILE = f'https://s3.{TESTABLE_REGION}.amazonaws.com/{TESTABLE_BUCKET_NAME}/mutable.txt'
TESTABLE_BUCKET_URL_WITH_FILE = f'https://s3.{TESTABLE_REGION}.amazonaws.com/{TESTABLE_BUCKET_NAME}/list-objects/one'
TESTABLE_BUCKET_URL_WITHOUT_FILE = f'https://s3.{TESTABLE_REGION}.amazonaws.com/{TESTABLE_BUCKET_NAME}/list-objects/zero'
TESTABLE_BUCKET_URL_BASE = f'https://s3.{TESTABLE_REGION}.amazonaws.com/{TESTABLE_BUCKET_NAME}'
TESTABLE_DATA_DIR = os.path.join(os.getcwd(), 'tess_enumerator_data')
TESTABLE_TEMPLATE_DIR = os.path.join(PROJECT_DIR, '../tess_enumerator_test_templates')
TESTABLE_TESS_DATA_CUBE = 'https://s3.us-east-1.amazonaws.com/stpubdata/tess/public/mast/tess-s0022-4-4-cube.fits'
TESTABLE_TESS_DATA_CUBE__LOCAL = os.path.join(os.getcwd(), 'tess_enumerator_test_data', 'tess-s0022-4-4-cube.fits')

# PYTEST_DATA_DIR = f'{PROJECT_DIR}/astro_cloud_test_data'
# PYTEST_TEMPLATE_DIR = f'{PROJECT_DIR}/astro_cloud_test_templates'
# # We'll use AWS for datum storage right now
# DATUM_STORAGE_BASE_URL = 'https://s3.us-east-1.amazonaws.com/datum-storage.org'
# DATUM_STORAGE_BASE_URL__FITS = f'{DATUM_STORAGE_BASE_URL}/fits-files'
