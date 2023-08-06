
from .Element import Element

class Rect(Element):
    name = "rect"

    def __init__(self,x,y,w,h,**kwargs):
        super().__init__(self.name,**kwargs)
        self.attributes['x'] = x
        self.attributes['y'] = y
        self.attributes['w'] = w
        self.attributes['h'] = h

    