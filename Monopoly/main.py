# -*- coding: utf-8 -*-

import pygame
import random

from pygame.locals import *

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BOARD_COLOR = (173, 216, 230)
TEXT_COLOR = (0, 0, 0)
                #   RED          GREEN         BLUE        YELLOW
PLAYER_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
CORNER_SIZE = 150
SIDE_SQUARE_SIZE = (SCREEN_WIDTH - 2 * CORNER_SIZE) // 9
CENTER_IMAGE_SIZE = 400
DICE_SIZE = 100

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Monopoly')

# Font
font = pygame.font.Font(None, 24)
dice_font = pygame.font.Font(None, 72)

# Player class
class Player:
    def __init__(self, color):
        self.color = color
        self.position = 0
        self.money = 1500
        self.properties = []
        self.jailed = False
        self.groups = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

class Square:
    def __init__(self, name):
        self.name = name
    
    def on_land(self, player):
        pass

class Property(Square):
    def __init__(self, name, price, rent, group):
        super().__init__(name)
        self.price = price
        self.rent = rent
        self.owner = None
        self.group = group
        self.house_price = self.price * 3
        self.hotel_price = self.house_price * 2
        self.building = {"house": 0, "hotel": 0}
    
    def on_land(self, player):
        group_list = []
        if self.owner is None:
            return self.offer_to_buy(player)
        elif self.owner != player:
            return self.pay_rent(player)
        elif self.owner == player:
            for k, v in player.groups.items():
                if v == groups[k]:
                    return self.buy_building(player)
                elif v < groups[k]:
                    return None
                     
    def offer_to_buy(self, player):
        return f"Do you want to buy \n{self.name} for £{self.price}?"
    
    def pay_rent(self, player):
        return f"Pay £{self.rent} rent to {self.owner.color}"

    def buy_building(self, player):
        return f"Do you want to buy a building for the price of £{self.house_price}"

class Chance(Square):
    def on_land(self, player):
        return "Draw a Chance card!"

class CommunityChest(Square):
    def on_land(self, player):
        return "Draw a Community Chest card!"

board = [
    Square("Go"), 
    Property("Mediterranean Avenue", 60, 2, 1), 
    CommunityChest("Community Chest"), 
    Property("Baltic Avenue", 60, 4, 1), 
    Square("Income Tax"), 
    Property("Reading Railroad", 200, 25, 9), 
    Property("Oriental Avenue", 100, 6, 2), 
    Chance("Chance"), 
    Property("Vermont Avenue", 100, 6, 2), 
    Property("Connecticut Avenue", 120, 8, 2), 
    Square("Jail"), 
    Property("St. Charles Place", 140, 10, 3), 
    Property("Electric Company", 150, 75, None), 
    Property("States Avenue", 140, 10, 3), 
    Property("Virginia Avenue", 160, 12, 3), 
    Property("Pennsylvania Railroad", 200, 25, 9), 
    Property("St. James Place", 180, 14, 4), 
    CommunityChest("Community Chest"), 
    Property("Tennessee Avenue", 180, 14, 4), 
    Property("New York Avenue", 200, 16, 4), 
    Square("Free Parking"), 
    Property("Kentucky Avenue", 220, 18, 5), 
    Chance("Chance"), 
    Property("Indiana Avenue", 220, 18, 5), 
    Property("Illinois Avenue", 240, 20, 5), 
    Property("B&O Railroad", 200, 25, 9), 
    Property("Atlantic Avenue", 260, 22, 6), 
    Property("Ventnor Avenue", 260, 22, 6), 
    Property("Water Works", 150, 75, None), 
    Property("Marvin Gardens", 280, 24, 6), 
    Square("Go to Jail"), 
    Property("Pacific Avenue", 300, 26, 7), 
    Property("North Carolina Avenue", 300, 26, 7), 
    CommunityChest("Community Chest"), 
    Property("Pennsylvania Avenue", 320, 28, 7), 
    Property("Short Line", 200, 25, 9), 
    Chance("Chance"), 
    Property("Park Place", 350, 35, 8), 
    Square("Luxury Tax"), 
    Property("Boardwalk", 400, 50, 8)
]

groups = {
    1: 2,
    2: 3,
    3: 3,
    4: 3,
    5: 3,
    6: 3,
    7: 3,
    8: 2,
    9: 4
}

def draw_text(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    line_spacing = -2

    font_height = font.size("Tg")[1]

    while text:
        i = 1

        if y + font_height > rect.bottom:
            break

        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1
        
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        
        surface.blit(image, (rect.left, y))
        y += font_height + line_spacing

        text = text[i:]
    return text

# Function to draw the board
def draw_board():
    screen.fill(BOARD_COLOR)

    # Draw the perimeter squares
    for i, square in enumerate(board):
        if i == 0:
            x, y = SCREEN_WIDTH - CORNER_SIZE, SCREEN_HEIGHT - CORNER_SIZE
            width, height = CORNER_SIZE, CORNER_SIZE
        elif i < 10:
            x = SCREEN_WIDTH - CORNER_SIZE - (i - 1) * SIDE_SQUARE_SIZE - SIDE_SQUARE_SIZE
            y = SCREEN_HEIGHT - CORNER_SIZE
            width, height = SIDE_SQUARE_SIZE, CORNER_SIZE
        elif i == 10:
            x, y = 0, SCREEN_HEIGHT - CORNER_SIZE
            width, height = CORNER_SIZE, CORNER_SIZE
        elif i < 20:
            x = 0
            y = SCREEN_HEIGHT - CORNER_SIZE - (i - 11) * SIDE_SQUARE_SIZE - SIDE_SQUARE_SIZE
            width, height = CORNER_SIZE, SIDE_SQUARE_SIZE
        elif i == 20:
            x, y = 0, 0
            width, height = CORNER_SIZE, CORNER_SIZE
        elif i < 30:
            x = CORNER_SIZE + (i - 21) * SIDE_SQUARE_SIZE
            y = 0
            width, height = SIDE_SQUARE_SIZE, CORNER_SIZE
        elif i == 30:
            x, y = SCREEN_WIDTH - CORNER_SIZE, 0
            width, height = CORNER_SIZE, CORNER_SIZE
        else:
            x = SCREEN_WIDTH - CORNER_SIZE
            y = CORNER_SIZE + (i - 31) * SIDE_SQUARE_SIZE
            width, height = CORNER_SIZE, SIDE_SQUARE_SIZE

        if isinstance(square, Property) and square.owner is not None:
            square_color = square.owner.color
        else:
            square_color = BOARD_COLOR
        
        if isinstance(square, Property) and square.building.values is not 0:
            for k, v in square.building.items():
                if square.building[k] >= 1:
                    house = f"House: {square.building[k]}"
                    house_surf = font.render(house, True, TEXT_COLOR)
                    screen.blit(house_surf, (x + 5, y + height // 2 + 10))
                


        pygame.draw.rect(screen, square_color, (x, y, width, height))
        pygame.draw.rect(screen, TEXT_COLOR, (x, y, width, height), 2)
        draw_text(screen, square.name, TEXT_COLOR, (x + 5, y + 5, width - 10, height // 2), font)
        if isinstance(square, Property):
            price_text = f"£{square.price}"
            price_surface = font.render(price_text, True, TEXT_COLOR)
            screen.blit(price_surface, (x + 5, y + height // 2 + 5))

    # Draw the center image
    console_text = f""
    center_x = (SCREEN_WIDTH - CENTER_IMAGE_SIZE) // 2
    center_y = (SCREEN_HEIGHT - CENTER_IMAGE_SIZE) // 2
    screen.blit(center_image, (center_x, center_y))
# Function to draw players
def draw_players(players):
    for player in players:
        if player.position == 0:
            x, y = SCREEN_WIDTH - CORNER_SIZE // 2, SCREEN_HEIGHT - CORNER_SIZE // 2
        elif player.position < 10:
            x = SCREEN_WIDTH - CORNER_SIZE - (player.position - 1) * SIDE_SQUARE_SIZE - SIDE_SQUARE_SIZE // 2
            y = SCREEN_HEIGHT - CORNER_SIZE // 2
        elif player.position == 10:
            x, y = CORNER_SIZE // 2, SCREEN_HEIGHT - CORNER_SIZE // 2
        elif player.position < 20:
            x = CORNER_SIZE // 2
            y = SCREEN_HEIGHT - CORNER_SIZE - (player.position - 11) * SIDE_SQUARE_SIZE - SIDE_SQUARE_SIZE // 2
        elif player.position == 20:
            x, y = CORNER_SIZE // 2, CORNER_SIZE // 2
        elif player.position < 30:
            x = CORNER_SIZE + (player.position - 21) * SIDE_SQUARE_SIZE + SIDE_SQUARE_SIZE // 2
            y = CORNER_SIZE // 2
        elif player.position == 30:
            x, y = SCREEN_WIDTH - CORNER_SIZE // 2, CORNER_SIZE // 2
        else:
            x = SCREEN_WIDTH - CORNER_SIZE // 2
            y = CORNER_SIZE + (player.position - 31) * SIDE_SQUARE_SIZE + SIDE_SQUARE_SIZE // 2

        pygame.draw.circle(screen, (0, 0, 0), (x, y), 17)
        pygame.draw.circle(screen, player.color, (x, y), 15)

def offer_to_buy(property, player):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
            elif event.type == KEYDOWN:
                if event.key == K_y:
                    player.money -= property.price
                    player.properties.append(property)
                    property.owner = player
                    running = False
                elif event.key == K_n:
                    running = False
        
        screen.fill((255, 255, 255))
        text = font.render(f"Do you want to buy {property.name} for £{property.price}? (Y/N)", True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()
    
    return True

def buy_building(property, player):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
            elif event.type == KEYDOWN:
                if event.key == K_y:
                    if property.building["house"] < 4:
                        player.money -= property.house_price
                        property.building["house"] += 1
                        running = False
                    elif property.building["house"] == 4:
                        player.money -= property.hotel_price
                        property.building["house"] -= 1
                        property.building["hotel"] += 1
                        running = False
                elif event.key == K_n:
                    running = False
        
        screen.fill((255, 255, 255))
        text = font.render(f"Houses: {property.building['house']}\n Hotels: {property.building['hotel']}\n Do you want to buy a building for £{property.house_price if property.building['house'] < 4 else property.hotel_price}? (Y/N)", True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()
    
    return True

def pay_rent(property, player):
    running = True
    while running:
        screen.fill((255, 255, 255))
        text = font.render(f"Pay £{property.rent} rent to {property.owner.color}. Press Y to pay.", True, TEXT_COLOR)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
            elif event.type == KEYDOWN:
                if event.key == K_y:
                    if player.money >= property.rent:
                        player.money -= property.rent
                        player.properties.append(property)
                        property.owner.money += property.rent
                        running = False
                    else:
                        text = font.render(f"You don't have enough money to pay rent, you go to jail!", True, TEXT_COLOR)
                        running = False
        
        
        
        screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()

    return True

def trade_properties(player, other_player):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
            elif event.type == KEYDOWN:
                if event.key == K_t:
                    property_to_trade = choose_property(player, "Offer")
                    if property_to_trade:
                        property_to_receive = choose_property(other_player, "Receive")
                        if property_to_receive:
                            player.properties.remove(property_to_trade)
                            other_player.properties.append(property_to_trade)
                            other_player.properties.remove(property_to_receive)
                            player.properties.append(property_to_receive)
                            property_to_trade.owner = other_player
                            property_to_receive.owner = player
                            running = False
                elif event.key == K_ESCAPE:
                    running = False
    
        screen.fill((255, 255, 255))
        text = font.render(f"Press 'T' to trade properties with {other_player.color} or 'ESC' to cancel.", True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()
    return True

def buy_property_from_player(player, other_player):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
            elif event.type == KEYDOWN:
                if event.key == K_b:
                    property_to_buy = choose_property(other_player, "Buy")
                    if property_to_buy:
                        if player.money >= property_to_buy.price:
                            player.money -= property_to_buy.price
                            other_player.money += property_to_buy.price
                            player.properties.append(property_to_buy)
                            other_player.properties.remove(property_to_buy)
                            property_to_buy.owner = player
                            running = False
                elif event.key == K_ESCAPE:
                    running = False
        
        screen.fill((255, 255, 255))
        text = font.render(f"Press 'B' to buy a property from {other_player} or 'ESC' to cancel.", True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()
    return True

def sell_property_to_bank(player):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
            elif event.type == KEYDOWN:
                if event.key == K_s:
                    property_to_sell = choose_property(player, "Sell")
                    if property_to_sell:
                        player.money += property_to_sell // 2
                        player.properties.remove(property_to_sell)
                        property_to_sell.owner = None
                        running = False
                    elif event.key == K_ESCAPE:
                        running = False
        
        screen.fill((255, 255, 255))
        text = font.render(f"Press 'S' to sell a property to the bank or 'ESC' to cancel.", True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()
    return True

def choose_property(player, action):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return None
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    return player.properties[0] if len(player.properties) > 0 else None
                elif event.key == K_2:
                    return player.properties[1] if len(player.properties) > 1 else None
                elif event.key == K_3:
                    return player.properties[2] if len(player.properties) > 2 else None
                elif event.key == K_4:
                    return player.properties[3] if len(player.properties) > 3 else None
                elif event.key == K_ESCAPE:
                    return None
        
        screen.fill((255, 255, 255))
        text = font.render(f"Press 1-4 to {action} a property or 'ESC' to cancel.", True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()
    return True
# Main function
def main():
    # Create players
    players = [Player(color) for color in PLAYER_COLORS]
    current_player = 0
    dice_roll_1 = 0
    dice_roll_2 = 0

    # Main game loop
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play= False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Roll dice and move player
                    dice_roll_1 = random.randint(1, 6)
                    dice_roll_2 = random.randint(1, 6)
                    if players[current_player].jailed:
                        if dice_roll_1 == dice_roll_2:
                            players[current_player].jailed = False
                            players[current_player].position = (players[current_player].position + (dice_roll_1 + dice_roll_2)) % 40
                            current_square = board[players[current_player].position]
                            result = current_square.on_land(players[current_player])
                        else:
                            pass
                    else:
                        players[current_player].position = (players[current_player].position + (dice_roll_1 + dice_roll_2)) % 40
                        current_square = board[players[current_player].position]
                        result = current_square.on_land(players[current_player])

                    if isinstance(current_square, Property):
                        if current_square.owner is None:
                            play = offer_to_buy(current_square, players[current_player])
                        elif current_square.owner != players[current_player]:
                            play = pay_rent(current_square, players[current_player])
                        elif current_square.owner == players[current_player]:
                            play = buy_building(current_square, players[current_player])
                    elif isinstance(current_square, (Chance, CommunityChest)):
                        play = draw_card(current_square)
                    elif isinstance(current_square, Square):
                        if current_square.name == "Go":
                            players[current_player].money += 200
                        elif current_square.name == "Income Tax":
                            players[current_player].money -= 200
                        elif current_square.name == "Jail":
                            pass
                        elif current_square.name == "Go to Jail":
                            players[current_player].position = 10
                        elif current_square.name == "Luxury Tax":
                            players[current_player].money -= 100
                        
                    # End turn and switch to next player
                    current_player = (current_player + 1) % len(players)
                elif event.key == K_t:
                    other_player = players[(current_player + 1) % len(players)]
                    running = trade_properties(players[current_player], other_player)
                elif event.key == K_b:
                    other_player = players[(current_player + 1) % len(players)]
                    running = buy_property_from_player(players[current_player], other_player)
                elif event.key == K_s:
                    running = sell_property_to_bank(players[current_player])


                    

        # Update game logic here

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw board and players
        draw_board()
        draw_players(players)

        if dice_roll_1 and dice_roll_2:
            dice1_text = dice_font.render(str(dice_roll_1), True, TEXT_COLOR)
            dice2_text = dice_font.render(str(dice_roll_2), True, TEXT_COLOR)
            screen.blit(dice1_text, (SCREEN_WIDTH // 2 - DICE_SIZE // 2, SCREEN_HEIGHT // 2 + DICE_SIZE + DICE_SIZE))
            screen.blit(dice2_text, (SCREEN_WIDTH // 2 + DICE_SIZE // 2, SCREEN_HEIGHT // 2 + DICE_SIZE + DICE_SIZE))

        player_1_info = font.render("Player 1:", True, TEXT_COLOR)
        player_1_money = font.render(f"Money:£{players[0].money}", True, TEXT_COLOR)

        player_2_info = font.render("Player 2:", True, TEXT_COLOR)
        player_2_money = font.render(f"Money:£{players[1].money}", True, TEXT_COLOR)

        player_3_info = font.render("Player 3:", True, TEXT_COLOR)
        player_3_money = font.render(f"Money:£{players[2].money}", True, TEXT_COLOR)

        player_4_info = font.render("Player 4:", True, TEXT_COLOR)
        player_4_money = font.render(f"Money:£{players[3].money}", True, TEXT_COLOR)

        screen.blit(player_1_info, (SCREEN_WIDTH // 2 - 300, (SCREEN_HEIGHT // 2) // 2 - 100))
        screen.blit(player_1_money,(SCREEN_WIDTH // 2 - 300, (SCREEN_HEIGHT // 2) // 2 - 75))
        screen.blit(player_2_info, (SCREEN_WIDTH // 2 + 200, (SCREEN_HEIGHT // 2) // 2 - 100))
        screen.blit(player_2_money,(SCREEN_WIDTH // 2 + 200, (SCREEN_HEIGHT // 2) // 2 - 75))
        screen.blit(player_3_info, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 250))
        screen.blit(player_3_money,(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 275))
        screen.blit(player_4_info, (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 250))
        screen.blit(player_4_money,(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 275))
        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

def draw_card(square):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    running = False
        
        screen.fill((255, 255, 255))
        text = font.render(square.on_land(None), True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()

    return True

# Run the game
if __name__ == '__main__':
    main()
