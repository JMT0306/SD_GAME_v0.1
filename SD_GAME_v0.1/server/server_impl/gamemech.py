from typing import Union

# Constantes
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
class GameMech:
    def __init__(self, nr_x: int, nr_y: int):
        self.nr_max_x = nr_x
        self.nr_max_y = nr_y
        self.players = dict()
        self.walls = dict()
        self.collectibles = dict()  # Adicionando colecionáveis
        self.world = dict()
        for x in range(self.nr_max_x):
            for y in range(self.nr_max_y):
                self.world[(x, y)] = []
        self.nr_players = 0
        self.pos_players = [(5, 5), (2, 2), (1, 1)]
        self.nr_walls = 0
        self.nr_collectibles = 0
        self.add_wall_around()
        self.add_collectibles()

    def add_collectibles(self, num_collectibles=10):
        import random
        for _ in range(num_collectibles):
            while True:
                x = random.randint(1, self.nr_max_x - 2)
                y = random.randint(1, self.nr_max_y - 2)
                if not self.is_wall(self.world[(x, y)]):
                    self.collectibles[self.nr_collectibles] = (x, y)
                    self.world[(x, y)].append(["collectible", self.nr_collectibles])
                    self.nr_collectibles += 1
                    break

    def get_collectibles(self):
        return self.collectibles

    def get_nr_x(self):
        return self.nr_max_x

    def get_nr_y(self):
        return self.nr_max_y

    def get_players(self):
        return self.players

    def is_wall(self, objects):
        for obj in objects:
            if obj[0] == "wall" and obj[1] == "wall":
                return True
        return False

    def add_wall(self, x: int, y: int):
        if not self.is_wall(self.world[(x, y)]):
            self.walls[self.nr_walls] = ["wall", (x, y)]
            self.world[(x, y)].append(["obst", "wall", self.nr_walls])
            self.nr_walls += 1
            return True
        return False

    def get_walls(self):
        return self.walls

    def add_wall_around(self):
        for x in range(0, self.nr_max_x):
            for y in range(0, self.nr_max_y):
                if x in (0, self.nr_max_x - 1) or y in (0, self.nr_max_y - 1):
                    self.walls[self.nr_walls] = ["wall", (x, y)]
                    self.world[(x, y)].append(["obst", "wall", self.nr_walls])
                    self.nr_walls += 1
        return True

    def add_player(self, name: str):
        self.players[self.nr_players] = [name, self.pos_players[self.nr_players]]
        self.world[self.pos_players[self.nr_players]].append(["player", name, self.nr_players])
        self.nr_players += 1
        return (self.nr_players - 1, self.pos_players[self.nr_players - 1])

    def move_to(self, pos: tuple, dir: int):
        if dir == UP:
            new_pos = (pos[0], max(pos[1] - 1, 0))
        elif dir == DOWN:
            new_pos = (pos[0], min(pos[1] + 1, self.nr_max_y - 1))
        elif dir == LEFT:
            new_pos = (pos[0] - 1, pos[1]) if pos[0] > 0 else pos
        elif dir == RIGHT:
            new_pos = (pos[0] + 1, pos[1]) if pos[0] < self.nr_max_x - 1 else pos
        return new_pos

    def obstacle_in_pos(self, pos: tuple):
        objects = self.world[pos]
        for obj in objects:
            if obj[0] == "obst":
                return True
        return False

    def collect_item(self, player_id: int, collectible_id: int):
        if collectible_id in self.collectibles:
            del self.collectibles[collectible_id]
            for pos, items in self.world.items():
                for item in items:
                    if item[0] == "collectible" and item[1] == collectible_id:
                        items.remove(item)
                        break
            print(f"Player {player_id} collected item {collectible_id}")

    def execute(self, nr_player: int, dir: int):
        pos = self.players[nr_player][1]
        name = self.players[nr_player][0]
        new_pos = self.move_to(pos, dir)
        if self.obstacle_in_pos(new_pos):
            new_pos = pos
        self.players[nr_player] = [name, new_pos]
        self.world[pos].remove(["player", name, nr_player])
        self.world[new_pos].append(["player", name, nr_player])
        print(f"Player {nr_player} moved to {new_pos}")
        return new_pos
