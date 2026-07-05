def log_game_event(text):
    """Appends game text to an external log file to track the player's journey."""
    with open("game_output_log.txt", "a", encoding="utf-8") as file:
        file.write(text + "\n")

# You can then call log_game_event("Player chose the forest path") 
# anywhere in your script to save real-time game logs!