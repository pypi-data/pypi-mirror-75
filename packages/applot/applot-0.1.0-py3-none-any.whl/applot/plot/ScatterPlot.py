
from . import base
from .. import svg, util
from .colors import colors

class ScatterPlot(base.PlotBase):
    plot_name  = "PlotBase"

    
    def __init__(self,x,y,color='black',radius=1,title=None,**kwargs):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.title = title

        self.xrange = min(x), max(x)
        self.yrange = min(y), max(y)

        # Set plot x/y min/max
        if 'xmin' in kwargs:
            self.xrange = kwargs['xmin'],self.xrange[1]
        if 'xmax' in kwargs:
            self.xrange = self.xrange[0],kwargs['xmax']
        if 'ymin' in kwargs:
            self.yrange = kwargs['ymin'],self.yrange[1]
        if 'ymax' in kwargs:
            self.yrange = self.yrange[0],kwargs['ymax']

        # Check if xticks is specified
        if 'xticks' in kwargs:
            self.xticks = kwargs['xticks']
            self.n_xticks = len(kwargs['xticks'])
        else:
            if 'n_xticks' in kwargs:
                self.n_xticks = kwargs['n_xticks']
            else:
                self.n_xticks = self._n_xticks
            self.xticks = util.linspace(
                *self.xrange,
                self.n_xticks
                )
        # Check if xticks is specified
        if 'yticks' in kwargs:
            self.yticks = kwargs['yticks']
            self.n_yticks = len(kwargs['yticks'])
        else:
            if 'n_yticks' in kwargs:
                self.n_yticks = kwargs['n_yticks']
            else:
                self.n_yticks = self._n_yticks
            self.yticks = util.linspace(
                *self.yrange,
                self.n_yticks
                )

        # xmin, xmax = self.xrange
        # self.xscale = util.make_scale(
        #     xmin,
        #     xmax
        # )
        



        if radius in kwargs:
            radius = kwargs['radius']
        else:
            radius=None
        if title in kwargs:
            title = kwargs['title']
        else:
            title=None

    def toSvg(self):
        pass

