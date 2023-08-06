
from ... import svg, util

class PlotObject:
    def __init__(self,x1,y1,x2,y2):
        self.pos = {
            "x1":x1, 
            "y1":y1, 
            "x2":x2, 
            "y2":y2,
            "w": x2-x1,
            "h": y2-y1,
        }
        self._makeScales()  
    
    def __str__(self):
        return str(self.toSVG())

    def render(self): 
        return self.__str__()

    def _makeScales(self):
        self._xscale = util.make_scale(
            0,100,self.pos['x1'],self.pos['x2']
        )
        self._yscale = util.make_scale(
            0,100,self.pos['y1'],self.pos['y2']
        )

    def toSVG(self):
        # Child classes should override this...
        raise NotImplementedError

