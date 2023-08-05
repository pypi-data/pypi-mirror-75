crr_labels
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy| |code_climate_maintainability| |pip| |downloads|

Python package wrapping over FANTOM and Roadmap labels for cis-regulatory regions.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install crr_labels

Tests Coverage
----------------------------------------------
Since some software handling coverages sometimes get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Usage examples
-----------------------------------------------
Currently, we support `FANTOM CAGE data <http://fantom.gsc.riken.jp/5/data/>`_ and `Roadmap <https://egg2.wustl.edu/roadmap/web_portal/chr_state_learning.html>`_ but in the future an additional
cis-regulatory dataset based on open chromatin data will be added.

FANTOM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To retrieve the FANTOM promoters and enhancers you can proceed as follows:

.. code:: python

    from crr_labels import fantom

    enhancers, promoters = fantom(
        cell_lines=["HelaS3", "GM12878"], # list of cell lines to be considered.
        window_size=200, # window size to use for the various regions.
        genome = "hg19", # considered genome version. Currently supported only "hg19".
        center_enhancers = "peak", # how to center the enhancer window, either around "peak" or the "center" of the region.
        enhancers_threshold = 0, # activation threshold for the enhancers.
        promoters_threshold = 5, # activation threshold for the promoters.
        drop_always_inactive_rows = True, # whetever to drop the rows where no activation is detected for every rows.
        binarize = True, # Whetever to return the data binary-encoded, zero for inactive, one for active.
        nrows = None # the number of rows to read, usefull when testing pipelines for creating smaller datasets.
    )

The library will download and parse the fantom project raw data and return two dataframes for the required cell lines.
Consider reading the method docstring for more id-depth informations about the method.

The main steps are the following:

- The raw files are retrieved from the fantom dataset from the link specified in the `fantom_data.json file <https://github.com/LucaCappelletti94/crr_labels/blob/master/crr_labels/fantom_data.json>`_
- The window for the enhancers and promoters are expanded or compressed to the given window size. In particular:

  - The enhancers window can either be centered on the region center with the "center" mode or around the "peak" with the "peak" mode.
  - The promoters window is upstream in the positive strand from the end of the promoter and downstream on the negative strand from the start of the promoter.
- When multiple experiments are present for a cell line, for instance for "HelaS3", an average of the activation peaks is executed.
- Optionally (and by default) the rows that are always inactive for the chosen cell lines are dropped. You can specify this behaviour using the parameter "drop_always_inactive_rows".


Roadmap
~~~~~~~~~~~~~~~~~~~~~~~~~~~
To retrieve the Roadmap promoters and enhancers you can proceed as follows:

.. code:: python

    from crr_labels import roadmap

    enhancers, promoters = roadmap(
        cell_lines = ["HelaS3", "GM12878"], # List of cell lines to be considered.
        window_size = 200, # Window size to use for the various regions.
        genome = "hg19", # Considered genome version. Currently supported only "hg19".
        states = 18, # Number of the states of the model to consider. Currently supported only "15" and "18".
        enhancers_labels = ("7_Enh", "9_EnhA1", "10_EnhA2"), # Labels to encode as active enhancers.
        promoters_labels = ("1_TssA",), # Labels to enode as active promoters.
        nrows = None # the number of rows to read, usefull when testing pipelines for creating smaller datasets.
    )

Consider reading the method docstring for more in-depth information about the method.

Rendered datasets
----------------------------------
The following two datasets have labels for 7 common cell lines (GM12878, HelaS3, HepG2, K562, A549, H1, H9) and for various other that were not available in the other dataset.

FANTOM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following datasets contain data for the cell lines GM12878, HelaS3, HepG2, K562, A549, H1, H9, JURKAT, MCF7, HEK293, Caco2, HL60 and PC3.

+----------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------+
|   Nucleotides window | Genome   | Region-centered enhancers                                                                                                                      | Peak-centered enhancers                                                                                                                        | Promoters                                                                                                                               |
+======================+==========+================================================================================================================================================+================================================================================================================================================+=========================================================================================================================================+
|                  200 | hg19     | `Download <https://raw.githubusercontent.com/LucaCappelletti94/crr_labels/master/preprocessed/fantom/window_size/200/enhancers_center.bed>`__  | `Download <https://raw.githubusercontent.com/LucaCappelletti94/crr_labels/master/preprocessed/fantom/window_size/200/enhancers_peak.bed>`__    | `Download <https://raw.githubusercontent.com/LucaCappelletti94/crr_labels/master/preprocessed/fantom/window_size/200/promoters.bed>`__  |
+----------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------+
|                 1000 | hg19     | `Download <https://raw.githubusercontent.com/LucaCappelletti94/crr_labels/master/preprocessed/fantom/window_size/1000/enhancers_center.bed>`__ | `Download <https://raw.githubusercontent.com/LucaCappelletti94/crr_labels/master/preprocessed/fantom/window_size/1000/enhancers_peak.bed>`__   | `Download <https://raw.githubusercontent.com/LucaCappelletti94/crr_labels/master/preprocessed/fantom/window_size/1000/promoters.bed>`__ |
+----------------------+----------+------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------+


Roadmap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following datasets contain data for the cell lines GM12878, HelaS3, HepG2, K562, A549, H1, H9, DND41, HUES48, HUES6, HUES64 and IMR90.

+----------------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
|   Nucleotides window | Genome   | 15-states model enhancers                                                                                                                         | 15-states model promoters                                                                                                                         | 18-states model enhancers                                                                                                                         | 18-states model promoters                                                                                                                         |
+======================+==========+===================================================================================================================================================+===================================================================================================================================================+===================================================================================================================================================+===================================================================================================================================================+
|                  200 | hg19     | `Download <https://raw.githubusercontent.com/LucaCappelletti94/crr_labels/master/preprocessed/roadmap/window_size/200/state/15/enhancers.bed>`__  | `Download <https://raw.githubusercontent.com/LucaCappelletti94/crr_labels/master/preprocessed/roadmap/window_size/200/state/15/promoters.bed>`__  | `Download <https://raw.githubusercontent.com/LucaCappelletti94/crr_labels/master/preprocessed/roadmap/window_size/200/state/18/enhancers.bed>`__  | `Download <https://raw.githubusercontent.com/LucaCappelletti94/crr_labels/master/preprocessed/roadmap/window_size/200/state/18/promoters.bed>`__  |
+----------------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
|                 1000 | hg19     | `Download <https://raw.githubusercontent.com/LucaCappelletti94/crr_labels/master/preprocessed/roadmap/window_size/1000/state/15/enhancers.bed>`__ | `Download <https://raw.githubusercontent.com/LucaCappelletti94/crr_labels/master/preprocessed/roadmap/window_size/1000/state/15/promoters.bed>`__ | `Download <https://raw.githubusercontent.com/LucaCappelletti94/crr_labels/master/preprocessed/roadmap/window_size/1000/state/18/enhancers.bed>`__ | `Download <https://raw.githubusercontent.com/LucaCappelletti94/crr_labels/master/preprocessed/roadmap/window_size/1000/state/18/promoters.bed>`__ |
+----------------------+----------+---------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/crr_labels.png
   :target: https://travis-ci.org/LucaCappelletti94/crr_labels
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_crr_labels&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_crr_labels
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_crr_labels&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_crr_labels
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_crr_labels&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_crr_labels
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/crr_labels/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/crr_labels?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/crr-labels.svg
    :target: https://badge.fury.io/py/crr-labels
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/crr-labels
    :target: https://pepy.tech/badge/crr-labels
    :alt: Pypi total project downloads 

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/c0a7e110045a4d25933c65fe2014a33c
    :target: https://www.codacy.com/manual/LucaCappelletti94/crr_labels?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/crr_labels&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/7c18ec5176f2ebebef96/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/crr_labels/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/7c18ec5176f2ebebef96/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/crr_labels/test_coverage
    :alt: Code Climate Coverate
