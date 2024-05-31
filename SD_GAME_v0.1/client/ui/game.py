import pygame
import random
import player7
import player8
import wall
from .collectible import Collectible
from stub.client_stub import ClientStub

class Game(object):
    def __init__(self, cs: ClientStub, size: int):
        self.cs = cs
        self.id = ""
        nr_x = self.cs.get_nr_quad_x()
        nr_y = self.cs.get_nr_quad_y()
        self.width, self.height = nr_x * size, nr_y * size
        self.max_x, self.max_y = nr_x, nr_y
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("grid game")
        self.clock = pygame.time.Clock()
        self.grid_size = size
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        self.draw_grid(self.width, self.height, self.grid_size, (0, 0, 0))
        pygame.display.update()
        self.collectibles = pygame.sprite.LayeredDirty()
        self.wall_positions = []  # Lista para armazenar posições das paredes
        self.players = pygame.sprite.LayeredDirty()  # Inicializar a lista de jogadores aqui
        self.local_player = None

    def draw_grid(self, width: int, height: int, size: int, colour: tuple):
        for pos in range(0, height, size):
            pygame.draw.line(self.screen, colour, (0, pos), (width, pos))
        for pos in range(0, width, size):
            pygame.draw.line(self.screen, colour, (pos, 0), (pos, height))

    def create_player(self, size: int) -> None:
        try:
            name = input("What is your name?")
            (self.id, pos) = self.cs.set_player(name)
            print("Player ", name, " created with id: ", self.id)
            self.local_player = player7.Player(self.id, pos[0], pos[1], size, self.players)
            self.players.add(self.local_player)
        except Exception as e:
            print(f"Error creating player: {e}")

    def create_walls(self, size: int):
        try:
            self.walls = pygame.sprite.Group()
            walls = self.cs.get_walls()
            for wl in walls.values():
                (x, y) = wl[1]
                self.wall_positions.append((x, y))  # Armazena a posição da parede
                w = wall.Wall(0, x, y, size, self.walls)
                self.walls.add(w)
        except Exception as e:
            print(f"Error creating walls: {e}")

    def create_collectibles(self, size: int, num_collectibles: int):
        try:
            for _ in range(num_collectibles):
                while True:
                    x = random.randint(0, self.max_x - 1)
                    y = random.randint(0, self.max_y - 1)
                    if (x, y) not in self.wall_positions:
                        self.collectibles.add(Collectible(x, y, size, "images/bag.png", self.collectibles))
                        break
        except Exception as e:
            print(f"Error creating collectibles: {e}")

    def start_game(self) -> bool:
        try:
            return bool(self.cs.execute_start_game())
        except Exception as e:
            print(f"Error starting game: {e}")
            return False

    def get_objects(self, size):
        try:
            objects = self.cs.get_objects()
            print("Objects:", objects)

            players = objects["players"]
            collectibles = objects["collectibles"]

            for id, player_data in players.items():
                if int(id) == self.id:
                    self.local_player.set_pos(player_data[1])
                else:
                    player_found = False
                    for player in self.players:
                        if player.get_id() == int(id):
                            player.set_pos(player_data[1])
                            player_found = True
                            break
                    if not player_found:
                        player = player8.Player(int(id), player_data[1][0], player_data[1][1], size, self.players)
                        self.players.add(player)

            self.collectibles.empty()
            for cid, pos in collectibles.items():
                collectible = Collectible(pos[0], pos[1], size, "images/bag.png", self.collectibles)
                self.collectibles.add(collectible)
        except Exception as e:
            print(f"Error getting objects: {e}")

    def update_objects(self):
        try:
            objects = self.cs.get_objects()
            print("objects: ", objects)

            players = objects["players"]
            collectibles = objects["collectibles"]

            for id, player_data in players.items():
                for player in self.players:
                    if player.get_id() == int(id):
                        player.set_pos(player_data[1])
                        break
                else:
                    new_player = player8.Player(int(id), player_data[1][0], player_data[1][1], self.grid_size, self.players)
                    self.players.add(new_player)

            self.collectibles.empty()
            for cid, pos in collectibles.items():
                collectible = Collectible(pos[0], pos[1], self.grid_size, "images/bag.png", self.collectibles)
                self.collectibles.add(collectible)
        except Exception as e:
            print(f"Error updating objects: {e}")

    def collect_item(self, player_id: int, collectible_id: int):
        try:
            if collectible_id in self.collectibles:
                del self.collectibles[collectible_id]
                # Remove do mundo
                for pos, items in self.world.items():
                    for item in items:
                        if item[0] == "collectible" and item[1] == collectible_id:
                            items.remove(item)
                            break
                print(f"Player {player_id} collected item {collectible_id}")
        except Exception as e:
            print(f"Error collecting item: {e}")

    def run(self):
        try:
            self.create_walls(self.grid_size)
            self.create_collectibles(self.grid_size, 10)  # Número de colecionáveis
            self.walls.draw(self.screen)
            self.walls.update()
            self.create_player(self.grid_size)
            end = False
            if not self.start_game():
                raise Exception("Failed to start game.")
            self.get_objects(self.grid_size)

            frame_count = 0  # Adicionando um contador de quadros

            while not end:
                self.clock.tick(30)
                frame_count += 1  # Incrementa o contador a cada quadro

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end = True
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        end = True

                self.players.update(self, self.cs)

                if frame_count % 5 == 0:
                    self.update_objects()

                for collectible in self.collectibles:
                    if collectible.is_collected(self.local_player):
                        self.collectibles.remove(collectible)
                        self.local_player.collect_item()
                        # Envia a informação ao servidor
                        self.cs.collect_item(self.local_player.get_id(), collectible.get_id())

                rects = self.players.draw(self.screen)
                self.collectibles.draw(self.screen)
                self.draw_grid(self.width, self.height, self.grid_size, (0, 0, 0))
                pygame.display.update(rects)
                self.players.clear(self.screen, self.background)
                self.collectibles.clear(self.screen, self.background)
        except Exception as e:
            print(f"Error during game run: {e}")
        finally:
            pygame.quit()
