class Cell:
    def __init__(self, i, j, value=None):
        """
        :param i,j: integers represting the location inside the subgrid
        :param value: one integer if it is the known value of the cell,
                      None otherwise
        """
        self.i = i
        self.j = j
        if value == None:
            self.values = [1,2,3,4,5,6,7,8,9]
        else:
            self.values = [value]
        
    def __repr__(self):
        if len(self.values) == 1:
            return str(self.values[0])
        return '_'
    
