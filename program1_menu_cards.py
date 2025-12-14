import pygame
import random

# COLORS
WHITE = (255, 255, 255)
RED = (255, 127, 127)
PINK = (255, 182, 193)
BLACK = (0, 0, 0)
LIGHT_PINK = (255, 220, 210)
LIGHT_RED = (255, 145, 145)
DARK_PINK = (255, 105, 180)

# Fonts will be initialized in functions
font_large = None
font_medium = None
font_small = None
menu_font = None
button_font = None

class Card:
    def __init__(self, x, y, number, color=WHITE):
        self.x = x
        self.y = y
        self.width = 150
        self.height = 300
        self.number = number
        self.color = color
        self.clicked = False
        self.over_color = LIGHT_PINK
        self.is_hovered = False
        self.show_value = False
        self.target_x = x
        self.target_y = y
        self.is_moving = False

    def draw(self, screen):
        if self.clicked:
            card_color = LIGHT_PINK
            self.show_value = True
        elif self.is_hovered:
            card_color = self.over_color
        else:
            card_color = self.color

        pygame.draw.rect(screen, card_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height), 2)
        
        if self.show_value or self.clicked:
            number_text = font_large.render(str(self.number), True, RED)
            text_rect = number_text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
            screen.blit(number_text, text_rect)
        else:
            hidden_text = font_large.render("?", True, RED)
            text_rect = hidden_text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
            screen.blit(hidden_text, text_rect)
        
        heart_points = [
            (self.x + self.width//2, self.y + 40),
            (self.x + self.width//2 - 15, self.y + 30),
            (self.x + self.width//2 - 30, self.y + 40),
            (self.x + self.width//2, self.y + 70),
            (self.x + self.width//2 + 30, self.y + 40),
            (self.x + self.width//2 + 15, self.y + 30),
            (self.x + self.width//2, self.y + 40)
        ]
        pygame.draw.polygon(screen, RED, heart_points)
    
    def is_clicked(self, pos):
        x, y = pos
        if (self.x <= x <= self.x + self.width and 
            self.y <= y <= self.y + self.height):
            if not any(card.clicked for card in cards if card != self):
                self.clicked = True
                self.show_value = True
                for card in cards:
                    if card != self:
                        card.show_value = False
                return True
        return False
    
    def check_hover(self, pos):
        if any(card.clicked for card in cards):
            self.is_hovered = False
            return False
            
        x, y = pos
        self.is_hovered = (self.x <= x <= self.x + self.width and 
                           self.y <= y <= self.y + self.height)
        return self.is_hovered
    
    def update(self):
        if self.is_moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            if abs(dx) < 1 and abs(dy) < 1:
                self.x = self.target_x
                self.y = self.target_y
                self.is_moving = False
            else:
                self.x += dx * 0.2
                self.y += dy * 0.2

def init_fonts():
    """Initialize fonts once"""
    global font_large, font_medium, font_small, menu_font, button_font
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)
    menu_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 42)

def draw_background(screen):
    screen.fill(RED)
    for y in range(100, 500):
        pygame.draw.line(screen, PINK, (0, y), (800, y))
    
    try:
        logo_image = pygame.image.load("kiffy1.png")
        logo_image = pygame.transform.scale(logo_image, (180, 180))
        screen.blit(logo_image, (-25, -35))
    except:
        pass
    
    title_text = font_large.render("Kiffy's Valentine Gift <3", True, WHITE)
    screen.blit(title_text, (120, 30))

def draw_continue_button(screen, hover):
    button_rect = pygame.Rect(300, 470, 200, 50)
    button_color = LIGHT_PINK if hover else WHITE
    
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, RED, button_rect, 3, border_radius=10)
    
    continue_text = font_medium.render("Continue", True, RED)
    text_rect = continue_text.get_rect(center=button_rect.center)
    screen.blit(continue_text, text_rect)
    
    return button_rect

def show_menu():
    """Show main menu - returns 'start' or 'exit'"""
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Kiffy's Valentine Gift <3")
    clock = pygame.time.Clock()
    
    # Initialize fonts for this module
    init_fonts()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        start_rect = pygame.Rect(300, 450, 200, 60)
        exit_rect = pygame.Rect(300, 510, 200, 60)
        start_hover = start_rect.collidepoint(mouse_pos)
        exit_hover = exit_rect.collidepoint(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_hover:
                        return "start"
                    elif exit_hover:
                        return "exit"
        
        screen.fill(RED)
        for y in range(100, 500):
            pygame.draw.line(screen, PINK, (0, y), (800, y))
        
        try:
            logo = pygame.image.load("kiffy1.png")
            logo = pygame.transform.scale(logo, (300, 300))
            screen.blit(logo, (250, 50))
        except:
            pass
        
        title = menu_font.render("Kiffy's Valentine Gift", True, WHITE)
        screen.blit(title, (400 - title.get_width()//2, 270))
        
        screen.blit(font_medium.render("Mechanics: ", True, RED), (100, 325))
        screen.blit(font_medium.render("1. Pick a card for your budget", True, WHITE), (100, 350))
        screen.blit(font_medium.render("2. Buy gifts for your valentine", True, WHITE), (100, 380))
        screen.blit(font_medium.render("3. Don't spend outside your budget!", True, WHITE), (100, 410))
        
        start_color = LIGHT_PINK if start_hover else WHITE
        pygame.draw.rect(screen, start_color, start_rect, border_radius=15)
        pygame.draw.rect(screen, RED, start_rect, 3, border_radius=15)
        start_text = button_font.render("START", True, RED)
        screen.blit(start_text, start_text.get_rect(center=start_rect.center))
        
        exit_color = LIGHT_PINK if exit_hover else WHITE
        pygame.draw.rect(screen, exit_color, exit_rect, border_radius=15)
        pygame.draw.rect(screen, RED, exit_rect, 3, border_radius=15)
        exit_text = button_font.render("EXIT", True, RED)
        screen.blit(exit_text, exit_text.get_rect(center=exit_rect.center))
        
        pygame.display.flip()
        clock.tick(60)

def run_card_selection():
    """Run card selection game - returns selected budget amount or None if went back"""
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pick Your Budget!")
    clock = pygame.time.Clock()
    
    # Initialize fonts
    init_fonts()
    
    budgets = [400, 500, 600]
    random.shuffle(budgets)
    
    global cards
    cards = [
        Card(100, 150, f"{budgets[0]}"),
        Card(325, 150, f"{budgets[1]}"),
        Card(550, 150, f"{budgets[2]}")
    ]
    
    continue_hover = False
    continue_button_rect = None
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if continue_button_rect and continue_button_rect.collidepoint(mouse_pos):
                        for card in cards:
                            if card.clicked:
                                budget_str = card.number.replace("₱", "")
                                try:
                                    return int(budget_str)
                                except:
                                    return 0
                    else:
                        for card in cards:
                            card.is_clicked(mouse_pos)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    positions = [(100, 150), (325, 150), (550, 150)]
                    random.shuffle(positions)
                    for i, card in enumerate(cards):
                        card.target_x, card.target_y = positions[i]
                        card.is_moving = True
                        if card.clicked:
                            card.clicked = True
                            card.show_value = True
                elif event.key == pygame.K_ESCAPE:
                    return None
        
        for card in cards:
            card.update()
            card.check_hover(mouse_pos)
        
        show_continue = any(card.clicked for card in cards)
        continue_hover = False
        
        draw_background(screen)
        for card in cards:
            card.draw(screen)
        
        if show_continue:
            continue_button_rect = draw_continue_button(screen, continue_hover)
            continue_hover = continue_button_rect.collidepoint(mouse_pos)
            continue_button_rect = draw_continue_button(screen, continue_hover)
        
        instructions = font_small.render("Click a card for your Budget | Press 'S' to shuffle | ESC for Menu", True, WHITE)
        screen.blit(instructions, (150, 550))
        
        pygame.display.flip()
        clock.tick(60)