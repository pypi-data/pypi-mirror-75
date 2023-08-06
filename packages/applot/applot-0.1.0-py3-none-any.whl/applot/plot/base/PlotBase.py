
from ... import svg
from .PlotObject import PlotObject
from .PlotGrid import PlotGrid
from .PlotBg import PlotBg

"""
# Title
_title_x = 15
_title_y = 40
_title_font_size = 28
# Subtitle
_subtitle_x = 15
_subtitle_y = 70
_subtitle_font_size = 18
# Caption
_caption_x = 15
_caption_y = 385
_caption_font_size = 10

# Default n axis ticks
_n_xticks = 5
_n_yticks = 5

"""

class PlotBase:
    _default_positions = {
        'title': {}
    }

    def __init__(self):
        self.title = None
        self.inner = None
        self.xaxis = None
        self.yaxis = None

        self.bg_color = "#f0f0f0"

    def __str__(self):
        return str(self.toSVG())

    def render(self): 
        return self.__str__()

    def toSVG(self):
        # Child classes should override this...
        raise NotImplementedError

    def addTitle(self,title):
        self.title = title
        return self

    def addInner(self,inner):
        self.inner = inner
        return self

    def addXAxis(self,axis):
        self.xaxis = axis
        return self
    
    def addYAxis(self,axis):
        self.yaxis = axis
        return self

    def reposition(self):
        pass
