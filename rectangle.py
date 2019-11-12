from tkinter import Canvas
from verification_error import *

class Rectangle:
    
    """
    Initiates the rectangle with it's coordinates.
    param var: x, y the position and w, h the dimesion
    """
    def __init__(self, x, y, w, h):
        raise_type_error((x, int), (y, int), (w, int), (h, int))
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.id = None
        self.focus_on = False
        self.kwargs = {'fill':'', 'outline':'black', 'width':1, 'dash':(), 'dashoffset':0, 'state':'normal', 'stipple':'', 'tags':''}
    
    """
    Creates the rectangle in the canvas.
    param var: canvas The Canvas, kwargs the additional arguments.
    """
    def create_in_canvas(self, canvas,  **kwargs):
        raise_type_error((canvas, Canvas))
            
        try :
            self.kwargs = {**self.kwargs, **kwargs}
            self.id = canvas.create_rectangle( self.x, self.y, self.x + self.w, self.y + self.h, kwargs )
        except TclError:
                raise TclError( 'function: "create_in_canvas" of Rectangle was given bad arguments ' )

        
    #Modify's the ascepts (args) of rectangle
    """
    Modify's the attributes of an rectangle
    param var: canvas and kwargs the attributes.
    """
    def modify_aspects(self, canvas, **kwargs):
        raise_type_error((canvas, Canvas))
        
        if self.id != None:
            try:
                canvas.itemconfigure( self.id, kwargs )
            except TclError: 
                raise TypeError( 'function: "modify_aspects" of Rectangle was given bad arguments ' )

    
    """
    Moves the rectangle in the canvas according to the vector vx, vy.
    param var: canvas and vx, vy the vectors
    """
    def move(self, canvas, vx, vy):
        raise_type_error((canvas, Canvas))
        
        self.x += vx
        self.y += vy
        canvas.move( self.id, vx, vy )
        
    """
    Deletes the rectangle from the canvas.
    param var: canvas.
    """
    def delete(self, canvas):
        raise_type_error((canvas, Canvas))
        
        canvas.delete( self.id )
        
    
    def reset(self, canvas):
        raise_type_error((canvas, Canvas))

        self.focus_on = False
        self.modify_aspects( canvas, **self.kwargs )

    """
    return: string form of an rectangle.
    """
    def __str__(self):
        return 'Rectangle {} [x : {}, y : {}, w : {}, h : {}]'.format(self.id, self.x, self.y, self.w, self.h)
        