
from .Element import Element

class SVG(Element):
    name = "svg"

    def __init__(self,viewBox="0 0 100 100",**kwargs):
        super().__init__(self.name,**kwargs)
        self.attributes['viewBox'] = viewBox

        