import pygame
from stub.client_stub import ClientStub
from stub import UP, DOWN, LEFT, RIGHT

class Player(pygame.sprite.DirtySprite):
    def __init__(self, nr_player: int, pos_x: int, pos_y: int, size: int, *groups):
        super().__init__(*groups)
        self.my_id = nr_player
        self.size = size
        self.image = pygame.image.load('images/player_1.png') if nr_player == 0 else pygame.image.load('images/player_2.png')
        initial_size = self.image.get_size()
        size_rate = size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * size, pos_y * size), self.image.get_size())
        self.pos = [pos_x, pos_y]
        self.items_collected = 0

    def get_size(self):
        return self.new_size

    def get_id(self):
        return self.my_id

    def set_pos(self, pos):
        try:
            self.rect.x = pos[0] * self.size
            self.rect.y = pos[1] * self.size
            self.pos = pos
            self.dirty = 1  # Marcar como "sujo" para atualizar a renderização
            print(f"Player {self.my_id} pos updated to {self.pos}")
        except Exception as e:
            print(f"Error setting player position: {e}")

    def update(self, game: object, cs: ClientStub):
        if self.my_id != game.id:  # Verifica se é o jogador local
            return

        try:
            key = pygame.key.get_pressed()
            new_pos = self.pos
            if key[pygame.K_LEFT]:
                print(f"Player {self.my_id} moving left from {self.pos}")
                new_pos = cs.step(self.my_id, LEFT)
            if key[pygame.K_RIGHT]:
                print(f"Player {self.my_id} moving right from {self.pos}")
                new_pos = cs.step(self.my_id, RIGHT)
            if key[pygame.K_UP]:
                print(f"Player {self.my_id} moving up from {self.pos}")
                new_pos = cs.step(self.my_id, UP)
            if key[pygame.K_DOWN]:
                print(f"Player {self.my_id} moving down from {self.pos}")
                new_pos = cs.step(self.my_id, DOWN)
            self.set_pos(new_pos)
        except Exception as e:
            print(f"Error updating player position: {e}")

    def collect_item(self):
        self.items_collected += 1
        print(f"Items collected: {self.items_collected}")
