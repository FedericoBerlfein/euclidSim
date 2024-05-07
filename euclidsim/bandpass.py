import numpy as np
import os
from pathlib import Path
import galsim
from galsim.config import RegisterBandpassType
from astropy.table import Table

__all__ = ['EuclidBandpass']


def EuclidBandpass(
    band,
    logger=None, 
    AB_zeropoint=True
):
    """Return one of the Euclid bandpasses, specified by the single-letter name.

    The zeropoint is automatically set to the AB zeropoint normalization.

    Parameters
    ----------
    band : `str`
        The name of the bandpass. For VIS only in this case.
    logger : logging.Logger
        If provided, a logger for logging debug statements.
    AB_zeropoint:
        Should the routine set an AB zeropoint before returning the bandpass?
        If False, then it is up to the user to set a zero point.  [default:True]
    """
    bp = galsim.Bandpass(throughput='1', wave_type='nm', blue_limit=550, red_limit=900) 
    if AB_zeropoint:
        bp = bp.withZeropoint('AB')
    return bp


class EuclidBandpassBuilder(galsim.config.BandpassBuilder):
    """A class for building a EuclidBandpass in the config file
    """
    def buildBandpass(self, config, base, logger):
        """Build the Bandpass object based on the LSST filter name.

        Parameters:
            config:     The configuration dict for the bandpass type.
            base:       The base configuration dict.
            logger:     If provided, a logger for logging debug statements.

        Returns:
            the constructed Bandpass object.
        """
        req = { 'band' : str }
        kwargs, safe = galsim.config.GetAllParams(config, base, req=req)
        kwargs['logger'] = logger
        bp = EuclidBandpass(**kwargs)

        # Also, store the kwargs=None version in the base config.
        base['fiducial_bandpass'] = EuclidBandpass(band=kwargs['band'], logger=logger)
        logger.debug('bandpass = %s', bp)
        return bp, safe

RegisterBandpassType('EuclidBandpass', EuclidBandpassBuilder())
