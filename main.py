import pygame
import sys

def main():
    # Initialize pygame once
    pygame.init()
    
    # Import the programs
    import program1_menu_cards as menu_cards
    import program2_gift_store as gift_store
    import program3_end_page as end_page
    
    # Game state
    game_state = "menu"  # menu, cards, store, result
    player_budget = 0
    remaining_money = 0
    items_bought = []
    
    while True:
        if game_state == "menu":
            # Show menu from program 1
            result = menu_cards.show_menu()
            if result == "start":
                game_state = "cards"
            else:
                pygame.quit()
                sys.exit()
                
        elif game_state == "cards":
            # Show card selection from program 1
            budget = menu_cards.run_card_selection()
            if budget is None:
                game_state = "menu"  # Went back to menu
            else:
                player_budget = budget
                remaining_money = budget
                game_state = "store"
                
        elif game_state == "store":
            # Show gift store from program 2
            result = gift_store.run_gift_store(remaining_money)
            if result["action"] == "checkout":
                remaining_money = result["remaining_money"]
                items_bought = result["items_bought"]
                game_state = "result"
            elif result["action"] == "back":
                game_state = "menu"
                
        elif game_state == "result":
            # Calculate win/lose
            if remaining_money == 0:
                result_type = "win"
                message = "Perfect! You spent exactly your budget!"
            elif remaining_money > 0:
                result_type = "lose"
                message = f"Oh no! You still have {remaining_money} left!"
            else:
                result_type = "lose"
                message = f"Oops! You overspent by {abs(remaining_money)}!"
            
            # Show end page from program 3
            choice = end_page.show_result(result_type, message, player_budget, items_bought)
            if choice == "menu":
                game_state = "menu"
            else:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()