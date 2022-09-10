import Cell

class SubGrid:
    def __init__(self, i, cells=None):
        """
        :param i: an integer representing the number of the subgrid
        :param cells: an object from class Cell if the cell has a known value,
                      otherwise can be None
        """
        self.i = i
        self.grid = [[Cell.Cell(0,0),Cell.Cell(0,1),Cell.Cell(0,2)],
                      [Cell.Cell(1,0),Cell.Cell(1,1),Cell.Cell(1,2)],
                      [Cell.Cell(2,0),Cell.Cell(2,1),Cell.Cell(2,2)]]
        self.collected_values = []
        
        if cells != None:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    for cell in cells:
                        if cell.i == i and cell.j == j:
                            self.grid[i][j] = cell
                            self.collected_values.append(cell.values[0])
    
    def update_values(self):
        """
        adds the known value of the cells in the subgrid to the collected 
        values list of the subgrid
        """
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                    if len(self.grid[i][j].values) == 1:
                        if self.grid[i][j].values[0] not in self.collected_values:
                            self.collected_values.append(self.grid[i][j].values[0])
    
    def remove_values(self, cell):
        """
        if the cell value is not known for sure, this function removes from
        cell.value the known values of the other cell in the subgrid
        :param cell: an object from class Cell in the subgrid
        
        """
        if len(cell.values) > 1:
            cell.values=[val for val in cell.values if val not in self.collected_values]
            self.update_values()
    
    def check_cells_possibilities(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.remove_values(self.grid[i][j])
                

