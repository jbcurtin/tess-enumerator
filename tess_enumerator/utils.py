import math

import numpy as np

from tess_enumerator.constants import BLOCK_SIZE
from tess_enumerator.datatypes import FITSHeader

from astropy.io import fits


def as_np_dtype(bitpix: int) -> np.dtype:
    '''
    Image XTENSION has a BITPIX header that represents a datatype. This function takes that header and converts
        it to np.dtype
    '''
    if bitpix == 8:
        return np.dtype(np.uint8)

    elif bitpix == 16:
        return np.dtype(np.uint16)

    elif bitpix == 32:
        return np.dtype(np.uint32)

    elif bitpix == -32:
        return np.dtype(np.float32)

    elif bitpix == -64:
        return np.dtype(np.float64)

    raise NotImplementedError(f'BITPIX[{bitpix}] not implemented')

def find_data_byte_size(header: fits.Header) -> int:
    if header.get('SIMPLE', False) is True:
        return 0

    # https://github.com/AstrolabeProject/imdtk/blob/devel/imdtk/core/fits_irods_helper.py#L78
    if 0 in [header[f'NAXIS{idx}'] for idx in range(1, header['NAXIS'] + 1)]:
        return 0

    elif header.get('XTENSION', None) in ['IMAGE']:
        # https://ui.adsabs.harvard.edu/abs/1994A%26AS..105...53P/abstract
        # http://articles.adsabs.harvard.edu/pdf/1994A%26AS..105...53P
        # https://github.com/AstrolabeProject/imdtk/blob/devel/imdtk/core/fits_irods_helper.py#L65
        B: int = as_np_dtype(header['BITPIX']).itemsize
        G: int = header['GCOUNT']
        P: int = header['PCOUNT']
        N: typing.List[int] = [header[f'NAXIS{idx}'] for idx in range(1, header['NAXIS'] + 1)]
        S: float = B * G * (P + np.prod(N)) / BLOCK_SIZE
        return math.ceil(S) * BLOCK_SIZE

    elif header.get('XTENSION', None) in ['BINTABLE']:
        # NAXIS1 = number of bytes per row
        # NAXIS2 = number of rows in the table
        return math.ceil(header['NAXIS1'] * header['NAXIS2'] / BLOCK_SIZE) * BLOCK_SIZE

    elif header.get('XTENSION', None) in ['TABLE']:
        raise NotImplementedError('TABLE')

    else:
        raise NotImplementedError(header.get('XTENSION'))
