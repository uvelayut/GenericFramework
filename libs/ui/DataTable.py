from robot.api import logger
from libs.ui.AutoException import *

class DataTable(object):

    def __init__(self):
        self.__header_fields = []
        self.__table_rows = []
        self.__rows = 0
        return

    def _validate_index(self, index):
        self.__rows = len(self.__table_rows)

        try:
            index = int(index)
            assert(index > 0 and index <= self.row_count)
            index -= 1

        except:
            raise TypeError("Invalid Index or Type | Index: %s | Rows in Table: %d" % (index, self.row_count))

        return index

    @property
    def row_count(self):
        self.__rows = len(self.__table_rows)
        return self.__rows

    @property
    def column_count(self):
        if self.headers:
            return len(self.headers)

        if self.row_count:
            return len(self.__table_rows[0])

        return 0


    @property
    def headers(self):
        return self.__header_fields

    @headers.setter
    def headers(self, headers):
        if isinstance(headers, tuple):
            headers = list(headers)

        if isinstance(headers, list):
            self.__header_fields = headers
        else:
            raise AttributeError("Headers has to be list or Tuple")

    def row(self, index):

        index = self._validate_index(index)

        # if index < 0 or index > self.row_count:
        #     raise IndexError("Invalid Index or Type | Index: %s | Rows in Table: %d" % (index, self.row_count))

        # index -= 1
        return self.__table_rows[index]

    def add_row(self, record, index=-1):

        if index != -1:
            index = self._validate_index(index)

        if index == -1:
            self.__table_rows.append(record)
        elif index < self.__rows:
            self.__table_rows.insert(index, record)
        else:
            self.__table_rows.append(record)

    def get_field(self, row, field_name):

        row = int(row)
        field_name = str(field_name).strip().lower()
        field_names = [str(field).strip().lower() for field in self.__header_fields]
        field_value = None

        index = field_names.index(field_name)

        if index > -1:
            record = self.row(row)

            if record:
                try:
                    field_value = record[index]
                except IndexError:
                    logger.info("Field at Index not found | Index: %d | Field: %s" % (index, field_name))
        else:
            raise AutoException("Invalid Field | Field: %s | Available Fields: %s" % (field_name, repr(self.__header_fields)))

        return field_value

    def __repr__(self):

        table = []
        table.append(' | '.join(self.headers))
        table.append('\n')

        for index in range(1, self.row_count + 1):
            record = self.row(index)

            if record:
                table.append(' | '.join(record))
                table.append('\n')

        return ''.join(table).strip()

    def __str__(self):
        return self.__repr__()


def test_DataTable():

    dt = DataTable()
    headers = ('Field # 1', 'field 2', 'Field Number - 3')
    dt.headers = headers

    for x in range(10):
        record = [str(x), str(x*x), str(x*x*x)]
        dt.add_row(record)
        print(record)

    print("Headers: %s" % ' | '.join(dt.headers))
    for index in range(1, dt.row_count):
        record = dt.row(index)
        if record:
            print("Record # %d: %s" % (index, ' | '.join(record)))

    print("Table String Representation:\n%s" % dt)

if __name__ == '__main__':
    test_DataTable()
