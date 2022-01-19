from robot.api import logger
from SeleniumLibrary.base import keyword
from libs.ui.DataTable import DataTable
from libs.ui.AutoException import *


class DataTableUtils(object):

    def __init__(self):
        return

    @keyword("Get Table Row Count")
    def get_table_row_count(self, table):
        """
        Keyword: Get Table Row Count
            - Returns the number of rows in the table

        Parameters:
            :param table:
            - Table whose row count need to be fetched
        Returns: Number of rows in the Table

        Example:
        1. ${row_count}=    Get Table Row Count    table=${some_table}
        """

        row_count = 0
        if isinstance(table, DataTable):
            row_count = table.row_count

        return row_count

    @keyword("Get Table Headers")
    def get_table_headers(self, table):
        """
        Keyword: Get Table Headers
            - Returns the table headers if there are any.

        Parameters:
            :param table:
            - Table whose headers need to be fetched
        Returns: Headers of the Table

        Example:
        1. ${headers}=    Get Table Headers    table=${some_table}
        """
        headers = None
        if isinstance(table, DataTable):
            headers = table.headers

        return headers

    @keyword("Get Table Row As Dictionary")
    def get_table_row_as_dictionary(self, table, row):
        """
        Keyword: Get Table Row As Dictionary
            - Returns the table row as Dictionary

        Parameters:
            :param table:
            - Table whose row need to be fetched
            :param row:
            - Row number that need to be fetched

        Returns: Row of the Table as Dictionary

        Example:
        1. ${table_row_dict}=    Get Table Row As Dictionary    table=${some_table}    row=1
        """
        table_row = None
        row = int(row)

        if isinstance(table, DataTable):
            table_row = table.row(row)

            if table_row:
                table_headers = table.headers
                table_row_with_fields = dict(zip(table_headers, table_row))
                table_row = table_row_with_fields

        return table_row

    @keyword("Get Table Row As List")
    def get_table_row_as_list(self, table, row):
        """
        Keyword: Get Table Row As List
            - Returns the table row as List

        Parameters:
            :param table:
            - Table whose row need to be fetched
            :param row:
            - Row number that need to be fetched

        Returns: Row of the Table as List

        Example:
        1. ${table_row_list}=    Get Table Row As List    table=${some_table}    row=1
        """
        table_row = None
        row = int(row)

        if isinstance(table, DataTable):
            table_row = table.row(row)

        return table_row

    @keyword("Get Table Rows With Key")
    def get_table_rows_with_key(self, table, key, column=1, as_list=1):
        """
        Keyword: Get Table Rows With Key
            - Returns the table rows for the given key value on a specified column as a List of Lists or Dictionaries

        Parameters:
            :param table:
            - Table whose row(s) need to be fetched
            :param key:
            - Key value to match
            :param column:
            - Column number to get the key value to be matched.
            :param as_list:
            - 0 - Returns a list of Dictionaries
            - 1 - Returns a list of Lists
        Returns: Rows of the Table matching the key as a List of Lists or Dictionaries

        Example:
        1. ${table_row_list}=    Get Table Rows With Key    table=${some_table}    key=Spam    column=1    as_list=1
        """
        table_rows = list()
        column_count = table.column_count
        rows = 0

        if not key:
            raise IncompleteDataException("Missing Mandatory Parameter: key")

        if not column:
            column = 1

        if isinstance(table, DataTable):
            rows = table.row_count
            table_headers = table.headers

            if not table_headers:
                if rows:
                    table_headers = [x for x in range(1, column_count + 1)]

            if column > column_count or column < 1:
                raise IndexError("Table Column Count: %d | Column to retrieve: %d" % (column_count, column))

            for row in range(1, rows + 1):
                table_row = table.row(row)

                if key == table_row[column - 1]:
                    table_row_data_repr = None

                    if as_list:
                        table_row_data_repr = table_row
                    else:
                        table_row_data_repr = dict(zip(table_headers, table_row))

                    table_rows.append(table_row_data_repr)

        return table_rows

    @keyword("Get All Table Rows")
    def get_all_table_rows(self, table, as_list=False):
        """
        Keyword: Get All Table Rows
            - Returns all the rows of the table

        Parameters:
            :param table:
            - Table whose row(s) need to be fetched
            :param as_list:
            - False - Returns a list of Dictionaries
            - True - Returns a list of Lists

        Returns:
        - All rows of the table as list of lists or dictionaries

        Example:
        1. ${table_rows_as_lists}=    Get All Table Rows    table=${some_table}    as_list=True
        """
        table_rows = []

        if isinstance(table, DataTable):
            for row in range(1, table.row_count + 1):
                if as_list:
                    table_row = self.get_table_row_as_list(table, row)
                else:
                    table_row = self.get_table_row_as_dictionary(table, row)

                table_rows.append(table_row)

        return table_rows

    @keyword("Get Table Cell")
    def get_table_cell(self, table, row, column):
        """
        Keyword: Get Table Cell
            - Returns the Cell value of the Table of a given row and column

        Parameters:
            :param table:
            - Table whose row(s) need to be fetched
            :param row:
            - Row number of the table cell
            :param column:
            - Column number of the table cell

        Returns: Cell value of the Table of a given row and column

        Example:
        1. ${table_cell_value}=    Get Table Cell    table=${some_table}    row=2    column=3
        """
        cell_value = None
        row = int(row)
        column = int(column)

        table_row = table.row(row)

        if table_row and isinstance(table_row, (list, tuple)):
            row_length = len(table_row)

            if column <= row_length:
                cell_value = table_row[column - 1]
            else:
                raise AutoException("Invalid Column | Column: %d" % column)

        logger.info("get_table_cell | row: %d | column: %d | cell value: %s" % (row, column, cell_value))

        return cell_value

    @keyword("Get Table Field")
    def get_table_field(self, table, row, field):
        """
        Keyword: Get Table Cell
            - Returns the Cell value of the Table of a given row and field

        Parameters:
            :param table:
            - Table whose row(s) need to be fetched
            :param row:
            - Row number of the table cell
            :param field:
            - Name of the field of the table cell

        Returns: Cell value of the Table of a given row and field

        Example:
        1. ${table_cell_value}=    Get Table Cell    table=${some_table}    row=2    field=Messages
        """
        cell_value = None
        row = int(row)

        if isinstance(table, DataTable):
            cell_value = table.get_field(row, field)

        logger.info("get_table_field | Row: %d | Field: %s | Field value: %s" % (row, field, cell_value))

        return cell_value

    @keyword("Table Row Should Have Value")
    def table_row_should_have_value(self, table, row, value):
        """
        Keyword: Table Row Should Have Value
        - Checks if the given row of the table has the value

        Parameters:
            :param table:
            - Table whose row(s) need to be fetched
            :param row:
            - Row number of the table cell
            :param value:
            - value you want to verify

        Returns: NIL

        Example:
        1. Table Row Should Have Value    table=${some_table}    row=2    value=2015
        """

        cell_value = None
        row = int(row)

        table_row = table.row(row)

        if table_row and isinstance(table_row, (list, tuple)):
            return value in table_row

        logger.info("table_row_should_have_value | Value: %d | Not in Table." % value)
        return False

    @keyword("Table Field Should Have Value In Row")
    def table_field_should_have_value_in_row(self, table, row, field, value):
        """
        Keyword: Table Field Should Have Value In Row
        - Checks if the given row of the table has the value

        Parameters:
            :param table:
            - Table whose row(s) need to be fetched
            :param row:
            - Row number of the table cell
            :param field:
            - Name of the field of the table
            :param value:
            - value you want to verify

        Returns: NIL

        Example:
        1. Table Field Should Have Value In Row    table=${some_table}    row=2    field=Messages    value=2015
        """
        row = int(row)
        table_row = self.get_table_row_as_dictionary(table, row)

        if table_row and isinstance(table_row, dict):
            return value == table_row.get(field)

        logger.info(
            "table_field_should_have_value_in_row | Field: %s | Value: %d | Not in Table Row: %d." %
            (field, value, row)
        )
        return False


def test_data_table():

    dt = DataTable()
    headers = ('Number', 'Square', 'Cube')
    dt.headers = headers

    for x in range(10):
        record = [str(x), str(x*x), str(x*x*x)]
        dt.add_row(record)

    dtu = DataTableUtils()
    print("Headers: %s" % ' | '.join(dtu.get_table_headers(dt)))
    print("Rows in Table: %d" % dtu.get_table_row_count(dt))
    print("Table row as List > 2: %s" % repr(dtu.get_table_row_as_list(dt, 2)))
    print("Table row as Dictionary > 5: %s" % repr(dtu.get_table_row_as_dictionary(dt, 5)))

    print("Table Cell (Row:4, Col: 2): %s" % repr(dtu.get_table_cell(dt, 4, 2)))
    print("Table Field (Row:5, Field: 'Cube'): %s" % repr(dtu.get_table_field(dt, 5, 'Cube')))
    print("Table All Rows:\n%s" % '\n'.join([str(row) for row in dtu.get_all_table_rows(dt)]))

    for index in range(1, dtu.get_table_row_count(dt) + 1):
        record = dtu.get_table_row_as_list(dt, index)
        if record:
            print("Record # %d: %s" % (index, ' | '.join(record)))

    print(dt.headers)
    print(dt.row(1))

    print(
        "Get Table Rows With Key: Key: 2 | Repr: List: %s" %
        repr(dtu.get_table_rows_with_key(dt, key='2', as_list=1))
    )
    print(
        "Get Table Rows With Key: Key: 2 | Repr: Dict: %s" %
        repr(dtu.get_table_rows_with_key(dt, key='2', as_list=0))
    )
    dt.headers = []
    print(
        "Get Table Rows With Key: Key: 2 | Repr: List: %s" %
        repr(dtu.get_table_rows_with_key(dt, key='2', as_list=1))
    )
    print(
        "Get Table Rows With Key: Key: 2 | Repr: Dict: %s" %
        repr(dtu.get_table_rows_with_key(dt, key='2', as_list=0))
    )


if __name__ == '__main__':
    test_data_table()
