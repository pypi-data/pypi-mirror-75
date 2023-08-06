
from .Element import Element

class Polyline(Element):
    name = "polyline"

    def __init__(self,points,**kwargs):
        super().__init__(self.name,**kwargs)
        self.attributes['points'] = points

    