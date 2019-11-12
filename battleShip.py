from tkinter import *   
from verification_error import *
from grid import *
import copy
import threading

"""
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
                                            Boat                                                                
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
"""
class Boat:
    """
    Initiates a boat with a list of it's keys on the grid and the color of the boat.
    param var: list_keys a list of keys, team_color a color.
    """
    def __init__(self, list_keys, team_color):
        raise_type_error((list_keys, list))

        self.keys = list_keys
        self.team = team_color
        self.put = False

    """
    return : the keys and color of a boat.
    """
    def boat(self):
        return self.keys, self.team

    """
    Moves the boat according to the vx and vy.
    param var: vx and vy the vector.
    """
    def move(self, grid, vx, vy):
        raise_type_error((grid, Grid), (vx, int), (vy, int))

        keys = []
        
        for k in self.keys:
            keys.append( chr(ord(k[0]) + vx) + str(int(k[1:]) + vy) )
        
        for k in keys:
            if k not in grid.grid():
                return

        self.keys = keys

    """
    Rotate the boat to the inverse direction.
    param var: the grid.
    """
    def rotate(self, grid):
        raise_type_error( (grid, Grid) )

        if len( self.keys ) <= 1:
            return
        keys = list()

        def seperate_letter_number(keys):
            letter = set()
            number = set()
            for k in keys:
                letter.add( k[0] )
                number.add( ''.join(k[1:]) )
            return letter, number
                

        def default_variables_l(letters, numbers):
            mini_l = min( letters )
            if ord(mini_l) + len(numbers) <= ord('A') + grid.length():
                return mini_l, 1
            else:
                return mini_l, -1

        def default_variables_n(letters, numbers):
            mini_n = min( numbers )
            if int(mini_n) + len(letters) <= grid.length():
                return mini_n, 1
            else:
                return mini_n, -1

        letters, numbers = seperate_letter_number( self.keys )
        let, sign_l = default_variables_l(letters, numbers)
        num, sign_n = default_variables_n(letters, numbers)

        for letter in letters:
            for number in numbers:
                l = chr( ord(let) + (int(number) - int(num)) * sign_l )
                n = str( int(num) + (ord(letter) - ord(let)) * sign_n )
                res = l + n
                keys.append( res )

        self.keys = keys
    

    """
    Erases the boat drawing in the canvas.
    param var: canvas and grid.
    """
    def reset(self, canvas, grid):
        raise_type_error((canvas, Canvas), (grid, Grid))

        for k in self.keys:
            grid.reset_case(canvas, k)


    """
    Draw the boat in the canvas. 
    param var: canvas and grid.
    """
    def draw(self, canvas, grid):
        raise_type_error((canvas, Canvas), (grid, Grid))

        for k in self.keys:
            if not grid.is_taken(k):
                grid.case(k).modify_aspects(canvas, fill = self.team)

    """
    Fixes the position of the boat.
    """
    def put_in(self, grid):
        raise_type_error((grid, Grid))

        for k in self.keys:
            if grid.is_taken(k):
                return False

        for k in self.keys:
            grid.take_key(k)
            
        self.put = True
        return True

    """
    return: if the boat is fixed or not.
    """
    def placed(self):
        return self.put


    """
    return: the string of a boat.
    """
    def __str__(self):
        return 'id:' + str(self.team) + ' keys:' + str(self.keys)



"""
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
                                            Player                                                                
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
"""
class Player:

    """
    Initiates the player with its color.
    param var: color.
    """
    def __init__(self, x, y, w, h, size, color):
        raise_type_error((x, int), (y, int), (w, int), (h, int), (size, int))

        self.color = color
        self.num_boat = 0
        self.current_boat = -1
        self.total = 0
        self.boats = dict()    
        self._cancel = None

        self.grid = Grid(x, y, w - 100, h - 100, size)
        self.canvas = Canvas(width=w, height=h, bg = 'white')
        self.canvas.pack()
        self.grid.create_in_canvas(self.canvas, fill = 'blue')

        self.sol = set()

    """
    Adds all the boats to the player.
    param var: set_keys_dim a set of str.
    """
    def add_boats(self, set_keys_dim):
        raise_type_error((set_keys_dim, set))


        def add_boat(key_dim):
            raise_type_error((key_dim, str))

            l = key_dim.split( 'x' )
            if len(l) != 2:
                raise TypeError('Wrong format of dimension of boat')

            alphabet = list( string.ascii_uppercase )
            letters = [ alphabet[i] for i in range(int(l[0])) ]
            numbers = [ str(i) for i in range(int(l[1])) ]
            keys = [ x + y for x in letters for y in numbers ]

            self.boats[self.total] = Boat(keys, self.color)
            self.total += 1



        for key_dim in set_keys_dim:
            add_boat(key_dim)


    """
    return: True if all boats are placed.
    """
    def done_placed_and_reset(self, root):
        raise_type_error((root, Tk))

        def stop_placing(root):
            raise_type_error((root, Tk))

            if self._cancel is not None:
                root.unbind('<Key>', self._cancel)
                self._cancel = None

        if self.total == self.num_boat:
            self.grid.hide(self.canvas)
            stop_placing(root)
            self.sol = self._solutions()
            return True

        return False



    """
    Places all the boats in the grid.
    Deplaces a boat with direction arrows and places it with return.
    param var: root the Tk and canvas the Canvas
    """
    def placing_boats(self, root):
        raise_type_error((root, Tk))


        """
        Moves a boat and places the boat on the grid.
        param var: root the Tk, event, canvas and the grid.
        """
        def move(root, canvas, event):
            raise_type_error((canvas, Canvas))

            root.update()
            if self.done_placed_and_reset(root):
                return

            self.boats[self.num_boat].reset(canvas, self.grid)

            if not self.boats[self.num_boat].placed():
                if event.keysym == 'Right':
                    self.boats[self.num_boat].move(self.grid, 1, 0)
                elif event.keysym == 'Left':
                    self.boats[self.num_boat].move(self.grid, -1, 0)
                elif event.keysym == 'Down':
                    self.boats[self.num_boat].move(self.grid, 0, 1)
                elif event.keysym == 'Up':
                    self.boats[self.num_boat].move(self.grid, 0, -1)
                elif event.keysym == 'space':
                    self.boats[self.num_boat].rotate(self.grid)

                self.boats[self.num_boat].draw(canvas, self.grid)

            if event.keysym == 'Return' and self.boats[self.num_boat].put_in(self.grid):
                self.boats[self.num_boat].draw(canvas, self.grid)
                self.num_boat += 1

            root.update()


        self._cancel = root.bind('<Key>', lambda e: move(root, self.canvas, e), add='+')


    def _solutions(self):
        return set(k for boat in self.boats for k in self.boats[boat].boat()[0])

    """
    Player selects a case, changes the case color to show if hit or miss.
    param var: root the Tk
    """
    def select_case(self, root, player, event):
        raise_type_error((root, Tk), (player, Player))

        if len(self.sol) == 0 or len(player.sol) == 0:
            return

        self.hide(root)
        player.show(root)


        key = player.grid.get_key(event)

        if key in player.sol:
            player.grid.apply_to(player.canvas, event, key,  fill = self.color)
            player.sol.remove(key)
        else:
            player.grid.apply_to(player.canvas, event, key,  fill = 'black')


        if len(self.sol) == 0 or len(player.sol) == 0:
            root.update()
            return

        player.hide(root)
        self.show(root)


    """
    Shows the canvas.
    param var: root the Tk
    """
    def show(self, root):
        raise_type_error((root, Tk))

        self.canvas.pack()
        root.update()

    """
    Hides the canvas.
    param var: root the Tk
    """
    def hide(self, root):
        raise_type_error((root, Tk))

        self.canvas.pack_forget()
        root.update()


"""
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
                                            Players                                                               
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
"""
class Players:
    """
    Initiazes all the players.
    param var: x & y & w & h & size the int

    """
    def __init__(self, x, y, w, h, size,  nb_players):
        raise_type_error((x, int), (y, int), (w, int), (h, int), (size, int), (nb_players, int))

        self.players = dict()
        self.total = nb_players
        self.turn = 1

        for i in range(1, nb_players + 1):
            self.players[i] = Player( x, y, w, h, size, 'red' )


    """
    All all the boats to every player.
    param var: *args
    """
    def add_all_boats(self, *args):
        if len(args) != self.total:
            return False

        for id_player, set_keys_dim  in args:
            if not self.add_boats(id_player, set_keys_dim):
                return False

        return True



    """
    Add all the boats to a specified player.
    `id_player` identify's the player. 
    `id_player` must exist to add boats. 
    param var: id_player a int, set_keys_dim a set
    return: True if boats were added False otherwise.
    """
    def add_boats(self, id_player, set_keys_dim):
        raise_type_error((id_player, int), (set_keys_dim, set))

        if self.total < id_player < 1:
            return False

        self.players[id_player].add_boats(set_keys_dim)
        return True

    """
    Places all the boats of each player.
    param var: root the Tk
    """
    def place_all_boats(self, root):
        raise_type_error((root, Tk))

        for i in range(1, self.total + 1):
            self.players[i].show(root)
            self.players[i].placing_boats(root)

            while not self.players[i].done_placed_and_reset(root):
                root.update()


            self.players[i].hide(root)

        self.players[1].show(root)

    """
    Allow the players to play.
    param var: root the Tk
    """
    def play(self, root, event):
        raise_type_error((root, Tk))

        old_pl = self.turn
        next_pl = self.turn + 1 if self.turn + 1 <= self.total else 1

        self.players[old_pl].select_case(root, self.players[next_pl], event)

        self.turn = next_pl





"""
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
                                            Game                                                                
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
"""
class Game:
    """
    Initiaze the game.
    param var: root the Tk, x & y & w & h & size the int
    """
    def __init__(self, x, y, w, h, size):
        raise_type_error((x, int), (y, int), (w, int), (h, int), (size, int))
        self.root = Tk()
        self.root.geometry(str(w) + 'x' + str(h))
        self._cancel = None

        self.players = Players(x, y, w, h, size, 2)
        self.players.add_all_boats((1, {'1x2', '1x3', '2x4'}), (2, {'2x2', '3x2', '3x4'}))

        self.players.place_all_boats(self.root)

        self.root.bind('<Button-1>', lambda e : self.players.play(self.root, e))


        self.root.mainloop()

    def game(self):
        pass




g = Game(50, 50, 500, 500, 10)