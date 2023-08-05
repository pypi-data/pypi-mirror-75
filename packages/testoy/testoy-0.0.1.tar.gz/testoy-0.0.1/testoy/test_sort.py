import pytest
from .build_sort_case import build_sort_case

SORT_FUNC = {}

edge_cases = [([], [])]
small_cases = build_sort_case(-1000, 1000, 5, 10) # length 1 ~ 4
mid_cases = build_sort_case(-1000, 1000, 100, 10) # length 5 ~ 100
large_cases =  build_sort_case(-1000, 1000, 100, 20) # length 100 ~ 

# This decorator Saves the function to SORT_FUNC variable and execute pytesting.
def decorator_sort(f):
    """ Use this as a decorator function for your sorting function 
    """
    global SORT_FUNC
    SORT_FUNC[f.__name__] = f
    pytest.main(["-v", "-s"]) # Execute: >pytest -v -s (-s needed for printing normal print functions in the console)
    return f

# Fixture that will be used for testing functions
# --> This fixture returns the sorting function user has put
@pytest.fixture
def fixture_sort():
    return list(SORT_FUNC.values())[0]

# Test Case for Edge cases
@pytest.mark.parametrize("test_case, sorted", edge_cases)
def test_edge_cases(fixture_sort, test_case, sorted):
    print("TC:", test_case, "Sorted:", sorted)
    print("Your Sorting Result:", fixture_sort(test_case))
    assert fixture_sort(test_case) == sorted

# Test Case for small test cases
@pytest.mark.parametrize("test_case, sorted", small_cases)
def test_small_cases(fixture_sort, test_case, sorted):
    print("TC:", test_case, "Sorted:", sorted)
    print("Your Sorting Result:", fixture_sort(test_case))
    assert fixture_sort(test_case) == sorted 
    
# Test Case for mid-sized test cases
@pytest.mark.parametrize("test_case, sorted", mid_cases)
def test_mid_cases(fixture_sort, test_case, sorted):
    print("TC:", test_case, "Sorted:", sorted)
    print("Your Sorting Result:", fixture_sort(test_case))
    assert fixture_sort(test_case) == sorted 

# Test Case for large-sized test cases
@pytest.mark.parametrize("test_case, sorted", large_cases)
def test_large_cases(fixture_sort, test_case, sorted):
    print("TC:", test_case, "Sorted:", sorted)
    print("Your Sorting Result:", fixture_sort(test_case))
    assert fixture_sort(test_case) == sorted 