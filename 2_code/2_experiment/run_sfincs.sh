#!/bin/bash
#$ -cwd
echo $HOSTNAME 
echo $TMPDIR
# TMPDIR=~/tmp
SDIR=/p/11205283-hydromt-floodmodelling/compound_floodrisk_modelling/2_code/2_experiment

source ~/.bashrc
module load singularity
mamba activate hydromt

export OMP_NUM_THREADS=4

python ${SDIR}/3_run_sfincs.py $TMPDIR
python ${SDIR}/3_run_sfincs.py $TMPDIR
python ${SDIR}/3_run_sfincs.py $TMPDIR

exit