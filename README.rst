------------------------
compound flood modelling
------------------------

This repository contains all scripts and necessary data to reproduce the simulations and analysis performed for:

Eilander, Dirk; Couasnon, Anaïs; Sperna Weiland; Frederiek C., Ligtvoet, Willem; Bouwman, Arno; Winsemius, Hessel C.; Ward, Philip J. (submitted). 
Modeling compound flood risk and risk reduction using a globally-applicable framework: A case study in the Sofala region. Natural Hazards and Earth System Sciences Discussions.

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
