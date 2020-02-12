# To run tests:
#   cd nat-db
#   pytest
#
# Approx run time: 
#
# To extract notebook into pure python:
#   jupyter nbconvert --to python advanced-search.ipynb 

# Python library
import pathlib
# External packages
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import pytest
# Local packages

def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, Foo) and isinstance(right, Foo) and op == "==":
        return [
            "Comparing Foo instances:",
            "   vals: {} != {}".format(left.val, right.val),
        ]
# Then:
# #! def test_compare():
# #!     f1 = Foo(1)
# #!     f2 = Foo(2)
# #!     assert f1 == f2    

class TestNotebooks(object):
    # see: https://nbconvert.readthedocs.io/en/latest/api/index.html
    def check_nb_run_errors(self, nbfile):
        nb_file = pathlib.Path(__file__).parent.parent / nbfile
        print(f'nb_file={nb_file}')
        try:
            with open(nb_file) as f:
                nb = nbformat.read(f, as_version=4)
            ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
            #ep.preprocess(nb, {'metadata': {'path': 'notebooks/'}})
            ep.preprocess(nb, {})
        except Exception as err:
            error = err
        else:
            error = None

        assert error == None
        
    def test_utils_nb(self):
        self.check_nb_run_errors('utils.ipynb')

    def test_sia_nb(self):
        self.check_nb_run_errors('sia.ipynb')

    def test_ads_nb(self):
        self.check_nb_run_errors('advanced-search.ipynb')
        #!with open('executed_notebook.ipynb', mode='w', encoding='utf-8') as f:
        #!    nbformat.write(nb, f)

    def test_auth_nb(self):
        self.check_nb_run_errors('api-authentication.ipynb')

        
