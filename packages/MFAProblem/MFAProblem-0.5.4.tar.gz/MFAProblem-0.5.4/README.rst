MFA Problem
***********

Installation
------------

* git clone https://gitlab.com/libeigen/eigen.git
* export EIGEN_INCLUDE="Eigen Path" ou set EIGEN_INCLUDE="Eigen Path"
* pip install MFAProblem

Test
----
* python -m unittest discover mfa_problem.tests.unit
* python -m unittest discover mfa_problem.tests.integration

Scripts
-------
Example (modify file path):

* run_mfa_problem_main_with_excel.py - -input_file D:\\AFMFilieres\\mfa_problem\\data\\input\\pommes_poires.xlsx

Notebooks
---------
* pip install jupyter
* pip install ipyfilechooser
* install_mfa_problem_notebook.py
* cd ~/mfa_problem_notebook
* jupyter notebook basic_workflow.ipynb

Project
-------
* https://gitlab.com/su-model/mfa_problem