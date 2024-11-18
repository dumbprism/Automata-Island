import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AUTOMATA ISLAND')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
STROKE_COLOR = (255, 255, 255)  # Color for the text stroke

# Load custom font
custom_font_path = 'Stopwatch.otf' 
other_font_path = 'sfPro.otf' # Replace with your font file name
title_font = pygame.font.Font(custom_font_path, 74)
button_font = pygame.font.Font(custom_font_path, 48)
dev_font = pygame.font.Font(other_font_path, 28)

def draw_rounded_rect(surface, rect, color, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

def draw_stroked_text(surface, text, font, color, stroke_color, position, stroke_width=2):
    """Draws text with a stroke effect."""
    # Render stroke by drawing text multiple times with offset
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx != 0 or dy != 0:  # Skip the center
                stroke_text = font.render(text, True, stroke_color)
                surface.blit(stroke_text, (position[0] + dx, position[1] + dy))

    # Draw the main text
    main_text = font.render(text, True, color)
    surface.blit(main_text, position)

def draw_startup_screen():
    # Load background image
    background_img = pygame.image.load('startup_background.png')
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    
    # Set background opacity to 0.65
    background_img.set_alpha(165)  # 0.65 * 255 = 165
    screen.blit(background_img, (0, 0))

    # Draw game title with stroke
    title_text = "AUTOMATA ISLAND"
    draw_stroked_text(screen, title_text, title_font, "#2E7ADE", STROKE_COLOR, (WIDTH // 2 - title_font.size(title_text)[0] // 2, HEIGHT // 2 - 100))

    # Draw Start Button with rounded corners
    start_button = button_font.render("START GAME", True, BLACK)
    start_button_rect = start_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    button_bg_rect = start_button_rect.inflate(40, 20)
    draw_rounded_rect(screen, button_bg_rect, WHITE, 15)  # Rounded rectangle
    draw_stroked_text(screen, "START GAME", button_font, BLACK, STROKE_COLOR, (start_button_rect.x, start_button_rect.y))

    # Draw "Developed by" line in black
    developed_by_text = "Developed by"
    dev_by_position = (WIDTH // 2 - dev_font.size(developed_by_text)[0] // 2, HEIGHT - 150)
    screen.blit(dev_font.render(developed_by_text, True, BLACK), dev_by_position)

    # Developer names in black
    developers = [
        "1. T.Sasank Reddy [AIE22160]",
        "2. Kotamraju Arhant [AIE22123]",
        "3. Vakati Kushal [AIE22161]",
        "4. Ganganapalli Naveen [AIE22115]"
    ]

    for i, dev in enumerate(developers):
        dev_text = dev_font.render(dev, True, BLACK)  # Changed to BLACK
        screen.blit(dev_text, (WIDTH // 2 - dev_text.get_width() // 2, HEIGHT - 100 + i * 25))

    pygame.display.flip()

def main_menu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos
                    start_button_rect = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 - 30, 220, 60)
                    if start_button_rect.collidepoint(mouse_pos):
                        return  # Start game

        draw_startup_screen()

# Start the main menu
if __name__ == "__main__":
    main_menu()
