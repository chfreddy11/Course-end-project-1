# adventure_game.py
# Purpose: A text-based adventure game where players make strategic choices to find a hidden treasure.

import time

def delay_print(text, delay=1.0):
    """Helper function to print text with a small delay for better game pacing."""
    print(text)
    time.sleep(delay)

def ask_to_restart():
    """Handles the end-game choice to replay or exit."""
    while True:
        choice = input("\nWould you like to play again? (yes/no): ").strip().lower()
        if choice in ['yes', 'y']:
            print("\n--- Restarting your adventure... ---\n")
            return True
        elif choice in ['no', 'n']:
            print("\nThank you for playing! Goodbye.")
            return False
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

def forest_path(player_name):
    """Task 3: Handles the forest scenario and its decisions."""
    delay_print(f"\n{player_name} steps into the dense, dark forest. The canopy shuts out the sunlight.")
    delay_print("As you walk, you encounter a fork in the path.")
    print("1. Follow a rushing river to the north.")
    print("2. Climb a massive ancient tree to survey the land.")
    
    choice = input("What do you want to do? (1 or 2): ").strip()
    
    if choice == '1':
        delay_print("\nYou follow the river. Along the riverbank, you spot a half-buried golden chest...")
        delay_print("✨ SUCCESS! You found the legendary treasure! You win! ✨")
        return True
    elif choice == '2':
        delay_print("\nYou climb the massive tree. A branch snaps, and you fall into a pit of wild briars.")
        delay_print("❌ FAILURE: You are trapped and too injured to continue. Game Over.")
        return False
    else:
        delay_print("\nYou hesitate for too long. A pack of wolves surrounds you.")
        delay_print("❌ FAILURE: Lost in the wild. Game Over.")
        return False

def cave_path(player_name):
    """Task 4: Handles the cave scenario and its decisions."""
    delay_print(f"\n{player_name} cautiously enters the mysterious cave. Cold air brushes against your face.")
    delay_print("The light fades instantly, leaving you in pitch blackness.")
    print("1. Light a torch from your backpack.")
    print("2. Proceed carefully in the dark to save your resources.")
    
    choice = input("What do you want to do? (1 or 2): ").strip()
    
    if choice == '1':
        delay_print("\nYour torch illuminates the cave walls, revealing ancient murals and a hidden passageway.")
        delay_print("At the end of the passage sits the sparkling legendary treasure!")
        delay_print("✨ SUCCESS! You found the legendary treasure! You win! ✨")
        return True
    elif choice == '2':
        delay_print("\nYou stumble blind into the darkness, tripping over a ledge and falling into a deep chasm.")
        delay_print("❌ FAILURE: You fell into the abyss. Game Over.")
        return False
    else:
        delay_print("\nYou panic in the dark, lose your footing, and hit your head on a stalactite.")
        delay_print("❌ FAILURE: Unconscious in the dark. Game Over.")
        return False

def start_game():
    """Task 2: Introduces the game and captures the player's initial path choice."""
    print("==================================================")
    print("       WELCOME TO THE LEGENDARY TREASURE HUNT     ")
    print("==================================================")
    delay_print("You are a brave explorer seeking a lost treasure hidden in an ancient land.")
    
    player_name = input("Enter your explorer's name: ").strip()
    if not player_name:
        player_name = "Hero"
        
    delay_print(f"\nWelcome, Explorer {player_name}! Your quest begins now.")
    delay_print("Before you lie two paths leading into the unknown...")
    print("1. Explore the dark forest.")
    print("2. Enter the mysterious cave.")
    
    while True:
        choice = input("Which path do you choose? (1 or 2): ").strip()
        if choice == '1':
            return forest_path(player_name)
        elif choice == '2':
            return cave_path(player_name)
        else:
            print("Invalid choice. Please enter 1 or 2.")

def main():
    """Task 5: Main execution loop that runs and restarts the game."""
    # Setup verification (Task 1)
    print("[System]: Adventure Game project initialized successfully.\n")
    
    playing = True
    while playing:
        # start_game() returns True for a win, False for a loss
        start_game()
        
        # Ask to restart (handles the third ending condition)
        playing = ask_to_restart()

if __name__ == "__main__":
    main()