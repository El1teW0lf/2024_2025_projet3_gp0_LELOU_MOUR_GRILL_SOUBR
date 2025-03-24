from modules.tile import Tile
import numpy as np

class Map():
    def __init__(self,seed):
        
        self.size = (100,100)
        self.map =  np.empty(self.size, dtype=object)
        self._populate_map()

    
    def _populate_map(self):
        for y in range(self.map.shape[0]):
            for x in range(self.map.shape[1]): 
                self.map[y, x] = Tile(y,x,"volcano")
