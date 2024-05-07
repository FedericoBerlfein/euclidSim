"""
Euclid PSF Class
"""

import os
import logging
import numpy as np
import pickle
import galsim
from galsim.config import InputLoader, RegisterInputType, RegisterObjectType

#from .optical_system import OpticalZernikes, mock_deviations

def getPSF(band, pos=None, pupil_bin=4, wcs=None, logger=None):
    """Return one of the Euclid bandpasses, specified by the single-letter name.

    The zeropoint is automatically set to the AB zeropoint normalization.

    Parameters
    ----------
    band : `str`
        The name of the bandpass. For VIS only in this case.
    pos : galsim.PositionD
        Position in focal plane.
    pupil_bin: int
        The binning to apply to the pupil plane image.
    wcs:  
        The WCS to use to project the PSF into world coordinates.
    logger : logging.Logger
        If provided, a logger for logging debug statements.
    """
    lam = 700  # nm
    diam = 3.7   # meters
    lam_over_diam = (lam * 1.e-9) / diam  # radians
    lam_over_diam *= 206265  # Convert to arcsec
    psf = galsim.Airy(lam_over_diam)
    return psf


def BuildEuclidPSF(config, base, ignore, gsparams, logger):
    """
    This is an example implementation of a Euclid-like PSF
    """
    req = {}
    opt = {
        'pupil_bin' : int,
        'band' : str
    }

    kwargs, safe = GetAllParams(config, base, req=req, opt=opt, ignore=ignore)
    if 'band' not in kwargs:
        kwargs['band'] = base['band'].name

    psf = getPSF(band=kwargs['band'], logger=logger, **kwargs)

    return psf, safe


RegisterObjectType('EuclidPSF', BuildEuclidPSF)
