from tkinter import Canvas
from verification_error import *
import string
from rectangle import *
from text import *



class Grid:
    
    """
    Initiates the Grid with its coordinates, size of a grid.
    Size cannot be inferior to 0 and superior to 26.
    param var: x, y the position , w, h the dimesion and size the Size.
    """
    def __init__(self, x, y, w, h, size):
        raise_type_error((x, int), (y, int), (w, int), (h, int), (size, int))
        
        if size < 0:
            raise ValueError('size cannot be negative')
        elif size > 26:
            raise ValueError('size cannot be superieur to 26')

        self.x, self.y, self.w, self.h = x, y, w, h
        self.size = size
        self.alphabet = list( string.ascii_uppercase )
        self._ancientKey = ' '
        self._key = ' '

        def creation_of_dict_text_rect(x, y, w, h, size):

            di = dict()
            taken = dict()
            for i in range(size):
                for j in range(size):
                    pos_x = x + ( w // size * i )
                    pos_y = y + ( h // size * j )

                    di[self.alphabet[i] + str(j)] = Rectangle(pos_x, pos_y, w // size, h // size)
                    taken[self.alphabet[i] + str(j)] = False



            return di, taken


        def creation_row_col(x, y, w, h, size):

            row = set()
            col = set()
            for i in range(size):
                pos_x = x + ( w // size * i )
                pos_y = y + ( h // size * i )
                t_size = max(w, h) // size // 3
                row.add( (Text(pos_x + w // size // 2, y - t_size, t_size, self.alphabet[i]), pos_x, pos_x + w // size, i) )
                col.add( ( Text(x - t_size, pos_y + h // size // 2, t_size, str(i)), pos_y, pos_y + h // size, i) )

            return row, col


        self.d, self.taken = creation_of_dict_text_rect(x, y, w, h, size)
        self.row, self.col = creation_row_col(x, y, w, h, size)
            
    """
    Creates the gird in the given canvas.
    param var: canvas and kwargs the attributes.
    """    
    def create_in_canvas(self, canvas, **kwargs):
        raise_type_error((canvas, Canvas))
        
        for t, x1, x2, index in self.row:
            t.create_in_canvas(canvas)

        for t, x1, x2, index in self.col:
            t.create_in_canvas(canvas)

        for rect in self.d.values():
            rect.create_in_canvas(canvas, **kwargs)

    def get_key(self, event):
        

        def find_letter(x):
            for (t, x1, x2, index)  in self.row:
                if x1 <= x <= x2:
                    return self.alphabet[index]
            return ' '

        def find_number(y):
            for (t, y1, y2, index)  in self.col:
                if y1 <= y <= y2:
                    return str(index)
            return ' '

        return find_letter(event.x) + find_number(event.y)

    
    
    """
    Applys an action to a select case according to an event.
    param var: canvas, event, and kwargs the attributes.
    """ 
    def apply_to(self, canvas, event, key,  **kwargs):
        raise_type_error((canvas, Canvas), (key, str))

        if key in self.d:
            self.taken[key] = True
            self.d[key].modify_aspects(canvas, **kwargs)


    """
    Reset the case of the gird if it's not taken.
    param var: canvas the Canvas, key a str.
    """
    def reset_case(self, canvas, key):
        raise_type_error((canvas, Canvas), (key, str))

        if key in self.taken and self.taken[key] == False:
            self.d[key].reset(canvas)


    """
    return: The case correpond to the key
    """
    def case(self, key):
        raise_type_error((key, str))

        if key in self.d:
            return self.d[key]

    """
    Hides all the cases taken.
    param var: canvas the Canvas.
    """
    def hide(self, canvas):
        raise_type_error((canvas, Canvas))

        for k in self.taken:
            if self.taken[k]:
                self.d[k].reset(canvas)

    """
    param var: a key 
    """
    def take_key(self, key):
        raise_type_error((key, str))

        if key in self.taken:
            self.taken[key] = True

    """
    param var: a key 
    return : True if key is taken.
    """
    def is_taken(self, key):
        raise_type_error((key, str))

        if key in self.taken:
            return self.taken[key]
        return False

    """
    return : the dict of cases.
    """
    def grid(self):
        return self.d


    """
    return : the length of the grid.
    """
    def length(self):
        return self.size