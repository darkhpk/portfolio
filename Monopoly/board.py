import pygame

class Board(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        WIDTH = 800
        HEIGHT = 600
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center = (WIDTH / 2, HEIGHT - 10))

        