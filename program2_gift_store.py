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

def show_alert(screen, message):
    """Show a simple alert message"""
    alert_surf = pygame.Surface((400, 100), pygame.SRCALPHA)
    alert_surf.fill((255, 220, 220, 230))
    pygame.draw.rect(alert_surf, RED, (0, 0, 400, 100), 3)
    
    alert_text = font_small.render(message, True, RED)
    alert_surf.blit(alert_text, (200 - alert_text.get_width()//2, 40))
    
    screen.blit(alert_surf, (200, 250))
    pygame.display.flip()
    pygame.time.wait(700)

def run_gift_store(initial_money):
    """Run gift store"""
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Gift Store <3")
    clock = pygame.time.Clock()
    
    # Initialize fonts
    init_fonts()
    
    money = initial_money
    items_bought = []
    
    items = [
        {"name": "Love Letter", "price": 83},
        {"name": "Chocolate", "price": 143},
        {"name": "Single Rose", "price": 197},
        {"name": "Teddy Bear", "price": 263},
        {"name": "Perfume", "price": 337},
        {"name": "Jewelry", "price": 421}
    ]
    
    item_buttons = []
    for i, item in enumerate(items):
        row = i // 3
        col = i % 3
        x = 120 + col * 200
        y = 110 + row * 200
        item_buttons.append({
            "rect": pygame.Rect(x, y, 150, 180),
            "item": item,
            "hover": False,
            "bought": False  # Track if item is already bought
        })
    
    checkout_button = pygame.Rect(300, 500, 200, 50)
    back_button = pygame.Rect(20, 550, 150, 40)
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for btn in item_buttons:
            # Only show hover if not already bought
            btn["hover"] = not btn["bought"] and btn["rect"].collidepoint(mouse_pos)
        
        checkout_hover = checkout_button.collidepoint(mouse_pos)
        back_hover = back_button.collidepoint(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {"action": "back", "remaining_money": money, "items_bought": items_bought}
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for btn in item_buttons:
                        # Check if clicked, not already bought, and has enough money
                        if (btn["rect"].collidepoint(mouse_pos) and 
                            not btn["bought"] and 
                            money >= btn["item"]["price"]):
                            
                            item = btn["item"]
                            money -= item["price"]
                            items_bought.append(item["name"])
                            btn["bought"] = True  # Mark as bought
                            show_alert(screen, f"Bought {item['name']} for {item['price']}!")
                            break  # Exit loop after buying one item
                        elif (btn["rect"].collidepoint(mouse_pos) and 
                              not btn["bought"] and 
                              money < btn["item"]["price"]):
                            show_alert(screen, "Not enough money!")
                            break
                        elif (btn["rect"].collidepoint(mouse_pos) and 
                              btn["bought"]):
                            show_alert(screen, f"You already bought {btn['item']['name']}!")
                            break
                    
                    if checkout_button.collidepoint(mouse_pos):
                        return {"action": "checkout", "remaining_money": money, "items_bought": items_bought}
                    
                    if back_button.collidepoint(mouse_pos):
                        return {"action": "back", "remaining_money": money, "items_bought": items_bought}
        
        screen.fill(RED)
        for y in range(100, 500):
            pygame.draw.line(screen, PINK, (0, y), (800, y))
        
        title = font_large.render("GIFT STORE", True, WHITE)
        screen.blit(title, (400 - title.get_width()//2, 30))

        logo_image = pygame.image.load("kiffyhi.png")
        logo_image = pygame.transform.scale(logo_image, (130, 130))
        screen.blit(logo_image, (200, -20))

        logo_image = pygame.image.load("kiffyhi.png")
        logo_image = pygame.transform.scale(logo_image, (130, 130))
        screen.blit(logo_image, (480, -20))
        
        money_text = font_medium.render(f"Budget: {money}", True, WHITE)
        screen.blit(money_text, (400 - money_text.get_width()//2, 60))
        
        for btn in item_buttons:
            item = btn["item"]
            rect = btn["rect"]
            
            # Change color based on whether item is bought
            if btn["bought"]:
                # Gray out bought items
                card_color = DARK_PINK
                text_color = (200, 200, 200)  # Gray text
                heart_color = (200, 100, 100)  # Darker red
            elif btn["hover"]:
                card_color = LIGHT_PINK
                text_color = RED
                heart_color = RED
            else:
                card_color = WHITE
                text_color = RED
                heart_color = RED
            
            pygame.draw.rect(screen, card_color, rect, border_radius=10)
            pygame.draw.rect(screen, RED, rect, 2, border_radius=10)
            
            name_text = font_small.render(item["name"], True, text_color)
            screen.blit(name_text, (rect.x + 75 - name_text.get_width()//2, rect.y + 10))
            
            price_text = font_small.render(f"{item['price']}", True, text_color)
            screen.blit(price_text, (rect.x + 75 - price_text.get_width()//2, rect.y + 40))
            

            kiffy_logo = pygame.image.load("gifts.png")
            scaled_width = 100  # x+45 to x+105
            scaled_height = 100  # y+80 to y+120
            
            kiffy_logo = pygame.transform.scale(kiffy_logo, (scaled_width, scaled_height))
            
            # Position at the heart's top-left corner (x+45, y+80)
            screen.blit(kiffy_logo, (rect.x + 30, rect.y + 50))

            
            
            # Change button text based on status
            if btn["bought"]:
                status_text = font_small.render("SOLD OUT", True, text_color)
            else:
                status_text = font_small.render("CLICK TO BUY", True, DARK_PINK)
            screen.blit(status_text, (rect.x + 75 - status_text.get_width()//2, rect.y + 150))
        
        checkout_color = LIGHT_PINK if checkout_hover else WHITE
        pygame.draw.rect(screen, checkout_color, checkout_button, border_radius=10)
        pygame.draw.rect(screen, RED, checkout_button, 3, border_radius=10)
        checkout_text = font_medium.render("CHECKOUT", True, RED)
        screen.blit(checkout_text, checkout_text.get_rect(center=checkout_button.center))
        
        back_color = LIGHT_PINK if back_hover else WHITE
        pygame.draw.rect(screen, back_color, back_button, border_radius=8)
        pygame.draw.rect(screen, RED, back_button, 2, border_radius=8)
        back_text = font_small.render("Back to Menu", True, RED)
        screen.blit(back_text, back_text.get_rect(center=back_button.center))
        
        if items_bought:
            bought_text = font_small.render(f"Items: {', '.join(items_bought)}", True, WHITE)
            screen.blit(bought_text, (300, 550))
        
        pygame.display.flip()
        clock.tick(60)
