import pygame

# COLORS
WHITE = (255, 255, 255)
RED = (255, 127, 127)
PINK = (255, 182, 193)
LIGHT_PINK = (255, 220, 210)
LIGHT_RED = (255, 145, 145)
DARK_PINK = (255, 105, 180)

# Fonts will be initialized in the function
font_large = None
font_medium = None
font_small = None

def init_fonts():
    """Initialize fonts"""
    global font_large, font_medium, font_small
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)

def show_result(result_type, message, budget, items_bought):
    """Show result page - returns 'menu' or 'exit'"""
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game ResultS <3")
    clock = pygame.time.Clock()
    
    # Initialize fonts
    init_fonts()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        menu_button = pygame.Rect(240, 470, 150, 50)
        exit_button = pygame.Rect(410, 470, 150, 50)
        menu_hover = menu_button.collidepoint(mouse_pos)
        exit_hover = exit_button.collidepoint(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if menu_button.collidepoint(mouse_pos):
                        return "menu"
                    elif exit_button.collidepoint(mouse_pos):
                        return "exit"
        
        screen.fill(RED)
        for y in range(100, 500):
            pygame.draw.line(screen, PINK, (0, y), (800, y))
        
        if result_type == "win":
            title = font_large.render("YOU WIN!", True, RED)
        else:
            title = font_large.render("GAME OVER", True, WHITE)
        screen.blit(title, (400 - title.get_width()//2, 135))
        
        msg_text = font_medium.render(message, True, WHITE)
        screen.blit(msg_text, (400 - msg_text.get_width()//2, 170))
        
        budget_text = font_medium.render(f"Your Budget: {budget}", True, RED)
        screen.blit(budget_text, (400 - budget_text.get_width()//2, 220))
        
        if items_bought:
            items_text = font_small.render("Items you bought:", True, WHITE)
            screen.blit(items_text, (400 - items_text.get_width()//2, 270))
            
            items_list = ", ".join(items_bought)
            if len(items_list) > 40:
                items_list = items_list[:40] + "..."
            bought_text = font_small.render(items_list, True, RED)
            screen.blit(bought_text, (400 - bought_text.get_width()//2, 300))
        else:
            no_items = font_small.render("You didn't buy anything!", True, WHITE)
            screen.blit(no_items, (400 - no_items.get_width()//2, 270))
        
        try:
            cat = pygame.image.load("kiffyhi.png")
            cat = pygame.transform.scale(cat, (150, 150))
            screen.blit(cat, (325, 320))
        except:
            heart_points = [
                (400, 395),
                (370, 365),
                (340, 395),
                (400, 455),
                (460, 395),
                (430, 365),
                (400, 395)
            ]
            pygame.draw.polygon(screen, DARK_PINK, heart_points)
        
        menu_color = LIGHT_PINK if menu_hover else WHITE
        pygame.draw.rect(screen, menu_color, menu_button, border_radius=10)
        pygame.draw.rect(screen, RED, menu_button, 3, border_radius=10)
        menu_text = font_medium.render("Menu", True, RED)
        screen.blit(menu_text, menu_text.get_rect(center=menu_button.center))
        
        exit_color = LIGHT_PINK if exit_hover else WHITE
        pygame.draw.rect(screen, exit_color, exit_button, border_radius=10)
        pygame.draw.rect(screen, RED, exit_button, 3, border_radius=10)
        exit_text = font_medium.render("Exit", True, RED)
        screen.blit(exit_text, exit_text.get_rect(center=exit_button.center))
        
        pygame.display.flip()
        clock.tick(60)
