import pygame

class Collectible(pygame.sprite.DirtySprite):
    def __init__(self, x, y, size, image_path, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(image_path)
        initial_size = self.image.get_size()
        size_rate = size / initial_size[0]
        self.new_size = (int(initial_size[0] * size_rate), int(initial_size[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((x * size, y * size), self.image.get_size())
        self.pos = [x, y]
        self.dirty = 2
        self.id = id(self)  # Adiciona um identificador único para o coletável

    def get_id(self):
        return self.id

    def is_collected(self, player):
        return self.rect.colliderect(player.rect)
