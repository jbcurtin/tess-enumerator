import requests
import typing

from astropy.io import fits

from tess_enumerator.constants import END_CARD, BLOCK_SIZE, ENCODING
from tess_enumerator.utils import find_data_byte_size
from tess_enumerator.datatypes import FITSHeader

def load_headers(url: str, auth: 'request.AuthBase') -> typing.List[FITSHeader]:
    offset: int = 0
    headers: typing.List[FITSHeader] = []
    read_blocks: typing.List[str] = []
    header_data = []
    while True:
        response = requests.get(url, headers={
            'Range': f'bytes={offset}-{offset + BLOCK_SIZE - 1}',
        }, auth=auth)
        if response.status_code in [206]:
            try:
                header_data.append(response.content.decode(ENCODING))
            except UnicodeDecodeError as err:
                raise Exception("If this happens, it means the FITS file is invalid or the calculation is off")

            else:
                if END_CARD in header_data[-1]:
                    raw_header = ''.join(header_data)
                    fits_header = fits.Header.fromstring(raw_header)
                    data_byte_size = find_data_byte_size(fits_header)
                    data_offset = offset + len(raw_header)
                    data_stop = data_offset + data_byte_size
                    headers.append(FITSHeader(offset, offset + len(raw_header), data_offset, data_stop, fits_header))
                    header_data = []
                    offset = data_stop
                    continue

                else:
                    offset = offset + BLOCK_SIZE
                    continue

                pass
        elif response.status_code in [416]:
            return headers

        else:
            raise NotImplementedError(f'Unable to handle HTTP Code: {response.status_code}')

