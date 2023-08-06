
class colors:
    white = "ffffff"
    gray = "#f0f0f0"
    grey = gray
    mid_gray = "#808080"
    mid_grey = mid_gray
    dark_gray = "#404040"
    dark_grey = dark_gray
    black = "#000000"

    blue = "#3b7cff"
    red = "#fa2828"
    green = "#64ff4f"
    orange = "#ff711f"
    purple = "#b152ff"

    b = blue
    r = red
    g = green
    o = orange
    p = purple
    k = black
    w = white
    
    category10 = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf"
    ]
    tableau10 = [
        "#4e79a7",
        "#f28e2c",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc949",
        "#af7aa1",
        "#ff9da7",
        "#9c755f",
        "#bab0ab"
    ]

    @classmethod
    def get(cls,color,default='k'):
        if hasattr(cls,color):
            return getattr(cls,color)
        else: return default
