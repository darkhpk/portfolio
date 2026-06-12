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

# Load center image
center_image = pygame.image.load('media/center_image.jpeg')
center_image = pygame.transform.scale(center_image, (CENTER_IMAGE_SIZE, CENTER_IMAGE_SIZE))

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

    # Calculate side space and distribute extra pixels
    side_space = SCREEN_WIDTH - 2 * CORNER_SIZE
    base_square_size = side_space // 9
    extra_pixels = side_space - (base_square_size * 9)

    # Draw the perimeter squares
    for i, square in enumerate(board):
        if i == 0:
            x, y = SCREEN_WIDTH - CORNER_SIZE, SCREEN_HEIGHT - CORNER_SIZE
            width, height = CORNER_SIZE, CORNER_SIZE
        elif i < 10:
            # Bottom row (going left)
            square_width = base_square_size + (1 if i <= extra_pixels else 0)
            x = SCREEN_WIDTH - CORNER_SIZE
            for j in range(1, i):
                x -= base_square_size + (1 if j <= extra_pixels else 0)
            x -= square_width
            y = SCREEN_HEIGHT - CORNER_SIZE
            width, height = square_width, CORNER_SIZE
        elif i == 10:
            x, y = 0, SCREEN_HEIGHT - CORNER_SIZE
            width, height = CORNER_SIZE, CORNER_SIZE
        elif i < 20:
            # Left column (going up)
            square_height = base_square_size + (1 if (i-10) <= extra_pixels else 0)
            x = 0
            y = SCREEN_HEIGHT - CORNER_SIZE
            for j in range(11, i):
                y -= base_square_size + (1 if (j-10) <= extra_pixels else 0)
            y -= square_height
            width, height = CORNER_SIZE, square_height
        elif i == 20:
            x, y = 0, 0
            width, height = CORNER_SIZE, CORNER_SIZE
        elif i < 30:
            # Top row (going right)
            square_width = base_square_size + (1 if (i-20) <= extra_pixels else 0)
            x = CORNER_SIZE
            for j in range(21, i):
                x += base_square_size + (1 if (j-20) <= extra_pixels else 0)
            y = 0
            width, height = square_width, CORNER_SIZE
        elif i == 30:
            x, y = SCREEN_WIDTH - CORNER_SIZE, 0
            width, height = CORNER_SIZE, CORNER_SIZE
        else:
            # Right column (going down)
            square_height = base_square_size + (1 if (i-30) <= extra_pixels else 0)
            x = SCREEN_WIDTH - CORNER_SIZE
            y = CORNER_SIZE
            for j in range(31, i):
                y += base_square_size + (1 if (j-30) <= extra_pixels else 0)
            width, height = CORNER_SIZE, square_height

        if isinstance(square, Property) and square.owner is not None:
            square_color = square.owner.color
        else:
            square_color = BOARD_COLOR
        
        if isinstance(square, Property) and (square.building["house"] > 0 or square.building["hotel"] > 0):
            if square.building["house"] >= 1:
                house = f"House: {square.building['house']}"
                house_surf = font.render(house, True, TEXT_COLOR)
                screen.blit(house_surf, (x + 5, y + height // 2 + 10))
            if square.building["hotel"] >= 1:
                hotel = f"Hotel: {square.building['hotel']}"
                hotel_surf = font.render(hotel, True, TEXT_COLOR)
                screen.blit(hotel_surf, (x + 5, y + height // 2 + 25))
                


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
    # Calculate side space and distribute extra pixels (same as board)
    side_space = SCREEN_WIDTH - 2 * CORNER_SIZE
    base_square_size = side_space // 9
    extra_pixels = side_space - (base_square_size * 9)
    
    for idx, player in enumerate(players):
        pos = player.position
        
        if pos == 0:
            x, y = SCREEN_WIDTH - CORNER_SIZE // 2, SCREEN_HEIGHT - CORNER_SIZE // 2
        elif pos < 10:
            # Bottom row (going left)
            square_width = base_square_size + (1 if pos <= extra_pixels else 0)
            x = SCREEN_WIDTH - CORNER_SIZE
            for j in range(1, pos):
                x -= base_square_size + (1 if j <= extra_pixels else 0)
            x -= square_width // 2
            y = SCREEN_HEIGHT - CORNER_SIZE // 2
        elif pos == 10:
            x, y = CORNER_SIZE // 2, SCREEN_HEIGHT - CORNER_SIZE // 2
        elif pos < 20:
            # Left column (going up)
            square_height = base_square_size + (1 if (pos-10) <= extra_pixels else 0)
            x = CORNER_SIZE // 2
            y = SCREEN_HEIGHT - CORNER_SIZE
            for j in range(11, pos):
                y -= base_square_size + (1 if (j-10) <= extra_pixels else 0)
            y -= square_height // 2
        elif pos == 20:
            x, y = CORNER_SIZE // 2, CORNER_SIZE // 2
        elif pos < 30:
            # Top row (going right)
            square_width = base_square_size + (1 if (pos-20) <= extra_pixels else 0)
            x = CORNER_SIZE
            for j in range(21, pos):
                x += base_square_size + (1 if (j-20) <= extra_pixels else 0)
            x += square_width // 2
            y = CORNER_SIZE // 2
        elif pos == 30:
            x, y = SCREEN_WIDTH - CORNER_SIZE // 2, CORNER_SIZE // 2
        else:
            # Right column (going down)
            square_height = base_square_size + (1 if (pos-30) <= extra_pixels else 0)
            x = SCREEN_WIDTH - CORNER_SIZE // 2
            y = CORNER_SIZE
            for j in range(31, pos):
                y += base_square_size + (1 if (j-30) <= extra_pixels else 0)
            y += square_height // 2
        
        # Offset multiple players on same square
        offset = 10
        if idx == 1:
            x += offset
        elif idx == 2:
            y += offset
        elif idx == 3:
            x -= offset

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
                    if property.group is not None:
                        player.groups[property.group] += 1
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
                            # Update groups
                            if property_to_trade.group is not None:
                                player.groups[property_to_trade.group] -= 1
                                other_player.groups[property_to_trade.group] += 1
                            if property_to_receive.group is not None:
                                other_player.groups[property_to_receive.group] -= 1
                                player.groups[property_to_receive.group] += 1
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
                            # Update groups
                            if property_to_buy.group is not None:
                                other_player.groups[property_to_buy.group] -= 1
                                player.groups[property_to_buy.group] += 1
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
                        player.money += property_to_sell.price // 2
                        player.properties.remove(property_to_sell)
                        property_to_sell.owner = None
                        # Update groups
                        if property_to_sell.group is not None:
                            player.groups[property_to_sell.group] -= 1
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
def animate_dice():
    """Animate dice rolling"""
    animation_frames = 20
    for frame in range(animation_frames):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, 0, 0
        
        screen.fill((255, 255, 255))
        
        # Random dice values during animation
        temp_dice1 = random.randint(1, 6)
        temp_dice2 = random.randint(1, 6)
        
        # Draw animated dice
        dice1_text = dice_font.render(str(temp_dice1), True, TEXT_COLOR)
        dice2_text = dice_font.render(str(temp_dice2), True, TEXT_COLOR)
        screen.blit(dice1_text, (SCREEN_WIDTH // 2 - DICE_SIZE, SCREEN_HEIGHT // 2 - DICE_SIZE // 2))
        screen.blit(dice2_text, (SCREEN_WIDTH // 2 + DICE_SIZE // 2, SCREEN_HEIGHT // 2 - DICE_SIZE // 2))
        
        rolling_text = font.render("Rolling dice...", True, TEXT_COLOR)
        screen.blit(rolling_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 100))
        
        pygame.display.flip()
        pygame.time.delay(50)
    
    # Final dice values
    final_dice1 = random.randint(1, 6)
    final_dice2 = random.randint(1, 6)
    
    # Show final result
    for _ in range(30):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, 0, 0
        
        screen.fill((255, 255, 255))
        dice1_text = dice_font.render(str(final_dice1), True, TEXT_COLOR)
        dice2_text = dice_font.render(str(final_dice2), True, TEXT_COLOR)
        screen.blit(dice1_text, (SCREEN_WIDTH // 2 - DICE_SIZE, SCREEN_HEIGHT // 2 - DICE_SIZE // 2))
        screen.blit(dice2_text, (SCREEN_WIDTH // 2 + DICE_SIZE // 2, SCREEN_HEIGHT // 2 - DICE_SIZE // 2))
        
        result_text = font.render(f"You rolled: {final_dice1 + final_dice2}", True, TEXT_COLOR)
        screen.blit(result_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 100))
        
        pygame.display.flip()
        pygame.time.delay(30)
    
    return True, final_dice1, final_dice2

# Main function
def main():
    # Create players
    players = [Player(color) for color in PLAYER_COLORS]
    current_player = 0
    dice_roll_1 = 0
    dice_roll_2 = 0
    player_moved = False  # Track if player has moved this turn
    action_message = ""  # Message to display

    # Main game loop
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play= False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player_moved:
                    # Roll dice with animation and move player
                    play, dice_roll_1, dice_roll_2 = animate_dice()
                    if not play:
                        break
                    
                    if players[current_player].jailed:
                        if dice_roll_1 == dice_roll_2:
                            players[current_player].jailed = False
                            players[current_player].position = (players[current_player].position + (dice_roll_1 + dice_roll_2)) % 40
                            player_moved = True
                            action_message = "Escaped jail! Press B to buy, R to pay rent, H for building, or N for next turn"
                        else:
                            action_message = "Still in jail. Press N for next turn"
                            player_moved = True
                    else:
                        players[current_player].position = (players[current_player].position + (dice_roll_1 + dice_roll_2)) % 40
                        player_moved = True
                        current_square = board[players[current_player].position]
                        
                        # Set action message based on square type
                        if isinstance(current_square, Property):
                            if current_square.owner is None:
                                action_message = f"Landed on {current_square.name}. Press B to buy or N for next turn"
                            elif current_square.owner != players[current_player]:
                                action_message = f"Landed on {current_square.name} (owned). Press R to pay rent"
                            else:
                                action_message = f"Landed on your property. Press H to build or N for next turn"
                        elif isinstance(current_square, (Chance, CommunityChest)):
                            play = draw_card(current_square)
                            action_message = "Press N for next turn"
                        elif isinstance(current_square, Square):
                            if current_square.name == "Go":
                                players[current_player].money += 200
                                action_message = "Landed on Go! +£200. Press N for next turn"
                            elif current_square.name == "Income Tax":
                                players[current_player].money -= 200
                                action_message = "Income Tax: -£200. Press N for next turn"
                            elif current_square.name == "Jail":
                                action_message = "Just visiting. Press N for next turn"
                            elif current_square.name == "Go to Jail":
                                players[current_player].position = 10
                                players[current_player].jailed = True
                                action_message = "Go to Jail! Press N for next turn"
                            elif current_square.name == "Luxury Tax":
                                players[current_player].money -= 100
                                action_message = "Luxury Tax: -£100. Press N for next turn"
                            elif current_square.name == "Free Parking":
                                action_message = "Free Parking. Press N for next turn"
                            else:
                                action_message = "Press N for next turn"
                
                elif event.key == pygame.K_b and player_moved:
                    # Buy property
                    current_square = board[players[current_player].position]
                    if isinstance(current_square, Property) and current_square.owner is None:
                        play = offer_to_buy(current_square, players[current_player])
                        action_message = "Press N for next turn"
                    else:
                        action_message = "Cannot buy this property. Press N for next turn"
                
                elif event.key == pygame.K_r and player_moved:
                    # Pay rent
                    current_square = board[players[current_player].position]
                    if isinstance(current_square, Property) and current_square.owner is not None and current_square.owner != players[current_player]:
                        play = pay_rent(current_square, players[current_player])
                        action_message = "Press N for next turn"
                    else:
                        action_message = "No rent to pay. Press N for next turn"
                
                elif event.key == pygame.K_h and player_moved:
                    # Build house/hotel
                    current_square = board[players[current_player].position]
                    if isinstance(current_square, Property) and current_square.owner == players[current_player]:
                        # Check if player owns all properties in group
                        if current_square.group is not None and players[current_player].groups[current_square.group] == groups[current_square.group]:
                            play = buy_building(current_square, players[current_player])
                            action_message = "Press N for next turn"
                        else:
                            action_message = "You need to own all properties in the group. Press N for next turn"
                    else:
                        action_message = "Cannot build here. Press N for next turn"
                
                elif event.key == pygame.K_n and player_moved:
                    # Next turn
                    current_player = (current_player + 1) % len(players)
                    player_moved = False
                    dice_roll_1 = 0
                    dice_roll_2 = 0
                    action_message = f"Player {current_player + 1}'s turn. Press SPACE to roll dice"
                elif event.key == K_t and not player_moved:
                    other_player = players[(current_player + 1) % len(players)]
                    play = trade_properties(players[current_player], other_player)
                elif event.key == K_p and not player_moved:
                    other_player = players[(current_player + 1) % len(players)]
                    play = buy_property_from_player(players[current_player], other_player)
                elif event.key == K_s and not player_moved:
                    play = sell_property_to_bank(players[current_player])


                    

        # Update game logic here

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw board and players
        draw_board()
        draw_players(players)

        # Display current player turn
        turn_text = font.render(f"Player {current_player + 1}'s Turn", True, TEXT_COLOR)
        screen.blit(turn_text, (SCREEN_WIDTH // 2 - 70, 20))
        
        # Display action message
        if action_message:
            msg_lines = []
            if len(action_message) > 80:
                words = action_message.split()
                current_line = ""
                for word in words:
                    if len(current_line + word) < 80:
                        current_line += word + " "
                    else:
                        msg_lines.append(current_line)
                        current_line = word + " "
                msg_lines.append(current_line)
            else:
                msg_lines = [action_message]
            
            for idx, line in enumerate(msg_lines):
                msg_surf = font.render(line, True, (255, 0, 0))
                screen.blit(msg_surf, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 50 + idx * 25))

        if dice_roll_1 and dice_roll_2:
            dice1_text = dice_font.render(str(dice_roll_1), True, TEXT_COLOR)
            dice2_text = dice_font.render(str(dice_roll_2), True, TEXT_COLOR)
            screen.blit(dice1_text, (SCREEN_WIDTH // 2 - DICE_SIZE, SCREEN_HEIGHT // 2 + 50))
            screen.blit(dice2_text, (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 50))

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
        
        # Controls help text
        help_text = font.render("SPACE: Roll | B: Buy | R: Rent | H: Build | N: Next | T: Trade | P: Buy from player | S: Sell", True, TEXT_COLOR)
        screen.blit(help_text, (50, SCREEN_HEIGHT - 30))
        
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
