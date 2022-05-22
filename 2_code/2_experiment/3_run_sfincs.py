import pandas as pd
from os.path import join, isfile, isdir
import os
from distutils.dir_util import copy_tree
import sys

from run_sfincs import run_windows, run_unix

if __name__ == '__main__':

    base = "/p/11205283-hydromt-floodmodelling/compound_floodrisk_modelling"
    mdir = join(base, '3_models', 'sfincs')
    
    # 
    if os.name != 'nt':
        tmpdir = sys.argv[1]
        copy_tree(join(mdir, "00_base_riv"), join(tmpdir, "00_base_riv"))
        copy_tree(join(mdir, "qb000_qp000_h000_p000"), join(tmpdir, "qb000_qp000_h000_p000"))

    # simulations
    # scens = pd.read_csv(join(base, '4_results', 'sim_SCEN.csv'), index_col=0).rename(columns={'h_tsw_rp': 'h_rp'})
    scens = pd.read_csv(join(base, '4_results', 'sim_SCEN_indep.csv'), index_col=0).rename(columns={'h_tsw_rp': 'h_rp'})

    for i, run in scens.iterrows():
        name = run['scen']
        for postfix in ['','_dt0']:
            root = join(mdir, f'{name}{postfix}')
            if isfile(join(root, "sfincs.log")) or not isdir(root): 
                continue
            print(name)
            if os.name == 'nt':
                run_windows(root)
            else:
                sdir = join(tmpdir, name)
                run_unix(root, sdir)