from .testfunc import Test
from .test_simple import *
from .test_plot import *


def run_all():
    fail = 0
    fail += run_all_simple()
    fail += run_all_plot()
    if fail:
        print(f"FAIL: Running all tests!")
    else:
        print(f"SUCCESS: Running all tests!")
    print(Test.test_string)
