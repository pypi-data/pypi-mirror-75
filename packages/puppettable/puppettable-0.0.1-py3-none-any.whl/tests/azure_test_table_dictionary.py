import numpy as np
import pandas as pd
import os

from puppettable.implementations.azure.azure_table_service import AzureTableService

connection_string = os.environ["CONNECTION_STRING"]


tables = AzureTableService(connection_string=connection_string)


experiment_table = tables["puppettableTestDictionary": {}]


def test_structure_df(structure_list, assert_equal=None):

    def _assert_equal(arg1, arg2):
        assert (arg1 == arg2)

    if assert_equal is None:
        assert_equal = _assert_equal

    indexes = structure_list.index

    # TEST INDIVIDUAL ASSIGNMENT
    experiment_table[indexes[0]] = structure_list.loc[indexes[0]]
    experiment_table[indexes[1]] = structure_list.loc[indexes[1]]

    assert_equal(experiment_table[indexes[0]], structure_list.loc[indexes[0]])
    assert_equal(experiment_table[indexes[1]], structure_list.loc[indexes[1]])
    assert_equal(experiment_table[indexes[0]:indexes[1]], structure_list.loc[indexes[0]:indexes[1]].iloc[:-1])
    assert_equal(experiment_table[indexes[0]:], structure_list.loc[indexes[0]:])

    # TEST BATCH ASSIGNMENT
    experiment_table[indexes.tolist()] = structure_list
    experiment_table.sync()

    assert_equal(experiment_table[indexes[0]], structure_list.loc[indexes[0]])
    assert_equal(experiment_table[indexes[1]], structure_list.loc[indexes[1]])
    assert_equal(experiment_table[indexes[0]:indexes[1]], structure_list.loc[indexes[0]:indexes[1]].iloc[:-1])
    assert_equal(experiment_table[indexes[0]:], structure_list.loc[indexes[0]:])

def test_structure(structure_list, assert_equal=None):

    def _assert_equal(arg1, arg2):
        assert (arg1 == arg2)

    if assert_equal is None:
        assert_equal = _assert_equal

    # TEST INDIVIDUAL ASSIGNMENT
    experiment_table[0] = structure_list[0]
    experiment_table[1] = structure_list[1]

    assert_equal(experiment_table[0], structure_list[0])
    assert_equal(experiment_table[1], structure_list[1])
    assert_equal(experiment_table[0:1], structure_list[0:1])
    assert_equal(experiment_table[0:2], structure_list[0:2])

    # TEST BATCH ASSIGNMENT
    experiment_table[[0, 1]] = structure_list
    experiment_table.sync()

    assert_equal(experiment_table[0], structure_list[0])
    assert_equal(experiment_table[1], structure_list[1])
    assert_equal(experiment_table[0:1], structure_list[0:1])
    assert_equal(experiment_table[0:2], structure_list[0:2])

# TEST STRING
print("Testing strings...")
test_structure(["hello", "olleh"])

# TEST INT
print("Testing integers...")
test_structure([4, 3])

# TEST FLOAT
print("Testing floats...")
test_structure([4.2, 3.6])

# TEST LIST
print("Testing lists...")
test_structure([["hello", "ok"], ["testing", "test"]])

# TEST DICT
print("Testing dicts...")
test_structure([{"hello": "this is a test", "JA": 4}, {"this": "is another test", "JO": 2}])

# TEST NUMPY ARRAYS
def assert_equal(arg1, arg2):
    assert (all((arg1 == arg2).reshape(-1)))

print("Testing numpys...")
test_structure(np.random.randn(2, 4, 2), assert_equal=assert_equal)

# TEST PANDAS DATAFRAMES
def assert_equal(arg1, arg2):
    assert (all((arg1 == arg2).values.reshape(-1)))

print("Testing pandas...")
test_structure_df(pd.DataFrame(np.random.randn(2, 10), index=["sample1", "sample2"]), assert_equal=assert_equal)

