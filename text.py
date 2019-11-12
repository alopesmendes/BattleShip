from tkinter import Canvas
from verification_error import *

class Text:
    
    """
    Initiates the text with it's coordinates, size, and string.
    param var: x, y the position , size the dimesion and text the string.
    """
    def __init__(self, x, y, size, text):
        raise_type_error((x, int), (y, int), (size, int), (text, str))
        
        self.x = x
        self.y = y
        self.size = size
        self.text = text
    
    """
    Creates the text in the given canvas.
    param var: canvas and kwargs the attributes.
    """
    def create_in_canvas(self, canvas,  **kwargs):
        raise_type_error((canvas, Canvas))
        
        try :
            self.id = canvas.create_text( self.x, self.y, **kwargs, text = self.text, font = ('Times', str(self.size)))
        except TclError:
            raise TclError( 'function: "create_in_canvas" of Text was given bad arguments ' )
    
    def text(self):
        return text