import xarray as xr
import numpy as np
import pandas as pd
from os.path import join, isfile, isdir
import matplotlib.pyplot as plt
import subprocess
import os
from datetime import timedelta
from typing import Tuple, Union
from pathlib import Path
import glob
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
import sys
import shutil

import hydromt
from hydromt_sfincs import utils
from hydromt_sfincs import SfincsModel

def remove_dir_content(path: str) -> None:
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    if os.path.isdir(path):
        shutil.rmtree(path)

def read_binary_output(
    fn: Union[str, Path],
    ind: np.ndarray,
    timesteps: int,
    shape: Tuple[int],
    mv: float = -999.0,
    dtype: str = "f4",
) -> np.ndarray:
    """Read binary map.

    Parameters
    ----------
    fn: str, Path
        Path to map file.
    ind: np.ndarray
        1D array of flat index of binary maps.
    timesteps: int
        Numer of timesteps in the output file
    shape: tuple of int
        (nrow, ncol) shape of output map.
    mv: int or float
        missing value, by default -999.0.
    dtype: str, np.dtype, optional
        Data type, by default "f4".

    Returns
    -------
    ind: np.ndarray
        1D array of flat index of binary maps.
    """
    assert ind.max() <= np.multiply(*shape)
    nrow, ncol = shape
    data = np.full((timesteps, ncol, nrow), mv, dtype=dtype)
    with open(fn, 'r') as fid:
        for it in range(timesteps):
            d0 = np.full((ncol, nrow), mv, dtype=dtype)
            d0.flat[ind] = np.fromfile(fid, dtype=dtype, count=ind.size+2)[1:-1]
            data[it,:,:] = np.fliplr(d0)
    return data.transpose(0,2,1)

def postprocess(root, min_flddph=0):
    # open model instance
    mod = SfincsModel(root, mode='r')

    # get model props
    nrow, ncol = mod.config['nmax'], mod.config['mmax']
    tstart, tstop = mod.get_model_time()
    dt = timedelta(seconds=mod.config['dtmaxout'])
    time = pd.date_range(tstart+dt, end=tstop, freq=dt)

    # read zsmax
    ind = utils.read_binary_map_index(join(root, mod.config['indexfile']))
    da = xr.DataArray(
        data = read_binary_output(join(root, 'zsmax.dat'), ind, time.size, (nrow, ncol)),
        dims = ('timemax', 'y', 'x'),
        coords = {'timemax': time, **mod.staticmaps.raster.coords}
    )
    da_dep = mod.staticmaps['dep']

    # calculate hmax and write to raster
    hmax = (da-da_dep).where(da!=-999,0).where(da_dep!=da_dep.raster.nodata)
    hmax_tot = hmax.max('timemax')
    
    if not os.path.isfile(join(root, 'gis', 'hmax.tif')):
        hmax_tot.raster.set_nodata(-999)
        hmax_tot.raster.set_crs(mod.crs)
        mod.set_results(hmax_tot.fillna(-999), 'hmax')
        mod.write_raster('results.hmax')

    # plot hmax
    fig, ax = mod.plot_basemap(fn_out=None, variable='', geoms=[], plot_bounds=False, bmap='StamenTerrain')
    hmax_tot.where(hmax_tot>min_flddph).plot(
        ax=ax, cmap='viridis', vmin=min_flddph, vmax=3, cbar_kwargs=dict(shrink=0.5, label='flood depth [m]')
    )
    ax.set_title(os.path.basename(root))
    if not os.path.isdir(join(root, 'figs')):
        os.makedirs(join(root, 'figs'))
    plt.savefig(join(root, 'figs', f'hmax.png'), dpi=150)
    plt.close()

    # remove output binary files
    for fn in glob.glob(join(root, '*.dat')):
        try:
            os.unlink(fn)
        except:
            pass

def run_unix(root, sdir):
    # block! 
    with open(join(root, 'sfincs.log'), 'w') as f:
        f.write('')
    # copy run to tmpdir
    
    copy_tree(root, sdir)
    # run & postprocess
    os.chdir(sdir)
    cmd = f"singularity run -B{sdir}:/data --nv docker://deltares/sfincs-cpu |& tee {sdir}/sfincs.log"
    p = subprocess.run(cmd, shell = True)
    postprocess(sdir)
    # copy results back
    try:
        os.remove(join(root, 'sfincs.log'))
        copy_file(join(sdir, 'sfincs.log'), join(root, 'sfincs.log'))
        copy_file(join(sdir, 'gis', 'hmax.tif'), join(root, 'gis', 'hmax.tif'))
        copy_file(join(sdir, 'fig', 'hmax.png'), join(root, 'fig', 'hmax.png'))
        remove_dir_content(sdir)
    except:
        pass

def run_windows(root):
    fn_exe = "p:/11205283-hydromt-floodmodelling/02_models/bin/subgrid_openacc_11_rev295_16092021/sfincs.exe"
    # fn_exe = "p:/11205283-hydromt-floodmodelling/compound_floodrisk_modelling/3_models/bin/subgrid_openacc_11_rev382_31032022/sfincs.exe"
    with open(join(root, "sfincs.log"), 'w') as f:
        p = subprocess.Popen([fn_exe], stdout=f, cwd=root)
        p.wait()
    postprocess(root)