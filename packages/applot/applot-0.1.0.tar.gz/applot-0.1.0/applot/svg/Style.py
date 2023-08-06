
from .Element import Element

class Style(Element):
    name = "style"

    def __init__(self,style_dict={}):
        self.style_dict = style_dict

    def render(self):
        style_string = " ".join(
            f"{k}:{v};" for k, v in self.style_dict.items()
            )
        return f"<style>{style_string}</style>"

    