------------------------
compound flood modelling
------------------------

This repository contains all scripts and necessary data to reproduce the simulations and analysis performed for:

Eilander, D., Couasnon, A., Sperna Weiland, F. C., Ligtvoet, W., Bouwman, A., Winsemius, H. C., & Ward, P. J. (2022). Modeling compound flood risk and risk reduction using a globally-applicable framework: A case study in the Sofala region. In Natural Hazards and Earth System Sciences Discussions. https://doi.org/10.5194/nhess-2022-248

Getting started
---------------

1. Clone or download the repository and unzip all zip files in the "1_data" folder.
2. Install a conda environment based on the environment.yml file within this repository, see code below.
3. Then, follow the notebooks contained in the 2_code folder.

.. code-block:: console
  
  conda env create -f environment.yml


Repository outline
------------------

::

  > 1_data
    > 1_static
    > 2_forcing
  > 2_code
    > 1_prepare
    > 2_experiment
  > 3_models
    > sfincs (contains only base model)
    > fiat
  > 4_results (empty)
