import boto3
import requests
import tempfile
import typing
import types

from astropy.io import fits
from astropy.table import Table as Astropy_Table

from tess_enumerator.auth.aws import AWSAuth
from tess_enumerator.constants import TESS_BUCKET_NAME, TESS_CUBE_PREFIX, END_CARD, BLOCK_SIZE
from tess_enumerator.datatypes import FITSHeader
from tess_enumerator.base import load_headers

TESS_BUCKET_NAME = 'stpubdata'
TESS_CUBE_PREFIX = 'tess/public/mast/'


def list_data_cube_urls() -> types.GeneratorType:
    client = boto3.client('s3')
    for page in client.get_paginator('list_objects_v2').paginate(Bucket=TESS_BUCKET_NAME, Prefix=TESS_CUBE_PREFIX):
        for content in page['Contents']:
            key = content['Key']
            if key.endswith('.fits'):
                yield f'https://s3.us-east-1.amazonaws.com/{TESS_BUCKET_NAME}/{key}'

def request_header_info(url: str) -> typing.Any:
    return load_headers(url, AWSAuth(True))

def enumerate_bintable_data(url: str, header: FITSHeader, primary: FITSHeader) -> types.GeneratorType:
    # Make sure the FITSHeader passed is a Table or BinTable XTENSION
    assert header.fits.get('NAXIS', 0) == 2
    assert header.fits.get('BITPIX', 0) == 8
    assert header.fits.get('TFIELDS', 0) > 0 and header.fits.get('TFIELDS', 1000) < 1000
    for idx in range(1, header.fits['TFIELDS'] + 1):
        t_form = header.fits.get(f'TFORM{idx}', None)
        assert not t_form is None
        t_type = header.fits.get(f'TTYPE{idx}', None)
        assert not t_type is None

    else:
        if idx > 999:
            raise NotImplementedError(f'Invalid FITS Format')

    # NAXIS1 = number of bytes per row
    # NAXIS2 = number of rows in the table
    for idx in range(0, header.fits['NAXIS2']):
        idx_offset = idx + 1
        start = idx * header.fits['NAXIS1'] + header.data_offset
        stop = idx_offset * header.fits['NAXIS1'] + header.data_offset
        # start = 44315115840
        # stop = 44315115840 + header.fits['NAXIS1']
        response = requests.get(url, headers={
            'Range': f'bytes={start}-{stop}',
        }, auth=AWSAuth(True), stream=True)
        cutout_name = tempfile.NamedTemporaryFile().name
        with open(cutout_name, 'wb') as stream:
            stream.write(primary.as_string().encode('ascii'))
            new_header = header.clone()
            new_header.fits['NAXIS2'] = idx_offset - idx
            stream.write(new_header.as_string().encode('ascii'))
            for chunk in response.iter_content(1024):
                stream.write(chunk)

        yield Astropy_Table(fits.open(cutout_name)[1].data)
