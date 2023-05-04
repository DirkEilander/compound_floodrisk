#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Dirk Eilander (contact: dirk.eilander@vu.nl) and Anais Couasnon (contact anais.couasnon@vu.nl)
# Created: Nov 2nd 2018
#
# Xarray wrapper around astropy.stats.circstats functions 

# TODO: find a way to implement weights, both if weights == None, type(weights) == np.ndarray or type(weights) == xr.DataArray 

import xarray as xr
import numpy as np
import calendar

__all__ = ['circ_mean', 'doy_to_circ', 'circ_to_doy']

# circular stats
def circ_mean(circ_data, dim='time'):
    """Returns the mean of circular data [radian].
    
    Parameters
    ----------
    circ_data : xarray DataArray
        circular data [radian]
    dim : str, optional
        name of the core dimension (the default is 'time')
    
    Returns
    -------
    xarray DataArray
        circular mean
    """
    # wrap numpy function
    theta = xr.apply_ufunc(_circmean, circ_data, #kwargs={'weights':weights}, 
        input_core_dims=[[dim]], dask='parallelized', output_dtypes=[float])
    theta.name='theta'
    theta.attrs.update(unit='radian', description='circular mean')
    return theta

def doy_to_circ(doy, dim='year'):
    """Translate the day of the year (DOY) to circular angle [radian] with range [-pi, pi]"""
    # idx = np.isfinite(doy)
    # assert (doy[idx]>=1).all() and (doy[idx]<=366).all(), "doy should be in [1, 366] range"
    ndays = _get_ndays_year(doy, dim=dim)
    circ_doy = doy*2*np.pi / ndays # range [0, 2pi]
    circ_doy = xr.where(circ_doy>np.pi, -2*np.pi+circ_doy, circ_doy) # range [-pi, pi]
    return circ_doy

def circ_to_doy(circ_doy, dim='year'):
    """Translate a circular angle [radian] with range [-pi, pi] to day of the year (DOY) with range [0, 366]"""
    # idx = np.isfinite(circ_doy)
    # assert (np.abs(circ_doy[idx]) <= np.pi).all(), "circular doy should be in [-pi, pi] range"
    ndays = _get_ndays_year(circ_doy, dim=dim)
    circ_doy = xr.where(circ_doy<0, circ_doy+2*np.pi, circ_doy) #Convert to interval [0, 2pi]
    doy = circ_doy * ndays / (2*np.pi) #[0, ndays-1]
    doy = xr.where(doy<1, ndays, doy) # zeros should be ndays [1, ndays]
    return doy

def _get_ndays_year(doy, dim='year'):
    """get number of days in a year"""
    if dim:
        ndays = np.array([365+calendar.isleap(yr) for yr in doy[dim].values])
        ndays = xr.DataArray(ndays, dims=[dim], coords=[doy[dim].values])
    else:
        ndays = xr.apply_ufunc(lambda x: np.maximum(365, x), doy, 
            dask='parallelized', output_dtypes=[float])
    return ndays

# numpy functions from https://github.com/astropy/astropy/blob/v3.0.x/astropy/stats/circstats.py
# Copyright (c) 2011-2017, Astropy Developers
# copied to avoid astropy dependecy
# edits 
# -use nansum by default instead of sum
# -default axis is set to -1
# -added axis and newaxis where necessary to deal with ndarrays

def _components(data, p=1, phi=0.0, weights=None, axis=-1):
    """ Generalized rectangular components."""
    if weights is None:
        weights = np.ones((1,))
    try:
        weights = np.broadcast_to(weights, data.shape)
    except ValueError:
        raise ValueError('Weights and data have inconsistent shape.')

    # nansum instead of sum
    C = np.nansum(weights * np.cos(p * (data - phi)), axis)/np.nansum(weights, axis)
    S = np.nansum(weights * np.sin(p * (data - phi)), axis)/np.nansum(weights, axis)

    return C, S


def _angle(data, p=1, phi=0.0, weights=None, axis=-1):
    """ Generalized sample mean angle."""
    C, S = _components(data, p, phi, weights, axis)

    # theta will be an angle in the interval [-np.pi, np.pi)
    theta = np.arctan2(S, C)

    return theta


def _circmean(data, weights=None, axis=-1):
    """ Circular mean."""
    return _angle(data, 1, 0.0, weights, axis)