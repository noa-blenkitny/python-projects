# =============================================================================
# question 1
# =============================================================================


def flatten(rec_list):
    """
    returns a non recursive version of the list
    :param rec_list: a recursive list
    :return: a non recursive list. order of first appearance is preserved
    """

    if rec_list == []:
        return rec_list

    if type(rec_list[0]) == list:
        return flatten(rec_list[0]) + flatten(rec_list[1:])

    return rec_list[:1] + flatten(rec_list[1:])


# =============================================================================
# question 2
# =============================================================================

def partition_vl1(lst, acc1, acc2):
    """
    Checks if you can divide the list to two lists so the sum of one list + 
    acc1 will be the same of the second list + acc2
    :param lst: a list of integers
    :param acc1,acc2: integers
    :return: True/False
    """

    if acc1 == acc2 and lst == []:
        return True

    if lst == []:
        return False

    return partition_vl1(lst[1:], acc1+lst[0], acc2) or partition_vl1(lst[1:], acc1, acc2+lst[0])


def partition(lst):
    """
    Checks if you can divide the list to two lists with equal sums
    :param lst: a list of integers
    :return: True/False
    """

    return partition_vl1(lst, 0, 0)


# =============================================================================
# question 3
# =============================================================================

def are_neighbors(i1, j1, i2, j2):
    """
    :param i1,j1,i2,j2: integers representing elements in a mxn matrix implemented
    using list of lists
    :return: True if matrix[i1][j1] is the neigbhor of matrix[i2][j2],
    False otherwise

    """
    if (j1 == j2 and (i1 == i2+1 or i1 == i2-1)) or (i1 == i2 and (j1 == j2-1 or j1 == j2+1)):
        return True

    else:
        return False


def is_valid_move(matrix, i1, j1, i2, j2):
    """
    :param matrix: a mxn matrix implemented using list of lists
    :param i1,j1,i2,j2: integers that represent elements in the matrix 
    :return: True if the move from matrix[i1][j1] to matrix[i2][j2] is valid,
    False oterwise
    """
    if len(matrix) <= i2 or len(matrix[i1]) <= j2:
        return False

    if are_neighbors(i1, j1, i2, j2) is True and matrix[i1][j1] < matrix[i2][j2]:
        return True

    else:
        return False


def num_paths_vl1(matrix, i1, j1, i2, j2):
    """
    :param matrix:a mxn matrix implemented using list of lists
    :param i1,j1,i2,j2: integers that represent elements in the matrix
    :return: an integer representing the number of valid ways you can reach
    matrix[i2][j2] from matrix[i1][j1]
    """
    counter = 0

    if i1 == i2 and j1 == j2:
        return 1

    elif matrix[i1][j1] > matrix[i2][j2]:
        return 0

    if is_valid_move(matrix, i1, j1, (i1 + 1), (j1)):
        counter += num_paths_vl1(matrix, i1+1, j1, i2, j2)

    if is_valid_move(matrix, i1, j1, (i1), (j1+1)):
        counter += num_paths_vl1(matrix, i1, j1+1, i2, j2)

    if is_valid_move(matrix, i1, j1, (i1 - 1), (j1)):
        counter += num_paths_vl1(matrix, i1-1, j1, i2, j2)

    if is_valid_move(matrix, i1, j1, (i1), (j1-1)):
        counter += num_paths_vl1(matrix, i1, j1-1, i2, j2)

    return counter


def num_paths(matrix, i2, j2):
    """
    :param matrix:a mxn matrix implemented using list of lists
    :param i2,j2: integers that represent element in the matrix
    :return: an integer that represent the number of ways you can reach in
    valid moves from matrix[0][0] to matrix[i2][j2]
    """
    return num_paths_vl1(matrix, 0, 0, i2, j2)


# =============================================================================
# question 4
# =============================================================================

def minimal_cost_path_vl1(current, n, taxes, steps_options):
    """
    :param current: the floor you want to start the climb with. an integer
    that must be <= n
    :param n: an integer representing the floor you want to reach
    :param taxes: a list of integers, the length of the list is n+1
    :param steps_options: a list of integers, each integer must be <=n
    :return: an integer which is the minimum taxes you need to pay in order to 
    reach the nth floor from the current floor
    """
    if current == n:
        return 0
    temp = 0
    min_val = float('inf')

    for i in steps_options:
        if (current + i <= n):
            temp = (taxes[current + i] +
                    minimal_cost_path_vl1((current + i), n, taxes, steps_options))

            if min_val > temp:
                min_val = temp

    return min_val


def minimal_cost_path(n, taxes, steps_options):
    """
    :param n: an integer that represent the top floor
    :param taxes: a list of integers, the length of the list is n+1
    :param steps_options: a list of integers, each integer must be <=n
    :return: an integer which is the minimum taxes you need to pay in order to 
    reach the nth floor from the ground floor
    """
    return minimal_cost_path_vl1(0, n, taxes, steps_options)


def minimal_cost_path_vl2(current, n, taxes, steps_options, cost_buffer):
    """
    :param current: the floor you want to start the climb with. an integer
    that must be <= n
    :param n: an integer representing the floor you want to reach
    :param taxes: a list of integers, the length of the list is n+1
    :param steps_options: a list of integers, each integer must be <=n
    :param cost_buffer: a boolean list where each element is False.
    the length of the list is n+1
    :return: an integer which is the minimum taxes you need to pay in order to 
    reach the nth floor from the current floor

    """
    if current == n:
        return 0

    temp = 0
    min_val = float('inf')

    for i in steps_options:
        if (current + i <= n):
            if cost_buffer[current + i] == False:
                temp = minimal_cost_path_vl2(
                    (current + i), n, taxes, steps_options, cost_buffer)
                cost_buffer[current + i] = temp

            else:
                temp = cost_buffer[current + i]

            temp += taxes[current + i]

            if min_val > temp:
                min_val = temp

    return min_val


def minimal_cost_path_faster(n, taxes, steps_options):
    """
    :param n: an integer representing the floor you want to reach
    :param taxes: a list of integers, the length of the list is n+1
    :param steps_options: a list of integers, each integer must be <=n
    :return: an integer which is the minimum taxes you need to pay in order to 
    reach the nth floor from the ground floor

    """
    return minimal_cost_path_vl2(0, n, taxes, steps_options, [False] * (n + 1))
