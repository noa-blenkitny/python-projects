import pandas as pd
import ast


class TedAnalyzer:

    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_data(self):
        """returns a copy of the data"""
        return self.data.copy()

    def get_data_shape(self):
        """returns the size of the data"""
        return self.data.shape

    def get_top_n_by_col(self, column_name, n):
        """
        :param column_name: a string, a name of a column from the DataFrame 
        :param n: an integer
        :return: a copy of the top n rows from the data attribute, that has the 
        highest values in the column_name column
        """
        if n > self.data.shape[0]:
            return self.get_data().sort_values(column_name, ascending=False)

        else:
            return self.get_data().sort_values(column_name, ascending=False).head(n)

    def get_unique_values_as_list(self, column_name):
        """
        :param column_name: a string, a name of a column from the DataFrame 
        :return: a list of the unique values in the column column_name
        """
        return list(self.data[column_name].unique())

    def get_unique_values_as_dict(self, column_name):
        """
        :param column_name: a string, a name of a column from the DataFrame 
        :return: a dictionary of the unique value in column column_name as keys 
        and the number of rows they appear in as values.
        """
        return self.data[column_name].value_counts().to_dict()

    def get_na_counts(self):
        """Return a Series object with counts of the null values in each column."""
        nans = self.get_data().isna()
        return nans.sum()

    def get_all_na(self):
        """
        Returns a copy of the data attribute with all the rows that contain at
        least one null value.
        """
        return self.get_data()[pd.isnull(self.get_data()).any(axis=1)]

    def drop_na(self):
        """
        Removes all the rows that have at list a single column with null value
        from the data and reset the index of the result
        """
        self.data = self.data.dropna().reset_index()

    def get_unique_tags(self):
        """ Returns a list of all the unique strings from the “tags” column."""
        list_of_uniques = []
        tags = self.get_unique_values_as_list("tags")
        for tag in tags:
            # converting the string containing list to list
            tag = ast.literal_eval(tag)
            for word in tag:
                if word not in list_of_uniques:
                    list_of_uniques.append(word)

        return list_of_uniques

    def add_duration_in_minutes(self, new_column_name):
        """Adds a new column called new_column_name to the data attribute that 
        shows the “duration” value in minutes
        :param new_column_name: a string, the name of the column you want to add
        """
        self.data[new_column_name] = (self.data["duration"]/60).astype("int64")

    def filter_by_row(self, column_name, threshold):
        """
        :param column_name: a string, a name of a column from the DataFrame. 
        the column must be numeric
        :param threshold: an integer
        :return: a subset of the data attribute with all the rows that their 
        column_name values exceed the threshold
        """
        return self.data[self.data[column_name] > threshold]
