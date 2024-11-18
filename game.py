import pygame
import random
import time
import startup

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Automata Island')

# Colors for the texts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load background music
pygame.mixer.music.load('background_music.mp3')  # Ensure the file exists in the same folder
pygame.mixer.music.play(-1)  

# Load images
background_img = pygame.image.load('island_background.jpeg')  # Replace with your island background image
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

pirate_img = pygame.image.load('pirate.png')  # Ensure the pirate image file exists
pirate_img = pygame.transform.scale(pirate_img, (80, 60))

# Initialize font
font = pygame.font.Font(None, 36)  # Default font, size 36

# Game States (Finite Automata)
class GameState:
    PLAYING = 0
    GAME_OVER = 1

# Enemy class
class WordEnemy:
    def __init__(self, word, x, y, speed):
        self.word = word
        self.x = x
        self.y = y
        self.speed = speed  # Set speed based on the level
    
    def move(self):
        self.y += self.speed
    
    def draw(self, screen):
        text = font.render(self.word, True, RED)
        screen.blit(text, (self.x, self.y))

# Player Input
class Player:
    def __init__(self):
        self.input_text = ''
    
    def handle_input(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_RETURN:
            return True
        else:
            self.input_text += event.unicode
        return False
    
    def draw(self, screen):
        text = font.render(self.input_text, True, GREEN)
        screen.blit(text, (20, HEIGHT - 50))

# Expanded word list (200+ words)
word_list = [
     "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
    "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
    "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
    "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
    "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
    "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
    "even", "new", "want", "because", "any", "these", "give", "day", "most", "us",
    "is", "was", "were", "are", "been", "has", "had", "did", "should", "very",
    "much", "many", "such", "those", "so", "may", "about", "through", "still", "every",
    "just", "while", "find", "life", "day", "man", "thing", "part", "child", "eye",
    "never", "last", "door", "where", "after", "before", "great", "old", "year", "back",
    "little", "only", "round", "man", "year", "came", "show", "every", "good", "me",
    "give", "our", "under", "name", "very", "through", "just", "form", "sentence", "great",
    "think", "say", "help", "low", "line", "differ", "turn", "cause", "much", "mean",
    "before", "move", "right", "boy", "old", "too", "same", "tell", "does", "set",
    "three", "want", "air", "well", "also", "play", "small", "end", "put", "home",
    "read", "hand", "port", "large", "spell", "add", "even", "land", "here", "must",
    "treasure", "pirate", "ship", "island", "cannon", "map", "crew", "buccaneer", "sail", "anchor",
    "galleon", "cutlass", "flag", "captain", "ahoy", "voyage", "plunder", "booty", "skull", "crossbones",
    "lunar", "solar", "celestial", "astronaut", "extraterrestrial", "meteorite", "observatory", "radiation",
    "zenith", "aurora", "vacuum", "probe", "spacesuit", "supernova", "hypernova", "crater", "exoplanet", "lightyear",
    "infrared", "titan", "mars", "earth", "jupiter", "venus", "mercury", "pluto", "asterism", "redshift", "darkmatter",
    "plasma", "thermodynamics", "bigbang", "spacetime", "binary", "quantum", "asterisk", "proton", "neutron", 
    "schwarzschild", "escape", "event", "horizon", "wormhole", "multiverse", "singularity", "gravity", "gravitation",
    "lightcurve", "redgiant", "whitedwarf", "helium", "iron", "blackbody", "spectrum", "darkenergy", "vacuum", 
    "expansion", "nebula", "proxima", "radiation", "lightyear", "asteroidbelt", "timewarp", "gravitywell", 
    "nanobot", "hyperspace", "hypernova", "redshift", "blueshift", "halley", "m51", "voyager", "explorer", "juno",
]

# Function to display game over screen and handle restart/quit
def game_over_screen(score):
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - 70, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - 250, HEIGHT // 2 + 50))
    pygame.display.update()

    # Wait for player input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart game
                    waiting = False
                    return True  # Indicate to restart
                if event.key == pygame.K_q:  # Quit game
                    pygame.quit()
                    exit()
# Add the Pushdown Automaton Class and Challenge functionality at the right place in your code.
class PushdownAutomaton:
    def __init__(self, states, stack, transitions, start_state, accept_state):
        """
        Initialize the Pushdown Automaton.
        :param states: Set of states in the PDA.
        :param stack: Initial stack (usually empty).
        :param transitions: Dictionary of transitions.
        :param start_state: Initial state of the PDA.
        :param accept_state: Accept state of the PDA.
        """
        self.states = states
        self.stack = stack  # The PDA's stack
        self.transitions = transitions
        self.current_state = start_state
        self.accept_state = accept_state

    def step(self, input_symbol):
        """
        Perform a transition based on the current state and input symbol.
        :param input_symbol: The current input character.
        :return: True if the transition is valid, False otherwise.
        """
        if (self.current_state, input_symbol) in self.transitions:
            next_state, stack_action = self.transitions[(self.current_state, input_symbol)]

            # Update stack based on the action
            if stack_action == "PUSH":
                self.stack.append(input_symbol)
            elif stack_action == "POP" and self.stack:
                self.stack.pop()

            self.current_state = next_state
            return True  # Successful step

        return False  # Invalid input

    def is_accepted(self):
        """
        Check if the PDA is in an accept state with an empty stack.
        :return: True if accepted, False otherwise.
        """
        return self.current_state == self.accept_state and not self.stack

    def draw(self, screen):
       
        # Draw the stack contents
        stack_display = "Stack: " + "".join(self.stack) if self.stack else "Stack: Empty"
        stack_text = font.render(stack_display, True, WHITE)
        screen.blit(stack_text, (20, 100))

        # Draw the current state
        state_text = font.render(f"State: {self.current_state}", True, WHITE)
        screen.blit(state_text, (20, 140))

def pda_challenge(screen, background_img, pirate_img, font, player_x, player, score, word_speed):
   
    # Define PDA for sea-related words inside parentheses
    sea_related_words = {
        "pirate", "ship", "anchor", "island", "cannon", "map", "crew", "buccaneer",
        "sail", "galleon", "cutlass", "flag", "captain", "voyage", "plunder",
        "booty", "skull", "crossbones", "ahoy", "water", "fish", "shark", "sea",
        "lighthouse", "marine", "wave", "tides", "tsunami", "seashell", "shore", 
        "seashore", "rope", "sea spray", "soundings", "pearl", "fleet", "foam", 
        "hurricane"
    }

    states = {"q0", "q1", "q_accept", "q_reject"}
    transitions = {
        ("q0", "("): ("q1", "PUSH"),  # Open parenthesis starts
        ("q1", ")"): ("q0", "POP"),  # Closed parenthesis
        ("q1", "valid"): ("q1", ""),  # Valid sea word inside parentheses
        ("q0", ""): ("q_accept", ""),  # Input ends, PDA accepts
    }

    pda = PushdownAutomaton(states, [], transitions, "q0", "q_accept")

    running = True
    clock = pygame.time.Clock()
    input_sequence = ""
    start_time = time.time()
    time_limit = 15  # 15 seconds for the challenge

    while running:
        screen.blit(background_img, (0, 0))  # Render the game background

        # Draw the pirate
        screen.blit(pirate_img, (player_x, HEIGHT - 80))

        # Draw player input (regular gameplay)
        player.draw(screen)

        # Display the current score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH - 150, 20))  # Top-right corner

        # Display remaining time
        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_limit - elapsed_time)
        timer_text = font.render(f"Time Left: {int(remaining_time)}s", True, WHITE)
        screen.blit(timer_text, (WIDTH - 150, 60))

        if remaining_time <= 0:
            # Time up: Reject the sequence and apply penalty
            result_text = font.render("Time Up! PDA Rejected!", True, RED)
            screen.blit(result_text, (WIDTH - 300, 120))
            pygame.display.flip()
            time.sleep(2)
            return score - 2, word_speed + 0.5, False  # Deduct points, increase word speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Split the input into tokens and process each token
                    tokens = input_sequence.split()
                    valid = True

                    for token in tokens:
                        if token == "(":
                            pda.step("(")
                        elif token == ")":
                            if not pda.step(")"):
                                valid = False
                                break
                        elif token.lower() in sea_related_words:
                            if not pda.step("valid"):
                                valid = False
                                break
                        else:
                            valid = False
                            break

                    # Check PDA acceptance
                    if valid and pda.is_accepted():
                        result_text = font.render("Accepted! Bonus Applied!", True, GREEN)
                        screen.blit(result_text, (WIDTH - 300, 120))
                        pygame.display.flip()
                        time.sleep(2)
                        return score + 1, max(1.0, word_speed - 0.5), True  # Add score, slow word speed
                    else:
                        result_text = font.render("Rejected! Penalty Applied!", True, RED)
                        screen.blit(result_text, (WIDTH - 300, 120))
                        pygame.display.flip()
                        time.sleep(2)
                        return score - 2, word_speed + 0.5, False  # Deduct points, increase word speed

                else:
                    char = event.unicode
                    input_sequence += char

        # Draw input sequence (top-right corner)
        input_text = font.render(f"Enter secret code (e.g., '(word)'): {input_sequence}", True, WHITE)
        screen.blit(input_text, (WIDTH - 500, 100))

        pygame.display.flip()
        clock.tick(60)


def game_loop():
    startup.main_menu()

    while True:  # Add a loop to handle restarting the game
        running = True
        clock = pygame.time.Clock()
        player = Player()
        score = 0
        level = 1
        words_destroyed = 0
        word_enemies = []
        last_spawn_time = time.time()

        player_x = WIDTH // 2
        player_speed = 150
        word_speed = 1.5
        pda_triggered = False  # Tracks if PDA has been triggered for the current level
        word_speed_reset_time = None  # Time to reset word speed back to original

        while running:
            screen.blit(background_img, (0, 0))

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player_x -= player_speed
                    elif event.key == pygame.K_RIGHT:
                        player_x += player_speed
                    if player.handle_input(event):
                        for word_enemy in word_enemies:
                            if player.input_text == word_enemy.word:
                                word_enemies.remove(word_enemy)
                                words_destroyed += 1
                                score += 1
                                break
                        player.input_text = ''

            # Trigger PDA Challenge
            if (score >= 5 and not pda_triggered) or (words_destroyed == 0 and level > 1 and not pda_triggered):
                # Run PDA challenge and update game state
                score, word_speed, bonus_applied = pda_challenge(
                    screen, background_img, pirate_img, font, player_x, player, score, word_speed
                )

                # Apply bonuses or penalties
                if bonus_applied:
                    player_speed = min(player_speed + 10, 300)  # Cap player speed
                    word_speed_reset_time = time.time() + 120  # Reset word speed after 2 minutes
                else:
                    # Spawn multiple enemies as penalty
                    for _ in range(3):
                        word = random.choice(word_list)
                        x_pos = random.randint(50, WIDTH - 150)
                        word_enemies.append(WordEnemy(word, x_pos, 0, word_speed))

                pda_triggered = True  # Ensure PDA is triggered only once per level

            # Reset word speed after a specific duration
            if word_speed_reset_time and time.time() > word_speed_reset_time:
                word_speed = 1.5  # Reset to original word speed
                word_speed_reset_time = None  # Clear reset timer

            # Ensure pirate stays on-screen
            if player_x < 0:
                player_x = 0
            if player_x > WIDTH - 80:
                player_x = WIDTH - 80

            # Spawn new enemies dynamically based on level
            current_time = time.time()
            spawn_rate = max(0.5, 5 - level * 0.2)  # Faster spawn rate as levels increase

            if current_time - last_spawn_time > spawn_rate:
                num_words_to_spawn = min(level, 5)  # Spawn up to 5 words at higher levels
                for _ in range(num_words_to_spawn):
                    word = random.choice(word_list)
                    x_pos = random.randint(50, WIDTH - 150)
                    word_enemies.append(WordEnemy(word, x_pos, 0, word_speed))
                last_spawn_time = current_time

            for word_enemy in word_enemies:
                word_enemy.move()
                word_enemy.draw(screen)
                if word_enemy.y + 30 > HEIGHT - 50:
                    running = False  # Game over
                    break

            # Check level progression
            if words_destroyed >= 10 * level:
                level += 1
                words_destroyed = 0
                pda_triggered = False  # Reset PDA trigger for the new level

            # Draw the pirate and player input
            screen.blit(pirate_img, (player_x, HEIGHT - 80))
            player.draw(screen)

            # Draw the score and level
            score_text = font.render(f"Score: {score}", True, WHITE)
            level_text = font.render(f"Level: {level}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 40))

            pygame.display.flip()
            clock.tick(60)

        # Show Game Over screen
        restart = game_over_screen(score)
        if not restart:
            break  # Exit the main game loop and quit




if __name__ == "__main__":
    game_loop()


