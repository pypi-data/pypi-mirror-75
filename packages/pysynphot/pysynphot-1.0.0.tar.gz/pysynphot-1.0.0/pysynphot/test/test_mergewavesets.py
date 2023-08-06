from __future__ import absolute_import, division, print_function

import os

import numpy as np
import pytest
from astropy.utils.data import get_pkg_data_filename

from ..obsbandpass import ObsBandpass
from ..observation import Observation
from ..reddening import Extinction
from ..refs import getref, setref
from ..spectrum import BlackBody, FileSourceSpectrum, MergeWaveSets, MERGETHRESH

orig_graphtable = None
orig_comptable = None


@pytest.mark.remote_data
def test_merge_wave_sets():
    """
    The function S.spectrum.MergeWaveSets is designed so that merged wave sets
    have no two adjacent values which differ by less than
    S.spectrum.MERGETHRESH. This tests that.
    """
    bb = BlackBody(20000)
    ext = Extinction(0.04, 'gal1')
    new_wave = MergeWaveSets(bb.wave, ext.wave)
    delta = new_wave[1:] - new_wave[:-1]
    assert np.all(delta > MERGETHRESH), \
        'Deltas should be < {}, min delta = {}'.format(MERGETHRESH, delta.min())  # noqa


@pytest.mark.remote_data
class TestQSOCountrate(object):
    """
    Extinction curve waveset should not be merged into composite spectrum
    when applied. See https://github.com/spacetelescope/pysynphot/issues/44 .
    """
    @classmethod
    def setup_class(cls):
        global orig_graphtable, orig_comptable
        cfg = getref()
        orig_graphtable = cfg['graphtable']
        orig_comptable = cfg['comptable']

        # Answers computed using specified tables
        mtab = os.path.join(os.environ['PYSYN_CDBS'], 'mtab', 'OLD_FILES')
        setref(graphtable=os.path.join(mtab, '14l1632sm_tmg.fits'),
               comptable=os.path.join(mtab, '16n1832tm_tmc.fits'))

    def test_countrate(self):
        bp = ObsBandpass('acs,hrc,f850lp')

        fname = get_pkg_data_filename(os.path.join('data', 'qso_template.fits'))
        qso = FileSourceSpectrum(fname)
        sp_ext = qso * Extinction(1.0, 'mwavg')
        sp = sp_ext.renorm(20, 'vegamag', ObsBandpass('johnson,v'), force=True)

        obs = Observation(sp, bp, force='taper')
        c = obs.countrate()
        np.testing.assert_allclose(c, 2.3554364232173565e-05, rtol=0.008)

    @classmethod
    def teardown_class(cls):
        setref(graphtable=orig_graphtable, comptable=orig_comptable)
