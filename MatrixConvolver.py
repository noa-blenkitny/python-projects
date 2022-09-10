import numpy as np
import copy


class MatrixConvolver:

    def __init__(self):
        self.matrices_list = []

    def add_matrix(self, matrix):
        """
        If matrices_list is an empty list, append matrix to the
        matrices_list. Otherwise, append matrix only if the shape of matrix is 
        identical to that of the other matrices in matrices_list.
        :param matrix: a numpy array
        """
        if len(self.matrices_list) == 0:
            self.matrices_list.append(matrix)
        else:
            if matrix.shape == self.matrices_list[0].shape:
                self.matrices_list.append(matrix)

    def remove_matrix(self, element):
        """
        :param element: can be an integer (smaller than the length
        of self.matrices_list) or numpy array
        """
        if isinstance(element, np.ndarray):
            for matrix in self.matrices_list:
                if np.array_equal(matrix, element):
                    self.matrices_list.remove(matrix)
                    return

        elif isinstance(element, int):
            self.matrices_list.pop(element)

        else:
            return -1

    def get_matrices(self):
        """ returns a copy of the self.matrices_list """
        return copy.deepcopy(self.matrices_list)

    def reshape_matrices(self, new_shape):
        """
        reshapes the matrices in self.matrices list to the new shape
        :param new_shape: a tuple of integers
        :return: 0 if self.matrices_list is empty, -1 if an error occours.
        otherwise reshape the matrices and return None
        """
        if len(self.matrices_list) == 0:
            return 0

        else:
            try:
                new_list = []
                for matrix in self.matrices_list:
                    matrix = matrix.reshape(new_shape)
                    new_list.append(matrix)

                self.matrices_list = new_list

            except:
                return -1

    def conv(self, i, filter_matrix, stride_size=1):
        """
        :param i: the index of the matrix you want to convolve from self.matrices_list
        :param filter_matrix: a numpy array. the shape must be smaller than the 
        self.matrices_list[i]
        :param stride_size: integer representing the number of steps you want to
        move each time
        :return: the matrix after convolution
        """
        matrix = self.matrices_list[i]
        filter_row, filter_col = filter_matrix.shape
        res_row, res_col = matrix.shape
        res_row = int((res_row - filter_row + 1)/stride_size)
        res_col = int((res_col - filter_col + 1)/stride_size)
        res = np.zeros((res_row, res_col))
        for row in range(res_row):
            for col in range(res_col):
                res[row][col] = np.sum(matrix[row:row+filter_row,
                                              col:col+filter_col]*filter_matrix)
        return res
