
from ... import svg
from .PlotObject import PlotObject

class PlotTitle(PlotObject):
    _default_style = {
        'font-family': 'helvetica',
        'font-size': 5,
        'font-weight': 'bold',
        'fill': 'black'
    }

    def __init__(self,x1,y1,x2,y2,title="",style={}):
        super().__init__(x1,y1,x2,y2)
        self.title = title
        self.style = {
            **self._default_style,
            **style
        }

    def toSVG(self):
        return svg.Group(c=[
            svg.Text(
                x=self.pos['x1'],
                y=self.pos['y2'],
                text=self.title,
                a={**self.style}
            )
        ])

