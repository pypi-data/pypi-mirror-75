
class _Pos:
    @classmethod
    def xywh(cls,x,y,w,h):
        return cls(x,y,x+w,y+h)

    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = x2 - x1
        self.height = y2 - y1


