
from ... import svg
from .PlotObject import PlotObject

class PlotAxis(PlotObject):
    def __init__(self,x1,y1,x2,y2):
        super().__init__(x1,y1,x2,y2)

    def toSVG(self):
        raise NotImplementedError

