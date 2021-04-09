from tess_enumerator_tests.pytest_constants import TESTABLE_TESS_DATA_CUBE, TESTABLE_TESS_DATA_CUBE__LOCAL

def test__list_data_cube_urls() -> None:
    from tess_enumerator.observatory import list_data_cube_urls
    for idx, url in enumerate(list_data_cube_urls()):
        pass

    assert idx > 0
    print(idx)

def test__enumerate_headers():
    from astropy.io import fits
    from tess_enumerator.datatypes import FITSHeader
    from tess_enumerator.observatory import request_header_info, list_data_cube_urls

    data_cube = fits.open(TESTABLE_TESS_DATA_CUBE__LOCAL)
    remote_info = request_header_info(TESTABLE_TESS_DATA_CUBE)
    for idx, hdu in enumerate(data_cube):
        remote_header = remote_info[idx]
        assert remote_header.__class__ is FITSHeader
        for field_name, value in hdu.header.items():
            assert remote_header.fits.get(field_name) == value

def test__enumerate_bintable_data():
    from astropy.io import fits
    from tess_enumerator.observatory import request_header_info, enumerate_bintable_data

    data_cube = fits.open(TESTABLE_TESS_DATA_CUBE__LOCAL)
    remote_info = request_header_info(TESTABLE_TESS_DATA_CUBE)
    # DataCubes prepared by STScI have the following headers
    # No. 1 -> Primary Header
    # No. 2 -> Image XTENSION
    # No. 3 -> BinTable with Light Curve data
    for idx, entry in enumerate(enumerate_bintable_data(TESTABLE_TESS_DATA_CUBE, remote_info[2], remote_info[0]), 1):
        import pdb; pdb.set_trace()
        continue
