import random
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, name, icon):
        super().__init__()

        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect(center = (10, 420))

        self.name = name
        self.icon = icon
        self.position = None
        self.property = []
        self.building = {"House": 0, "Hotel": 0}
        self.cash = 1500.00

    def roll_dice(self):
        return (random.randint(1, 6), random.randint(1, 6))
    
    def buy(self, properties):
        pass

    def receive_money(self, amount):
        self.cash += amount
    
    def give_money(self, amount):
        self.cash -= amount
    
