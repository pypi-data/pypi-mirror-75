
from .Element import Element

class Group(Element):
    name = "g"

    def __init__(self,**kwargs):
        super().__init__(self.name,**kwargs)

    def dissolve(self):
        return self._schildren()


    