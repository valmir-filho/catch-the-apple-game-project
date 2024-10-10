import pygame
import random

# Initialize pygame.
pygame.init()

# Game window dimensions.
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon.
pygame.display.set_caption("Catch the Falling Objects")
icon = pygame.image.load("catch-the-apple-game-project/assets/images/basket.png")
pygame.display.set_icon(icon)

# Colors.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Basket (player).
basket_img = pygame.image.load("teste/assets/images/basket.png")
basket_width = 80  # Adjust width to 80 pixels.
basket_height = 80  # Adjust height to 80 pixels.
basket_img = pygame.transform.scale(basket_img, (basket_width, basket_height))  # Resize basket image.
basket_x = screen_width // 2 - basket_width // 2
basket_y = screen_height - basket_height - 10
basket_x_change = 0
basket_speed = 7

# Falling objects.
good_object_img = pygame.image.load("catch-the-apple-game-project/assets/images/apple.png")
good_object_img = pygame.transform.scale(good_object_img, (40, 40))  # Resize good object to 40x40 pixels.

bad_object_img = pygame.image.load("catch-the-apple-game-project/assets/images/bad_apple.png")
bad_object_img = pygame.transform.scale(bad_object_img, (40, 40))  # Resize bad object to 40x40 pixels.

falling_objects = []  # List to hold both good and bad objects.
object_speed = 7  # Medium speed for falling objects.
spawn_timer = 100  # Time between each new falling object.
score = 0
lives = 3
missed_apples = 0  # Counter for missed apples.

# Font for score, lives, and missed apples.
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 100)  # Larger font for Game Over text.

# Frame rate control.
clock = pygame.time.Clock()  # Create a clock object.
fps = 60


# Function to show score.
def show_score():
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))


# Function to show lives.
def show_lives():
    lives_text = font.render("Lives: " + str(lives), True, RED)
    screen.blit(lives_text, (screen_width - 120, 10))


# Function to show missed apples.
def show_missed_apples():
    missed_text = font.render("Missed Apples: " + str(missed_apples), True, RED)
    screen.blit(missed_text, (10, 50))


# Function to create a new falling object.
def create_falling_object():
    x_pos = random.randint(0, screen_width - 40)  # Adjust spawn range for objects new size.
    if random.randint(0, 1) == 0:
        return {'type': 'good', 'x': x_pos, 'y': -40, 'img': good_object_img}
    else:
        return {'type': 'bad', 'x': x_pos, 'y': -40, 'img': bad_object_img}


# Function to move and check collisions with falling objects.
def move_and_check_objects():
    global score, lives, missed_apples
    for obj in falling_objects[:]:
        obj['y'] += object_speed
        # Check if object hits the basket.
        if basket_x < obj['x'] < basket_x + basket_width and basket_y < obj['y'] + 40 < basket_y + basket_height:
            if obj['type'] == 'good':
                score += 1
            else:
                lives -= 1
            falling_objects.remove(obj)
        # Remove objects that fall off the screen.
        elif obj['y'] > screen_height:
            if obj['type'] == 'good':
                missed_apples += 1  # Increment missed apples if a good object is missed.
            falling_objects.remove(obj)

# Game loop.
running = True
while running:
    # Fill the background.
    screen.fill(WHITE)

    # Event handling.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movement control.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                basket_x_change = -basket_speed
            if event.key == pygame.K_RIGHT:
                basket_x_change = basket_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                basket_x_change = 0

    # Update basket position.
    basket_x += basket_x_change
    if basket_x < 0:
        basket_x = 0
    elif basket_x > screen_width - basket_width:
        basket_x = screen_width - basket_width

    # Add new objects periodically.
    spawn_timer -= 1
    if spawn_timer <= 0:
        falling_objects.append(create_falling_object())
        spawn_timer = 100

    # Move and check falling objects.
    move_and_check_objects()

    # Draw basket.
    screen.blit(basket_img, (basket_x, basket_y))

    # Draw all falling objects.
    for obj in falling_objects:
        screen.blit(obj['img'], (obj['x'], obj['y']))

    # Display score, lives, and missed apples.
    show_score()
    show_lives()
    show_missed_apples()

    # Game over condition.
    if lives <= 0 or missed_apples >= 3:
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))  # Center the text.
        screen.blit(game_over_text, game_over_rect)  # Display centered text.
        pygame.display.update()
        pygame.time.wait(2000)
        running = False

    # Update the display.
    pygame.display.update()

    # Control frame rate.
    clock.tick(fps)

# Quit pygame.
pygame.quit()
