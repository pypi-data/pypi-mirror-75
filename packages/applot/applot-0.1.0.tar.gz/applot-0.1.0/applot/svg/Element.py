

class Element:
    # name = None
    _attributes = {}
    _children = []

    # Default transformations
    _translate = (0,0)
    _scale = (1,1)
    _rotate = (0,0,0)
    
    # Element's transformations
    translate = (0,0)
    scale = (1,1)
    rotate = (0,0,0)
    
    def __init__(self,name=None,**kwargs):
        self.attributes = {
            **self._attributes
        }
        self.children = [
            *self._children
        ]

        self.name = name
        if 'attributes' in kwargs:
            self.attributes.update(
                kwargs['attributes']
            )
        if 'a' in kwargs:
            self.attributes.update(
                kwargs['a']
            )
        if 'children' in kwargs:
            self.children.extend(
                kwargs['children']
            )
        if 'c' in kwargs:
            self.children.extend(
                kwargs['c']
            )
        
    def __repr__(self):
        return f"<Element:{self.name} attrs:{len(self.attributes)} chldrn:{len(self.children)}/>"
        
    def __str__(self):
        # Add transformations if necessary
        if "transform" not in self.attributes:
            transform = []
            if self.translate != self._translate:
                transform.append(f"translate{self.translate}")
            if self.scale != self._scale:
                transform.append(f"scale{self.scale}")
            if self.rotate != self._rotate:
                transform.append(f"rotate{self.rotate}")
            if transform:
                self.attributes['transform'] = " ".join(transform)       
        # Create attribute string
        sattr = " ".join(
            f'{k}="{v}"' for k,v in 
            self.attributes.items()
        )
        # Render string of children
        schildren = self._schildren()
        # Format and return
        return f"<{self.name} {sattr}>{schildren}</{self.name}>"

    def _schildren(self):
        return "".join(str(c) for c in self.children)

    def __add__(self,other):
        pass

    def __radd__(self,other):
        pass

    def copy(self): 
        minime = self.__class__(
            children=[
                (c.copy() if hasattr(c,'copy') else c) 
                for c in self.children
                ],
            attributes={**self.attributes}
        )
        return minime
    
    def render(self):
        return self.__str__()

    def addChild(self,c,*args):
        self.children.append(c)
        self.children.extend(args)
        return self
    
    def delChild(self,c):
        i = self.children.index(c)
        self.children.pop(i)
        return self
        