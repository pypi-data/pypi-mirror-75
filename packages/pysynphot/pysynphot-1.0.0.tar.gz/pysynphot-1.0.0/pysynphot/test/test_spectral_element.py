from __future__ import absolute_import, division, print_function

import numpy as np
import pytest
from numpy.testing import assert_allclose

from ..obsbandpass import ObsBandpass
from ..spectrum import ArraySpectralElement


def test_sample_units():
    """Test that SpectralElement.sample respects internal units."""
    defwave = np.linspace(0.1, 1, 10)
    s = ArraySpectralElement(defwave, defwave, 'm', 'TestArray')
    assert_allclose(s(defwave * 1E10), s.sample(defwave))


@pytest.mark.remote_data
@pytest.mark.parametrize(
    ('obsmode', 'ans'),
    [('acs,hrc,f555w', 357.17),
     ('acs,sbc,f122m', 86.209624),
     ('acs,wfc1,f775w,pol_v', 444.05),
     ('cos,boa,nuv,mirrora', 370.65),
     ('nicmos,1,f090m,dn', 559.59),
     ('stis,0.2x29,mirror,fuvmama', 134.977476),
     ('wfc3,ir,f164n', 700.05),
     ('wfc3,uvis1,f336w', 158.44),
     ('wfc3,uvis2,f336w', 158.36)])
def test_photbw(obsmode, ans):
    """
    Test that SpectralElement.photbw returns results similar to
    Synphot to within 0.1%.

    .. note::

        For stis,0.2x29,mirror,fuvmama, Synphot value was 134.79.
        New ref value from STIS data update some time after April 2017.

        For acs,sbc,f122m, new ref value from ACS data update in
        Oct 2019 (Avila et al.).

    """
    band = ObsBandpass(obsmode)
    assert_allclose(band.photbw(), ans, rtol=1E-3)
