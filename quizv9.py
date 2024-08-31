import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Personality Teller Game")

# Load images
start_background = pygame.image.load('start_background.jpg')
question_backgrounds = [
    pygame.image.load('mountain.jpg'),
    pygame.image.load('ocean.jpg'),
    pygame.image.load('forest.jpg')
    # Add more backgrounds for other questions
]
result_background = pygame.image.load('result_background.jpg')

# Load music and sound effects
pygame.mixer.music.load('background_music.mp3')  # Ensure you have this music file in the same directory
select_sound = pygame.mixer.Sound('select_sound.wav')  # Ensure you have this sound file in the same directory
typing_sound = pygame.mixer.Sound('type_sound.mp3')  # Ensure you have a short loopable sound

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 139)
GRAY = (200, 200, 200)

# Font setup
font_size = 24
font = pygame.font.Font(None, font_size)
big_font_size = 36
big_font = pygame.font.Font(None, big_font_size)

# Questions and options
questions = [
    ("Which environment do you prefer?", ["Mountain", "Ocean", "Forest"]),
    ("Which weather do you enjoy the most?", ["Sunny day", "Rainy day", "Snowy day"]),
    ("Which type of vacation appeals to you the most?", ["Exploring a new city", "Relaxing on a beach", "Hiking in the wilderness"]),
    ("Which animal do you feel most connected to?", ["Eagle", "Dolphin", "Wolf"]),
    ("Which color palette do you prefer?", ["Warm tones", "Cool tones", "Neutral tones"]),
    ("Which activity do you find most fulfilling?", ["Reading a book", "Attending a social event", "Engaging in a creative hobby"]),
    ("Which time of day do you feel most energized?", ["Morning", "Afternoon", "Night"]),
    ("Which art form resonates with you the most?", ["Painting", "Music", "Literature"]),
    ("Which type of social setting do you prefer?", ["Large gathering", "Small group of friends", "Solo time"]),
    ("Which mode of transportation do you prefer?", ["Car", "Train", "Bicycle"])
]

# Personality traits mapping
personalities = {
    # Add all personality traits and their descriptions as in your provided dictionary
}

# Game variables
current_question = 0
user_choices = []

# Function to draw text with word wrapping
def draw_text(text, font, color, surface, x, y, width, wrap=True):
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        test_line = f"{current_line} {word}".strip()
        text_surface = font.render(test_line, True, color)
        if text_surface.get_width() <= width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    
    lines.append(current_line)  # Add the last line

    y_offset = y
    for line in lines:
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y_offset))
        y_offset += font.get_height()

# Function to draw a button with hover effect
def draw_button(text, font, color, surface, x, y, width, height, hover=False):
    button_color = (255, 255, 255, 128) if not hover else (200, 200, 200, 160)
    button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(button_surface, button_color, button_surface.get_rect(), border_radius=20)
    
    surface.blit(button_surface, (x, y))
    
    text_surface = font.render(text, True, DARK_BLUE)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    surface.blit(text_surface, text_rect)

# Function to draw the start screen
def draw_start_screen():
    screen.blit(start_background, (0, 0))
    draw_text("Do you want to go on an adventurous journey of knowing your soul and your deep lying emotions and capabilities?", big_font, WHITE, screen, 50, 150, screen_width - 100)
    button_width, button_height = 300, 50
    button_x = (screen_width - button_width) / 2
    button_y = 400
    mouse_pos = pygame.mouse.get_pos()
    hover = button_x < mouse_pos[0] < button_x + button_width and button_y < mouse_pos[1] < button_y + button_height
    draw_button("Continue to the Journey", font, BLUE, screen, button_x, button_y, button_width, button_height, hover=hover)
    pygame.display.update()

# Function to draw the question screen
def draw_question(question, options):
    screen.blit(question_backgrounds[current_question % len(question_backgrounds)], (0, 0))
    draw_text(question, big_font, WHITE, screen, 50, 50, screen_width - 100)
    button_width, button_height = 400, 50
    button_x = (screen_width - button_width) / 2
    for i, option in enumerate(options):
        button_y = 150 + i * (button_height + 20)
        mouse_pos = pygame.mouse.get_pos()
        hover = button_x < mouse_pos[0] < button_x + button_width and button_y < mouse_pos[1] < button_y + button_height
        draw_button(option, font, DARK_BLUE, screen, button_x, button_y, button_width, button_height, hover=hover)
    pygame.display.update()

# Function to generate the story based on user choices
def generate_story(choices):
    trait_count = {}
    
    for choice in choices:
        traits = personalities[choice].split(', ')
        for trait in traits:
            if trait in trait_count:
                trait_count[trait] += 1
            else:
                trait_count[trait] = 1

    story = "You are a unique individual with the following prominent traits:\n\n"

    if trait_count.get("Independent", 0) > 0:
        story += "• Fiercely independent, you carve your own path with a strong will.\n"
    if trait_count.get("Reflective", 0) > 0:
        story += "• Reflection guides your decisions, deepening your understanding of the world.\n"
    if trait_count.get("Grounded", 0) > 0:
        story += "• Your grounded approach keeps you balanced and calm amidst challenges.\n"
    if trait_count.get("Optimistic", 0) > 0:
        story += "• An optimistic outlook fills your days with positivity, allowing you to see the bright side.\n"
    if trait_count.get("Thoughtful", 0) > 0:
        story += "• Your thoughtful nature helps you connect deeply with others.\n"
    if trait_count.get("Calm", 0) > 0:
        story += "• You maintain a calm presence, offering comfort to those around you.\n"
    if trait_count.get("Adventurous", 0) > 0:
        story += "• An adventurous spirit drives you to seek new experiences.\n"
    if trait_count.get("Playful", 0) > 0:
        story += "• Playfulness brings joy and lightness to your relationships.\n"
    if trait_count.get("Loyal", 0) > 0:
        story += "• Loyalty is one of your defining traits, making you a reliable friend.\n"
    if trait_count.get("Passionate", 0) > 0:
        story += "• Passion drives your endeavors, infusing them with energy.\n"
    if trait_count.get("Practical", 0) > 0:
        story += "• A practical mindset helps you handle tasks efficiently.\n"
    if trait_count.get("Intellectual", 0) > 0:
        story += "• Your intellectual curiosity leads you to explore new ideas.\n"
    if trait_count.get("Extroverted", 0) > 0:
        story += "• Your extroverted nature makes you thrive in social settings.\n"
    if trait_count.get("Creative", 0) > 0:
        story += "• Creativity allows you to express yourself in unique ways.\n"
    if trait_count.get("Ambitious", 0) > 0:
        story += "• Ambition drives you to achieve your goals with determination.\n"
    if trait_count.get("Balanced", 0) > 0:
        story += "• You maintain a balanced approach to life, harmonizing different aspects.\n"
    if trait_count.get("Artistic", 0) > 0:
        story += "• An artistic sensibility enhances your appreciation for beauty.\n"
    if trait_count.get("Outgoing", 0) > 0:
        story += "• Your outgoing nature fosters meaningful connections with others.\n"
    if trait_count.get("Methodical", 0) > 0:
        story += "• A methodical approach helps you tackle challenges systematically.\n"
    if trait_count.get("Active", 0) > 0:
        story += "• An active lifestyle reflects your enthusiasm for vitality.\n"

    story += "\nThis rich tapestry of traits creates a vivid portrait of who you are, highlighting your unique personality and how you navigate through the world."

    return story

# Typing effect function
def type_story(story, surface, x, y, font, color, speed=50):
    """Displays the story with a typing effect and typewriter sound in loop."""
    story_length = len(story)
    displayed_text = ""
    
    # Start playing the typing sound in a loop
    typing_sound.play(-1)  # -1 means the sound will loop indefinitely
    
    for i in range(story_length):
        displayed_text += story[i]
        surface.blit(result_background, (0, 0))  # Blit background again to clear previous text
        draw_text(displayed_text, font, color, surface, x, y, screen_width - 100, wrap=False)
        pygame.display.update()
        
        # Control typing speed
        pygame.time.wait(speed)
        
        # Handle events while typing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    # Stop the typing sound once typing is complete
    typing_sound.stop()

# Function to show the final story and options to restart or exit
def show_story():
    screen.blit(result_background, (0, 0))
    story = generate_story(user_choices)
    type_story(story, screen, 50, 50, font, WHITE)
    
    restart_button_rect = pygame.Rect((screen_width - 200) / 2, 400, 200, 50)
    exit_button_rect = pygame.Rect((screen_width - 200) / 2, 470, 200, 50)

    draw_button("Restart", font, DARK_BLUE, screen, restart_button_rect.x, restart_button_rect.y, restart_button_rect.width, restart_button_rect.height)
    draw_button("Exit", font, DARK_BLUE, screen, exit_button_rect.x, exit_button_rect.y, exit_button_rect.width, exit_button_rect.height)
    
    pygame.display.update()
    
    action = None
    while not action:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse_pos):
                    action = 'restart'
                elif exit_button_rect.collidepoint(mouse_pos):
                    action = 'exit'
    return action

# Game loop
running = True
on_start_screen = True
music_playing = False

while running:
    if on_start_screen:
        draw_start_screen()
    elif current_question < len(questions):
        question, options = questions[current_question]
        draw_question(question, options)
    else:
        action = show_story()
        if action == 'restart':
            # Reset game variables for restart
            current_question = 0
            user_choices = []
            on_start_screen = True
            music_playing = False
        elif action == 'exit':
            running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if on_start_screen:
                button_width, button_height = 300, 50
                button_x = (screen_width - button_width) / 2
                button_y = 400
                if button_x < mouse_pos[0] < button_x + button_width and button_y < mouse_pos[1] < button_y + button_height:
                    on_start_screen = False
                    if not music_playing:
                        pygame.mixer.music.play(-1)
                        music_playing = True
            else:
                button_width, button_height = 400, 50
                button_x = (screen_width - button_width) / 2
                for i, option in enumerate(questions[current_question][1]):
                    button_y = 150 + i * (button_height + 20)
                    if button_x < mouse_pos[0] < button_x + button_width and button_y < mouse_pos[1] < button_y + button_height:
                        select_sound.play()
                        user_choices.append(option)
                        current_question += 1

    pygame.display.update()

pygame.quit()
