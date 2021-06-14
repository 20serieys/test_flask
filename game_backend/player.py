import random as rd
import math

class Player:
    def __init__(self, symbol="@"): 
        self._symbol = symbol
        self._x = None
        self._y = None
        self.money = 5 #ajout du paramètre money
        self.protection = 0 #ajout du paramètre protection
        self.PV = "* * *" #ajout du paramètre points de vie

    def initPos(self, _map) :
        n_row = len(_map)
        #n_col = len(_map[0])

        y_init = n_row//2
        found = False
        while found is False:
            y_init += 1
            for i,c in enumerate(_map[y_init]):
                if c == ".":
                    x_init = i
                    found = True
                    break

        self._x = x_init
        self._y = y_init

        _map[self._y][self._x] = self._symbol

    def set(self, x, y, money, PV, protection):
        self._x = x
        self._y = y
        self.PV = PV
        self.money = money
        self.protection = protection

    def move(self, dx, dy, map):
        new_x = self._x + dx
        new_y = self._y + dy

        if map[new_y][new_x] == "." or map[new_y][new_x] == "x" :
            ret =True
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = "x"
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"x"}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}]
            self._x = new_x
            self._y = new_y
        elif map[new_y][new_x] == "o": #ajout de l'interaction avec l'item money
            ret=True
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = "x"
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"x"}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}]
            self._x = new_x
            self._y = new_y
            self.money += 1
        elif map[new_y][new_x] == "A": #ajout de l'interaction avec l'item protection
            ret=True
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = "x"
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"x"}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}]
            self._x = new_x
            self._y = new_y
            self.protection += 1
        elif map[new_y][new_x] == "V": #ajout de l'interaction avec l'item PV
            ret=True
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = "x"
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"x"}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}]
            self._x = new_x
            self._y = new_y
            self.PV += " *"
        else:
            ret = False
            data = []
        return data, ret



class Monster:
    def __init__(self, symbol="$"):
        self._symbol = symbol
        self._x = None
        self._y = None

    
    def initPos(self, _map, _player):
        n_row = len(_map)
        n_col = len(_map[0])

        found = False
        while found is False:
            y_init = rd.randint(0, n_row - 1)
            x_init = rd.randint(0, n_col - 1)
            c = _map[y_init][x_init]
            if c == "." and math.sqrt((_player._x - x_init)**2 + (_player._y - y_init)**2) > 10:
                found = True
                break
        
        self._x, self._y = x_init, y_init

        _map[self._y][self._x] = self._symbol

    def set(self, x, y):
        self._x = x
        self._y = y
    
    
    def move_monster(self, _map, _player): #fonction permettant de faire bouger les monstres
        dx, dy = 0, 0

        x_distance = _player._x - self._x
        y_distance = _player._y - self._y

        if abs(x_distance) >= abs(y_distance) and x_distance!=0:
            dy = 0
            if x_distance > 0:
                dx = 1
            else:
                dx = -1

        elif abs(y_distance) > abs(x_distance):
            dx = 0
            if y_distance > 0:
                dy = 1
            else:
                dy = -1
            
        new_x = self._x + dx
        new_y = self._y + dy

        distance = math.sqrt((_player._x - self._x)**2 + (_player._y - self._y)**2)
        
        if distance < 15:

            if _map[new_y][new_x] not in ['#', '@', '$']:
                _map[self._y][self._x] = "."
                _map[new_y][new_x] = self._symbol

            elif dy == 0 and y_distance!=0:
                new_x = self._x #on maintient x à sa valeur d'origine puisque le déplacement est impossible
                if y_distance > 0: #on change la valeur de dy pour autoriser le déplacement selon y et se rapprocher du joueur
                    dy = 1
                else:
                    dy = -1

                new_y = self._y + dy

                if _map[new_y][new_x] not in ['#', '@', '$']:
                    _map[self._y][self._x] = "."
                    _map[new_y][new_x] = self._symbol
                else: 
                    new_y = self._y

            elif dx == 0 and x_distance!=0:
                new_y = self._y #on maintient y à sa valeur d'origine puisque le déplacement est impossible
                if x_distance > 0: #on change la valeur de dx pour autoriser le déplacement selon x et se rapprocher du joueur
                    dx = 1
                else:
                    dx = -1
                new_x = self._x + dx

                if _map[new_y][new_x] not in ['#', '@', '$']:
                    _map[self._y][self._x] = "."
                    _map[new_y][new_x] = self._symbol
                else:
                    new_x = self._x

            else:
                new_x = self._x
                new_y = self._y
                
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"."}, {"i": f"{new_y}", "j":f"{new_x}", "content":f"{self._symbol}"}]

            self._x = new_x
            self._y = new_y

        else:
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"."}, {"i": f"{self._y}", "j":f"{self._x}", "content":f"{self._symbol}"}]
            
        return data 


    