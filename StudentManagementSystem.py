import copy


class Node:
    def __init__(self, val):
        self.value = val
        self.next = None

    def __repr__(self):
        return '[' + str(self.value) + ']'


class Tree_node():
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.key) + ": " + str(self.val)

    def is_leaf(self):
        return (self.left == None) and (self.right == None)

    def find_successor(self):
        if self.right is None:
            return None
        tmp = self.right
        while tmp.left is not None:
            tmp = tmp.left
        return tmp


class Binary_search_tree():
    def __init__(self):
        self.root = None

    def search(self, key):
        ''' return node with key, uses recursion '''

        def lookup_rec(node, key):
            if node == None:
                return None
            elif key == node.key:
                return node
            elif key < node.key:
                return lookup_rec(node.left, key)
            else:
                return lookup_rec(node.right, key)

        return lookup_rec(self.root, key)

    def insert(self, key, val):
        ''' insert node with key,val into tree, uses recursion '''

        def insert_rec(node, key, val):
            if key == node.key:
                node.val = val     # update the val for this key
            elif key < node.key:
                if node.left == None:
                    node.left = Tree_node(key, val)
                else:
                    insert_rec(node.left, key, val)
            else:  # key > node.key:
                if node.right == None:
                    node.right = Tree_node(key, val)
                else:
                    insert_rec(node.right, key, val)
            return

        if self.root == None:  # empty tree
            self.root = Tree_node(key, val)
        else:
            insert_rec(self.root, key, val)

    def find_parent(self, key):
        parent = self.root
        children = self.root

        if self.root.key == key:
            return None, self.root

        while children.key != key:
            parent = children
            if parent.key > key:
                if parent.left is not None:
                    children = parent.left
                else:
                    return
            elif parent.key < key:
                if parent.right is not None:
                    children = parent.right
                else:
                    return
            else:
                break
        return parent, children

    def delete(self, key):
        if not self.search(key):
            return
        parent, children = self.find_parent(key)
        if children.is_leaf():  # basic case
            if parent is not None:
                if children.key > parent.key:
                    parent.right = None
                else:
                    parent.left = None

            else:
                self.root = None

        elif children.left is None:  # has one children - right
            if parent is not None:
                if children.key > parent.key:
                    parent.right = children.right
                else:
                    parent.left = children.right
            else:
                self.root = children.right

        elif children.right is None:  # has one children - left
            if parent is not None:
                if children.key < parent.key:
                    parent.left = children.left
                else:
                    parent.right = children.left
            else:
                self.root = children.left

        else:  # complicate case - 2 children
            successor = children.find_successor()
            successor_parent, successor = self.find_parent(successor.key)
            if successor.right is not None:
                if successor_parent.key != key:  # successor_parent shouldn't be deleted
                    successor_parent.left = successor.right
                else:
                    if children.key > parent.key:
                        parent.right = children.right
                    else:
                        parent.left = children.right
            else:  # successor is leaf
                if successor_parent.key > successor.key:
                    successor_parent.left = None
                else:
                    successor_parent.right = None
                children.key = successor.key
                children.val = successor.val

    def inorder(self):
        ''' return inorder traversal of values as str, uses recursion '''
        def inorder_rec(curr_node, res):
            if curr_node != None:
                inorder_rec(curr_node.left, res)
                res.append((curr_node.key, curr_node.val))
                inorder_rec(curr_node.right, res)
            return res

        if self.root == None:  # empty tree
            return []
        else:
            return inorder_rec(self.root, [])

    def __repr__(self):
        # no need to understand the implementation of this one
        out = ""
        # need printree.py file or make sure to run it in the NB
        for row in printree(self.root):
            out = out + row + "\n"
        return out


def printree(t, bykey=True):
    """Print a textual representation of t
    bykey=True: show keys instead of values"""
    # for row in trepr(t, bykey):
    #        print(row)
    return trepr(t, bykey)


def trepr(t, bykey=False):
    """Return a list of textual representations of the levels in t
    bykey=True: show keys instead of values"""
    if t == None:
        return ["#"]

    thistr = str(t.key) if bykey else str(t.val)

    return conc(trepr(t.left, bykey), thistr, trepr(t.right, bykey))


def conc(left, root, right):
    """Return a concatenation of textual represantations of
    a root node, its left node, and its right node
    root is a string, and left and right are lists of strings"""

    lwid = len(left[-1])
    rwid = len(right[-1])
    rootwid = len(root)

    result = [(lwid+1)*" " + root + (rwid+1)*" "]

    ls = leftspace(left[0])
    rs = rightspace(right[0])
    result.append(ls*" " + (lwid-ls)*"_" + "/" + rootwid *
                  " " + "\\" + rs*"_" + (rwid-rs)*" ")

    for i in range(max(len(left), len(right))):
        row = ""
        if i < len(left):
            row += left[i]
        else:
            row += lwid*" "

        row += (rootwid+2)*" "

        if i < len(right):
            row += right[i]
        else:
            row += rwid*" "

        result.append(row)

    return result


def leftspace(row):
    """helper for conc"""
    # row is the first row of a left node
    # returns the index of where the second whitespace starts
    i = len(row)-1
    while row[i] == " ":
        i -= 1
    return i+1


def rightspace(row):
    """helper for conc"""
    # row is the first row of a right node
    # returns the index of where the first whitespace ends
    i = 0
    while row[i] == " ":
        i += 1
    return i

# =============================================================================
#
# =============================================================================


class Subject:

    def __init__(self, name, grade, points):
        self.name = name
        self.grade = float(grade)
        self.points = float(points)

    def __repr__(self):
        return str(self.name) + ", " + str(self.grade) + "[" + str(self.points) + "]"


class Student:

    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.points = 0.0
        self.head = None

    def find_sub_in_list(self, sub):
        """ 
        helper func that checks a subject is in a linked list
        :param sub: Node object, the value is from class Subject
        :return: True if the sub in the student's linked list of subjects,
        False otherwise
        """
        p = self.head
        while p is not None:
            if p.value.name == sub.value.name:
                return True
            else:
                p = p.next
        return False

    def add_subjects(self, lst):
        """
        :param lst: a list of Subjects (objects from class Subject)
        """

        for sub in lst:
            new_sub = Node(sub)

            if self.find_sub_in_list(new_sub):
                p = self.head
                while p.value.name != new_sub.value.name:
                    p = p.next
                else:
                    p.value = new_sub.value

            else:  # sub is not in the list
                new_sub.next = self.head
                self.head = new_sub
        self.points = self.sum_of_points()

    def get_average(self):
        list_of_points = []
        list_of_avg = []
        sub = self.head
        if self.head == None:  # no subjects
            return 0.0
        else:
            while sub is not None:
                list_of_points.append(sub.value.points)
                list_of_avg.append(sub.value.grade*sub.value.points)
                sub = sub.next
            return float(sum(list_of_avg)/sum(list_of_points))

    def sum_of_points(self):
        """ checks the num of points a student has based on how many subject he passed"""
        res = 0.0
        cur_sub = self.head
        while cur_sub is not None:
            if cur_sub.value.grade > 55.0:
                res += cur_sub.value.points
            cur_sub = cur_sub.next
        return res

    def __lt__(self, other):
        return self.get_average() < other.get_average()

    def __gt__(self, other):
        return self.get_average() > other.get_average()

    def __le__(self, other):
        return self.get_average() <= other.get_average()

    def __ge__(self, other):
        return self.get_average() >= other.get_average()

    def __eq__(self, other):

        if not isinstance(other, Student):
            return False

        return self.get_average() == other.get_average()

    def __ne__(self, other):
        return self.get_average() != other.get_average()

    def is_warning(self):
        """cheacks if a student is in warning based on the average/num of falied subjects"""

        if self.head == None:  # Doesn't have subjects
            return False

        elif self.get_average() <= 65.0:
            return True

        else:
            cur_sub = self.head
            failed_sub = 0
            while cur_sub is not None:
                if cur_sub.value.grade < 56.0:
                    failed_sub += 1
                cur_sub = cur_sub.next
            if failed_sub > 1:
                return True

        return False

    def __repr__(self):
        info = "Student " + str(self.name) + "[" + str(self.student_id) + "], "

        if self.head == None:
            return info + "avg:0.0, points:0.0, grades:no subjects yet."

        else:
            info += "avg:" + str(self.get_average()) + ", points:"
            info += str(self.points) + ", grades:"
            list_of_sub = ""
            cur_sub = self.head
            while cur_sub is not None:
                sub_info = str(cur_sub.value.name) + "(" + str(cur_sub.value.points) + \
                    ")-" + str(cur_sub.value.grade)
                list_of_sub += sub_info + ", "
                cur_sub = cur_sub.next
            list_of_sub = list_of_sub.rstrip(" ")
            list_of_sub = list_of_sub.rstrip(",")
            list_of_sub += "."
            return info + list_of_sub


class ForeignStudent(Student):

    def __init__(self, name, student_id):
        Student.__init__(self, name, student_id)

    def get_average(self):
        cur_sub = self.head
        highest_score = 0
        while cur_sub is not None:
            if cur_sub.value.grade > highest_score:
                highest_score = cur_sub.value.grade
            cur_sub = cur_sub.next
        return (Student.get_average(self)+highest_score)/2

    def __repr__(self):
        return "Foreign" + Student.__repr__(self)


class Queue:

    def __init__(self):
        self.__items = []

    def enqueue(self, val):
        self.__items.insert(0, val)

    def dequeue(self):
        return None if self.is_empty() else self.__items.pop()

    def front(self):
        return None if self.is_empty() else self.__items[-1]

    def rear(self):
        return None if self.is_empty() else self.__items[0]

    def __len__(self):
        return len(self.__items)

    def is_empty(self):
        return len(self.__items) == 0

    def __repr__(self):
        if self.is_empty():
            return ""
        else:
            res = ""
            for item in reversed(self.__items):
                res += str(item)
                res += "\n"
            res = res.strip("\n")
            return res


class Department:

    def __init__(self, name):
        self.name = name
        self.students_BST = Binary_search_tree()
        self.id2nodes = {}

    def __repr__(self):
        info = "Department: " + str(self.name) + "\n"
        list_of_student = self.students_BST.inorder()
        for student in list_of_student:
            info += str(student[1]) + "\n"

        return info

    def insert(self, student):
        """
        adds a student to the department
        :param student: an object from class Student
        """
        if self.id2nodes.get(student.student_id) == None:
            self.students_BST.insert(student.get_average(), student)
            self.id2nodes[student.student_id] = copy.copy(
                Tree_node(student.get_average(), student))

    def delete_student_by_id(self, student_id):
        """
         removes a student from the department
        :param student_id: int representing the id of the student
        """
        student = self.id2nodes.get(student_id)
        if student != None:  # if the student is in id2nodes
            student = student.val  # the object of student
            self.students_BST.delete(student.get_average())
            del self.id2nodes[student_id]

    def add_subject_by_student_id(self, student_id, subject):
        """
         adds subject to a student 
        :param student_id: int representing the id of the student
        :patam subject: from class Subject
        """
        student = self.id2nodes.get(student_id)
        if student != None:  # if the student is in id2nodes
            student = student.val
            self.delete_student_by_id(student_id)
            student.add_subjects([subject])
            self.insert(student)

    def warnings(self):
        """ returns a Queue of the student in warning"""
        queue_of_warnings = Queue()
        list_of_student = self.students_BST.inorder()
        for student in list_of_student:
            if student[1].is_warning():  # the object Student
                queue_of_warnings.enqueue(student[1])
        return queue_of_warnings
