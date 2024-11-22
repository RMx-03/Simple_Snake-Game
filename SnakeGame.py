'''
Snake Game Using Pygame

Game Mechanics:
1. Snake moves continuously in a single direction
2. Movement abilities - Up, Down, Left, Right - keyboard inputs 
3. Grow longer on eating food, and its speed increases.
4. Game ending: The snake collides with itself

'''
# Libraries
import pygame, time, random  

# Initialize Pygame
pygame.init()  

# Constants - Display dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
GRID_SIZE = 20  # Each block size
SNAKE_SPEED = 20  

# Colors
MAGENTA = (255, 0, 255)  # Food color
GREEN = (0, 255, 0)  # Snake color
RED = (255, 0, 0)  # Game Over text
BLACK = (0, 0, 0)  # Background
YELLOW = (255, 255, 102)  # Score 

# Fonts
FONT_STYLE = pygame.font.SysFont("Tahoma", 30, bold = True)
SCORE_FONT = pygame.font.SysFont("Courier", 40)

# Setting up the game display
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")  # Game window title

# Clock for controlling FPS 
CLOCK = pygame.time.Clock()  

# Initialize Global Variables
x_head = y_head = x_change = y_change = 0
snake = []
snake_length = 1
food_x = food_y = 0
direction = None
game_quit = False
game_over = False


'''Reset all the game variables on the start of a new game.'''
def initialize_game():
    global x_head, y_head, x_change, y_change, snake, snake_length, food_x, food_y, direction, game_quit, game_over
    # Snake head starting position 
    x_head = SCREEN_HEIGHT // 2
    y_head= SCREEN_WIDTH // 2
    # Store the changing values
    x_change = 0
    y_change = 0
    # Snake position storage    
    snake = []
    snake_length = 1
    # Variables to manage direction 
    direction = None
    game_quit = False
    game_over = False
    # Random generation of food co-ordinates 
    food_x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
    food_y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE


'''Draw the snake.'''
def snake_struct():
    for segment in snake:
        pygame.draw.rect(DISPLAY, GREEN, [segment[0], segment[1], GRID_SIZE, GRID_SIZE])


'''Draw the random food position.'''
def spawn_food():
    pygame.draw.rect(DISPLAY, MAGENTA, [food_x, food_y, GRID_SIZE, GRID_SIZE])


'''Display the score.'''
def show_score():
    score = SCORE_FONT.render(f"Your Score: {snake_length - 1}", True, YELLOW)
    DISPLAY.blit(score, [0, 0])  # at the top left corner


'''Display text in the game window.'''
def message(msg, color):
    txt = FONT_STYLE.render(msg, True, color)
    txt_rect = txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))  # Helps in centering the text display
    DISPLAY.blit(txt, txt_rect)


'''Handle user inputs.'''
def handle_events():
    global direction, game_quit, game_over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'
            elif event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'


'''Update the snake's position and check for food collision.'''
def update_snake():
    global x_head, y_head, snake_length, food_x, food_y
    # Update the co-ordinates after the movement 
    x_head += x_change  
    y_head += y_change

    snake_head = [x_head, y_head]  # To store the positional value of the head movement
    snake.append(snake_head)  # Add the current head position to the snake list there by forming the body structure of snake

    # Remove tail if snake is too long 
    if len(snake) > snake_length:
        del snake[0]

    # Check if snake eats food and increase the length 
    if x_head == food_x and y_head == food_y:
        snake_length += 1
        while [food_x, food_y] in snake:  # Spawn new food location
            food_x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            food_y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE


'''Game Over Conditions - Check for collisions with walls or itself.'''
def check_collisions():
    global game_over
    # Snake moves out of screen boundaries
    if x_head >= SCREEN_WIDTH or x_head < 0 or y_head >= SCREEN_HEIGHT or y_head < 0:
        game_over = True
    # Head touches the body
    if [x_head, y_head] in snake[:-1]:
        game_over = True


'''Main Game Loop.'''
def game_loop():
    global game_quit, game_over, x_change, y_change, direction
    initialize_game()


    while not game_quit:
        handle_events()
        
        # Define Snake Movements
        if direction == 'LEFT':
            x_change = -GRID_SIZE
            y_change = 0
        if direction == 'RIGHT':
            x_change = GRID_SIZE
            y_change = 0
        if direction == 'UP':
            y_change = -GRID_SIZE
            x_change = 0 
        if direction == 'DOWN':
            y_change = GRID_SIZE
            x_change = 0  

        
        update_snake()
        check_collisions()

        DISPLAY.fill(BLACK)  # Uodate the Background after Movement of snake
        spawn_food()
        snake_struct()
        show_score()
        pygame.display.update()


        if game_over:
            DISPLAY.fill(BLACK)
            message("Game Over! Press R-Play Again or ESC-Quit", RED)
            show_score()
            pygame.display.update()

            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:                        
                        game_quit = True
                        game_over = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:  # For restarting with r-key
                            game_loop()
                        elif event.key == pygame.K_ESCAPE:  # For quitting with Esc-key
                            game_quit = True
                            game_over = False

        CLOCK.tick(SNAKE_SPEED + snake_length // 5)  # Increase the speed with increasing score


if __name__ == "__main__":
    game_loop()
    pygame.quit()
    quit()