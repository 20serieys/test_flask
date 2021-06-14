from .map_generator import Generator
from .player import Player
from .player import Monster



class Game:
    def __init__(self, width=96, height=32):
        self._generator = Generator(width=width, height=height)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._map = self._generator.tiles_level

        self._player = Player()
        self._player.initPos( self._map )
        self._player2 = Player()
        self._player2.initPos( self._map )

        #création de monstres:        
        self._monster_1 = Monster()
        self._monster_1.initPos(self._map, self._player)
        self._monster_2 = Monster()
        self._monster_2.initPos(self._map, self._player)
        self._monster_3 = Monster()
        self._monster_3.initPos(self._map, self._player)
        self._monster_4 = Monster()                     #trois monstres pour chaque joueur
        self._monster_4.initPos(self._map, self._player2)
        self._monster_5 = Monster()
        self._monster_5.initPos(self._map, self._player2)
        self._monster_6 = Monster()
        self._monster_6.initPos(self._map, self._player2)
        self.monsters = [self._monster_1, self._monster_2, self._monster_3, 
                         self._monster_4, self._monster_5, self._monster_6]


    def getMap(self):
        return self._map

    def getStat(self): #permet d'obtenir les stats du joueur dans app.py
        return self._player.PV, self._player.money, self._player.protection, self._player2.PV, self._player2.money, self._player2.protection

    def move_1(self, dx, dy):
        return self._player.move(dx, dy, self._map)
    
    def move_2(self, dx, dy):
        return self._player2.move(dx, dy, self._map)

    def move_monsters(self):
        data_monsters = []
        data_monsters.append(self._monster_1.move_monster(self._map, self._player))
        data_monsters.append(self._monster_2.move_monster(self._map, self._player))
        data_monsters.append(self._monster_3.move_monster(self._map, self._player))
        data_monsters.append(self._monster_4.move_monster(self._map, self._player2))
        data_monsters.append(self._monster_5.move_monster(self._map, self._player2))
        data_monsters.append(self._monster_6.move_monster(self._map, self._player2))

        return data_monsters

    def set_save(self):
        save = {}
        pr = self._player
        player_2 = self._player2
        save['player'] = {'x' : pr._x, 'y' : pr._y, 'PV': pr.PV, 'money': pr.money, 'protection': pr.protection}
        save['player_2'] = {'x' : pr._x, 'y' : pr._y, 'PV': pr.PV, 'money': pr.money, 'protection': pr.protection}
        loc_monsters = {}
        for i, monster in enumerate(self.monsters):
            loc_monsters[i] = {'x': monster._x, 'y': monster._y}
        save['monsters'] = loc_monsters
        save['map'] = self._map
        return save

    def charge(self, data):
        self._map = data['map']
        self._player.set(**data['player'])
        self._player2.set(**data['player_2'])
        mstrs = data['monsters']
        for key in data['monsters']:
            loca = (mstrs['x'], mstrs['y'])
            self.monsters[key].set(*loca)