
from .Element import Element

class Text(Element):
    name = "text"

    def __init__(self,x,y,text,**kwargs):
        super().__init__(self.name,**kwargs)
        self.children = [text]
        self.attributes['x'] = x
        self.attributes['y'] = y
        

    