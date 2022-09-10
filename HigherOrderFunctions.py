import copy
from functools import reduce


class Schema:

    def __init__(self, name):
        self.__tables = []
        self.__schema_name = name

    def get_tables(self):
        return self.__tables

    def add_table(self, table):
        self.__tables.append(table)

    def get_name(self):
        return self.__schema_name

    # I need to return only the tables that have the key in them so first I need to filter the list
    # of tables and than return the name of each table
    def find_tables_by_key(self, key): return list(map(lambda table: table.get_table_name(),
                                                       list(filter(lambda table: key in table.get_key(), self.get_tables()))))


class Table:
    def __init__(self, key_set, other_columns, values_types, table_name):
        self.__key = tuple(key_set)
        self.__other_columns = tuple(other_columns)
        self.__records = []
        self.__table_name = table_name
        self.__values_types = copy.deepcopy(values_types)

    def __repr__(self):
        columns = []
        res = 'Table: '+self.__table_name + '\n'
        res += "Columns: "
        for key in self.__key:
            res += str(key)+'(Key) '
            columns.append(key)
        for column in self.__other_columns:
            res += column + ' '
            columns.append(column)
        res += '\nRows:\n'
        for row in self.__records:
            for k in columns:
                res += str(row[k])+'\t'
            res += '\n'
        return res

    def add_record(self, row):
        if self.is_fitted(row) and self.equal_values(row) and self.contains_key(row) == False:
            self.__records.append(row)

    def get_key(self):
        return self.__key

    def get_values_types(self):
        return self.__values_types

    def get_other_columns(self):
        return self.__other_columns

    def get_table_name(self):
        return self.__table_name

    def get_records(self):
        return self.__records

    def columns_names(self): return [
        column for column in self.get_key() + self.get_other_columns()]

    def new_row_keys(self, new_row): return [key for key in new_row.keys()]

    def is_fitted(self, new_row): return all([key in self.new_row_keys(new_row) for key in self.columns_names()]) \
        and all([key in self.columns_names() for key in self.new_row_keys(new_row)])

    def other_record_types(self, new_row): return dict(
        map(lambda item: (item[0], type(item[1])), new_row.items()))

    def equal_values(self, new_row): return all([item in self.other_record_types(new_row).items() for item in self.get_values_types().items()]) \
        and all([item in self.get_values_types().items() for item in self.other_record_types(new_row).items()])

    def other_row_keys(self, new_row): return dict(
        filter(lambda item: item[0] in self.get_key(), new_row.items()))

    def contains_key(self, new_row): return any(list(map(lambda dic: self.other_row_keys(new_row) == dic,
                                                         [self.other_row_keys(x) for x in self.get_records()])))

    def select(self, func): return list(filter(func, self.get_records()))

    def sum_of_column(self, column_name): return reduce(
        lambda x, y: x+y, list(dic[column_name] for dic in self.get_records()), 0)
