import SubGrid

class Grid:
    def __init__(self, sub_grids=None):
        self.rows= [[],[],[],[],[],[],[],[],[]]
        self.columns= [[],[],[],[],[],[],[],[],[]]
        self.sub_grids= [SubGrid.SubGrid(0), SubGrid.SubGrid(1), SubGrid.SubGrid(2), SubGrid.SubGrid(3),
                         SubGrid.SubGrid(4), SubGrid.SubGrid(5), SubGrid.SubGrid(6), SubGrid.SubGrid(7), SubGrid.SubGrid(8)]
        
        if sub_grids != None:
            for sub in sub_grids:
                    self.sub_grids[sub.i] = sub
                   

    def update_values(self):
        """
        this funcntion appends the known value of each cell to the corresponding
        list of the grid rows and colums.
        """
        for sub in self.sub_grids:
            for i in range(len(sub.grid)):
                for j in range(len(sub.grid[i])):
                    if len(sub.grid[i][j].values) == 1:
                #Using the following formula to know were I am in the grid:
                #row num = 3 * int(sub.i / 3) + cell.i
                #col num = 3 *(sub.i % 3) + cell].j
            
                        if sub.grid[i][j].values[0] not in self.rows[3*int(sub.i/3) + sub.grid[i][j].i]:
                            self.rows[3*int(sub.i/3) + sub.grid[i][j].i].append(sub.grid[i][j].values[0])
                                          
                        if sub.grid[i][j].values[0] not in self.columns[3*(sub.i%3) + sub.grid[i][j].j]:
                            self.columns[3*(sub.i%3) + sub.grid[i][j].j].append(sub.grid[i][j].values[0])

            
    def remove_values(self, cell, grid_num):
        """
        removes the values from the cell.values that are already in the row and
        column of the cell
        :param cell: object from class Cell
        :param grid_num: integer representing the subgrid number
        
        """
        if len(cell.values) > 1:   
            cell.values= [val for val in cell.values if val not in self.rows[3*int(grid_num/3)+cell.i]]
            cell.values= [val for val in cell.values if val not in self.columns[3*(grid_num%3) + cell.j]]
        self.update_values()
        
    
    def check_possibilities(self):
        for sub in self.sub_grids:
            sub.check_cells_possibilities()
            
        self.update_values()
        
        for sub in self.sub_grids:
            for i in range(len(sub.grid)):
                for j in range(len(sub.grid[i])):
                    self.remove_values(sub.grid[i][j],sub.i)

    
    def is_solved(self):
        """
        checks if the sudoko is solved by checking if every cell has only one
        value in cell.values
        :return: True if the sudoko is solved, False otherwise
        """
        for sub in self.sub_grids:
               for i in range(len(sub.grid)):
                   for j in range(len(sub.grid[i])):
        
                       if len(sub.grid[i][j].values) == 1:
                          continue
        
                       else:
                          return False
        return True

    
    def solve(self):
        while self.is_solved() == False:
            self.check_possibilities()

    
    def __repr__(self):
        res = ''
        for i in range(9):
            if i % 3 == 0:
                res = res + '\n\n'
            for j in range(9):
                if j % 3 == 0:
                    res = res + '    '
                res = res + str(self.sub_grids[3 * int(i / 3)+ int(j / 3)].grid[i % 3][j % 3]) + ' '
            res = res + '\n'
        return res