import pytest
import glob2
import fnmatch

from .structure import get_directory_structure


@pytest.fixture
def parent_directory_structure_expected():
    return sorted(
        [
            'jaffle_shop/models/overview.md',
            'jaffle_shop/models/staging/src_seed/schema.yml',
            'jaffle_shop/models/staging/src_seed/stg_customers.sql',
            'jaffle_shop/models/staging/src_seed/stg_payments.sql',
            'jaffle_shop/models/staging/src_seed/stg_orders.sql',
            'jaffle_shop/models/staging/src_seed/sensitive/schema.yml',
            'jaffle_shop/models/staging/src_seed/sensitive/stg_customers_pii.sql',
            'jaffle_shop/models/final/sales/schema.yml',
            'jaffle_shop/models/final/sales/fnl_sales_newcustomers.sql',
            'jaffle_shop/models/final/finance/schema.yml',
            'jaffle_shop/models/final/finance/fnl_finance_customerreturns.sql',
            'jaffle_shop/models/warehouse/schema.yml',
            'jaffle_shop/models/warehouse/docs.md',
            'jaffle_shop/models/warehouse/wh_orders.sql',
            'jaffle_shop/models/warehouse/wh_customers.sql'
        ]
    )

def filter_string_list_by_substring(substring, string_list):
    return [str for str in string_list if substring in str]


def test_parent_directory_structure(parent_directory_structure_expected):
    parent_directory_structure_current = sorted(glob2.glob('jaffle_shop/models/**/*.*'))
    assert parent_directory_structure_expected == parent_directory_structure_current, \
        "Found an issue with the overall directory structure. If the issue is not shown in a more specific test when check which files are failing for more information."

def get_path_filters():
    path_filters = {
        "staging": "Found an issue with the staging directory structure. Ensure all staging models are located in a subdirectory named after their source database e.g. models/staging/src_example_db/model_x.sql",
        "warehouse": "Found an issue with the warehouse directory structure. Ensure you have a model for both customer and order data as well as a docs.md for documenting the complexity around order statuses.",
        "final": "Found an issue with the final directory structure. Ensure each model is located in a sub directory matching the department of the business it relates too e.g. models/final/sales - Each of these directories should have its own schema.yml",
        "sensitive" : "Found an issue with sensitive data structure...raw_customers.csv contains PII. Please ensure all sensitive columns have been hashed correctly in the staging layer."
    }
    for filter, error_message in path_filters.items():
            yield filter, error_message


@pytest.mark.parametrize(
    "path_filter_pair", get_path_filters(), ids=[i[0] for i in get_path_filters()]
)
def test_sub_directory_structure(parent_directory_structure_expected, path_filter_pair):
    path_filter, error_message = path_filter_pair
    expected_structure = filter_string_list_by_substring(path_filter, parent_directory_structure_expected)
    current_structure = sorted(glob2.glob(f'jaffle_shop/models/**/{path_filter}/**/*.*'))
    assert current_structure == expected_structure, error_message