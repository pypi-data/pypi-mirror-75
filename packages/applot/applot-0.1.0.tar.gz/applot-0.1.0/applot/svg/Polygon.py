
from .Element import Element

class Polygon(Element):
    name = "polygon"

    def __init__(self,points,**kwargs):
        super().__init__(self.name,**kwargs)
        self.attributes['points'] = points

    